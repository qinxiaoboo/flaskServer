from flaskServer.config.config  import CHROME_EXTEND_UPDATE,CHROME_EXTEND_PATH
from loguru import logger
import json
import os
import shutil
import fnmatch
CHROME_EXTEND_DEFAULT_PAHT = r'C:\Users\Administrator\AppData\Local\google\Chrome\User Data\Default\Extensions\\'


def get_version_from_manifest(file_path):
    """从 manifest.json 文件中获取 version 字段"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件 {file_path} 不存在")
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
            return data.get('version', None)  # 获取 version 字段，若不存在返回 None
        except json.JSONDecodeError:
            raise ValueError(f"文件 {file_path} 不是有效的 JSON 格式")


def compare_versions(dir1, dir2):
    """比较两个目录下的 manifest.json 文件中的 version 字段"""
    # 构造 manifest.json 文件路径
    manifest1 = os.path.join(dir1, 'manifest.json')
    manifest2 = os.path.join(dir2, 'manifest.json')
    try:
        # 获取两个文件的 version 字段
        version1 = get_version_from_manifest(manifest1)
        version2 = get_version_from_manifest(manifest2)
        # 比较 version 字段
        if version1 == version2:
            logger.info(f"{dir1}两个 manifest.json 文件中的版本号相同: {version1}")
            return False
        else:
            logger.info(f"版本号不同:\n{dir1}: {version1}\n{dir2}: {version2}")
            return True
    except (FileNotFoundError, ValueError) as e:
        logger.error(f"发生错误: {e}")
        return False


def get_latest_directory(parent_dir):
    """获取指定目录下最新修改的文件夹路径"""
    # 确保给定路径是有效的目录
    if not os.path.isdir(parent_dir):
        raise ValueError(f"{parent_dir} 不是有效的目录")

    # 列出目录下所有子文件夹
    directories = [d for d in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, d))]

    if not directories:
        raise ValueError(f"{parent_dir} 目录下没有子文件夹")

    # 获取每个文件夹的最后修改时间，并根据修改时间排序
    directories.sort(key=lambda d: os.path.getmtime(os.path.join(parent_dir, d)), reverse=True)

    # 返回最新的文件夹路径
    latest_dir = os.path.join(parent_dir, directories[0])
    return latest_dir


def copy_and_replace(src_dir, dest_dir):
    # 遍历源目录中的所有文件和目录
    for item in os.listdir(src_dir):
        src_item = os.path.join(src_dir, item)
        dest_item = os.path.join(dest_dir, item)

        if os.path.isdir(src_item):
            if item.startswith("_"):
                if not os.path.exists(dest_item) :
                    # 复制目录
                    shutil.copytree(src_item, dest_item)
            else:
                # 如果目标目录已存在同名目录，先删除
                if os.path.exists(dest_item):
                    shutil.rmtree(dest_item)
                # 复制目录
                shutil.copytree(src_item, dest_item)
        else:

            # 如果是文件，直接复制
            shutil.copy2(src_item, dest_item)


def updateExten():
    if isinstance(CHROME_EXTEND_UPDATE, list):
        for item in CHROME_EXTEND_UPDATE:
            if ":" in item:
                l = item.split(":")
                name = l[0]
                key = l[1]
                # 比较两个目录中的 manifest.json 文件
                dir1 = os.path.join(CHROME_EXTEND_PATH, name)
                dir2 = get_latest_directory(os.path.join(CHROME_EXTEND_DEFAULT_PAHT, key))
                flag  = compare_versions(dir1, dir2)
                if flag:
                    copy_and_replace(dir2, dir1)
                    logger.info(f"{dir2}目录下的内容，移动到{dir1}目录下")
    logger.info("插件更新完成")

if __name__ == '__main__':
    updateExten()
