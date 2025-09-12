import os
import shutil

# 設定來源資料夾與目標資料夾
source_dir = os.path.dirname(os.path.abspath(__file__))
dest_dir = os.path.join(source_dir, "新增資料夾")

# 如果目標資料夾不存在，就建立一個
if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

# 取得來源資料夾下所有檔案的列表，並過濾掉資料夾
all_files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]

# 排除自己這個 .py 檔案
all_files = [f for f in all_files if not f.endswith(".py")]

# 根據修改時間排序，最新的在前面
all_files.sort(key=lambda x: os.path.getmtime(os.path.join(source_dir, x)), reverse=True)

# 取得最新的兩個檔案
files_to_move = all_files[:2]

# 移動檔案
for file_name in files_to_move:
    source_file_path = os.path.join(source_dir, file_name)
    dest_file_path = os.path.join(dest_dir, file_name)
    shutil.move(source_file_path, dest_file_path)
    print(f"已將 {file_name} 移動至 {dest_dir}")

print("\n操作完成！")
