import shutil
from pathlib import Path


def removePath(path):

    try:
        shutil.rmtree(path)
        print(f"文件夹 '{path}' 及其所有内容已成功删除")
    except FileNotFoundError:
        print(f"文件夹 '{path}' 未找到")
    except PermissionError:
        print(f"没有权限删除文件夹 '{path}'")
    except Exception as e:
        print(f"删除文件夹时发生错误: {e}")
