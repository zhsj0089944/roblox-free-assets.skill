# 素材源 API 与下载地址（已验证）

## game-icons.net（通过 GitHub，本地索引搜索）

### 搜索图标（本地，无 API 调用）
```bash
python3 ~/.workbuddy/skills/roblox-free-assets/scripts/search_icons.py {关键词} 10
```

输出格式：`{artist}/{icon-name}.svg`

### 下载 SVG
```
https://raw.githubusercontent.com/game-icons/icons/master/{artist}/{icon-name}.svg
```

示例：
```
https://raw.githubusercontent.com/game-icons/icons/master/lorc/crossed-swords.svg
https://raw.githubusercontent.com/game-icons/icons/master/delapouite/ancient-sword.svg
https://raw.githubusercontent.com/game-icons/icons/master/lorc/shield.svg
```

### 转换命令（黑底→透明底）
```bash
magick input.svg -background none -alpha set -channel RGBA -fuzz 10% -fill "rgba(0,0,0,0)" -opaque black -resize 512x512 PNG32:output.png
```

### 主要艺术家

| 艺术家 | 风格特点 | 图标数量 |
|--------|----------|----------|
| lorc | 精细线条，种类最多 | 2000+ |
| delapouite | 厚实卡通风格 | 1500+ |
| sbed | 简洁几何 | 200+ |
| carl-olsen | 写实风格 | 100+ |

---

## Lucide Icons

### 下载 SVG
```
https://unpkg.com/lucide-static@latest/icons/{name}.svg
```

示例：
```
https://unpkg.com/lucide-static@latest/icons/x.svg
https://unpkg.com/lucide-static@latest/icons/settings.svg
https://unpkg.com/lucide-static@latest/icons/search.svg
```

### 转换命令（已经是透明底）
```bash
magick input.svg -background none -resize 512x512 PNG32:output.png
```

---

## Phosphor Icons

### 下载 SVG
```
https://phosphoricons.com/icons/{name}/regular.svg
```

6 种粗细：thin / light / regular / bold / fill / duotone

---

## Mixkit 音效

### 搜索页面
```
https://mixkit.co/free-sound-effects/{category}/
```

### 常用分类
- UI 音效：https://mixkit.co/free-sound-effects/user-interface/
- 游戏音效：https://mixkit.co/free-sound-effects/game/
- 通知：https://mixkit.co/free-sound-effects/notification/

### 下载方式
Mixkit 需要浏览器交互下载。备选：sfxr.me 在线生成。

---

## unDraw 插画

### 下载 SVG
```
https://undraw.co/illustrations/svg/undraw_{name}.svg
```

### 带自定义颜色
```
https://undraw.co/illustrations/svg/undraw_{name}.svg?color=FF6B6B
```

---

## Roblox 内置字体

```
Enum.Font.Arcade          -- 像素复古
Enum.Font.FredokaOne      -- 圆润可爱
Enum.Font.IndieFlower     -- 手写轻松
Enum.Font.PermanentMarker  -- 标记笔粗体
Enum.Font.GothamBold       -- 现代粗体
Enum.Font.GothamMedium     -- 现代中等
Enum.Font.GothamBlack      -- 超粗体
Enum.Font.SourceSans       -- 标准无衬线
Enum.Font.SourceSansBold   -- 标准粗体
Enum.Font.Roboto           -- 机器人风格
Enum.Font.RobotoMono       -- 等宽字体
Enum.Font.Cartoon          -- 卡通风
Enum.Font.Fantasy          -- 奇幻风
Enum.Font.SciFi            -- 科幻风
```

---

## 常用游戏图标搜索关键词

| 需求 | 搜索词 | 大约结果数 |
|------|--------|-----------|
| 剑 | sword | 40+ |
| 盾 | shield | 30+ |
| 药水 | potion | 20+ |
| 心 | heart | 25+ |
| 星 | star | 30+ |
| 闪电 | lightning | 15+ |
| 火 | fire | 25+ |
| 冰 | ice / frost | 20+ |
| 金币 | coin | 15+ |
| 宝箱 | chest / treasure | 20+ |
| 骷髅 | skull | 25+ |
| 王冠 | crown | 15+ |
| 弓 | bow | 20+ |
| 斧 | axe | 20+ |
| 杖 | staff | 30+ |
| 匕首 | dagger | 15+ |
| 头盔 | helmet | 25+ |
| 铠甲 | armor | 30+ |
| 卷轴 | scroll | 15+ |
| 食物 | food | 40+ |
