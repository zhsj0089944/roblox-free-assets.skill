---
name: roblox-free-assets
description: |
  Roblox 游戏免费商用素材获取与使用。当需要图标、插画、音效、字体等美术资源时使用。
  触发条件：找图标、找素材、UI 图片、游戏图标、音效、字体、美术资源、免费素材、商用素材。
agent_created: true
---

# Roblox Free Commercial-Use Assets

User says "find me a sword icon" → you search, download, convert, upload, and hand back an AssetId + ready-to-use code. No browser needed.

## Output rules

Return the result as plain text (AssetId + code snippet). At most create 1 md file for batch AssetId tracking. No extra docs, logs, or reports.

---

## Icon workflow

### Step 1: Search

**Game icons (swords/shields/potions/skills) → local index search**

```bash
# English
python3 {skill_path}/scripts/search_icons.py sword -n 10

# Chinese (auto-translated)
python3 {skill_path}/scripts/search_icons.py 剑 -n 10
python3 {skill_path}/scripts/search_icons.py 盾牌 -n 5

# Fuzzy search (on by default)
python3 {skill_path}/scripts/search_icons.py weapon -n 10

# JSON output
python3 {skill_path}/scripts/search_icons.py sword -n 10 --json
```

Output: `{artist}/{icon-name}.svg` (e.g. `lorc/crossed-swords.svg`)

**UI icons (close/settings/menu) → just use Lucide**

Guess the name from the quick-ref table below. No search needed.

### Step 2: Download SVG

**game-icons.net (via GitHub raw):**
```bash
curl -sL "https://raw.githubusercontent.com/game-icons/icons/master/{artist}/{icon-name}.svg" -o /tmp/roblox_asset.svg
```

**Lucide:**
```bash
curl -sL "https://unpkg.com/lucide-static@latest/icons/{name}.svg" -o /tmp/roblox_asset.svg
```

### Step 3: SVG → PNG

**game-icons (black bg, needs removal):**
```bash
magick /tmp/roblox_asset.svg -background none -alpha set -channel RGBA -fuzz 10% -fill "rgba(0,0,0,0)" -opaque black -resize 512x512 PNG32:/tmp/roblox_icon.png
```

**Lucide (already transparent):**
```bash
magick /tmp/roblox_asset.svg -background none -resize 512x512 PNG32:/tmp/roblox_icon.png
```

### Step 4: Start local HTTP server

```bash
cd /tmp && python3 -m http.server 18888 &
```

### Step 5: Upload to Roblox

```
mcp__Roblox_Studio__upload_image(imagePaths: ["http://localhost:18888/roblox_icon.png"])
```

Returns `rbxassetid://XXXXX`.

### Step 6: Cleanup

```bash
kill $(lsof -ti:18888) 2>/dev/null
rm -f /tmp/roblox_asset.svg /tmp/roblox_icon.png
```

### Step 7: Reply

```
Icon uploaded!
AssetId: rbxassetid://XXXXX
Source: game-icons.net (CC BY 3.0)
Attribution: Add "Icons by game-icons.net" to game Description

Usage:
local icon = Instance.new("ImageLabel")
icon.Image = "rbxassetid://XXXXX"
icon.Size = UDim2.new(0, 48, 0, 48)
icon.BackgroundTransparency = 1
icon.Parent = parentFrame
```

---

## Batch download

```bash
# Download + convert in one shot
python3 {skill_path}/scripts/download_icons.py sword -n 10 -o ~/Desktop/icons

# With Roblox upload script
python3 {skill_path}/scripts/download_icons.py 剑 -n 20 -o ~/Desktop/icons --create-script
```

Flags: `-n` count, `-o` output dir, `-s` size (default 512), `-w` threads (default 4), `--create-script` generates a Lua upload script for Roblox Studio.

---

## Sound effects (semi-auto)

1. Search: `WebFetch: https://mixkit.co/free-sound-effects/{category}/`
2. Download: `curl -sL "{url}" -o /tmp/roblox_sound.mp3`
3. Upload: user manually uploads in Studio → Home → Audio (MCP only handles images)

