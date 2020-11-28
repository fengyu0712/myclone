import re,time

def simulateAndSendMessage(self, deviceType, host, fromPort, toPort, groupId):
    #使用主题前缀中解析出的Vxx作为版本
    pattern = '/v\d{1,}/\d{3}/'
    topicPrefix = self.mqTopicPrefixEdit.toPlainText()
    info = re.search(pattern, topicPrefix)
    infos = info[0]
    vers = infos[1:-1].split('/')
    parserVersion = vers[0]
    industryVersion = vers[1]
    print("版本信息:" + parserVersion + ":" + industryVersion)

    factory = DeviceFactory(self.__rootdir)
    selectedDevice = factory.create(deviceType, industryVersion)

    #根据groupId组装UI控件实例
    sendIntervalEdit = eval('self.sendIntervalEdit' + str(groupId + 1))

    HOST = self.mqAddressEdit.toPlainText()

    mqttSender = MessageProxy()
    mqttSender.setUri(HOST, int(self.mqPortEdit.toPlainText()), 'mqtt')
    mqttSender.setAccount(self.mqAccountEdit.toPlainText(), self.mqPasswordEdit.toPlainText())
    mqttSender.setTopicPrefix(self.mqTopicPrefixEdit.toPlainText())

    while (self.__isSendList[groupId]):
      for port in range(fromPort, toPort + 1):
        #设置电表地址
        selectedDevice.setAddress(host, port, 0)
        #使用主题前缀中解析出的版本号传入
        msg = selectedDevice.simulateMessage(parserVersion, industryVersion)
        print('-GROUP' + str(groupId) + '-' + msg)
        #hmsg = bytes.fromhex(msg)
        mqttSender.send('dtu/up/firemonitor', msg)

      time.sleep(int(sendIntervalEdit.toPlainText()) * 60)



if __name__=="__main__":
    # 类测试代码
    print('-- Basic test for deviceModel --')
    factory = DeviceFactory('../rules')
    emeter = factory.create('emeter')

    print('-- Basic test for messageProxy --')
    mqttSender = MessageProxy()
    mqttSender.setUri('47.99.93.72', 1883, 'mqtt')
    mqttSender.setAccount('sapain', 'password')
    mqttSender.setTopicPrefix('/sapain/')

    print('-- Send Test Start --')

    for ip in range(100, 199):
        # 设置电表地址
        emeter.setAddress('192.168.2.0', ip, 0)
        # 使用v1解析器和100模板生成模拟数据
        msg = emeter.simulateMessage('v1', '000')
        mqttSender.send('test', msg)
        print('--MSG--' + msg)

    print('-- Send Test Over --')