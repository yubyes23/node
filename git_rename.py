import os
import shutil

# --- 配置区 ---
# 自动定位到当前脚本所在的仓库根目录
TARGET_DIR = os.getcwd()  

def restore_string(bad_str):
    """万能乱码还原"""
    try:
        # 针对 latin1 -> gbk 乱码
        good_str = bad_str.encode('latin1').decode('gbk')
        return good_str
    except Exception:
        try:
            # 兼容有些可能是 utf-8 错误识别为 gbk 的情况
            return bad_str.encode('gbk').decode('utf-8')
        except Exception:
            return bad_str


def force_rename_recursively(root_dir):
    print("=" * 70)
    print(f"🚀 开始对大杂烩库执行【物理强行重命名】...")
    print(f"📍 目标路径: {root_dir}")
    print("=" * 70)

    success_count = 0
    fail_count = 0

    # 使用自底向上遍历，确保先改子文件，后改父文件夹
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        
        # 1. 物理重命名所有乱码文件
        for fname in filenames:
            new_fname = restore_string(fname)
            if new_fname != fname:
                old_file_path = os.path.join(dirpath, fname)
                new_file_path = os.path.join(dirpath, new_fname)
                
                # 跳过脚本自身
                if "force_physical_rename" in fname:
                    continue
                
                try:
                    # 使用 os.rename 强行修改
                    os.rename(old_file_path, new_file_path)
                    print(f"✅ [文件成功] {fname}  ===>  {new_fname}")
                    success_count += 1
                except Exception as e:
                    # 如果失败，尝试用 shutil.move 强力移位
                    try:
                        shutil.move(old_file_path, new_file_path)
                        print(f"⚡ [文件强移] {fname}  ===>  {new_fname}")
                        success_count += 1
                    except Exception as e2:
                        print(f"❌ [文件失败] '{fname}' | 原因: {e2}")
                        fail_count += 1

        # 2. 物理重命名所有乱码文件夹
        for dname in dirnames:
            new_dname = restore_string(dname)
            if new_dname != dname:
                old_dir_path = os.path.join(dirpath, dname)
                new_dir_path = os.path.join(dirpath, new_dname)
                
                try:
                    os.rename(old_dir_path, new_dir_path)
                    print(f"📂 [目录成功] {dname}  ===>  {new_dname}")
                    success_count += 1
                except Exception as e:
                    try:
                        shutil.move(old_dir_path, new_dir_path)
                        print(f"⚡ [目录强移] {dname}  ===>  {new_dname}")
                        success_count += 1
                    except Exception as e2:
                        print(f"❌ [目录失败] '{dname}' | 原因: {e2}")
                        fail_count += 1

    print("=" * 70)
    print(f"✨ 物理重命名完成！成功/强移: {success_count} 个， 失败: {fail_count} 个。")
    print("=" * 70)


if __name__ == "__main__":
    if os.path.exists(TARGET_DIR):
        force_rename_recursively(TARGET_DIR)
    else:
        print(f"❌ 找不到路径: {TARGET_DIR}")