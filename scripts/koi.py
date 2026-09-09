"""Shared local renderer for CLI and browser. No model or network calls."""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAYOUTS = {"single": "突出一个主要场景，动作关系清楚。", "explain": "在一张图内按三个步骤组织内容，不编造事实。", "cover": "预留标题区域。"}
ASPECTS = (None, "1:1", "3:4", "16:9")
# Deliberately conservative lexical hints, not semantic colour understanding.
COLORS = r"(?:红|橙|黄|绿|青|蓝|紫|粉|黑|白|灰|棕|褐|金|银)(?:色|衣|裙|帽|伞)|\b(?:red|orange|yellow|green|blue|purple|pink|black|white|grey|gray|brown)\b"

def catalogue():
    return json.loads((ROOT / "wireframes/styles.json").read_text())

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
        parts.append("配色选择：以本风格配色为准。主题中的物体与动作保留，其中的颜色要求可被风格配色替代。")
    elif variant:
        parts.append("配色选择：保留主题明确指定的颜色；这是放宽配色的变体，不要求复现样图配色。")
    if aspect:
        parts.append("画幅比例：" + aspect)
    parts.append("为独立标题预留干净区域；不绘制任何文字。" if caption else "不绘制文字。")
    warnings = []
    if needs_choice:
        warnings.append("检测到颜色词，可能与固定配色冲突；请选择遵循风格或保留主题颜色。词语检测不代表语义判断。")
    if variant:
        warnings.append("已放宽配色；此变体没有对应生图验证。")
    return {"schema": "koi-stylekit.v0.2", "style": {"id": style["id"], "name": style["name"], "version": style["version"], "source": style["source"]}, "brief": {"subject": subject, "purpose": purpose, "aspect": aspect, "caption": caption, "color_policy": color_policy}, "validation": style["validation"], "palette_variant": variant, "color_hints": hints, "warnings": warnings, "status": "needs_color_choice" if needs_choice else "ready", "prompt_zh": None if needs_choice else "\n\n".join(parts)}

def render_request(data):
    if not isinstance(data, dict):
        raise ValueError("请求必须是 JSON 对象")
    allowed = {"style_id", "subject", "purpose", "aspect", "caption", "color_policy"}
    if set(data) - allowed:
        raise ValueError("存在未知输入字段")
    style = next((s for s in catalogue() if s["id"] == data.get("style_id")), None)
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
