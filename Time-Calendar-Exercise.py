import datetime
from collections import defaultdict

"""
Time and Calendar Exercise

Overview
Create a system of classes to represent time, dates, and appointments in a calendar application.
"""

#Part 1: Time Class

#First, create a Time class similar to the example in previous chapters:

#1. Create a Time class with attributes for hours, minutes, and seconds
class Time:
    """represents a time in the format HH:MM:SS """
    def __init__(self, hours, minutes, seconds):
        self.hours = hours 
        self.minutes = minutes
        self.seconds = seconds

    #2. Add a __str__ method that formats the time as "HH:MM:SS"
    def __str__(self):
        """formats a string representation of Time Class HH:MM:SS"""
        return f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}"   #adds a space if single digit

    #3. Write a method is_valid that checks if the time is valid (hours 0-23, minutes 0-59, seconds 0-59)
    def is_valid(self):
        """Checks that Time object is a valid time value"""
        return (0 <= self.hours <= 23) and (0 <= self.minutes <= 59) and (0 <= self.seconds <= 59)
    
    #4. Implement a __lt__ method to compare times chronologically
    def __lt__(self, other):
        """defines < behavior"""
        if isinstance(other, Time): #when would you use isinstance() over asserting is_valid?
            return (self.to_seconds() < other.to_seconds())
        else: 
            return "Not a Valid Time Class"

    #5. Add methods to add and subtract times, ensuring proper carry/borrow operations
    def to_seconds(self):
        """to make operations easier, converting time objects to seconds"""
        return (self.hours * 3600) + (self.minutes * 60) + self.seconds

    def add_time(self, other):
        """add two Time objects together and return a Time object that is a combination of both"""
        assert self.is_valid() and other.is_valid()
        self_seconds = self.to_seconds()
        other_seconds = other.to_seconds()
        total_seconds = self_seconds + other_seconds
        minutes, second = divmod(total_seconds, 60) #Find minutes and seconds
        hour, minute = divmod(minutes, 60) #find hours 
        return Time(hour, minute, second)
    
    def subtract_time(self, other):
        """subtract two Time objects and retunr a time object that is a combination of both"""
        assert self.is_valid() and other.is_valid()
        self_seconds = self.to_seconds()
        other_seconds = other.to_seconds()
        total_seconds = self_seconds - other_seconds
        minutes, second = divmod(total_seconds, 60)
        hour, minute = divmod(minutes, 60)
        return Time(hour, minute, second)
    
    def __eq__(self, other):
        """define behavior for == operator, returns True if they are the same time"""
        if (
            self.hours == other.hours 
            and self.minutes == other.minutes 
            and self.seconds == other.seconds
        ):
            return True
        else:
            return False

#Part 2: Date Class

#Create a Date class to represent calendar dates:

#1. Initialize with year, month, and day attributes
class Date:
    """Object representing date in the format YYYY-MM-DD"""
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    #Add a __str__ method that formats the date as "YYYY-MM-DD"
    def __str__(self):
        """Define string representation of Date Class"""
        return f"{self.year:04d}-{self.month:02d}-{self.day:02d}" #adds 0 for padding single digits
    
   #Write a method is_valid that checks if the date is valid (considering month lengths and leap years)
    def is_valid(self):
        """checks if Date object is valid, ie not over 31 days etc"""
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
        """define < behavior"""
        #year and month can be the same
        if self.year < other.year:
            return True
        elif self.year == other.year and self.month < other.month:
            return True
        elif self.year == other.year and self.month == other.month and self.day < other.day: #but not day
            return True
        else:
            False
    
    #Add a method to calculate the day of the week for any date
    #I gave up and used datetime
    def get_day(self):
        """gets day of week given a Date object"""
        date = datetime.datetime(self.year, self.month, self.day)
        day_of_week = date.strftime('%A') #gives a day name, not index number (0=monday)
        return day_of_week
    
    def get_week_start(self):
        """defines the first day of the week for any given date in that week"""
        date = datetime.datetime(self.year, self.month, self.day)
        monday = date - datetime.timedelta(days=date.weekday())#date minus its index resets to monday
        return Date(monday.year, monday.month, monday.day)
    
    def __eq__(self, other):
        """defines == behavior"""
        if (
            self.year == other.year  
            and self.month == other.month  
            and self.day == other.day  
        ):
            return True
        else:
            return False

#Part 3: Appointment Class

#Create an Appointment class that inherits from both Date and Time:

#Create a new class DateTime that combines date and time information

class DateTime:
    """I realize now I woas probably supposed to be using this intead of datetime.datetime, or at least combining them"""
    def __init__(self,year, month, day, hours, minutes, seconds):
        self.date = Date(year, month, day)
        self.time = Time(hours, minutes, seconds)

#Create an Appointment class that inherits from DateTime and adds:
#A title attribute
#A duration attribute (in minutes)
#A location attribute
#A description attribute 
                
