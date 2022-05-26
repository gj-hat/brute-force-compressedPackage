import itertools
import zipfile
from concurrent.futures import ProcessPoolExecutor
import py7zr
import sys
import getopt

pas_len = ''
pass_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.!@#$%^&*()_+-=[]{}|;\':",<>?/'
process_num = 0
out_path = ''
file_form = '7z'
path = ''

try:
    opts, args = getopt.gnu_getopt(sys.argv[1:], "l:p:t:o:h", [])
except:
    sys.exit()
for opt, value in opts:
    if opt in "-h":
        print("|---------------------------------------------------------------------|")
        print("|                                                                     |")
        print("|        这是一个基于python的暴力破解工具,目前支持7z,zip格式          |")
        print("|        作者: 郭小傻 版本:v1.0  时间: 2022年05月25日19:04:21         |")
        print("|                                                                     |")
        print("|---------------------------------------------------------------------|")
        print("")
        print("-l 密码长度区间例如8-16")
        print("-p 可能含有的密码字符串 如果不填写则使用默认字符集 \n   例如您大致记得您的密码只有小写则此处可填写abcdefghijklmnopqrstuvwxyz")
        print("-t 线程数 这取决于您的电脑 可以省略")
        print("-o 输出文件路径 可以省略")
        print("最后一个参数是文件路径")
        sys.exit()
    if opt in "-p":
        # 可能含有的密码字符串
        pass_chars = value
    if opt in "-t":
        # 线程数
        process_num = value
    if opt in "-o":
        # 输出文件路径
        out_path = value
    if opt in "-l":
        # 密码长度区间例如1-2
        pas_len = value
# 文件路径
path = args[0]
if pas_len == '' or path == '':
    sys.exit()
if out_path == '':
    # 获取文件路径
    out_path = path.split('.')[0] + '_out.txt'
if path.endswith('.zip'):
    file_form = 'zip'
elif path.endswith('.7z'):
    file_form = '7z'


def fun_7z(filename, password):
    try:
        with py7zr.SevenZipFile(filename, mode='r', password=password) as z:
            z.extractall()
        return True
    except:
        return False


def fun_zip(filename, password):
    try:
        zip_file = zipfile.ZipFile(filename, 'r')
        zip_file.open(pwd=password)
        return True
    except:
        return False


def thread_fun(psd_le):
    for c in itertools.permutations(pass_chars, psd_le):
        password = "".join(c)
        zip_pojie(password)


def zip_pojie(password):
    if file_form == 'zip':
        result = fun_zip(path, password)
    elif file_form == '7z':
        result = fun_7z(path, password)
    else:
        print("格式不支持")
    if not result:
        print("%s is error." % password)
    else:
        print('Decompression succeeded,password is:', password)
        f = open("out_path", 'w')
        f.write('Decompression succeeded,password is:' + password + '\n')


if __name__ == '__main__':
    l = pas_len.split("-")
    le = [i for i in range(int(l[0]), int(l[1]) + 1)]
    if process_num != 0:
        with ProcessPoolExecutor(max_workers=int(process_num)) as pool:
            pool.map(thread_fun, le)
    else:
        with ProcessPoolExecutor() as pool:
            pool.map(thread_fun, le)
