# # -*- coding:utf-8 -*-
# # Filename: class.py
# # Author: Lizi
# # Time: 2019/12/21 14:42
#
# # class Dog():
# #     def __init__(self,name,age):
# #         self.name = name
# #         self.age = age
# #
# #     def sit(self):
# #         print(self.name.title() + " is now sitting")
# #
# #     def roll(self):
# #         print(self.name.title() + ' roll over !')
# #
# # my_dog = Dog('whille','6')                                                   # 将返回的值赋给变量 my_dog 实例
# # print("my dog is name " + my_dog.name.title())                               #  my_dog.name访问属性，name和age为属性
# # print("my dog is " + str(my_dog.age))
# # my_dog.sit()                                                                 # 调用Dog类里面的sit方法
#
#
# # class Car():
# #     def __init__(self,make,model,year):
# #         self.make = make
# #         self.model = model
# #         self.year = year
# #         self.odometer_reading = 0                                               # 给属性设置默认值
# #
# #     def get_descriptive_name(self):
# #         long_name = str(self.year) + " " +self.make + " " +self.model
# #         return long_name
# #
# #     def read_odometer(self):
# #         print("This car has " + str(self.odometer_reading) + " miles on it")
# #
# #     def update_odometer(self,mileage):                                          # 通过方法修改属性的值，将mileage的值赋给odometer_reading
# #         if mileage >= self.odometer_reading:
# #             self.odometer_reading = mileage
# #         else:
# #             print("You can not roll back an odometer!")
# #
# #     def fill_gas_tank(self,gas):
# #         print("This car has " + str(gas) + " L")
# #
# # class ElectricCar(Car):
# #     def __init__(self,make,model,year):
# #         super().__init__(make,model,year)                                          #super()函数将父类和子类关联起来，调用父类的__init__()方法，让子类实例包含父类的所有属性
# #         self.battery_size = 70                                                     # 子类特有的属性
# #
# #     def describe_battery(self):                                                    # 子类特有的方法
# #         print("This car has a  " + str(self.battery_size) + "_kmh battery")
# #
# #     #当子类的方法和父类的方法名相同时，在调用同一方法时，默认调用子类的，父类的失效
# #     def fill_gas_tank(self):
# #         print("This car dose not need gas tank!")
#
# # my_new_car = Car("audi",'a4',2019)                                               # 给属性设置默认值时，无需提供实参
# # print(my_new_car.get_descriptive_name())
# # my_new_car.odometer_reading = 23                                               # 第一种修改属性值的方法：通过访问属性，直接修改属性的值，原本是0，现改为23
# # my_new_car.update_odometer(100)                                                  # 调用update_odometer方法修改odometer_reading的值
# # my_new_car.read_odometer()
#
# # my_tesla = ElectricCar('tesla','model s',2020)
# # print(my_tesla.get_descriptive_name())
# # my_tesla.describe_battery()
# # my_tesla.fill_gas_tank()
#
#
# # 将实例用作属性
# class Car():
#     def __init__(self,make,model,year):
#         self.make = make
#         self.model = model
#         self.year = year
#         self.odometer_reading = 89                                               # 给属性设置默认值
#
#     def get_descriptive_name(self):
#         long_name = str(self.year) + " " +self.make + " " +self.model
#         return long_name
#
#     def read_odometer(self):
#         print("This car has " + str(self.odometer_reading) + " miles on it")
#
#     def update_odometer(self,mileage):                                          # 通过方法修改属性的值，将mileage的值赋给odometer_reading
#         if mileage >= self.odometer_reading:
#             self.odometer_reading = mileage
#         else:
#             print("You can not roll back an odometer!")
#
# class Battery():
#     def __init__(self,battery_size=70):
#         self.battery_size = battery_size
#
#     def describe_battery(self):                                                    # 子类特有的方法
#         print("This car has a  " + str(self.battery_size) + "_kmh battery")
#
#
# class ElectricCar(Car):
#     def __init__(self,make,model,year):
#         super().__init__(make,model,year)                                          #super()函数将父类和子类关联起来，调用父类的__init__()方法，让子类实例包含父类的所有属性
#         self.battery = Battery()
#
#
# # my_tesla = ElectricCar('tesla','model s',2020)
# # print(my_tesla.get_descriptive_name())
# # my_tesla.battery.describe_battery()


from random import choice
x = choice(['hello world e',[1,2,3,4,'l']])
print(x.count('l'))