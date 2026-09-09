# Koi StyleKit

本地插画风格工具箱候选版：真实参考样图、中文提示词、风格包导出，以及共用渲染器的 Python CLI 与 Skill。

## 启动

需要 Python 3.10+，无第三方依赖。在仓库根目录运行：

```sh
python3 scripts/serve.py
```

打开 http://127.0.0.1:4317/ 。旧的 `python3 -m http.server` 只能展示静态页，不能处理本版导出。

选择双色孔版 → 填入示例 → 预览 → 按提示选择配色优先级 → 再次预览 → 复制或下载风格包。

网页只向本机渲染器发送主题，不调用 AI 或外部服务，不记录请求正文。“记住风格”只在浏览器保存风格 ID。对照页包含外部样图链接；主画廊图片均在本地。

## CLI

```sh
python3 scripts/koi.py list
python3 scripts/koi.py render --style duotone-print --subject '绿色的书' --color-policy subject
python3 scripts/koi.py render --style duotone-print --subject '猫撑伞' --format text
```

可选参数：`--purpose single|explain|cover`、`--aspect 1:1|3:4|16:9`、`--caption '独立标题'`。

固定配色检测到常见颜色词时，默认返回 `needs_color_choice`、空提示词并以退出码 2 结束。使用 `--color-policy style` 遵循风格，或 `subject` 保留主题颜色。检测是保守词语匹配，会漏报或误报；用户可主动选择。保留主题颜色会放宽固定配色并标为未验证变体。

网页 `/api/render` 与 CLI 共用 scripts/koi.py；导出 schema 为 koi-stylekit.v0.2。标题独立保存，不要求图片模型绘制文字。

## Skill

入口为 SKILL.md，需要完整仓库中的 scripts 和 wireframes/styles.json。尚未全局安装；没有在线生图、英文翻译、MCP 或自动发布能力。

## 验证

```sh
python3 -m unittest discover -s tests -v
```

测试涵盖 HTTP/CLI 导出相等、配色选择、标题分离、输入校验。实际图片仅为候选效果；用户认可了画风方向，未完成广泛跨主题或跨模型稳定性验证。

[画风验证](docs/画风验证.md) · [验收记录](docs/验收记录.md) · [项目流程](docs/项目流程图.md)

上游配方来源和许可见 styles.json 与 docs/THIRD_PARTY_LICENSES.txt。yang0 完整库和原始样图未打包。项目新增代码与文档采用 MIT，来源见 [ATTRIBUTION.md](ATTRIBUTION.md)。尚未提交、推送或发布；跨操作系统测试仍待完成。

## 从下载包开始

下载并解压完整仓库到任意目录，进入该目录后执行启动命令。无需 pip install。不要仅下载 SKILL.md。

在支持自定义 Skill 的宿主中，将完整目录作为 Skill 包使用；具体发现目录按宿主配置。此仓库不自动改写全局技能目录。可以先让 Agent 阅读根目录 SKILL.md，再按其中命令验证调用。

静态 HTML 单独打开不能导出，需要运行本地 Python 服务。服务默认仅监听 127.0.0.1，端口占用时可运行 `python3 scripts/serve.py --port 4318`。
