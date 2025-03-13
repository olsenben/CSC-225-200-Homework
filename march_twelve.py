import csv 
from datetime import datetime

class Pet:
    """Base class for pets"""
    def __init__(self, name, breed, weight, color):
        self.name = name
        self.breed = breed
        self.weight = self._parse_weight(weight)
        self.color = color 

    def _parse_weight(self, weight_str):
       """handle different formats for weight""" 
       if isinstance(weight_str, str) and '-' in weight_str:
           weight_val = weight_str.split('-')[0].strip()
           return float(weight_val)
       return float(weight_str)
                
    def __str__(self):
        return f"{self.name} is a {self.breed}, weighs {self.weight} lbs"

class Dog(Pet):
    def __init__(self, name, breed, weight, color):
      super().__init__(name, breed, weight, color)
      self.species="canine"

    def bark(self):
        return f"{self.name} says WOOF!!"

    def exercise_needs(self):
        high_energy_breeds = ["Jack Russell Terrier", "husky", "Aussie", "Doodle", "Border Collie"]

        if any(breed.lower() in self.breed.lower() for breed in high_energy_breeds):
            return "High"
        else:
            return "Low"

class Cat(Pet):
    def __init__(self, name, breed, weight, color):
        super().__init__(name, breed, weight, color)
        self.species="feline"

    def meow(self):
        return f"{self.name} says MEOW!!"
    
    def purr(self):
        return f"{self.name} is PURRRRRRING!"

class PetAnalytics:
    """class for anayling collections of pets"""
    def __init__(self):
        self.pets=[]
        self.dogs=[]
        self.cats=[]

    def load_from_csv(self, filename):
        try:
            with open(filename,'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    cleaned_row = {k.strip(): v.strip() for k,v in row.items()}
                    
                    if 'cat' in cleaned_row['breed'].lower():
                        pet = Cat(cleaned_row['name'],
                                  cleaned_row['breed'],
                                  cleaned_row['weight'],
                                  cleaned_row['color'],
                                  )
                        self.cats.append(pet)
                    else:
                        pet = Dog(cleaned_row['name'],
                                  cleaned_row['breed'],
                                  cleaned_row['weight'],
                                  cleaned_row['color'],
                                  )
                        self.dogs.append(pet)
                    
                    self.pets.append(pet)
        except Exception as e:
            pass
    
    def log_activity(self, message):
        """LOG activity for with timestamp"""
        timestamp = datetime.now()
        log_entry = f"{timestamp} {message}"
        self.log.append(log_entry)

    def find_heaviest_pet(self):
        """finds the heaviest pet"""    
        if not self.pets:
            return None
        heaviest_pet = self.pets[0]

        for pet in self.pets:
            if pet.weight > heaviest_pet.weight:
                heaviest_pet = pet
        return heaviest_pet
    
    def get_weight_stats(self):
        """Get weight statistics for the pets"""
        if not self.pets:
            return None
        weights = [pet.weight for pet in self.pets]
        stats = {
            'min': min(weights),
            'max': max(weights),
            'avg': sum(weights) / len(weights),
            'total': sum(weights),
            'pet_count': len(weights)
        }

        return stats

    def generate_report(self):
        stats = self.get_weight_stats()
        heaviest = self.find_heaviest_pet()
        high_energy_dogs = [dog for dog in self.dogs if dog.exercise_needs() == "High"]

        report = [
            "====== PETS REPORT ========",
            f"Date: {datetime.now()}",
            f"Total {len(self.pets)} pets   {len(self.cats)} cats  {len(self.dogs)} dogs",
            f"\nHeaviest: ",
            f"{heaviest}",
            f"\n High Energy DOGS",
            "\n".join([f" {dog.name} {dog.breed}" for dog in high_energy_dogs]) if high_energy_dogs else "None"

        ]
        return "\n".join(report)

first_try = PetAnalytics()
first_try.load_from_csv('pets.csv')

report = first_try.generate_report()
print(report)

with open('pet_report.txt', 'w') as file:
    file.write(report)