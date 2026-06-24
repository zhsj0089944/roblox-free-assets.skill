#!/usr/bin/env python3
"""本地搜索 game-icons 图标索引，支持模糊搜索和拼音匹配。"""

import json
import sys
import os
import re
from difflib import SequenceMatcher
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(SCRIPT_DIR, "..", "references", "game-icons-index.json")

# 简单的中英文映射表（常见游戏术语）
ZH_EN_MAP = {
    "剑": "sword", "刀": "blade", "盾": "shield", "斧": "axe", "锤": "hammer",
    "弓": "bow", "箭": "arrow", "矛": "spear", "枪": "gun", "杖": "staff",
    "药水": "potion", "药": "potion", "血": "heart", "命": "heart", "红": "red",
    "蓝": "blue", "绿": "green", "金": "gold", "银": "silver", "铁": "iron",
    "木": "wood", "石": "stone", "火": "fire", "水": "water", "冰": "ice",
    "雷": "lightning", "风": "wind", "土": "earth", "暗": "dark", "光": "light",
    "毒": "poison", "毒药": "poison", "骷髅": "skull", "骷": "skull",
    "王": "king", "王冠": "crown", "皇冠": "crown", "宝": "treasure",
    "宝箱": "chest", "箱": "chest", "钥匙": "key", "门": "door",
    "星星": "star", "星": "star", "月": "moon", "太阳": "sun", "日": "sun",
    "龙": "dragon", "蛇": "snake", "狼": "wolf", "熊": "bear", "鸟": "bird",
    "鱼": "fish", "虫": "bug", "花": "flower", "树": "tree", "草": "grass",
    "山": "mountain", "海": "sea", "河": "river", "云": "cloud", "雨": "rain",
    "雪": "snow", "风": "wind", "雷电": "lightning", "闪电": "lightning",
    "技能": "skill", "魔法": "magic", "法术": "spell", "咒": "spell",
    "攻击": "attack", "防御": "defense", "速度": "speed", "力量": "power",
    "智慧": "wisdom", "幸运": "luck", "经验": "experience", "金币": "coin",
    "钻石": "diamond", "宝石": "gem", "珍珠": "pearl", "水晶": "crystal",
    "武器": "weapon", "装备": "equipment", "盔甲": "armor", "头盔": "helmet",
    "靴": "boot", "鞋": "boot", "手套": "glove", "戒指": "ring",
    "项链": "necklace", "披风": "cape", "斗篷": "cloak",
    "书": "book", "卷轴": "scroll", "地图": "map", "指南针": "compass",
    "望远镜": "telescope", "时钟": "clock", "沙漏": "hourglass",
    "食物": "food", "面包": "bread", "肉": "meat", "苹果": "apple",
    "啤酒": "beer", "酒": "wine", "杯": "cup", "碗": "bowl",
    "旗帜": "flag", "徽章": "badge", "标志": "symbol", "符号": "symbol",
    "十字": "cross", "星形": "star", "心形": "heart", "圆形": "circle",
    "方形": "square", "三角": "triangle", "箭头": "arrow",
    "上": "up", "下": "down", "左": "left", "右": "right",
    "前": "forward", "后": "back", "大": "big", "小": "small",
    "新": "new", "旧": "old", "开": "open", "关": "close",
    "加": "plus", "减": "minus", "乘": "multiply", "除": "divide",
    "等于": "equal", "不等于": "not-equal", "大于": "greater", "小于": "less",
    "问号": "question", "感叹": "exclamation", "信息": "info",
    "警告": "warning", "错误": "error", "成功": "success",
    "搜索": "search", "设置": "settings", "菜单": "menu",
    "用户": "user", "人": "person", "男人": "man", "女人": "woman",
    "孩子": "child", "婴儿": "baby", "老人": "elderly",
    "家": "home", "房子": "house", "建筑": "building", "城堡": "castle",
    "塔": "tower", "桥": "bridge", "路": "road", "门": "gate",
    "商店": "shop", "市场": "market", "银行": "bank", "医院": "hospital",
    "学校": "school", "图书馆": "library", "教堂": "church",
    "工厂": "factory", "农场": "farm", "矿山": "mine", "森林": "forest",
    "沙漠": "desert", "雪地": "snow", "火山": "volcano", "洞穴": "cave",
}

