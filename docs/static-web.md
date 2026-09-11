# 纯静态网页版交接

## 当前状态（2026-09-11）

[正式画廊](https://www.starshoreai.com/koi-stylekit/gallery/)已通过 HTTPS 浏览器验收。1280px 桌面及 320/390/440px 手机模拟流程通过，详见 [验收记录](验收记录.md)。以下构建与本地验证记录保留原执行日期；其中“本轮未部署”描述的是 9 月 10 日静态迁移阶段。

## 本次约定

访客通过网页完成浏览 → 选风格 → 填主题 → 配色选择 → 预览 → 复制/下载，无需安装 Python。沿用现有流程，不新增账户、遥测、模型调用或上传；主题只留在当前浏览器内存。收藏仍只保存风格 ID。样图来自历史候选生成，不代表跨主题稳定。

## 给星岸主站会话

构建产物：本项目 `dist/`，完整上传其内容即可。支持域名根目录和子目录（例如 `/koi-stylekit/gallery/`）；目录 URL 须带尾斜杠或由静态服务器重定向。所有运行资源都是相对地址，无 `/api/render` 请求、无 Python 服务依赖、无第三方运行时 CDN。

不要发布仓库根目录、测试输出或 Python 预览服务器。保留 `.nojekyll`，GitHub Pages 可发布整个构建产物。本轮未配置 Pages、域名、canonical 或站点提交；不要把本地地址当在线体验链接。

```sh
python3 -m pip install -r requirements-build.txt
python3 scripts/build_static.py
python3 -m http.server 4321 --bind 127.0.0.1 --directory dist
```

构建依赖 Pillow 11.x；使用者无需依赖。`dist/` 与 `outputs/` 已忽略，不提交生成资源。原始 PNG/输入 JSON 保留在 `wireframes/`。构建生成 WebP 缩略图（最大 480px）和详情图（最大 1200px）；列表懒加载缩略图，详情按需载入大图。构建脚本或源图更新会使对应图片缓存失效。发布前建议从干净的构建目录生成，避免目录删除后留下旧产物。

当前产物约 **67.44 MB（64.32 MiB）**；目录原始图片共 **772.82 MB**。308 张缩略图共 **10.94 MB**，平均约 **35.5 KB**；详情图共 **54.78 MB**。这是完整发布包，非首屏下载量。用途案例的九张图片也已压缩，原图不进入发布包。

## 行为一致性与维护

`wireframes/styles.json` 和 `render-rules.json` 是两端共享数据，Python `scripts/koi.py` 为行为基准；浏览器实现为 `renderer.mjs`。保留 CLI、旧风格 ID 和旧 HTTP 测试。当前未自动翻译 Python 代码，仍有两份流程实现，必须通过对照测试防止漂移。

```sh
# 除 Python 外，对照测试要求 Node.js 22+
python3 -m unittest discover -s tests -v
```

12 项测试通过。7,797 组请求逐字段对照，覆盖 308 个风格的全部支持用途 × 三种配色策略 × 四种比例，以及非法输入、旧 ID、emoji、占位符字面量和 Unicode 空白。规则和配方文字只在共享数据中维护。CI 已添加 Node 设置，远程 CI 本轮未运行。

## 浏览器验证

普通 `http.server`：4321 提供 `dist/` 根路径，4320 提供仓库目录，以 `/dist/` 验证子路径。自动化脚本 `scripts/verify_static.cjs` 需要 Playwright 与 Chrome；可设置 `BROWSER_CHANNEL`。在项目目录安装 Playwright 后运行 `node scripts/verify_static.cjs`；本机使用已有依赖，没有给使用者增加依赖。

验证覆盖：48 家族、100 条分页、比较、收藏刷新保留、详情、配色阻止预览、保留主题配色、剪贴板内容、实际下载文件与 CLI 全字段一致；1280px 桌面及 320/390/440px 手机宽度无横向溢出。静态根路径与子路径均加载，图片 decode 成功。网络只出现 GET，未观察到主题提交请求；浏览器无未捕获异常。

本地截图、下载文件、报告在 `outputs/static/`。这是 Chrome 自动化及截图检查，未宣称 iPhone Safari 真机验收。剪贴板在 HTTPS/localhost 且权限允许时自动复制；被拒绝时提供选中文本手动复制，不影响 JSON 下载。

## 未完成与接入注意

- 主站已接入并上线，后续部署路径与缓存策略仍由主站维护；本项目不直接修改主站。
- 真机 Safari、其他浏览器和真实移动网络性能仍待验收。
- 五语仅指项目文档，网页和提示词仍主要是中文。
- 308 项为 48 家族加 260 变体，样图仍为候选。
- 纯静态版本不等于离线 PWA；首次资源加载需要网络，资源失败提示刷新。
- 旧 Python `/api/render` 为 CLI/历史兼容保留，不属于部署产物，也不被网页调用。

## 纸雕案例包增量交接（2026-09-11）

重新构建完整 dist/ 后由主站沿现有流程同步，新增路径为 cases/style-applications/paper-kit.html，入口位于实际用途案例页。页面包含天气、书店、完整人物、独立耳机四个案例及原始 JSON；人物和耳机方向获用户认可，配色偏差、重复生成与跨模型限制继续保留。原始 PNG 留在源码，构建产物使用 WebP。

同步时同时检查画廊 og:description 的准确配方数量文案。不要仅复制 HTML：四张 WebP 和四份 JSON 也是必需资源。当前完整产物 67,603,710 字节；尚未在主站部署本增量。
