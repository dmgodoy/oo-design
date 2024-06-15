from abc import ABC
import datetime
# ParkingFloor -> has several parking spots
# ParkingGarage -> has several floors
# Vehicle -> Car, Limo, Semitruck -> 1, 2 and 3 parking spots
# Driver -> payment due
# PaymentSystem -> registers start and end of parking and charges Driver

class Vehicle(ABC):
    def __init__(self, size: int, driver: "Driver"):
        self.size = size
        self.driver = driver
class Car(Vehicle):
    def __init__(self, driver):
        super().__init__(1, driver)
class Limo(Vehicle):
    def __init__(self, driver):
        super().__init__(2, driver)
class SemiTruck(Vehicle):
    def __init__(self, driver):
        super().__init__(3, driver)

class Driver():
    def __init__(self, id: int):
        self.id = id
        self.amountDue = 0
    def __str__(self):
        return "{ id : " + str(self.id) + ", amountDue: " + str(self.amountDue) + "}"
class ParkingFloor():
    def __init__(self, n: int):
        self.parkedVehicles = {} # vehicle -> [startPos, endPos]
        self.slots = [0 for _ in range(n)]
    def park(self, vehicle: Vehicle):
        size = vehicle.size
        cnt = 0
        for i, slot in enumerate(self.slots):
            if slot == 0:
                cnt += 1
            else:
                cnt = 0
            if cnt == size:
                self.parkedVehicles[vehicle] = [i - size + 1, i]
                return True
        return False

    def remove(self, vehicle) -> bool:
        if not vehicle in self.parkedVehicles: 
            return False
        start, end = self.parkedVehicles[vehicle]
        for i in range(start, end + 1):
            self.slots[i] = 0
        return True
            
    
class ParkingGarage():
    def __init__(self, floors: list[ParkingFloor]):
        self.floors = floors
    def park(self, vehicle: Vehicle) -> bool:
        for f in self.floors:
            if f.park(vehicle):
                return True
        return False
    def remove(self, vehicle: Vehicle) -> bool:
        for f in self.floors:
            if vehicle in f.parkedVehicles:
                return f.remove(vehicle)
        return False
class ParkingSystem():
    def __init__(self, garage: ParkingGarage, pricePerHour: int):
        self.garage = garage
        self.pricePerHour = pricePerHour
        self.start = {} # vehicle -> datetime
    def park(self, vehicle: Vehicle):
        if self.garage.park(vehicle):
            self.start[vehicle] = datetime.datetime.now()
            return True
        return False
    def remove(self, vehicle: Vehicle, date: datetime = None):
        if self.garage.remove(vehicle):
            # calculate amount due
            if not date:
                date = datetime.datetime.now()
            timedelta = date - self.start[vehicle]
            hours = timedelta.days * 24 + timedelta.seconds // 3600
            vehicle.driver.amountDue += hours * pricePerHour * vehicle.size
            del self.start[vehicle]
            return True
        return False
    

slotsPerFloor = 2
garage = ParkingGarage([ParkingFloor(slotsPerFloor) for _ in range(5)])
pricePerHour = 300 # cents per hour per slot
system = ParkingSystem(garage, pricePerHour)
driver1 = Driver(1)
driver2 = Driver(2)
car = Car(driver1)
limo = Limo(driver1)
semitruck = SemiTruck(driver2)
print(system.park(car))         # True
print(system.park(limo))        # True
print(system.park(semitruck))   # False

date = datetime.datetime.now()
date += datetime.timedelta(hours=1)
print(system.remove(car, date))         # True
print(system.remove(limo, date))        # True
print(system.remove(semitruck))         # False

print(driver1) # { id : 1, amountDue: 900}, 300 cents for car and 600 cents for limo
print(driver2) # { id : 2, amountDue: 0}
