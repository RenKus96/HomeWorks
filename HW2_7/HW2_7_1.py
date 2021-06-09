import math
import importlib

class Shape: #class Shape(object)    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def square(self):
        return 0
    
class Circle(Shape):
    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.radius = radius
        
    def square(self):
        return math.pi*self.radius**2
    
class Rectangle(Shape):
    def __init__(self, x, y, height, width):
        super().__init__(x, y) 
        self.height = height
        self.width = width

    def square(self):
        return self.width*self.height
    
class Parallelogram(Rectangle):
    def __init__(self, x, y, height, width, angle):
        super().__init__(x, y, height, width) 
        self.angle = angle

    def print_angle(self):
        print(self.angle)
        
    def __str__(self):
        result = super().__str__()
        return result + f'\nParallelogram: основание - {self.width}, сторона - {self.height}, угол между ними - {self.angle}'
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def square(self):
        return self.width*(self.height*math.sin(math.radians(self.angle)))
    
class Triangle(Rectangle):
    def __init__(self, x, y, height, width, angle):
        super().__init__(x, y, height, width) 
        self.angle = angle

    def print_angle(self):
        print(self.angle)
        
    def __str__(self):
        result = super().__str__()
        return result + f'\nTriangle: одна сторона - {self.width}, другая сторона - {self.height}, угол между ними - {self.angle}'
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def square(self):
        return self.width*(self.height*math.sin(math.radians(self.angle)))/2

class Scene:
    def __init__(self):
        self._figures = []
        
    def add_figure(self, figure):
        self._figures.append(figure)
     
    def total_square(self):
        return sum(f.square() for f in self._figures)
    
    @staticmethod
    def create_from_file(filepath):
        """
        Figure;x;y;...
        Circle;0;0;10
        Circle;10;0;2
        Rectange;100;0;45;25
        """
        new_scene = Scene()
        for line in open(filepath):
            clazz, x, y, *args = [int(arg) if i>0 else str(arg) for i,arg in enumerate(line.split(';'))]
            my_module = importlib.import_module("__main__")
            MyClass = getattr(my_module, clazz)
            c = MyClass(x, y, *args)
            new_scene.add_figure(c)
        return new_scene
    
    def save_to_file(self, filepath):
        with open(filepath, "w") as f:
            for figure in self._figures:
                line = [figure.__class__.__name__]
                for attribute  in figure.__dict__:
                    line.append(str(getattr(figure, attribute)))
                f.write('{}\n'.format(';'.join(line)))
        
r = Rectangle(0, 0, 10, 20)
r1 = Rectangle(10, 0, 10, 20)
r2 = Rectangle(0, 20, 100, 20)

c = Circle(10, 0, 10)
c1 = Circle(100, 100, 5)

p = Parallelogram(1, 2, 20, 30, 45)
p1 = Parallelogram(1, 2, 20, 30, 90)
print('Фигура:\n {}'.format(str(p1)))
print('Площадь фигуры:\n {}'.format(p1.square()))

t = Triangle(1, 2, 20, 30, 45)
t1 = Triangle(1, 2, 20, 30, 90)
print('Фигура:\n {}'.format(str(t1)))
print('Площадь фигуры:\n {}'.format(t1.square()))

scene = Scene()
scene.add_figure(r)
scene.add_figure(r1)
scene.add_figure(r2)
scene.add_figure(c)
scene.add_figure(c1)
scene.add_figure(p)
scene.add_figure(p1)
scene.add_figure(t)
scene.add_figure(t1)
print('Общая площадь сцены №1: {}'.format(scene.total_square()))
# scene.save_to_file('scene1.txt')
scene2 = Scene().create_from_file('scene1.txt')
print('Общая площадь сцены №2: {}'.format(scene2.total_square()))