---

## Fonts (no download needed)

| Style | Font | Code |
|-------|------|------|
| Pixel/retro | Arcade | `Enum.Font.Arcade` |
| Rounded/cute | FredokaOne | `Enum.Font.FredokaOne` |
| Handwritten | IndieFlower | `Enum.Font.IndieFlower` |
| Bold headers | PermanentMarker | `Enum.Font.PermanentMarker` |
| Modern sans | GothamBold | `Enum.Font.GothamBold` |
| Standard body | SourceSans | `Enum.Font.SourceSans` |

---

## Asset sources

| Type | Primary | Fallback | License |
|------|---------|----------|---------|
| Game icons | game-icons.net | — | CC BY 3.0 (attribution required) |
| UI icons | Lucide | Phosphor / Tabler | MIT |
| Sound FX | Mixkit | sfxr.me | Free |
| Illustrations | unDraw | Storyset | unDraw: no attribution |
| Fonts | Roblox built-in | — | N/A |

## License red lines

| ✅ OK | ❌ Avoid |
|-------|---------|
| CC0 / Public Domain | CC BY-NC (no commercial) |
| MIT / ISC / BSD | CC BY-ND (no modification) |
| CC BY (attribution) | Unlicensed assets |

Attribution template:
```
--- Credits ---
Icons: game-icons.net (CC BY 3.0)
Sound Effects: Mixkit (Free License)
```

---

## Lucide quick ref

| Use | Name | Use | Name |
|-----|------|-----|------|
| Close | x | Settings | settings |
| Menu | menu | Search | search |
| Check | check | Plus/minus | plus / minus |
| Arrow right | chevron-right | Arrow left | chevron-left |
| User | user | Mail | mail |
| Home | home | Star | star |
| Heart | heart | Bookmark | bookmark |
| Edit | edit | Delete | trash-2 |
| Copy | copy | Download | download |
| Upload | upload | Share | share |
| Eye | eye | Eye off | eye-off |
| Lock | lock | Unlock | unlock |
| Info | info | Warning | alert-circle |
| Success | check-circle | Error | x-circle |

---

## Chinese keywords

| 中文 | English | 中文 | English |
|------|---------|------|---------|
| 剑 | sword | 盾 | shield |
| 斧 | axe | 锤 | hammer |
| 弓 | bow | 箭 | arrow |
| 矛 | spear | 枪 | gun |
| 杖 | staff | 药水 | potion |
| 血 | heart | 红/蓝/绿 | red/blue/green |
| 金/银/铁 | gold/silver/iron | 木/石 | wood/stone |
| 火/水/冰 | fire/water/ice | 雷/风 | lightning/wind |
| 暗/光 | dark/light | 毒 | poison |
| 骷髅 | skull | 王冠 | crown |
| 宝箱 | chest | 钥匙 | key |
| 龙 | dragon | 蛇/狼/熊 | snake/wolf/bear |
| 技能 | skill | 魔法 | magic |
| 攻击/防御 | attack/defense | 速度/力量 | speed/power |
| 武器 | weapon | 装备 | equipment |
| 盔甲 | armor | 头盔 | helmet |
| 钻石 | diamond | 宝石/金币 | gem/coin |
| 书/卷轴 | book/scroll | 地图/指南针 | map/compass |
| 食物/面包 | food/bread | 啤酒 | beer |
| 旗帜 | flag | 徽章 | badge |
| 星星/月/太阳 | star/moon/sun | 花/树 | flower/tree |
| 山/海 | mountain/sea | 雨/雪 | rain/snow |

---

## Dependencies

- `references/game-icons-index.json` — 4176 icons, offline search
- `scripts/search_icons.py` — fuzzy search with Chinese support
- `scripts/download_icons.py` — batch download with concurrency
- `scripts/update_index.py` — sync index from GitHub
- ImageMagick 7 — SVG→PNG
- Python 3 — scripts
- curl — downloads
- Roblox Studio MCP — upload (optional)
