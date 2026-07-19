import os
import shutil
import json

# 🎯 目标路径配置
SOURCE_DIR = r"D:\volume\drpy-node-me\json"
TARGET_DIR = r"D:\volume\drpy-node-me\json\json"

# 确保目标文件夹（内层json）存在，如果不存在就自动创建一个
os.makedirs(TARGET_DIR, exist_ok=True)

def check_is_target_json(file_path):
    """ 🔍 深度特征比对：通过关键词特征识别是不是这类带有特定标签的 JSON 文件 """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
            # 1. 检查数据结构是否符合 CMS 标准（含有 list）
            if not isinstance(data, dict) or "list" not in data:
                return False
                
            for item in data["list"]:
                # 2. 特征一：如果包含 'vod_tags'，且里面有“丝袜美腿”或“无码流出”这类特定标签
                if "vod_tags" in item and isinstance(item["vod_tags"], list):
                    adult_keywords = ["丝袜美腿", "多P群交", "无码流出", "美丽的乳房"]
                    if any(keyword in item["vod_tags"] for keyword in adult_keywords):
                        return True
                        
                # 3. 特征二：如果图片或者播放链接里包含了特定网站的关键标识（比如 missav, whos, aaaaa.io）
                vod_pic = item.get("vod_pic", "")
                vod_url = item.get("vod_play_url", "")
                if "missav" in vod_pic or "whos.tv" in vod_url or "aaaaa.io" in vod_url:
                    return True
                    
    except Exception as e:
        # 如果文件损坏或者编码不对，先跳过保护
        pass
    return False

def start_moving():
    print(f"🚀 开始扫描外层目录: {SOURCE_DIR}")
    print("--------------------------------------------------")
    
    move_count = 0
    
    # 遍历外层目录下的所有文件（使用 os.scandir 性能更高，且不会套娃递归进去）
    for entry in os.scandir(SOURCE_DIR):
        # 只处理文件，并且后缀必须是 .json
        if entry.is_file() and entry.name.endswith(".json"):
            file_path = entry.path
            
            # 判定是否符合你给出的 JSON 特征
            if check_is_target_json(file_path):
                target_path = os.path.join(TARGET_DIR, entry.name)
                
                print(f"📦 匹配成功！发现目标文件: {entry.name}")
                try:
                    # 移动文件到内层 json 文件夹中
                    shutil.move(file_path, target_path)
                    print(f"   ➔ 已成功移动至: \\json\\json\\{entry.name}")
                    move_count += 1
                except Exception as e:
                    print(f"   ❌ 移动失败 (可能文件被占用): {e}")
                    
    print("--------------------------------------------------")
    print(f"🏁 归类完成！共精准分离并移动了 {move_count} 个特定的 JSON 文件。")

if __name__ == "__main__":
    if os.path.exists(SOURCE_DIR):
        start_moving()
    else:
        print(f"❌ 找不到源路径: {SOURCE_DIR}，请检查路径是否正确。")