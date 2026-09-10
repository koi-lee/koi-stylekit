# Koi StyleKit

[简体中文](README.md) | **English** | [日本語](README.ja.md) | [한국어](README.ko.md)

Preview illustration styles, choose a recipe, and reuse it with a new subject.

A local illustration gallery, Python CLI, and agent skill sharing one prompt renderer. **Exports prompts; does not generate images.**

Machine-readable discovery: [LLM project summary](wireframes/llms.txt) · [crawler rules](wireframes/robots.txt). After deployment, replace the Sitemap placeholder in `robots.txt` with the production URL.

[v0.2.0-alpha is available](https://github.com/koi-lee/koi-stylekit/releases/tag/v0.2.0-alpha). Documentation is available in Chinese and English. The gallery interface and exported style instructions are primarily Chinese; English documentation does not enable English prompt output.

## Styles

The catalogue contains **308 recipes: 48 style families and 260 technique/composition variants**. Filter by medium, family, or number, then preview, compare, and export. Variants are treatments within a family; samples do not guarantee repeatability. See [catalogue scope and sample evidence](docs/catalogue-expansion.en.md).

| Emotional sketch | Colored pencil diary | Duotone print | Layered paper |
| --- | --- | --- | --- |
| ![Sketch](wireframes/assets/style-10-rain-v1.png) | ![Pencil](wireframes/assets/yang-169-v1.png) | ![Print](wireframes/assets/yang-167-v1.png) | ![Paper](wireframes/cases/interview-cards/paper.png) |
| `emotional-sketch` | `colored-pencil-diary` | `duotone-print` | `layered-paper` |

These are AI-generated candidate images, not guarantees for new subjects or other models.

## Quick start

Requires Python 3.10+ with no third-party dependencies.

```sh
git clone https://github.com/koi-lee/koi-stylekit.git
cd koi-stylekit
python3 scripts/serve.py
```

On Windows, replace `python3` with `py -3` if needed. You can also download and extract the source ZIP from GitHub before running the server.

Open the [local gallery](http://127.0.0.1:4317/):

1. Choose a style, such as 双色孔版 (Duotone print), then fill in the example subject.
2. Preview the prompt. The example's green book triggers a palette warning.
3. Choose whether to follow the style palette or preserve the subject's colors.
4. Copy the prompt into your image generation tool, or download the JSON recipe.
5. Reuse the style with another subject.

Images are not generated in the gallery. Preserving subject colors produces an unverified palette variant.

## CLI

```sh
python3 scripts/koi.py list
python3 scripts/koi.py render --style colored-pencil-diary --subject 'A cat under an umbrella' --format text
python3 scripts/koi.py render --style duotone-print --subject 'A green book' --color-policy subject
python3 scripts/koi.py render --style layered-paper --subject 'Two hands passing a book' --aspect 16:9 --color-policy style --format text
```

An English subject is accepted, but the recipe instructions remain Chinese.

| Option | Values and behavior |
| --- | --- |
| `--purpose` | `single` (default), `explain` (three steps), `cover` (space for a title) |
| `--aspect` | Optional: `1:1`, `3:4`, `16:9`; omitted means unspecified |
| `--caption` | Separate title in JSON; not text to be drawn inside the image |
| `--color-policy` | `ask` (default), `style`, `subject` |
| `--format` | `json` (default) or `text` |

Color detection uses limited lexical matching and can miss conflicts or raise false alarms. When a choice is required, JSON contains `status: needs_color_choice` and `prompt_zh: null`, and the CLI exits with code 2. Text mode reports the issue without producing a conflicting prompt. Other input errors also exit with code 2.

The gallery and CLI share `scripts/koi.py`. The export schema is `koi-stylekit.v0.2`. Legacy IDs `minimal-line` and `ink-accent` remain accepted and export as `emotional-sketch` and `colored-pencil-diary`, respectively.

## Agent skill

Ask an agent with local file and command access to read [SKILL.md](SKILL.md), for example:

> Read this repository's SKILL.md and export a layered-paper prompt for two hands passing a book.

Keep the **entire repository** when installing the skill, not just SKILL.md. Use your host's skill discovery directory. Installation and discovery have been verified locally in Codex; other hosts and model behavior have not been fully tested. This project does not change global configuration.

## Layered paper evidence

The original sample used a separate English prompt; subsequent reference-based images used that sample as input. The exported Chinese recipe was then used directly, without a reference image, for weather and bookshop subjects. Both retained paper texture and the main palette but added extra objects. The user accepted the current Alpha visual baseline. Repeatability and cross-model consistency remain unverified, and exports do not attach reference images.

The [paper series HTML](wireframes/cases/interview-cards/paper-series.html) contains images and actual requests. View it through the [local server](http://127.0.0.1:4317/cases/interview-cards/paper-series.html); GitHub displays HTML source rather than running the page.

## Privacy and limitations

- Subjects stay in browser and local renderer memory; the tool does not upload them or log their contents. Explicit exports save a file to your downloads.
- Remembering a style stores only its ID in the browser. The server listens on `127.0.0.1` and is not intended for public hosting.
- The catalogue contains 308 recipes: 48 style families and 260 technique/composition variants, with category and family filters, numbered search, and pagination. Sample availability is shown on each card. The v0.2.0-alpha tag still contains four styles. Individual visual approval is not evidence of general consistency. Cover and three-step layouts have not completed visual validation.
- No online image generation, English recipe output, reference-image input, MCP, paid features, or automatic social publishing.
- Main gallery samples are local files. Research comparison pages may link to external references.
- The interview-card examples have not been integrated into that product or evaluated for learning effectiveness.

## Troubleshooting

Port in use: run `python3 scripts/serve.py --port 4318` and open that port instead. Restart the server if it stops, then retry the retained input.

Page opens but export fails: start with `scripts/serve.py`. Opening HTML directly or running a plain `http.server` does not provide the renderer API.

## Validation and contributing

```sh
python3 -m unittest discover -s tests -v
```

Isolated installation and CLI/HTTP output equality have been checked. Release commit `bbc76de` passed all six [CI jobs](https://github.com/koi-lee/koi-stylekit/actions/runs/34359647023): Windows/macOS/Ubuntu with Python 3.10/3.14.

See [Contributing in English](CONTRIBUTING.en.md). Detailed [roadmap](docs/项目流程图.md), [acceptance history](docs/验收记录.md), and [visual evidence](docs/画风验证.md) are currently in Chinese and include historical states.

## Attribution and license

Thanks to [threerocks/hand-drawn-styles](https://github.com/threerocks/hand-drawn-styles) for recipe and workflow inspiration, and [yang0/handraw-style](https://github.com/yang0/handraw-style) for the numbered-gallery and medium-classification ideas. See [ATTRIBUTION.md](ATTRIBUTION.md) (Chinese) for scope. The full yang0 library and its original images are not included.

New code and documentation use the [MIT license](LICENSE), with [upstream MIT notices](docs/THIRD_PARTY_LICENSES.txt) preserved.
