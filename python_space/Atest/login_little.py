login_inf={'username':'admin','password':'123456'}
user_name=login_inf['username']
password=login_inf['password']

u_name=input("请输入账户名：")
time=3
while True:
    if u_name ==user_name:
        u_password = input("请输入登录密码：")
        time = time - 1
        while time >= 0:
            if u_password==password:
                print("登录成功")
                break
            else:
                if time>0:
                    print("您还有%s次机会"%time)
                    u_password=input("密码错误，请重新输入：")
                    time-=1
                else:
                    print("错误次数已达最大次数，程序即将退出")
                    break
        break
    else:
        u_name=input("请输入正确的账户名:")

