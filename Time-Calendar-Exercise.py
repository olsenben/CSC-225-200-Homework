import datetime

"""
Time and Calendar Exercise

Overview
Create a system of classes to represent time, dates, and appointments in a calendar application.
"""

#Part 1: Time Class
#First, create a Time class similar to the example in previous chapters:

#1. Create a Time class with attributes for hours, minutes, and seconds
class Time:
    def __init__(self, hours, minutes, seconds):
        self.hours = hours 
        self.minutes = minutes
        self.seconds = seconds

    #2. Add a __str__ method that formats the time as "HH:MM:SS"
    def __str__(self):
        return f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}"   

    #3. Write a method is_valid that checks if the time is valid (hours 0-23, minutes 0-59, seconds 0-59)
    def is_valid(self):
        return (0 <= self.hours <= 23) and (0 <= self.minutes <= 59) and (0 <= self.seconds <= 59)
    
    #4. Implement a __lt__ method to compare times chronologically
    def __lt__(self, other):
        if isinstance(other, Time): #when would you use isinstance() over asserting is_valid?
            return (self.to_seconds() < other.to_seconds())
        else: 
            return "Not a Valid Time Class"

    #5. Add methods to add and subtract times, ensuring proper carry/borrow operations
    def to_seconds(self):
        return (self.hours * 3600) + (self.minutes * 60) + self.seconds

    def add_time(self, other):
        assert self.is_valid() and other.is_valid()
        self_seconds = self.to_seconds()
        other_seconds = other.to_seconds()
        total_seconds = self_seconds + other_seconds
        minutes, second = divmod(total_seconds, 60)
        hour, minute = divmod(minutes, 60)
        return Time(hour, minute, second)
    
    def subtract_time(self, other):
        assert self.is_valid() and other.is_valid()
        self_seconds = self.to_seconds()
        other_seconds = other.to_seconds()
        total_seconds = self_seconds - other_seconds
        minutes, second = divmod(total_seconds, 60)
        hour, minute = divmod(minutes, 60)
        return Time(hour, minute, second)

#Part 2: Date Class

#Create a Date class to represent calendar dates:

#1. Initialize with year, month, and day attributes
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    #Add a __str__ method that formats the date as "YYYY-MM-DD"
    def __str__(self):
        return f"{self.year:04d}-{self.month:02d}-{self.day:02d}"
    
   #Write a method is_valid that checks if the date is valid (considering month lengths and leap years)
    def is_valid(self):
        if self.month == 2:
            return 1 <= self.day <= 29 #29 for leap years
        
        elif 1 <= self.month <= 12 and self.month % 2 == 0: #even months have 30 days
            return 1 <= self.day <= 30
        
        elif 1 <= self.month <= 12: #odd months have 31 days
            return 1 <= self.day <= 31
        else:
            return False #anything less than 1 or greater than 12 is invalid

    #Implement __lt__ to compare dates chronologically
    def __lt__(self, other):
        if self.year < other.year:
            return True
        elif self.year == other.year and self.month < other.month:
            return True
        elif self.year == other.year and self.month == other.month and self.day < other.day:
            return True
        else:
            False
    
    #Add a method to calculate the day of the week for any date
    #I gave up and used datetime
    def get_day(self):
        date = datetime.datetime(self.year, self.month, self.day)
        day_of_week = date.strftime('%A')
        return day_of_week


time = Time(18, 3,43)
time_2 = Time(1, 15, 30)

print (time_2 < time)

date = Date(1300,1,31)
date_2 = Date(2025,3,4)

print(date_2.get_day())
