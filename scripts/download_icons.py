#!/usr/bin/env python3
"""批量下载和转换图标，支持并发和错误重试。"""

import os
import sys
import json
import subprocess
import argparse
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional, Tuple

# 默认配置
DEFAULT_OUTPUT_DIR = "/tmp/roblox_icons"
DEFAULT_SIZE = 512
MAX_RETRIES = 3
RETRY_DELAY = 1  # 秒
MAX_WORKERS = 4  # 并发数

def run_command(cmd: str, retries: int = MAX_RETRIES) -> Tuple[bool, str]:
    """执行命令，支持重试"""
    for attempt in range(retries):
        try:
            result = subprocess.run(
                cmd, 
                shell=True, 
                capture_output=True, 
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                return True, result.stdout
            else:
                if attempt < retries - 1:
                    time.sleep(RETRY_DELAY)
                    continue
                return False, result.stderr
        except subprocess.TimeoutExpired:
            if attempt < retries - 1:
                time.sleep(RETRY_DELAY)
                continue
            return False, "命令执行超时"
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(RETRY_DELAY)
                continue
            return False, str(e)
    return False, "未知错误"

def download_svg(icon_path: str, output_path: str) -> bool:
    """下载 SVG 文件"""
    url = f"https://raw.githubusercontent.com/game-icons/icons/master/{icon_path}"
    cmd = f'curl -sL "{url}" -o "{output_path}"'
    success, error = run_command(cmd)
    
    if not success:
        print(f"  ❌ 下载失败: {icon_path} - {error}")
        return False
    
    # 验证文件是否下载成功
    if not os.path.exists(output_path) or os.path.getsize(output_path) < 100:
        print(f"  ❌ 下载的文件无效: {icon_path}")
        return False
    
    return True

def convert_svg_to_png(svg_path: str, png_path: str, size: int = DEFAULT_SIZE) -> bool:
    """将 SVG 转换为 PNG，处理透明背景"""
    # 检测 SVG 类型（game-icons 是黑底白图，Lucide 是透明背景）
    with open(svg_path, 'r', encoding='utf-8') as f:
        svg_content = f.read()
    
    # 判断是否是 game-icons 的黑底白图
    if 'fill="#000"' in svg_content or 'fill="black"' in svg_content:
        # game-icons: 黑底白图，需要去黑底
        cmd = f'magick "{svg_path}" -background none -alpha set -channel RGBA -fuzz 10% -fill "rgba(0,0,0,0)" -opaque black -resize {size}x{size} "PNG32:{png_path}"'
    else:
        # Lucide 或其他: 透明背景
        cmd = f'magick "{svg_path}" -background none -resize {size}x{size} "PNG32:{png_path}"'
    
    success, error = run_command(cmd)
    
    if not success:
        print(f"  ❌ 转换失败: {svg_path} - {error}")
        return False
    
    # 验证输出文件
    if not os.path.exists(png_path):
        print(f"  ❌ 转换后的文件不存在: {png_path}")
        return False
    
    return True

def process_single_icon(icon_info: Dict, output_dir: str, size: int) -> Optional[Dict]:
    """处理单个图标：下载 + 转换"""
    name = icon_info["name"]
    artist = icon_info["artist"]
    icon_path = icon_info["path"]
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 文件路径
    svg_path = os.path.join(output_dir, f"{name}.svg")
    png_path = os.path.join(output_dir, f"{name}.png")
    
    # 如果 PNG 已存在，跳过
    if os.path.exists(png_path):
        print(f"  ⏭️  跳过已存在: {name}")
        return {
            "name": name,
            "artist": artist,
            "svg_path": svg_path,
            "png_path": png_path,
            "status": "skipped"
        }
    
    # 下载 SVG
    if not download_svg(icon_path, svg_path):
        return None
    
    # 转换为 PNG
    if not convert_svg_to_png(svg_path, png_path, size):
        return None
    
    print(f"  ✅ 完成: {name}")
    return {
        "name": name,
        "artist": artist,
        "svg_path": svg_path,
        "png_path": png_path,
        "status": "success"
    }

def download_icons_batch(
    icons: List[Dict], 
    output_dir: str = DEFAULT_OUTPUT_DIR, 
    size: int = DEFAULT_SIZE,
    max_workers: int = MAX_WORKERS
) -> List[Dict]:
    """批量下载和转换图标"""
    results = []
    failed = []
    
    print(f"开始处理 {len(icons)} 个图标...")
    print(f"输出目录: {output_dir}")
    print(f"图标尺寸: {size}x{size}")
    print(f"并发数: {max_workers}")
    print("-" * 60)
    
    # 使用线程池并发处理
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有任务
        future_to_icon = {
            executor.submit(process_single_icon, icon, output_dir, size): icon
            for icon in icons
        }
        
        # 收集结果
        for future in as_completed(future_to_icon):
            icon = future_to_icon[future]
            try:
                result = future.result()
                if result:
                    results.append(result)
                else:
                    failed.append(icon)
            except Exception as e:
                print(f"  ❌ 处理异常: {icon['name']} - {e}")
                failed.append(icon)
    
    # 打印统计
    print("-" * 60)
    print(f"处理完成:")
    print(f"  ✅ 成功: {len(results)}")
    print(f"  ❌ 失败: {len(failed)}")
    
    if failed:
        print(f"\n失败的图标:")
        for icon in failed:
            print(f"  - {icon['path']}")
    
    return results

def create_roblox_upload_script(results: List[Dict], output_dir: str) -> str:
    """创建 Roblox Studio 上传脚本"""
    script_content = """-- Roblox 图标批量上传脚本
-- 在 Roblox Studio 中运行此脚本

local HttpService = game:GetService("HttpService")
local InsertService = game:GetService("InsertService")

-- 图标列表
local icons = {
"""
    
    for i, result in enumerate(results, 1):
        name = result["name"]
        png_path = result["png_path"]
        script_content += f'    {{name = "{name}", path = "{png_path}"}},\n'
    
    script_content += """}

-- 上传函数
local function uploadIcon(iconInfo)
    local success, result = pcall(function()
        -- 读取图片文件
        local file = io.open(iconInfo.path, "rb")
        if not file then
            warn("无法读取文件: " .. iconInfo.path)
            return nil
        end
        
        local content = file:read("*all")
        file:close()
        
        -- 上传到 Roblox
        local assetId = InsertService:CreateAsset(content, Enum.AssetType.Image)
        return assetId
    end)
    
    if success then
        print(string.format("✅ %s: rbxassetid://%d", iconInfo.name, result))
        return result
    else
        warn(string.format("❌ %s: %s", iconInfo.name, tostring(result)))
        return nil
    end
end

-- 批量上传
print("开始上传图标...")
local uploaded = 0
local failed = 0

for _, icon in ipairs(icons) do
    local assetId = uploadIcon(icon)
    if assetId then
        uploaded = uploaded + 1
    else
        failed = failed + 1
    end
    wait(0.5)  -- 避免请求过快
end

print(string.format("\\n上传完成: %d 成功, %d 失败", uploaded, failed))
"""
    
    # 保存脚本
    script_path = os.path.join(output_dir, "upload_to_roblox.lua")
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    return script_path

def main():
    parser = argparse.ArgumentParser(description="批量下载和转换 game-icons 图标")
    parser.add_argument("keyword", help="搜索关键词")
    parser.add_argument("-n", "--limit", type=int, default=10, help="下载数量（默认10）")
    parser.add_argument("-o", "--output", default=DEFAULT_OUTPUT_DIR, help="输出目录")
    parser.add_argument("-s", "--size", type=int, default=DEFAULT_SIZE, help="图标尺寸（默认512）")
    parser.add_argument("-w", "--workers", type=int, default=MAX_WORKERS, help="并发数（默认4）")
    parser.add_argument("--no-fuzzy", action="store_true", help="禁用模糊搜索")
    parser.add_argument("--create-script", action="store_true", help="创建 Roblox 上传脚本")
    
    args = parser.parse_args()
    
    # 导入搜索模块
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from search_icons import search
    
    # 搜索图标
    print(f"搜索图标: {args.keyword}")
    icons = search(args.keyword, args.limit, not args.no_fuzzy)
    
    if not icons:
        print("没有找到匹配的图标")
        return
    
    print(f"找到 {len(icons)} 个图标")
    
    # 批量下载和转换
    results = download_icons_batch(
        icons, 
        args.output, 
        args.size, 
        args.workers
    )
    
    # 创建上传脚本（如果需要）
    if args.create_script and results:
        script_path = create_roblox_upload_script(results, args.output)
        print(f"\n已创建上传脚本: {script_path}")
        print("在 Roblox Studio 中运行此脚本即可批量上传图标")
    
    # 保存结果列表
    if results:
        result_path = os.path.join(args.output, "icon_list.json")
        with open(result_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n结果已保存到: {result_path}")

if __name__ == "__main__":
    main()
