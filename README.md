# SteamCommentsTool

<div align="center">


<!-- prettier-ignore-start -->
<!-- markdownlint-disable-next-line MD036 -->
_✨Steam个人资料留言板留言工具_
<!-- prettier-ignore-end -->

</div>

<p align="center">
  <a href="https://raw.githubusercontent.com/ab-Royo/SteamCommentsTool/master/LICENSE">
    <img src="https://img.shields.io/badge/license-GPL3.0-GREEN" alt="license">
  </a>
  <img src="https://img.shields.io/badge/python-3.6|3.7|3.8|3.9-blue" alt="python">
  <img src="https://img.shields.io/badge/SQLite-3-ff69b4" alt="SQLite">
</p>


## 简介

Steam个人资料留言板留言工具。支持一次发送至多个好友，支持不同好友自定义称呼



## TODO
- [x] 可以使用[SteamCommentsToDB](https://github.com/ab-Royo/SteamCommentsToDB)的数据库
- [ ] 仅需登录一次，后续自动登录
- [ ] 留言内容目前仅命令行输入，之后可通过json传入
- [ ] 自动获取好友列表至数据库
- [ ] Steam留言风控问题...


## 如何使用
推荐3.9.X版本的Python环境，然后按照以下步骤进行操作
https://www.python.org/ftp/python/3.9.13/python-3.9.13-amd64.exe
>如何安装Python
>https://www.liaoxuefeng.com/wiki/1016959663602400/1016959856222624


### 1.获取本项目
**如果你是新手**

跳转至 [Releases](https://github.com/ab-Royo/SteamCommentsTool/releases) 页面，下载最新版本的压缩包，解压到你想要的位置。此包已包含了本项目的所有文件，你可以直接运行本项目。


---

**如果你有一定代码基础**

如果你有Git，在命令行中输入以下命令
```
git clone https://github.com/ab-Royo/SteamCommentsTool.git
```

如果你没有Git，那么你可以点击本页面右上角的**Code**按钮，然后选择**Download ZIP**，下载完成后解压到你想要的位置

### 2.安装依赖
*（如果你在上一步直接在Releases中下载了项目则略过本步骤）*

进入你解压出来的文件夹中
#### Windows10:
点击文件资源管理器左上角**文件**，选择**打开Windows PowerShell**
在命令行中分别输入以下2条命令
```Python{.line-numbers}
pip install requests
pip install -U "steam[client]"
```

#### Windows11:
在文件资源管理器窗口内空白处单击鼠标右键，选中**在终端中打开**
在命令行中分别输入以下2条命令
```Python{.line-numbers}
pip install requests
pip install -U "steam[client]"
```
---

之后前往`C:\Users\用户名\AppData\Local\Programs\Python\Python39\Lib\site-packages\steam\__init__.py`,添加代码
```
from steam.client import SteamClient
```

### 3.创建并配置数据库
#### Windows10:
在 `SteamCommentsTool` 文件夹内，点击文件资源管理器左上角**文件**，选择**打开Windows PowerShell**，在弹出的窗口中输入以下命令
```
python main.py
```
#### Windows11:
在 `SteamCommentsTool` 文件夹内，在文件资源管理器窗口内空白处单击鼠标右键，选中**在终端中打开**，在弹出的窗口中输入以下命令
```
python main.py
```
---
随后程序提示数据库不存在，将会在 `SteamCommentsTool` 文件夹内生成一个名为 `friends.db` 的数据库文件，此时你需要配置数据库
#### friends表架构（这是本程序使用的数据库表）
| 列名          | 数据类型      | 描述           |
|-------------|-----------|--------------|
| userID      | char(64)  | 用户的SteamID64 |
| nickname    | char(100) | 你对用户的称呼      |
| profileName | char(100) | 用户的个人资料昵称    |
| recently    | char(10)  | 用户是否符合时间次数条件 |
#### msg表结构
| 列名         | 数据类型        | 描述              |
|------------|-------------|-----------------|
| ContentID  | varchar(30) | Steam每一条评论的唯一ID |
| userID     | char(64)    | 评论发送者的SteamID64 |
| nickName   | char(100)   | 评论发送者的昵称        |
| userAvatar | char(200)   | 评论发送者的头像        |
| Content    | char(1000)  | 评论内容            |
| UnixTime   | char(100)   | 评论发送的Unix时间     |
| sendTime   | char(20)    | 评论发送的北京时间       |

你需要一个SQLite数据库管理工具，例如 [DB Browser for SQLite (免费)](https://sqlitebrowser.org/dl/)，[DataGrip](https://www.jetbrains.com/datagrip/)等等

使用数据库工具打开`SteamDB.db` ，找到表名为`friends`的表，在表中**添加字段**：
1. userID列是要留言的好友的64位SteamID
2. nickname列是你对好友的昵称
3. profileName列是好友的个人资料昵称（这个可以 **不填留空** ，新增此列的原因是可以通过[SteamCommentsToDB](https://github.com/ab-Royo/SteamCommentsToDB)使用msg表的数据导入信息）
4. recently列是 是否留言，如果要留言则填写文字`true`，否则填写`false`（此列的内容可以通过[SteamCommentsToDB](https://github.com/ab-Royo/SteamCommentsToDB)使用msg表的数据导入信息）

获取好友的SteamID64可以使用使用 [SteamID64](https://steamid.xyz/) 等网页工具，或通过[SteamCommentsToDB项目](https://github.com/ab-Royo/SteamCommentsToDB)使用msg表的数据导入信息


### 4.配置代理
如果你的网络不能直连Steam（即无法打开 https://steamcommunity.com ），那么你需要配置代理，否则请跳过这一步

将 `\SteamCommentsTool\Settings.py` 中的 **"Proxy": false** 字段中的`False`改为`True`，并在 **"ProxyURL":** 字段的引号内填入你的代理地址，如果你使用ClashforWindows，那么默认的代理地址就是：
>127.0.0.1:7890


### 5.再次运行本项目
#### Windows10:
在 `SteamCommentsTool` 文件夹内，点击文件资源管理器左上角**文件**，选择**打开Windows PowerShell**，在弹出的窗口中输入以下命令
```Python
python main.py
```
#### Windows11:
在 `SteamCommentsTool` 文件夹内，在文件资源管理器窗口内空白处单击鼠标右键，选中**在终端中打开**，在弹出的窗口中输入以下命令
```Python
python main.py
```
---

随后根据程序提示操作即可:
1. 首先应该提示 数据库已存在
2. 输入Username：输入你登录Steam时输入的用户名（注意不是用户昵称，也不是注册邮箱），然后按回车键确认；
3. 输入Password：输入你的账号密码，输入密码时命令行没有文字显示是正常现象，输入后按回车键确认；
4. Enter 2FA code / Email code：如果你启用了 手机令牌或是邮箱令牌 ，请在此输入令牌验证码输入后按回车键确认。
5. 输入留言内容：输入留言内容，可以输入`{0}`用于替换数据库里每位好友的`nickname`的内容，输入`{n}`来换行，之后按回车键确认，程序会自动向数据库内所有的64位SteamID发送留言。
>需要说明的是:登录获取Cookie功能使用第三方ValvePython开源的[Steam](https://github.com/ValvePython/steam)项目完成，本程序不存储也不传输用户密码信息。



## 常见问题

1. 程序运行时出现以下提示
```Python
Traceback (most recent call last):
File"X:\...\SteamCommentsTool\main.py"，line 14，in <module>
client = steam.steamClient()
AttributeError: module 'steam' has no attribute 'steamClient!
```
程序依赖Steam包异常或安装失败。

请阅读教程第2步确保Steam库配置正常。

2. 程序登录时出现以下提示
```Python
WebAPI boostrap failed: HTTPSConnectionPool(host='api.steampowered.com'，port=443):Read timed out. (read timeout=3)
``````
或是 发送留言时发生异常
```Python
HTTPSConnectionPool(host='steamcommunity.com', port=443): Max retries exceeded with url: /comment/Profile/post/7656xxxx/-1/ (Caused by ProxyError('Cannot connect to proxy.', NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x00000281D78EBE50>: Failed to establish a new connection: [WinError 10061] 由于目标计算机 积极拒绝，无法连接。')))
```
或是 发送留言时发生异常(已确认对方未关闭留言板)
```Python
{'success': False, 'error': 'The settings on this account do not allow you to add comments.'}
```
网络异常或代理配置错误。

请阅读教程第4步确保代理配置正常，或更换你的网络节点。

3. 程序留言时出现以下提示
```Python
给 xxx 留言失败！
xxx POST结果为： ...
```
请查看对方留言板是否开启好友才能留言，或是禁止留言；可参考POST结果中`'error':`的提示信息。

4. 程序登录时出现以下提示
```Python
Incorrect code 或 Invalid password
```
令牌验证码错误 或 账户名(非昵称)错误 或 密码错误

5. 程序输入留言内容时出现以下提示
```Python
IndexError: Replacement index 1 out of range for positional args tuple
```
请仅使用`{0}`作为nickname替换符，`{n}`作为换行符
不要使用`{1}`、`{2}`等等，否则会出现此错误

6. 程序运行时提示数据库未创建，但文件夹内已有`friends.db`

2023/8/2日更新后启用了新数据库`SteamDB.db`，你可以自行将原数据库文件中的数据写入新数据库文件中。

本次更新数据库实现两个Steam项目的数据库的共用，将支持 Steam留言获取->按时间次数条件筛选->自动填写`friends表`->符合条件留言 。



## ovo
- 作者是自学Python的初学者，本程序是作者学习Python的练手项目，程序不规范有疏漏在所难免，欢迎ISSUE或PR指正。
- 本程序开发初衷是为了方便Steam各好友之间留言便利快捷，请勿滥用本程序用于广告等违背本意的用途。
- 我觉得对于批量留言的诚意问题，每个人见仁见智。我个人认为，使用程序来批量留言并不是缺乏诚意，而是一种便捷的方式。 **但是，这并不意味着对好友的留言轻视，对于我来说，我会在留言之后再次认真地回复好友的留言。** 
- 不建议使用本程序大规模留言，易遭到Steam风控（无法发出或留言被隐藏）；因为使用本程序造成的任何后果均由使用者自行承担。


### =D
Miku39佬的Steam assistant项目厉害！是看到了Miku39佬的项目之后有了写Steam的两个项目的想法！

**感谢以下开发者对本项目作出的贡献：**

<a href="https://github.com/ab-Royo/SteamCommentsTool/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=ab-Royo/SteamCommentsTool" />
</a>

Made with [contrib.rocks](https://contrib.rocks).

如果有任何问题或建议，欢迎ISSUE或PR。
