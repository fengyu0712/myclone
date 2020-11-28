# a = '''"test_output":	{
#
# 		"ev":	"online tts",
#
# 		"text":	"八十的风",
#
# 		"data":	0,
#
# 		"info":	"f13f0fe9-075b-4fe9-a3a0-8fe998928fe9"
#
# 	}
#
# } '''
# import re
#
# asr_mid_pattern = "text\":	\"(.*)\"[\\s\\S]*\"info\":	\"(.*)\""
#
# b = re.findall(asr_mid_pattern, a)
# print(b)
