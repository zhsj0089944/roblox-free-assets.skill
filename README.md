# roblox-free-assets

Free commercial-use assets for Roblox game UI — icons, illustrations, sound effects, fonts.

An AI skill that searches, downloads, converts, and uploads assets in one flow. Works with WorkBuddy, OpenCode, Cursor, Claude, or any assistant that supports skills.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## What it does

Building Roblox game UIs (skill trees, inventories, shops, HUDs) means you need lots of icons. Finding free commercial-use ones, converting formats, uploading to Studio — it's all tedious. This skill automates it.

Say "find me a sword icon" and the AI searches a local index of 4176 game icons, downloads the SVG, converts to transparent PNG, uploads to Roblox Studio, and hands you the AssetId + ready-to-use Luau code. No browser needed.

Also includes Lucide for UI icons (close, settings, menu...), plus pointers to free sound effects, illustrations, and fonts.

## Install

```bash
git clone https://github.com/zhsj0089944/roblox-free-assets.skill.git
cp -r roblox-free-assets.skill <your-skills-dir>/roblox-free-assets
```

Where `<your-skills-dir>` is `~/.workbuddy/skills/`, `~/.opencode/skills/`, `~/.cursor/skills/`, `~/.claude/skills/`, or whatever your assistant uses.

Once installed, just talk to your AI: "find me a sword icon", "I need 10 weapon icons", etc.

## CLI usage

```bash
# Search (offline, supports Chinese keywords)
python3 scripts/search_icons.py sword -n 10
python3 scripts/search_icons.py 剑 -n 10

# Fuzzy search
python3 scripts/search_icons.py weapon -n 10

# Batch download + convert
python3 scripts/download_icons.py sword -n 10 -o ~/Desktop/icons

# Update the icon index from GitHub
python3 scripts/update_index.py
```

## How it works

| Step | Online? | What happens |
|------|:---:|---|
| Search | No | Local JSON index + Python, zero API calls |
| Download SVG | Yes | Fetches from GitHub (game-icons) or unpkg (Lucide) |
| Convert to PNG | No | ImageMagick — handles bg removal + transparency |
| Upload to Roblox | Yes | Via Roblox Studio MCP |

## Features

- **Fuzzy search** — finds related icons even with imprecise keywords
- **Chinese keywords** — 剑→sword, 盾→shield, 药水→potion, 100+ terms mapped
- **Batch operations** — concurrent download with retry (4 threads, 3 retries)
- **Smart conversion** — auto-detects black-bg game-icons vs transparent Lucide
- **License compliance** — reminds you about CC BY 3.0 attribution where needed
- **JSON output** — `--json` flag for programmatic use

## Asset sources

| Type | Source | License |
|------|--------|---------|
| Game icons | [game-icons.net](https://game-icons.net) (4176+) | CC BY 3.0 — attribution required |
| UI icons | [Lucide](https://lucide.dev) (2000+), [Phosphor](https://phosphoricons.com) (6000+), [Tabler](https://tabler.io/icons) (5000+) | MIT / ISC |
| Sound effects | [Mixkit](https://mixkit.co) | Free, no attribution |
| Illustrations | [unDraw](https://undraw.co), [Storyset](https://storyset.com) | Free |
| Fonts | Roblox built-in (Arcade, FredokaOne, GothamBold...) | N/A |

## Dependencies

| Tool | Purpose | Required? |
|------|---------|:---:|
| Python 3 | Search & batch scripts | Yes |
| ImageMagick 7 | SVG → PNG conversion | Yes |
| curl | Download SVGs | Yes |
| Roblox Studio MCP | Auto-upload | Optional |

## Chinese keyword support

The search script translates Chinese game terms automatically:

| 中文 | English | 中文 | English |
|------|---------|------|---------|
| 剑 | sword | 盾 | shield |
| 斧 | axe | 弓 | bow |
| 药水 | potion | 骷髅 | skull |
| 王冠 | crown | 龙 | dragon |
| 技能 | skill | 魔法 | magic |
| 武器 | weapon | 装备 | equipment |
| 火 | fire | 冰 | ice |
| 钻石 | diamond | 金币 | coin |

...and 80+ more. See [SKILL.md](SKILL.md) for the full list.

## File structure

```
roblox-free-assets/
├── README.md
├── SKILL.md                        # Workflow for AI assistants
├── LICENSE
├── references/
│   ├── game-icons-index.json       # 4176 icon index (110KB)
│   ├── asset-sources.md
│   └── quick-ref.md
└── scripts/
    ├── search_icons.py             # Local search with fuzzy matching
    ├── download_icons.py           # Batch download + convert
    └── update_index.py             # Sync index from GitHub
```

## License

Code: [MIT](LICENSE). When using game-icons.net icons commercially, add `Icons by game-icons.net` to your game description. Other sources have their own licenses — see the table above.
