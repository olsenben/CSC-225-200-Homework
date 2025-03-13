import csv
import os

file_exists = os.path.isfile("dogs.csv")

if not file_exists:
    with open('dogs.csv', 'w', newline='') as file:
        csv_write = csv.writer(file)
        csv_write.writerow(["name", "breed", "weight", "color"])
    print("created dogs.csv file with headers")



def create_dog_csv():
    """create a new dog and save it to csv file"""

    with open('dogs.csv', "a", newline="") as file:
        csv_write = csv.writer(file)

        csv_write.writerow(["cactus", "german shepherd", 80, "dark brown"])
        csv_write.writerow(["Ronan", "chocolate", 75, "dark brown"])
        csv_write.writerow(["princess", "dachshund", 20, "brown"])
        csv_write.writerow(["fluffy", "rabbit", 15, "white"])

    
    print("dogs created and added to dogs.csv")

def display_dogs():
    with open('dogs.csv', 'r') as file:
        csv_read = csv.reader(file)
        header = next(csv_read)

        print(f"Dog database lists each dog's {header}")
        print("All Dogs: ")
        for dog in csv_read:
            name, breed, weight, color = dog
            print(f"{name}, {breed}, {weight}, {color}")

def search_by_breed():
    breed_search = input("Enter breed: ").lower()          
    found_dogs = []
    with open('dogs.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for dog in reader:
            if breed_search in dog[1].lower():
                found_dogs.append(dog)
    if found_dogs:
        print(f"Found {breed_search}")
        for dog in found_dogs:
            print(f"Name: {dog[0]}, Weight: {dog[2]}lbs, Color: {dog[3]}")
    else:
        print(f"No Dogs Matching {breed_search} ")

def find_heaviest_dog():
    weight_of_heavy_dog = 0
    heaviest_dog = None
    with open('dogs.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for dog in reader:
            try:
                weight = float(dog[2])
                if weight > weight_of_heavy_dog:
                    weight_of_heavy_dog = weight
                    heaviest_dog = dog
            except ValueError:
                continue
    if heaviest_dog: 
        print(f"the heaviest dog is {heaviest_dog[0]}")
        print(f"and they weight {heaviest_dog[2]} lbs")

        

# name = input("whats your name?")

# quest = input("what is your quest?")

# color = input("what is your favorite color?")

# print(f"hello, {name}, who's quest is {quest}, and favorite color is {color}!")

# hi_temp = 55
# print(f"glad it hit {hi_temp} today")