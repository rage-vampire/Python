#输入某年某月某日，判断这一天是这一年的第几天？
# year = int(input('请输入年份：'))
# month = int(input('请输入月份：'))
# if month >12:
#     print('请输入正确的月份')
# day = int(input('请输入日期：'))
# month_1 = [1,3,5,7,8,10,12]
# month_2 = [4,6,9,11]
# count_1 = 0
# count_2 = 0
# for i in range(1,month):
#     if i in month_1:
#         count_1 +=1
#     if i in month_2:
#         count_2 +=1
# if month > 2:
#     if (year % 400 == 0) or ((year % 4 == 0) and (year % 100 != 0)):
#         days = count_1 * 31 + count_2 * 30 + day + 29
#     else:
#         days = count_1 * 31 + count_2 * 30 + day + 28
# else:
#     days = day+31
# print(days)

year = int(input('year: '))
month = int(input('month: '))
day = int(input('day: '))

months = (0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334)
if 0 < month <= 12:
    sum = months[month - 1]
else:
    print('data error')
sum += day
leap = 0
if (year % 400 == 0) or ((year % 4 == 0) and (year % 100 != 0)):
    leap = 1
if (leap == 1) and (month > 2):
    sum += 1
print('it is the %dth day.' % sum)







