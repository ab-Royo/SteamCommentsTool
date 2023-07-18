# -*- coding: utf-8 -*-
import json
import os
import sqlite3 as sqlite
import Logcolor
import requests


class Update:
    @staticmethod
    def checkUpdate():
        try:
            response = requests.get("https://api.github.com/repos/ab-Royo/SteamCommentsTool/releases/latest")
            print(Logcolor.responseINFO() + "Github最新正式版本 v" + response.json()["tag_name"] + ", 发布时间 " + response.json()["published_at"])
        except Exception as e:
            print(Logcolor.responseERROR() + f"检查Github更新失败: {e}")


# TODO: 读取 "./config/settings.json" 下的配置
class Proxy:
    @staticmethod
    def ProxyStatus():
        with open("./config/settings.json", encoding="utf-8", mode="r") as __settings:
            __settings = __settings.read()
            __settings = json.loads(__settings)
            __ProxyStatus = __settings["Proxy"]["Enable"]
            if __ProxyStatus == "":
                print("./config/settings.json 文件中 Enable 属性为空!")
                pass
            else:
                return __ProxyStatus

    @staticmethod
    def ProxyMode():
        with open("./config/settings.json", encoding="utf-8", mode="r") as __settings:
            __settings = __settings.read()
            __settings = json.loads(__settings)
            __ProxyMode = __settings["Proxy"]["ProxyMode"]
            if __ProxyMode == "":
                print("./config/settings.json 文件中 ProxyMode 属性为空!")
                pass
            else:
                return __ProxyMode

    @staticmethod
    def ProxyURL():
        with open("./config/settings.json", encoding="utf-8", mode="r") as __settings:
            __settings = __settings.read()
            __settings = json.loads(__settings)
            __ProxyURL = __settings["Proxy"]["ProxyURL"]
            if __ProxyURL == "":
                print("./config/settings.json 文件中 ProxyURL 属性为空!")
            else:
                return __ProxyURL


class DataBase:
    @staticmethod
    def initDB():
        __DBExist = os.path.exists("./friends.db")
        # 如果文件存在
        if __DBExist == 1:
            print(Logcolor.databaseINFO() + "数据库已存在!请根据提示输入用户名、密码、验证码（如有）")
        else:
            # 创建数据库文件并初始化
            __steamDB = sqlite.connect("friends.db")
            print(Logcolor.databaseWARN() + "数据库不存在!")
            # 创建游标 (cursor)
            __cursor = __steamDB.cursor()
            """
            id 64位ID pk
            nickname 好友昵称
            """
            __cursor.execute('''CREATE TABLE friends
            (id varchar(30) primary key,
            nickname char(50));''')
            # 提交并关闭流
            print(Logcolor.databaseINFO() + "数据库已创建。请进入friends.db编辑好友信息")
            print(Logcolor.databaseINFO() + "使用数据库工具打开`friends.db` ，找到表名为`friends`的表，在表中添加字段：id是要留言的好友的64位SteamID，nickname列是对好友的昵称")
            __steamDB.commit()
            __steamDB.close()
            # 退出程序
            exit()

    @staticmethod
    def getDatabase():
        try:
            conn = sqlite.connect("friends.db")
            c = conn.cursor()
            c.execute("SELECT id, nickname FROM friends")
            # TODO：自动获取好友列表
            friends = c.fetchall()
            conn.close()
            print(Logcolor.databaseINFO() + "数据库读取成功")
            return friends
        except Exception as e:
            print(Logcolor.databaseERROR() + f"数据库异常：{e}")
            pass


if __name__ == "__main__":
    # settings
    print("ProxyStatus: " + str(Proxy.ProxyStatus()))
    print("ProxyMode: " + str(Proxy.ProxyMode()))
    print("ProxyURL: " + str(Proxy.ProxyURL()))
    Update.checkUpdate()
