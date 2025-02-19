import turtle

#exercise 15.1
class Point:
    def __init__(self,x,y):
        """represents a point in 3d space"""
        self.x = x
        self.y = y

class Rectangle:
    def __init__(self, corner_x, corner_y, width, height):
        self.width = width
        self.height = height
        self.corner = Point(corner_x,corner_y)



#Write a definition for a class named Circle with attributes center and radius,
#where center is a Point object and radius is a number.
class Circle:
    def __init__(self, center_x, center_y, radius):
        self.center = Point(center_x,center_y)
        self.radius = radius

#Instantiate a Circle object that represents a circle with its center at (150, 100) and radius 75.
circle = Circle(150, 100, 75)

#Write a function named point_in_circle that takes a Circle and a Point and returns True if the
#Point lies in or on the boundary of the circle.
def point_in_circle(circle, point):
    delta_x = circle.center.x - point.x
    delta_y = circle.center.y - point.y
    distance = (delta_x**2 + delta_y**2)**0.5
    return distance <= circle.radius 

#Write a function named rect_in_circle that takes a Circle and a Rectangle and returns True if
#the Rectangle lies entirely in or on the boundary of the circle.
def rect_in_circle(circle, rectangle):
    corner_1 = rectangle.corner
    corner_2 = Point(rectangle.corner.x + rectangle.width, rectangle.corner.y)
    corner_3 = Point(rectangle.corner.x, rectangle.corner.y + rectangle.height)
    corner_4 = Point(rectangle.corner.x + rectangle.width, rectangle.corner.y + rectangle.height)
    return point_in_circle(circle,corner_1) and point_in_circle(circle, corner_2) and point_in_circle(circle,corner_3) and point_in_circle(circle,corner_4)

def rect_circle_overlap(circle, rectangle):
    corner_1 = rectangle.corner
    corner_2 = Point(rectangle.corner.x + rectangle.width, rectangle.corner.y)
    corner_3 = Point(rectangle.corner.x, rectangle.corner.y + rectangle.height)
    corner_4 = Point(rectangle.corner.x + rectangle.width, rectangle.corner.y + rectangle.height)
    return point_in_circle(circle,corner_1) or point_in_circle(circle, corner_2) or point_in_circle(circle,corner_3) or point_in_circle(circle,corner_4)


#exercise 15.2
#Write a function called draw_rect that takes a Turtle object and a Rectangle and
#uses the Turtle to draw the Rectangle. 
def draw_rect(turtle, rectangle):
    turtle.setposition(rectangle.corner.x,rectangle.corner.y)
    for i in range(2):    
        turtle.forward(rectangle.width)
        turtle.left(90)
        turtle.forward(rectangle.height)
        turtle.left(90)

rec = Rectangle(0,0,500,100)  
squirt  = turtle.Turtle()

draw_rect(squirt,rec)