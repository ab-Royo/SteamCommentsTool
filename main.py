# 导入需要的模块
import time
import random
import requests
import steam
import Settings
import Logcolor
from utils import DataBase, Update
# 项目版本
__version__ = "1.0.0-alpha"
# 定义成功和失败的次数
success_count = 0
fail_count = 0
not_send_count = 0

# 版本信息，检查更新
print(Logcolor.responseINFO() + "SteamCommentsTool 当前版本 v" + __version__)
Update.checkUpdate()
# 检测数据库存在, 初始化
# DataBase.initDB()
DataBase.initSteamDB()

# 创建 Steam 客户端对象
client = steam.SteamClient()

# 登录 Steam 账号
# TODO: 无密码登录，keylogin()
client.cli_login()

# 获取cookie
cookie_jar = client.get_web_session().cookies
cookie_dict = cookie_jar.get_dict()

# Debug cookie_dict字典值查看
# print(cookie_dict)

# 读取配置文件,获取代理信息
Enable = Settings.Proxy
ProxyMode = Settings.ProxyMode
ProxyURL = Settings.ProxyURL

# 如果代理开启
if Enable:
    print(Logcolor.responseWARN() + "代理模式已启用, 代理地址为: {}://{}".format(ProxyMode, ProxyURL))
else:
    print(Logcolor.responseWARN() + "代理模式未启用")

# 连接数据库，获取 64 位 ID 和昵称
# friends = DataBase.getDatabase()
friends = DataBase.getSteamDB()

# 手动输入留言文本，使用 {0} 作为昵称的占位符
# TODO：json留言支持
text = input("请输入留言文本（使用{0}作为对好友称呼的占位符,使用{n}来作为换行的占位符）：")

# 把“\n” 替换成换行符
text = text.replace("{n}", "\n")

# 遍历好友列表，替换昵称，发送留言请求
if Enable:
    proxy = {ProxyMode: ProxyURL}  # 拼接 proxy
    for userID, nickname, recently in friends:
        # 替换昵称
        message = text.format(nickname)
        # 构造留言请求的 URL 和参数
        Headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/110.0.0.0 Safari/537.36'
        }
        url = f"https://steamcommunity.com/comment/Profile/post/{id}/-1/"
        data = {
            "comment": message,
            "count": 6,
            "sessionid": cookie_dict["sessionid"],
            "feature2": -1
        }
        if recently == "true":
            # 发送留言请求
            try:
                response = requests.post(url, headers=Headers, data=data, proxies=proxy, cookies=cookie_dict)
                # 检查留言是否成功
                if response.json()["success"]:
                    print(Logcolor.responseINFO() + f" {nickname} 留言成功！https://steamcommunity.com/profiles/{id}")
                    # 更新成功次数
                    success_count += 1
                else:
                    print(Logcolor.responseERROR() + f" {nickname} 留言失败！https://steamcommunity.com/profiles/{id}")
                    print(Logcolor.responseWARN() + f"{nickname} POST错误信息为：{response.json()}")
                    # 更新失败次数
                    fail_count += 1
            except Exception as e:
                print(Logcolor.responseERROR() + f"requests异常：{e}")
                # 更新失败次数
                fail_count += 1
            # 随机间隔2-5秒，减少风控概率
            time.sleep(random.uniform(2, 5))
        else:
            print(Logcolor.responseWARN() + f" {nickname} 不发送留言，recently值为false")
            not_send_count += 1
    # 打印成功和失败的次数
    print(Logcolor.responseINFO() + f"完成全部留言，成功 {success_count} 次，失败 {fail_count} 次，不发送{not_send_count} 次。")

# 如果代理未开启
else:
    for userID, nickname, recently in friends:
        # 替换昵称
        message = text.format(nickname)
        # 构造留言请求的 URL 和参数
        Headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/110.0.0.0 Safari/537.36'
        }
        url = f"https://steamcommunity.com/comment/Profile/post/{id}/-1/"
        data = {
            "comment": message,
            "count": 6,
            "sessionid": cookie_dict["sessionid"],
            "feature2": -1
        }
        if recently == "True":
            # 发送留言请求
            try:
                response = requests.post(url, headers=Headers, data=data, cookies=cookie_dict)
                # 检查留言是否成功
                if response.json()["success"]:
                    print(Logcolor.responseINFO() + f" {nickname} 留言成功！https://steamcommunity.com/profiles/{id}")
                    # 更新成功次数
                    success_count += 1
                else:
                    print(Logcolor.responseERROR() + f" {nickname} 留言失败！https://steamcommunity.com/profiles/{id}")
                    print(Logcolor.responseWARN() + f"{nickname} POST错误信息为：{response.json()}")
                    # 更新失败次数
                    fail_count += 1
            except Exception as e:
                print(Logcolor.responseERROR() + f"requests异常：{e}")
                # 更新失败次数
                fail_count += 1
            # 随机间隔2-5秒，减少风控概率
            time.sleep(random.uniform(2, 5))
        else:
            print(Logcolor.responseWARN() + f" {nickname} 不发送留言，recently值为false")
            not_send_count += 1
    # 打印成功和失败的次数
    print(Logcolor.responseINFO() + f"完成全部留言，成功 {success_count} 次，失败 {fail_count} 次，不发送{not_send_count} 次。")
