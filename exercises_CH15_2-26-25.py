
class Point:
    def __init__(self, x,y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"point({self.x},{self.y})"

class Rectangle:
    def __init__(self, corner_x, corner_y, width, height):
        self.width = width
        self.height = height
        self.corner = Point(corner_x,corner_y)

class Circle:
    def __init__(self, color, radius, center_x, center_y):
        self.color = color
        self.radius = radius 
        self.center = Point(center_x,center_y)

    def area(self):
        return 3.15*self.radius*self.radius


    def __repr__(self):
        return f"my area is {3.15*self.radius*self.radius}"

    def __str__(self):
        """message for humans to read"""
        return f" I'm a {self.color} circle and my radius is {self.radius}, my area is {self.area()} and my center is {self.center}"
    

rec = Rectangle(5,6,1,9)

print(rec.corner)