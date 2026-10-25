# Bee哥 · 暗线情报雷达 V2

手机优先的轻量网页，适合通过 GitHub Pages 免费托管（以 GitHub 当时的政策为准）。

## 能做什么
- 每日按计划搜集 **公开媒体 RSS 标题**，按类别展示、搜索、收藏、未读标记
- 标题点击跳转来源，调查问题一键复制
- iPhone Safari → 分享 → 添加到主屏幕

## 快速部署
1. 在 GitHub 新建一个 **Public** 仓库，例如 `bee-radar`。
2. 上传此压缩包的 **全部内容，保持文件夹结构**（含 `.github/workflows/update.yml` 隐藏目录）。
3. 仓库 **Settings → Pages → Build and deployment → Deploy from a branch**，Branch 选 `main`、Folder 选 `/(root)`，保存。
4. 打开 **Actions → Update intelligence feed → Run workflow** 手动生成第一次线索。若 Actions/工作流写入权限受限，需在 **Settings → Actions → General → Workflow permissions** 启用 Read and write permissions（有些组织策略可能禁止）。
5. 网页通常位于 `https://你的GitHub用户名.github.io/bee-radar/`，实际以 Pages 显示的链接为准。
6. 用 iPhone Safari 打开网页，选择 **分享 → 添加到主屏幕**。

## 更新说明
- 工作流设为 UTC 01:00，等于马来西亚时间 09:00。GitHub Actions 的 schedule **不保证准时**，负载高时可能延迟或跳过。
- 运行脚本从 Google News RSS 搜集媒体标题；Google 可随时修改或限制 RSS，可打开 Actions 日志诊断。
- 网页读取 `data/feed.json`，所以在 GitHub Actions 更新成功前不会有新闻。
- “未读”“收藏”保存在本机浏览器的 localStorage。删除浏览器资料、更换手机或某些 iOS 数据清理可能导致丢失。
- **不提供手机通知、自动事实核查、私人资料库、跨设备同步或持续后台抓取**。这些需下一阶段接入服务端数据库与合法的推送服务。
- 新闻标题可能不准确。不要据此指控任何人违法；发布调查前须核对原始文件、法律状态及独立证据。

## 手动本地测试
在仓库根目录运行 `python -m http.server 8000` 后访问 `http://localhost:8000/`。RSS 更新需联网运行 `python scripts/update.py`。
