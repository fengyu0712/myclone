# def result(score):
#     if score.isdigit():
#         if score >=0 and score<60:
#             print ("输入成绩不及格")
#         elif score >=60 and score <80:
#             print ("输入成绩及格")
#         elif score >=80 and score <=100:
#             print ("输入成绩为优秀")
#         else:
#             print ("输入成绩无效")
#     else:
#         print(
#             "请输入0-100的整数"
#         )
#
#
# result("")
a = input("请输入字符串/元组/列表：")
def e_judge(a):
    if len(a)>5:
        print("Ture")
    else:
        print("False")
e_judge(a)