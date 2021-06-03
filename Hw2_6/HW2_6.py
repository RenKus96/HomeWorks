# 1 задание.
# Создать класс Robot и его потомков - классы SpotMini, Atlas и Handle. 
# В родительском классе должно быть определен конструктор и как минимум 3 атрибута и 1 метод. 
# В классах-потомках должны быть добавлены минимум по 1 новому методу и по 1 новому атрибуту.

# Robot - type, moving, appointment
class Robot:
    """Общий класс Robot"""
    def __init__(self, name='Robot', type=None, movement=None, appointment=None):
        # print(self.__doc__)
        self.name = name
        self.type = type
        self.movement = movement
        self.appointment = appointment

    def info(self):
        info_str  = 'Я Робот. Меня зовут - {}\n'.format(self.name)
        info_str += 'Мой тип - {}\n'.format(self.type)
        info_str += 'Мой метод перемещения - {}\n'.format(self.movement)
        info_str += 'Моё назначение - {}'.format(self.appointment)
        return info_str

# Atlas - bipedal humanoid robot
class Atlas(Robot):
    """Класс робота - Atlas"""
    def __init__(self, name='C-3PO', generation = '1'):
        super().__init__()
        # print(self.__doc__)
        self.name = name
        self.generation = generation
        self.type = 'humanoid'
        self.movement = 'bipedal'
        self.appointment = 'multifunctional'
    def hello(self):
        print('Я могу сказать вам ПРИВЕТ на 7 миллионах диалектов')
    
# Spot - Quadruped Robot
class Spot(Robot):
    """Класс робота - Spot"""
    def __init__(self, name='Djulbars', generation = '1', module='Camera'):
        super().__init__()
        # print(self.__doc__)
        self.name = name
        self.generation = generation
        self.module = module
        self.type = 'zoomorphic'
        self.movement = 'quadruped'
        self.appointment = 'multifunctional'
    def barking(self):
        print('Гав... гаф гаф... ррр')

# Handle - Robot with two flexible legs on wheels
class Handle(Robot):
    """Класс робота - Handle"""
    def __init__(self, name='R2-D2', generation='1', hand_type='vacuum'):
        super().__init__()
        # print(self.__doc__)
        self.name = name
        self.generation = generation
        self.hand_type = hand_type
        self.type = 'zoomorphic'
        self.movement = 'wheels'
        self.appointment = 'Manipulating or carrying'
    def report(self, count=0):
        print('Я перетащил {} ящиков'.format(count))


# 2. Создать классы Point и Cirle, отнаследованные от класса Shape. В классе Shape хранятся только координаты центра фигуры.
# Создать в классе Circle булевый метод contains, который принимает в качестве параметра точку (экземпляр класса Point) 
# и проверяет находится ли данная точка внутри окружности. Координаты центра окружности и точки могут быть произвольными. 
# Если точка попадает на окружность, то это считается вхождением.
# p = Point(1, 42)
# c = Circle(0, 0, 10)
# c.contains(p) # False
# 3*. Реализовать задание 2 таким образом, чтобы для проверки вхождения точки в окружность вместо вызова метода contains можно было написать:
# p in c 
class Shape:
    '''Класс определяет базовую форму с координатами центра (x,y)'''
    def __init__(self, x=0, y=0):
        '''Определяем пременые x и y'''
        if isinstance(x, (int, float)) and isinstance(y, (int, float)):
            self.x = x
            self.y = y
        else:
            raise TypeError('Координаты центра (x,y) должны быть числовыми!')

class Circle(Shape):
    '''Класс определяет окружность с координатами в точке (x,y)'''
    def __init__(self, x, y, radius):
        super().__init__(x, y)
        if isinstance(radius, (int, float)) and radius > 0:
            self.radius = radius
        else:
            raise TypeError('Радиус должен быть положительным числом!')
    def contains(self, point):
        return (point.x-self.x)**2+(point.y-self.y)**2 <= self.radius**2

    def __contains__(self, point):
        return (point.x-self.x)**2+(point.y-self.y)**2 <= self.radius**2

class Point(Shape):
    '''Класс определяет Точку с координатами (x,y)'''
    def __init__(self, x, y):
        super().__init__(x, y)

if __name__ == "__main__":

    robot = Robot(type='Zoomorphic', movement='wheels', appointment='War')
    print(robot.info())

    robot_1 = Atlas()
    print(robot_1.info())
    robot_1.hello()

    robot_2 = Spot()
    print(robot_2.info())
    print('Мой функциональный модуль -',robot_2.module)
    robot_2.barking()

    robot_3 = Handle()
    print(robot_3.info())
    print('Мой манипулятор оснащён модулем типа -',robot_3.hand_type)
    robot_3.report(10)

    p = Point(1, 42)
    c = Circle(0, 0, 10)
    print('1. Через Circle.contains(Point):')
    print('Точка ({},{}) {}лежит внутри окружности с центром в точке ({},{}) и радиусом {}'.format(p.x,p.y,'' if c.contains(p) else 'не ',c.x,c.y,c.radius))
    print('1. Через Point in Circle:')
    print('Точка ({},{}) {}лежит внутри окружности с центром в точке ({},{}) и радиусом {}'.format(p.x,p.y,'' if p in c else 'не ',c.x,c.y,c.radius))
