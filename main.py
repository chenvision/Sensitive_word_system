import os
import shutil
source_directory=r"D:\@DevCode\project2\农机作业轨迹数据"
destination_directory=r"D:\@DevCode\project2\实验数据"
if not os.path.exists(destination_directory):
    os.makedirs(destination_directory)

files=[f for f in os.listdir(source_directory) if f.endswith(".xlsx")]
# 检查文件数量并选择第50个文件
if len(files) >= 50:
    file_50 = files[49]  # 索引从0开始，所以第50个文件索引为49
    file_path = os.path.join(source_directory, file_50)

    # 复制文件到目标目录
    shutil.copy(file_path, os.path.join(destination_directory, file_50))
    print(f"第50个表格文件 {file_50} 已复制到 {destination_directory}")
else:
    print("文件夹中的.xlsx文件少于50个。")