#第一章：类
# 类的成员:属性和方法
# 定义
# class 类名:
#     属性名 = 属性值
#     def 方法名(self):
#         方法体
class Car:
    wheels = 4
    def drive(self):
        print("行驶")

# 创建对象  对象名 = 类名()
# 对象名.属性名
# 对象名.方法名()

#定义一个类Car
# class Car:
#     wheels = 4
#     def drive(self):
#         print("行驶")
#创建Car类的对象
# car = Car()
#使用对象
# print(car.wheels)
# car.drive()

#类属性和实例属性
# 一. 类属性
# 在类中方法外定义的属性，类属性可以通过类或对象进行访问，但只能通过类名修改类属性的值，而不能通过对象修改类属性的值，类属性属于类。
# print(Car.wheels)
# print(car.wheels)
#2. 实例属性
# 在类中方法中定义的属性，在程序中(类的外部)，实例属性属于对象，只能用对象访问或修改(不能通过类名进行修改)
class Car:
    def drive(self): #自定义方法
        self.wheels=4 
    def __init__(self,name): #构造方法(在类实例化时自动调用)
        self.name=name
car=Car('ford')
car.drive()
print(car.wheels) #4
print(car.name) # ford
# 2）修改实例属性
# 实例属性通过对象进行修改
car.drive()
lorry=Car('Ferrari') 
lorry.drive()
car.wheels=3
print(car.wheels)
print(lorry.wheels)
#3.私有属性


#二.类的方法
#1.实例方法
#(调用实例方法时，形参self会自动接收调用该方法的对象，self代表类的实例)
#只能通过对象调用
class truck:
    def drive(self):
        print('truck')
lorrys=truck()
lorrys.drive()
# 2. 类方法
# 定义在类中，使用@classmethod装饰器修饰的方法，类方法中形参表的第一个参数为cls，代表类本身，它在类方法被调用时自动接收调用该方法的类。
class truck2:
    wheels=3
    @classmethod
    def stop(cls):
        print(cls.wheels)   #使用cls访问类属性
        cls.wheels=4 #使用cls修改类属性
        print(cls.wheels)
truck2.stop()
t=truck2()
t.stop() #可通过对象调用

#3.类的静态方法
# 定义在类中，使用@staticmethod装饰器修饰的方法，和实例方法跟类方法比，静态方法没有任何默认参数，它适用于与类无关的操作，或无须使用类成员的操作，常见于一些工具类中。
#定义一个类Car
class Car2:
    wheels=5
    @staticmethod
    def test():
        print("我是静态方法")
        print(f'类属性的值={Car2.wheels}')
car2 = Car2()
car2.test()
Car2.test() #可通过类与对象调用

#三、类的私有成员
# 在类内部可以直接访问，在类外部不能直接访问，需要通过调用类的公有方法来访问。 
#  __属性名
#  __方法名
class Car3:
    __wheels = 4  #私有的类属性
    def __drive(self):  #私有方法
        print("行驶")
    def test(self):   #在公有方法中访问私有成员
        print(f"轿车有{self.__wheels}个轮子")
        self.__drive()
 
car3 = Car3()
car3.test()
#四、特殊方法

#1.构造方法
# 作用：在创建对象时对对象的属性进行初始化。(在创建对象时系统会自动调用类的构造方法)
#__init__

# （1）使用无参构造方法创建对象时，所有对象的属性都有相同的初始值
class Car4:
    def __init__(self):  #无参构造方法
        self.color = "红色"
    def drive(self):
        print(f"车的颜色为：{self.color}")
 
car_one = Car4()
car_one.drive()
 
car_two = Car4()
car_two.drive()
#（2）使用有参构造方法创建对象时，所有对象的属性可以有不同的初始值
class Car:
    def __init__(self,color):  #有参构造方法
        self.color = color     #给实例属性赋值为color
    def drive(self):
        print(f"车的颜色为：{self.color}")
 
car_one = Car("红色")
car_one.drive()
 
car_two = Car("蓝色")
car_two.drive()

#2.折构方法
#作用：销毁对象时系统自动调用该方法
# 每个类中默认都有一个析构方法。
# 如果一个类中显式定义了析构方法，那么销毁该类的对象时调用的时显式定义的析构方法；如果一个类中没有定义析构方法，那么销毁该类的对象时会调用默认的析构方法。
class Car5:
    def __init__(self):
        self.color = "蓝色"
        print("构造方法执行，对象被创建")
    def __del__(self):
        print("析构方法执行，对象被销毁")
 
car5 = Car5()      
print(car5.color)
 
del car5   #使用del语句删除对象的引用，此时会执行析构方法
try:
    print(car5.color)
except Exception as e:
    print(e)  #这行代码因为已经销毁了对象，在使用car对象访问属性会报错




