"""Shared local renderer for CLI and browser. No model or network calls."""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULES = json.loads((ROOT / "wireframes/render-rules.json").read_text(encoding="utf-8"))
LAYOUTS = RULES["layouts"]
ASPECTS = tuple(RULES["aspects"])
COLORS = RULES["colors"]

def catalogue():
    return json.loads((ROOT / "wireframes/styles.json").read_text(encoding="utf-8"))

def render(style, subject, purpose="single", aspect=None, caption=None, color_policy="ask"):
    if not isinstance(subject, str) or not subject.strip() or len(subject) > 1200:
        raise ValueError("主题须为 1–1200 字符")
    if purpose not in LAYOUTS or purpose not in style["uses"]:
        raise ValueError("不支持的用途")
    if aspect not in ASPECTS:
        raise ValueError("不支持的画幅比例")
    if caption is not None and (not isinstance(caption, str) or len(caption) > 80):
        raise ValueError("标题最多 80 字符")
    if color_policy not in ("ask", "style", "subject"):
        raise ValueError("不支持的配色选择")
    subject = subject.strip()
    caption = (caption or "").strip() or None
    limited = bool(style.get("palette_limited"))
    hints = sorted(set(re.findall(COLORS, subject, flags=re.I))) if limited else []
    needs_choice = bool(hints and color_policy == "ask")
    recipe = style["recipe"]
    variant = limited and color_policy == "subject"
    if variant:
        recipe = style["subject_palette_recipe"]
    parts = [recipe.replace("{subject}", subject), LAYOUTS[purpose]]
    if limited and color_policy == "style":
        parts.append(RULES["style_choice"])
    elif variant:
        parts.append(RULES["subject_choice"])
    if aspect:
        parts.append(RULES["aspect_prefix"] + aspect)
    parts.append(RULES["caption"] if caption else RULES["no_caption"])
    warnings = []
    if needs_choice:
        warnings.append(RULES["conflict"])
    if variant:
        warnings.append(RULES["variant"])
    return {"schema": RULES["schema"], "style": {"id": style["id"], "name": style["name"], "version": style["version"], "source": style["source"]}, "brief": {"subject": subject, "purpose": purpose, "aspect": aspect, "caption": caption, "color_policy": color_policy}, "validation": style["validation"], "palette_variant": variant, "color_hints": hints, "warnings": warnings, "status": "needs_color_choice" if needs_choice else "ready", "prompt_zh": None if needs_choice else "\n\n".join(parts)}

def render_request(data):
    if not isinstance(data, dict):
        raise ValueError("请求必须是 JSON 对象")
    allowed = {"style_id", "subject", "purpose", "aspect", "caption", "color_policy"}
    if set(data) - allowed:
        raise ValueError("存在未知输入字段")
    style = next((s for s in catalogue() if (s["id"] == data.get("style_id") or data.get("style_id") in s.get("aliases", []))), None)
    if style is None:
        raise ValueError("请选择有效风格")
    return render(style, data.get("subject"), data.get("purpose", "single"), data.get("aspect"), data.get("caption"), data.get("color_policy", "ask"))

def main():
    parser = argparse.ArgumentParser(description="Koi StyleKit 本地提示词工具")
    parser.add_argument("command", choices=["list", "render"])
    parser.add_argument("--style")
    parser.add_argument("--subject")
    parser.add_argument("--purpose", choices=list(LAYOUTS), default="single")
    parser.add_argument("--aspect", choices=ASPECTS[1:])
    parser.add_argument("--caption")
    parser.add_argument("--color-policy", choices=["ask", "style", "subject"], default="ask")
    parser.add_argument("--format", choices=["json", "text"], default="json")
    args = parser.parse_args()
    if args.command == "list":
        print(json.dumps(catalogue(), ensure_ascii=False, indent=2))
        return
    try:
        result = render_request(dict(style_id=args.style, subject=args.subject, purpose=args.purpose, aspect=args.aspect, caption=args.caption, color_policy=args.color_policy))
    except ValueError as error:
        parser.error(str(error))
    if args.format == "text" and result["status"] != "ready":
        parser.error(result["warnings"][0] + " 使用 --color-policy style 或 subject。")
    print(result["prompt_zh"] if args.format == "text" else json.dumps(result, ensure_ascii=False, indent=2))
    if result["status"] != "ready":
        raise SystemExit(2)

if __name__ == "__main__":
    main()
