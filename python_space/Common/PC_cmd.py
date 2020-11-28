import os

def open_exe(file):
    os.startfile(file)
def cmd(shell):
    os.system(shell)
if __name__=="__main__":
    file="D:\Program Files (x86)\Appium\Appium.exe"
    shell1="start /b node 'D:/Program Files (x86)/Appium/node_modules/appium/lib/server/main.js' --address 127.0.0.1 --port 4723"
    shell2="allure generate E:\python_space/1test\Test_pytest\ -o E:\python_space/1test\Test_pytest\ --clean"
    shell3="allure open -h 127.0.0.1 -p 8083 ./report/"
    # open_exe(file)
    cmd(shell2)
    cmd(shell3)