class Appointment(DateTime):
    """Object to represent an apppointment on a given Date and Time object"""
    #is there a way to inherit methods without having to expressly insert every attribute? 
    # can I just use an object? I dont think so, WOULD BE NICE
    def __init__(self,year, month, day, hours, minutes, seconds, title, duration, location, description):
        super().__init__(year, month, day, hours, minutes, seconds)
        """duration should be formatted 00:00:00, or hours:minutes:seconds as a string"""
        self.date = Date(year, month, day)
        self.time = Time(hours, minutes, seconds)
        self.title = title
        self.duration = duration
        self.location = location
        self.description = description
    
    def conflicts_with(self, other):
        """Checks if a given appointment conflicts with another given appointment"""
        hours, minutes, seconds = map(int, self.duration.split(':'))
        duration = Time(hours, minutes, seconds)
        return self.date == other.date and self.time < other.time < self.time.add_time(duration) #does that start time of other overlap with the duration of self
    
    def __str__(self):
        "Format string for appointment"
        return(f"{self.title},\n{self.date.get_day()}, {self.date}, {self.time},\nDuration: {self.duration},\nLocation: {self.location},\nDescription: {self.description}")
    
#Part 4: Calendar Class
#Create a Calendar class to manage a collection of appointments:

#1. Initialize with a name and an empty list of appointments

class Calendar:
    """class that holds appointment objects in a list"""
    def __init__(self,name):
        self.name = name
        self.appointments = []

    #2. Add methods to add and remove appointments
    def add_appointment(self, appointment):
        """it adds an appointment"""
        self.appointments.append(appointment)
    
    def remove_appointment(self, appointment):
        """ditto but remove"""
        self.appointments.remove(appointment)
    
    #3. Create a method to find all appointments on a given date
    def find_appointments_on(self, date):
        """finds all appointments on a given date (Date object)"""
        return [appt for appt in self.appointments if appt.date == date]
    
    #4. Implement a method to find conflicts among all appointments
    def find_conflicts(self):
        """finds all conflicting appointments in calendar"""
        conflicts = []
        for i, appt in enumerate(self.appointments): #enumerate so you only check each once
            for other_appt in self.appointments[i+1:]: #dont check against self
                if appt.conflicts_with(other_appt):
                    conflicts.append(f"Conflict between {appt.title} and {other_appt.title}")
        return conflicts
    
    #5 Add a method to print a formatted daily or weekly view of appointments
    def show_appointments(self, grouped:str ="weekly"):
        """
        print a formatted daily or weekly view of appointments
        
        Input:
            grouped (str): grouped by "weekly" or "daily"

        Output: 
            str: formatted list of dialy or weekly appointments
        """
        #this was a pain tbh
        if grouped == "daily": 
            appointments_by_date = defaultdict(list) #defaultdict allows you to create a key, value pair if they dont exist upon calling them with default behavior
            
            for appt in self.appointments: #check all apppointments
                appointments_by_date[str(appt.date)].append(appt) #key must be a string
            
            for date, appts in sorted(appointments_by_date.items()): #sort dictionary by key
                print (f"\nAppointments for {date} ({appts[0].date.get_day()})") #values are appointment objects in a list 
                for appt in sorted(appts, key=lambda x: x.time): #sort the list of appointments by time (of day) (Time objects btw)
                    print(f"\n{appt}") #print its details
        
        #group by week instead 
        elif grouped == "weekly":
            appointments_by_week = defaultdict(list)
            for appt in self.appointments:
                #overall the behavior is the same as above but we are storing the appointments 
                #in a dictionary with the first day of the week that the appointment falls in as 
                #the key, representing a week.
                week_start = appt.date.get_week_start() 
                appointments_by_week[str(week_start)].append(appt)#remember key must be a string
            
            #same as above
            for week_start, appts in sorted(appointments_by_week.items()):
                print (f"\nAppointments for week {week_start}:")
                for appt in sorted(appts, key=lambda x: datetime.datetime(x.year, x.month, x.day)): #except we are sorting by day instead of time.
                    print(f"\n{appt}")

        else:
            print("Invalid group. Use 'daily' or 'weekly'") #wrong argument passed message

#Part 5: Specialized Calendar Types

#Create at least two specialized calendar types that inherit from Calendar:

