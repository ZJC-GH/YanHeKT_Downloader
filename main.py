'''
Project      :
FilePath     : \FINAL\main.py
Descripttion :
Author       : GDDG08
Date         : 2022-11-08 02:07:44
LastEditors  : ZJC-GH
LastEditTime : 2023-02-23 02:06:00
'''
import requests
import m3u8dl
import sys
import os
import time

headers = {
    'Origin': 'https://www.yanhekt.cn',
    "xdomain-client": "web_user",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26'
}


if __name__ == '__main__':

    # 这段代码会首先检查是否有命令行参数提供；如果没有，就会提示用户输入课程ID。
    if len(sys.argv) > 1:
        courseID = sys.argv[1]
    else:
        courseID = input("请输入课程ID: ")

    course = requests.get(
        f'https://cbiz.yanhekt.cn/v1/course?id={courseID}&with_professor_badges=true', headers=headers)
    req = requests.get(f'https://cbiz.yanhekt.cn/v2/course/session/list?course_id={courseID}', headers=headers)
    print(course.json()['data']['name_zh'])

    videoList = req.json()['data']
    for i, c in enumerate(videoList):
        print(i, c['title'])

    dirName = r'./' + course.json()['data']['name_zh'] + '-' + course.json()['data']['professors'][0]['name']

    if not os.path.exists(dirName):
        os.makedirs(dirName)

    # 自动遍历下载所有视频，并分别下载投影录屏(vga)和视频(video)格式
    for i, c in enumerate(videoList):
        fileNameVGA = str(courseID) + '-' + c['title'].replace("/", "-") + '-VGA'  # 防止文件名中的/导致路径错误
        filePathVGA = os.path.join(dirName, fileNameVGA)
        fileNameVideo = str(courseID) + '-' + c['title'].replace("/", "-") + '-Video'
        filePathVideo = os.path.join(dirName, fileNameVideo)

        # 下载投影录屏
        if 'vga' in c['videos'][0] and not os.path.isfile(filePathVGA + '.mp4'):  # 检查是否存在vga链接且文件未下载
            print(f"Downloading VGA for {fileNameVGA}")
            m3u8dl.M3u8Download(c['videos'][0]['vga'], dirName, fileNameVGA, max_workers=32)
        elif 'vga' in c['videos'][0]:
            print(f"{fileNameVGA}.mp4 already exists. Skipping download.")

        # 下载视频
        if 'main' in c['videos'][0] and not os.path.isfile(filePathVideo + '.mp4'):  # 检查是否存在main链接且文件未下载
            print(f"Downloading Video for {fileNameVideo}")
            m3u8dl.M3u8Download(c['videos'][0]['main'], dirName, fileNameVideo, max_workers=64)
        elif 'main' in c['videos'][0]:
            print(f"{fileNameVideo}.mp4 already exists. Skipping download.")

    # input("按 Enter 键退出...")
    # 输出等待信息
    print("此处等待10秒，之后将自动退出或进行批处理文件中的下一命令。")

    # 等待10秒，也能避免拥塞
    time.sleep(10)
