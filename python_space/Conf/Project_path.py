import os
# from Common.conf import Read_conf
Conf_file_path=os.path.split(os.path.realpath(__file__))[0]
projectfail=os.path.dirname(Conf_file_path)
# print(projectfail)
"根据配置文件读取当前项目所在的绝对路径"
# projectfail=Read_conf(os.path.join(Conf_file_path+"//project_path.conf")).get_value("Path","projectfail")
Common_path=os.path.join(projectfail,"Common/")
Conf_path=os.path.join(projectfail,"Conf/")
InterfaceTest_path=os.path.join(projectfail,"InterfaceTest/")
Log_path=os.path.join(projectfail,"Log/")
TestData_path=os.path.join(projectfail,"Testdata/")
# TestAudioData_path=os.path.join(TestData_path,"test_audio/")
TestResult_path=os.path.join(projectfail,"TestResult/Result/")
TestReport_path=os.path.join(projectfail,"TestResult/Report/")
Source_path=os.path.join(projectfail,"Source/")
Image_path=os.path.join(projectfail,"Image/")
PO_path=os.path.join(projectfail,"Page_Object/")
TestCase_path=os.path.join(projectfail,"TestCase/")