#1 WorkCalendar - with methods specific to work appointments
class WorkCalendar(Calendar):
    """subclass of calendar that has specialized functions"""
    def __init__(self, name, work_start='09:00:00', work_end="17:00:00"):
        super().__init__(name)
        self.name = name
        self.work_start = self._convert_time(work_start) 
        self.work_end = self._convert_time(work_end)
        self.appointments = []
    
    def _convert_time(self, time_str):
        """I forget what kind of function this is but 'dont use it outside of this class' is what it means
        converts to Time object. I honestly should have put this in all the classes somehow.
        """
        hours, minutes, seconds = map(int, time_str.split(':'))#splits and converts to integers
        return Time(hours, minutes, seconds)

    def add_appointment(self, appointment):
        """uh oh I had a function here that checked if the appointment was during working hours and i somehow pasted over it :(
        it even checked to make sure the duration didnt go past work_end time """
        return super().add_appointment(appointment)

    
    def remove_appointment(self, appointment):
        return super().remove_appointment(appointment)    
    
    def find_appointments_on(self, date):
        return super().find_appointments_on(date)    
    
    def find_conflicts(self):
        return super().find_conflicts()    

    def show_appointments(self, grouped:str ="weekly"):
        """
        print a formatted daily or weekly view of appointments
        
        Input:
            grouped (str): grouped by "weekly" or "daily"

        Output: 
            str: formatted list of dialy or weekly appointments
        """
        #same as calendar class so if you want documentation please check calendar class.
        # Minor change in print statement 
        if grouped == "daily": 
            appointments_by_date = defaultdict(list)
            
            for appt in self.appointments:
                appointments_by_date[str(appt.date)].append(appt)
            
            for date, appts in sorted(appointments_by_date.items()):
                print (f"\nWork Appointments for {date} ({appts[0].date.get_day()})")
                for appt in sorted(appts, key=lambda x: x.time):
                    print(f"\n{appt}")
        
        elif grouped == "weekly":
            appointments_by_week = defaultdict(list)
            for appt in self.appointments:
                week_start = appt.date.get_week_start()
                appointments_by_week[str(week_start)].append(appt)
            
            for week_start, appts in sorted(appointments_by_week.items()):
                print (f"\nWork Appointments for week {week_start}:")
                for appt in sorted(appts, key=lambda x: datetime.datetime(x.year, x.month, x.day)):
                    print(f"\n{appt}")

        else:
            print("Invalid group. Use 'daily' or 'weekly'")

#SchoolCalendar - with methods specific to academic appointments
class SchoolCalendar(Calendar):
    def __init__(self, name):
        """subclass of calendar that has specialized functions"""

        super().__init__(name)
        self.name = name
        self.appointments = []


    def add_class(self, title, start_date, time, duration, location, description, months=5):
        """adds a class that reoccurs weekly for a defined number of months. looking back, this needs more flexible implementation
         since some classes meet multiple times a week """
        date = start_date
        for _ in range(months):
            self.add_appointment(Appointment(date.year, date.month, date.day, time.hours, time.minutes, time.seconds, title, duration, location, description))
            date = datetime.datetime(date.year, date.month, date.day) + datetime.timedelta(weeks=1)
            date = Date(date.year, date.month, date.day)
    
    def show_classes(self, grouped:str ="weekly"):
        """
        print a formatted daily or weekly view of appointments
        
        Input:
            grouped (str): grouped by "weekly" or "daily"

        Output: 
            str: formatted list of dialy or weekly appointments
        """
        if grouped == "daily": 
            appointments_by_date = defaultdict(list)
            
            for appt in self.appointments:
                appointments_by_date[str(appt.date)].append(appt)
            
            for date, appts in sorted(appointments_by_date.items()):
                print (f"\nClasses for {date} ({appts[0].date.get_day()})")
                for appt in sorted(appts, key=lambda x: x.time):
                    print(f"\n{appt}")
        
        elif grouped == "weekly":
            appointments_by_week = defaultdict(list)
            for appt in self.appointments:
                week_start = appt.date.get_week_start()
                appointments_by_week[str(week_start)].append(appt)
            
            for week_start, appts in sorted(appointments_by_week.items()):
                print (f"\nClasses for week {week_start}:")
                for appt in sorted(appts, key=lambda x: datetime.datetime(x.year, x.month, x.day)):
                    print(f"\n{appt}")

        else:
            print("Invalid group. Use 'daily' or 'weekly'")

if __name__ == "__main__":
    cal = WorkCalendar("Work Calendar")
    
    # Creating appointments
    appt1 = Appointment(2025, 5, 1, 9, 0, 0, "Team meeting", "1:00:00", "conference room","team check in")
    appt2 = Appointment(2025, 5, 1, 10, 30, 0, "Client call", "00:20:00","office",  "bob vances refridgeration")
    appt3 = Appointment(2025, 5, 1, 12, 0, 0, "Lunch","00:30:00","break room",  "cold macaroni" )
    appt4 = Appointment(2025, 5, 1, 9, 30, 0, "Project Review", "00:30:00","conference room",  "project updates")  # Conflict!
    
    # Adding appointments
    cal.add_appointment(appt1)
    cal.add_appointment(appt2)
    cal.add_appointment(appt3)
    cal.add_appointment(appt4)
    
    # Show all appointments
    cal.show_appointments("daily")
    
    # Find conflicts

    conflicts = cal.find_conflicts()
    if conflicts:
        print("\nConflicts found:")
        for conflict in conflicts:
            print(conflict)
    else:
        print("No conflicts detected.")





        
        
            


















time = Time(18, 3,43)
time_2 = Time(1, 15, 30)

print (time_2 < time)

date = Date(1300,1,31)
date_2 = Date(2025,3,4)
date_3 = Date(1300,1,31)

date_time = Appointment(2025,3,4,18, 3,43, "Meeting 1", "0:0:20","outside", "1 on 1")
date_time2 =  Appointment(2025,3,4,18, 23,43, "meeting 1", "0:0:20","outside", "1 on 1")

print(date_time)