def simple_fuzzy_match(query: str, target: str) -> float:
    """简单的模糊匹配算法，返回 0-1 的相似度分数"""
    query = query.lower().strip()
    target = target.lower().strip()
    
    # 完全匹配
    if query == target:
        return 1.0
    
    # 包含匹配
    if query in target:
        # 计算位置权重，开头匹配分数更高
        pos = target.find(query)
        if pos == 0:
            return 0.9
        elif pos < len(target) * 0.3:
            return 0.8
        else:
            return 0.7
    
    # 单词边界匹配（用 - 或 _ 分隔的单词）
    words = re.split(r'[-_]', target)
    for word in words:
        if query in word:
            return 0.6
    
    # 序列匹配
    seq_ratio = SequenceMatcher(None, query, target).ratio()
    if seq_ratio > 0.6:
        return seq_ratio * 0.5
    
    return 0.0

def translate_keyword(keyword: str) -> list:
    """将中文关键词翻译成英文，返回可能的英文关键词列表"""
    keyword = keyword.lower().strip()
    results = []
    
    # 直接映射
    if keyword in ZH_EN_MAP:
        results.append(ZH_EN_MAP[keyword])
    
    # 尝试拆分匹配
    for zh, en in ZH_EN_MAP.items():
        if zh in keyword or keyword in zh:
            results.append(en)
    
    # 去重
    return list(set(results))

def search(keyword: str, limit: int = 10, fuzzy: bool = True):
    """
    搜索图标，支持：
    1. 精确匹配（子字符串）
    2. 模糊匹配（相似度）
    3. 中文翻译匹配
    """
    with open(INDEX_PATH, "r") as f:
        icons = json.load(f)
    
    keyword = keyword.lower().strip()
    matches = []
    
    # 获取可能的英文关键词
    en_keywords = translate_keyword(keyword)
    all_keywords = [keyword] + en_keywords
    
    for name, artist in icons.items():
        name_lower = name.lower()
        best_score = 0.0
        matched_keyword = keyword
        
        # 对每个关键词尝试匹配
        for kw in all_keywords:
            # 精确包含匹配
            if kw in name_lower:
                # 计算精确匹配分数
                pos = name_lower.find(kw)
                if pos == 0:
                    score = 1.0
                elif pos < len(name_lower) * 0.3:
                    score = 0.9
                else:
                    score = 0.8
                
                if score > best_score:
                    best_score = score
                    matched_keyword = kw
            
            # 模糊匹配（如果启用）
            if fuzzy:
                fuzzy_score = simple_fuzzy_match(kw, name_lower)
                if fuzzy_score > best_score:
                    best_score = fuzzy_score
                    matched_keyword = kw
        
        # 如果有匹配结果
        if best_score > 0.3:  # 最低相似度阈值
            matches.append({
                "name": name,
                "artist": artist,
                "path": f"{artist}/{name}.svg",
                "score": best_score,
                "matched_keyword": matched_keyword
            })
    
    # 按分数排序（高分优先），然后按名称排序
    matches.sort(key=lambda x: (-x["score"], x["name"]))
    
    return matches[:limit]

def search_with_output(keyword: str, limit: int = 10, fuzzy: bool = True):
    """搜索并格式化输出"""
    results = search(keyword, limit, fuzzy)
    
    if not results:
        print(f"没有找到包含 '{keyword}' 的图标")
        print("提示：尝试使用英文关键词，或更具体的描述")
        return []
    
    print(f"找到 {len(results)} 个图标：")
    print("-" * 60)
    
    for i, r in enumerate(results, 1):
        score_str = f"{r['score']:.2f}"
        print(f"{i:2d}. {r['path']:<40} (相似度: {score_str})")
    
    print("-" * 60)
    print(f"使用示例：")
    print(f"  下载第一个: curl -sL 'https://raw.githubusercontent.com/game-icons/icons/master/{results[0]['path']}' -o icon.svg")
    
    return results

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="搜索 game-icons 图标")
    parser.add_argument("keyword", help="搜索关键词（支持中文）")
    parser.add_argument("-n", "--limit", type=int, default=10, help="返回结果数量（默认10）")
    parser.add_argument("--no-fuzzy", action="store_true", help="禁用模糊搜索")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    
    args = parser.parse_args()
    
    results = search(args.keyword, args.limit, not args.no_fuzzy)
    
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        search_with_output(args.keyword, args.limit, not args.no_fuzzy)
