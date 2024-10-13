import os


def str_in_list(st, li):
    """字符串存在与list成员中"""
    for l in li:
        if st in l:
            return True
    return

def path_win2linux(filepath):
    """路径windows格式转换成linux格式"""
    try:
        filepath = os.path.abspath(filepath)
        if '\\' in filepath:
            filepath = '/'.join(filepath.split(
                '\\'))  # transform the windows path to linux path
    finally:
        return filepath

# string 按转/分割成list
def Str2List(string, spl="\n"):
    l = string.split(spl)
    if l:
        d = list(filter(None, l))
        return d