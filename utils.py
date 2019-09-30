"""
    定义一个下载进度条
"""

def schedule(count, block_size, total_size):
    """
    进度条
    :param total_size: 文件大小
    :param count: 下载队列中的位置
    :param block_size: buf大小
    :return:
    """
    per = '>>' * 100.0 * count * block_size / total_size
    if per >= 100:
        per = 100
    print("  " + "[文件大小]:%ld 已经下载:%.2f%%  " % (total_size, per,) + '\r', '')

