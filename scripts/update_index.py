#!/usr/bin/env python3
"""更新 game-icons 图标索引，从 GitHub 仓库拉取最新数据。"""

import json
import os
import sys
import subprocess
import argparse
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(SCRIPT_DIR, "..", "references", "game-icons-index.json")
BACKUP_DIR = os.path.join(SCRIPT_DIR, "..", "references", "backups")

def run_command(cmd: str) -> tuple:
    """执行命令并返回结果"""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True,
            timeout=60
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "命令执行超时"
    except Exception as e:
        return False, "", str(e)

def backup_index():
    """备份当前索引文件"""
    if not os.path.exists(INDEX_PATH):
        return None
    
    os.makedirs(BACKUP_DIR, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"game-icons-index_{timestamp}.json")
    
    try:
        import shutil
        shutil.copy2(INDEX_PATH, backup_path)
        print(f"✅ 已备份当前索引: {backup_path}")
        return backup_path
    except Exception as e:
        print(f"⚠️  备份失败: {e}")
        return None

def fetch_game_icons_repo():
    """从 GitHub 获取 game-icons 仓库信息"""
    print("📥 正在从 GitHub 获取 game-icons 仓库信息...")
    
    # 使用 GitHub API 获取仓库内容
    url = "https://api.github.com/repos/game-icons/icons/contents"
    cmd = f'curl -sL "{url}"'
    
    success, output, error = run_command(cmd)
    
    if not success:
        print(f"❌ 获取仓库信息失败: {error}")
        return None
    
    try:
        data = json.loads(output)
        return data
    except json.JSONDecodeError as e:
        print(f"❌ 解析 JSON 失败: {e}")
        return None

def extract_icons_from_github():
    """从 GitHub 提取图标信息"""
    print("🔍 正在提取图标信息...")
    
    # 获取所有艺术家目录
    repo_data = fetch_game_icons_repo()
    if not repo_data:
        return None
    
    icons = {}
    artist_dirs = []
    
    # 找到所有艺术家目录
    for item in repo_data:
        if item.get("type") == "dir" and not item.get("name", "").startswith("."):
            artist_dirs.append(item["name"])
    
    print(f"📁 找到 {len(artist_dirs)} 个艺术家目录")
    
    # 遍历每个艺术家目录
    for artist in artist_dirs:
        print(f"  处理艺术家: {artist}")
        
        url = f"https://api.github.com/repos/game-icons/icons/contents/{artist}"
        cmd = f'curl -sL "{url}"'
        
        success, output, error = run_command(cmd)
        
        if not success:
            print(f"    ⚠️  获取 {artist} 的图标失败: {error}")
            continue
        
        try:
            artist_data = json.loads(output)
            
            # 提取 SVG 文件
            for item in artist_data:
                if item.get("type") == "file" and item.get("name", "").endswith(".svg"):
                    icon_name = item["name"].replace(".svg", "")
                    icons[icon_name] = artist
            
            print(f"    ✅ 找到 {len([i for i in icons.values() if i == artist])} 个图标")
            
        except json.JSONDecodeError as e:
            print(f"    ⚠️  解析 {artist} 的数据失败: {e}")
            continue
        
        # 避免请求过快
        import time
        time.sleep(0.5)
    
    return icons

def update_index(icons: dict):
    """更新索引文件"""
    print(f"📝 正在更新索引文件...")
    
    # 读取现有索引
    existing_icons = {}
    if os.path.exists(INDEX_PATH):
        try:
            with open(INDEX_PATH, "r", encoding="utf-8") as f:
                existing_icons = json.load(f)
        except Exception as e:
            print(f"⚠️  读取现有索引失败: {e}")
    
    # 合并图标（新数据优先）
    merged_icons = {**existing_icons, **icons}
    
    # 按名称排序
    sorted_icons = dict(sorted(merged_icons.items()))
    
    # 保存索引
    try:
        with open(INDEX_PATH, "w", encoding="utf-8") as f:
            json.dump(sorted_icons, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 索引更新完成:")
        print(f"   - 原有图标: {len(existing_icons)}")
        print(f"   - 新增图标: {len(icons) - len(set(icons.keys()) & set(existing_icons.keys()))}")
        print(f"   - 总计图标: {len(sorted_icons)}")
        
        return True
    except Exception as e:
        print(f"❌ 保存索引失败: {e}")
        return False

def update_from_local_repo(repo_path: str):
    """从本地仓库更新索引"""
    print(f"📁 从本地仓库更新: {repo_path}")
    
    if not os.path.exists(repo_path):
        print(f"❌ 本地仓库不存在: {repo_path}")
        return None
    
    icons = {}
    
    # 遍历所有目录
    for root, dirs, files in os.walk(repo_path):
        # 跳过隐藏目录
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        
        # 获取相对路径
        rel_path = os.path.relpath(root, repo_path)
        
        # 如果是艺术家目录（直接子目录）
        if os.path.dirname(rel_path) == ".":
            artist = rel_path
            
            # 查找 SVG 文件
            for file in files:
                if file.endswith(".svg"):
                    icon_name = file.replace(".svg", "")
                    icons[icon_name] = artist
    
    return icons

def main():
    parser = argparse.ArgumentParser(description="更新 game-icons 图标索引")
    parser.add_argument("--local", type=str, help="从本地仓库更新（提供仓库路径）")
    parser.add_argument("--no-backup", action="store_true", help="不备份当前索引")
    parser.add_argument("--force", action="store_true", help="强制更新（即使索引已存在）")
    
    args = parser.parse_args()
    
    # 检查是否需要更新
    if os.path.exists(INDEX_PATH) and not args.force:
        try:
            with open(INDEX_PATH, "r", encoding="utf-8") as f:
                current_icons = json.load(f)
            print(f"📊 当前索引包含 {len(current_icons)} 个图标")
            
            if not args.force:
                response = input("是否继续更新？(y/N): ").strip().lower()
                if response != "y":
                    print("已取消更新")
                    return
        except Exception as e:
            print(f"⚠️  读取当前索引失败: {e}")
    
    # 备份当前索引
    if not args.no_backup:
        backup_index()
    
    # 获取图标数据
    if args.local:
        icons = update_from_local_repo(args.local)
    else:
        icons = extract_icons_from_github()
    
    if not icons:
        print("❌ 没有获取到图标数据")
        return
    
    # 更新索引
    if update_index(icons):
        print("🎉 索引更新成功！")
    else:
        print("❌ 索引更新失败")

if __name__ == "__main__":
    main()
