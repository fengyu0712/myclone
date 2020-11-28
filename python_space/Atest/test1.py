import subprocess,os

def open_exe(file):
    os.startfile(file)
def cmd(shell):
    os.system(shell)
def cmd2(shell):
    subprocess.check_call(shell)
    pass
if __name__=="__main__":
    file="D:\Program Files (x86)\Appium\Appium.exe"
    shell1="start /b node 'D:/Program%Files%(x86)/Appium/node_modules/appium/lib/server/main.js' --address 127.0.0.1 --port 4723"
    shell2="allure generate E:\python_space\TestResult/Result/allure_result -o E:\python_space\TestResult/Report/allure_report --clean"
    shell3="allure open E:\python_space\TestResult/Report/allure_report"
    open_exe(file)
    # cmd(shell2)
    cmd(shell1)
