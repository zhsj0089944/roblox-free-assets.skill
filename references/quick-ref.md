# AI 自动获取素材速查卡

## 用户说什么 → AI 做什么

| 用户说 | AI 自动执行 |
|--------|------------|
| "找个剑的图标" | GitHub API 搜索 game-icons → 下载 SVG → 去黑底转 PNG → 上传 Roblox → 返回 AssetId |
| "找一套技能图标" | 批量搜索 → 批量下载 → 批量转换 → 批量上传 → 返回对照表 |
| "找个关闭按钮" | 直接下载 Lucide x.svg → 转 PNG → 上传 → 返回 AssetId |
| "找个点击音效" | Mixkit 搜索 → 下载 MP3 → 返回文件路径（用户手动上传 Studio） |
| "用什么字体" | 推荐 Roblox 内置字体，给出 Enum.Font 代码 |

## 完整命令链

### game-icons.net 图标
```bash
# 1. 搜索（本地索引，无 API）
python3 ~/.workbuddy/skills/roblox-free-assets/scripts/search_icons.py sword 10

# 2. 下载
curl -sL "https://raw.githubusercontent.com/game-icons/icons/master/lorc/crossed-swords.svg" -o /tmp/roblox_asset.svg

# 3. 转 PNG（黑底→透明底）
magick /tmp/roblox_asset.svg -background none -alpha set -channel RGBA -fuzz 10% -fill "rgba(0,0,0,0)" -opaque black -resize 512x512 PNG32:/tmp/roblox_icon.png

# 4. 启动 HTTP 服务器
cd /tmp && python3 -m http.server 18888 &

# 5. 上传（MCP）
# mcp__Roblox_Studio__upload_image(imagePaths: ["http://localhost:18888/roblox_icon.png"])

# 6. 清理
kill $(lsof -ti:18888) 2>/dev/null
```

### Lucide 图标
```bash
# 1. 下载（直接猜名字）
curl -sL "https://unpkg.com/lucide-static@latest/icons/x.svg" -o /tmp/roblox_asset.svg

# 2. 转 PNG（已经是透明底）
magick /tmp/roblox_asset.svg -background none -resize 512x512 PNG32:/tmp/roblox_icon.png

# 3-6 同上
```

## 协议速记

- **game-icons.net** → CC BY 3.0 → 署名：`Icons by game-icons.net`
- **Lucide / Phosphor / Tabler** → MIT → 无需署名
- **Mixkit** → 免费商用 → 无需署名
- **unDraw** → 免费商用 → 无需署名
- **❌ animal-island-ui** → CC BY-NC → **不能商用**
