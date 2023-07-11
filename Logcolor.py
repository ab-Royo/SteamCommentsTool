def responseINFO():
    return "\033[92m[POST_message] \033[0m"


def responseWARN():
    return "\033[93m[POST_warning] \033[0m"


def responseERROR():
    return "\033[31m[POST_error] \033[0m"

def databaseINFO():
    return "\033[92m[DB_message] \033[0m"


def databaseWARN():
    return "\033[93m[DB_warning] \033[0m"


def databaseERROR():
    return "\033[31m[DB_error] \033[0m"

def message():
    return "\033[95m[message] \033[0m"

# 调试, 分别输出三种不同颜色的消息
if __name__ == "__main__":
    print(responseINFO() + "这是一条消息")
    print(responseWARN() + "这是一条警告")
    print(responseERROR() + "这是一条错误")
    print(databaseINFO() + "这是一条消息")
    print(databaseWARN() + "这是一条警告")
    print(databaseERROR() + "这是一条错误")
    print(message() + "这是一条消息")