#第二章：封装
#对外隐藏类的实现细节，提供用于访问类成员的公开接口的
#定义类是要满足一下特点：
#1.将属性私有化2.定义两个供外界调用的公有方法，分别用于设置和获取私有属性的值
class Person:
    def __init__(self,name):
        self.name = name
        self.__age = 1      #将实例属性age私有化
    #设置私有属性值的方法
    def set_age(self,new_age):
        if 0< new_age <= 120:
            self.__age = new_age
    #获取私有属性值的方法
    def get_age(self):
        return self.__age
 
person = Person("小明")
person.set_age(18)
print(f"年龄为{person.get_age()}岁")

#第三章：继承
#继承是面向对象的重要特征之一，它主要用于描述类与类之间的关系，在原有类的基础上扩展原有类的功能。
# 如果类与类之间具有继承关系，被继承的类称为父类或基类，继承其他类的类称为子类或派生类。
# 子类会自动拥有父类的公有成员，但不会拥有父类的私有成员，也不能访问父类的私有成员。

#一、单继承

#class 子类名(父类名):
class Cat(object):
    def __init__(self,color):
        self.color = color
    def walk(self):
        print("猫走路")
#定义继承Cat类的折耳猫类
class ScottishFold(Cat):
    pass    #关键字pass用于表示一个空的代码块
fold = ScottishFold("灰色")   #创建子类的对象
print(f"{fold.color}的折耳猫")  #用子类对象调用从父类继承来的实例属性
fold.walk()    #用子类对象调用从父类继承来的实例方法

#二、多继承
#程序中的一个类可以继承多个类，也自动拥有所有父类的公有成员，多继承的语法格式为：

#定义一个表示房子的类
class House(object):
    def live(self):
        print("供人居住")
 
#定义一个表示汽车的类
class Car:
    def drive(self):
        print("行驶")
 
#定义一个表示房车的类，继承House类和Car类
class HouseCar(House,Car):
    pass
 
#定义房车对象
house_car = HouseCar()
house_car.live()
house_car.drive()

# 如果继承的多个父类中有同名的方法怎么办？

# 如果子类继承的多个父类是平行关系的类，那么子类先继承哪个类，就会先调用哪个类的方法。

# 例如在上述代码的House和Car类中添加一个test()方法：

#定义一个表示房子的类
class House(object):
    def live(self):
        print("供人居住")
    def test(self):
        print("House类的test方法")
 
#定义一个表示汽车的类
class Car:
    def drive(self):
        print("行驶")
    def test(self):
        print("Car类的test方法")
 
#定义一个表示房车的类，继承House类和Car类
class HouseCar(House,Car):
    pass
 
#定义房车对象
house_car = HouseCar()
house_car.live()
house_car.drive()
#用房车对象调用test方法试试
house_car.test()

#三、重写 

# 子类会原封不同地继承父类的方法，但子类有时需要按自己的需求对继承来的方法进行调整。

# 此时可以在子类中重写从父类继承来的方法。

# python中重写父类方法的方式：在子类中定义和父类方法同名的方法，然后重新编写方法体即可。

#Person类
class Person1(object):
    def say_hello(self):
        print("打招呼")
 
#定义Person的子类
class Chinese(Person1):
    def say_hello(self):   #重写父类中的say_hello方法
        super().say_hello() #在内部重新调用被重写的方法
        print("吃了吗")
 
chinese = Chinese()
chinese.say_hello()


#第三章、多态
#多态是面向对象的重要特征，它的表现形式是：让不同类的同一方法，可以通过相同的接口调用，表现出不同的行为。
class Cat:
    def shout(self):
        print("喵喵")
class Dog:
    def shout(self):
        print("汪汪")
 
#定义一个接口，通过这个接口调用Cat类和Dog类中的shout()方法
def shout(obj):
    obj.shout()
 
cat = Cat()
dog = Dog()
shout(cat)
shout(dog)

#四、运算符重载
# 运算符重载：赋予了内置运算符新的功能，使内置运算符可以适应更多的数据类型。

# 理解：当定义一个类时，在这个类中重写object基类中内置的有关运算符的特殊方法，那么该特殊方法对应的运算符将支持对该类的实例进行运算。

class Calculator(object):
    def __init__(self,number):  #记录数值
        self.number = number
    def __add__(self, other):   #重载运算符+
        self.number = self.number + other
        return self.number
    def __sub__(self, other):   #重载运算符-
        self.number = self.number - other
        return self.number
    def __mul__(self, other):    #重载运算符*
        self.number = self.number * other
        return self.number
    def __truediv__(self, other):   #重载运算符/
        self.number = self.number / other
        return self.number
 
#创建Calculator类的对象，让该对象使用运算符与一个数分别执行加减乘除操作
calculator = Calculator(10)
print(calculator + 5)
print(calculator - 5)
print(calculator * 5)
print(calculator / 5)
