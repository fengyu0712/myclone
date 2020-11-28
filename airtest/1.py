# -*- encoding=utf8 -*-
__author__ = "lijq36"

from airtest.core.api import *
from airtest.cli.parser import cli_setup

if not cli_setup():
    auto_setup(__file__, logdir=True, devices=[
            "Android://127.0.0.1:5037/127.0.0.1:62001?cap_method=JAVACAP&&ori_method=ADBORI",
    ])snapshot(msg="请填写测试点.")
snapshot(msg="请填写测试点.")
snapshot(msg="请填写测试点.")
snapshot(msg="请填写测试点.")
sleep(1.0)
sleep(1.0)
sleep(1.0)
sleep(1.0)
sleep(1.0)
sleep(1.0)



# script content
print("start...")


# generate html report
# from airtest.report.report import simple_report
# simple_report(__file__, logpath=True)

start_app('com.midea.ai.appliances')

