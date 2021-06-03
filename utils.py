# coding=utf-8
import os
import shutil
import socket


def get_local_host_ip():
    # 反回本机ip地址，失败返回127.0.0.1
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception as e:
        print('get local ip error, err={}'.format(e))
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


def copy_py_as_pyc(file_path):
    file_path = os.path.abspath(file_path)
    des_path = file_path.replace('.py', '.pyc')
    shutil.copyfile(file_path, des_path)
