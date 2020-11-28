import configparser , time , hmac , hashlib , logging , os , sys , random
from linkkit import linkkit

#模拟设备属性
prop_data = {
    "PowerSwitch" : 1 ,
    "WindSpeed" : 1 ,
    "WorkMode" : 1 ,
    }
filter_data = {
    'CartridgesLife' : 5000.1 ,
    }


#A 进行基本的配置
LOG_FORMAT = "%(thread)d %(asctime)s  %(levelname)s %(filename)s %(lineno)d %(message)s"
DATE_FORMAT = "%m/%d/%Y-%H:%M:%S-%p"
logging.basicConfig(format=LOG_FORMAT , datefmt=DATE_FORMAT)
# 读取相关配置：HostName 、ProductKey 、DeviceName 、DeviceSecret
conf = configparser.ConfigParser()
config_path = 'F:\python\ws\conf\WIFI_GPRS_Config.cfg'    # 配置文件路径
conf.read(config_path)
HostName = conf.get('SETTINGS' , 'hostname')
ProductKey = conf.get('SETTINGS' , 'productkey')
DeviceName = conf.get('SETTINGS' , 'devicename')
ProductSecret = conf.get('SETTINGS' , 'productsecret')  # 一型一密
#如果是一机一密，则直接获取配置文件的DeviceSecret ，否则DeviceSecret 置空，进行一型一密的设备注册获取设备密钥
if conf.has_option('SETTINGS' , 'devicesecret'):
    DeviceSecret = conf.get('SETTINGS' , 'devicesecret')
else:
    DeviceSecret = ''

#B 初始化MQTT连接、配置物模型
lk = linkkit.LinkKit(
    host_name=HostName ,
    product_key=ProductKey ,
    device_name=DeviceName ,
    device_secret=DeviceSecret ,  # 一机一密 / 一型一密
    # product_secret = ProductSecret   #一型一密 若使用一型一密，增加此行
)

lk.enable_logger(level=logging.DEBUG)
lk.thing_setup('../Resources/WIFI_GPRS_Data.json')   #物模型路径

#若使用一型一密，需要使用此方法（使用一机一密请跳过此步）：

#C. 一型一密下注册设备
#若使用一型一密，需要使用此方法（使用一机一密请跳过此步）：
def on_device_dynamic_register(rc, value, userdata):
    if rc == 0:
        conf.set('SETTINGS', 'DEVICESECRET', value)  # 持久化device secret
        with open(config_path, 'w') as configfile:
            conf.write(configfile)
        logging.info("dynamic register device success, rc:%d, value:%s,userdata:%s" % (rc, value, userdata))
    else:
        logging.warning("dynamic register device fail,rc:%d, value:%s" % (rc, value))


# 首次启动判断，若无DEVICESECRET，则调用如上注册函数
if not conf.has_option('SETTINGS', 'DEVICESECRET'):
    lk.on_device_dynamic_register = on_device_dynamic_register
'''一型一密 ， 首次需要持久化device secret，首次之再次启动模拟设备只能使用持久化的devicesecret，否则会无法连接；
另外一型一密需要提前开启产品的动态注册接口'''

#D、各类回调函数
#@连接
def on_connect(session_flag , rc , userdata) :
    logging.info("on_connect:%d,rc:%d,userdata:" % (session_flag , rc))

#@断开连接
def on_disconnect(rc , userdata) :
    logging.info("on_disconnect:rc:%d,userdata:" % rc)

#@Topic消息
def on_topic_message(topic , payload , qos , userdata) :
    logging.info("on_topic_message:" + topic + " payload:" + str(payload) + " qos:" + str(qos))

#@订阅
def on_subscribe_topic(mid , granted_qos , userdata) :
    logging.info("on_subscribe_topic mid:%d, granted_qos:%s" %
                 (mid , str(','.join('%s' % it for it in granted_qos))))
#@取消订阅
def on_unsubscribe_topic(mid , userdata) :
    logging.info("on_unsubscribe_topic mid:%d" % mid)

#@发布消息
def on_publish_topic(mid , userdata) :
    logging.info("on_publish_topic mid:%d" % mid)

#@上报属性
def on_thing_prop_post(request_id , code , data , message , userdata) :
    logging.info("on_thing_prop_post request id:%s, code:%d message:%s, data:%s,userdata:%s" %
                 (request_id , code , message , data , userdata))

#@云端设置属性
def on_thing_prop_changed(message , userdata) :
    if "PowerSwitch" in message.keys() :
        prop_data["PowerSwitch"] = message["PowerSwitch"]
    elif "WindSpeed" in message.keys() :
        prop_data["WindSpeed"] = message["WindSpeed"]
    elif "WorkMode" in message.keys() :
        prop_data["WorkMode"] = message["WorkMode"]
    else :
        logging.warning("wrong data:%s" % message)
    lk.thing_post_property(message)  # SDK不会主动上报属性变化，如需要修改后再次上报云端，需要调用thing_post_property()发送
    print('prop_data:' , prop_data)
    print('message:' , message)
    logging.info("on_thing_prop_changed  data:%s " % message)

'''注意SDK不会主动上报属性变化，如需要修改后再次上报云端，需要调用thing_post_property()发送==
@用户可以进行属性上报，事件上报，服务响应，此调用需要在连接前'''
def on_thing_enable(userdata) :
    logging.info("on_thing_enable")

#E、SDK回调函数连接
lk.on_connect = on_connect
lk.on_disconnect = on_disconnect
lk.on_thing_enable = on_thing_enable
lk.on_subscribe_topic = on_subscribe_topic
lk.on_unsubscribe_topic = on_unsubscribe_topic
lk.on_topic_message = on_topic_message
lk.on_publish_topic = on_publish_topic
# lk.on_thing_call_service = on_thing_call_service
# lk.on_thing_event_post = on_thing_event_post
lk.on_thing_prop_changed = on_thing_prop_changed
lk.on_thing_prop_post = on_thing_prop_post
lk.connect_async()
lk.start_worker_loop()
time.sleep(2)  # 延时

