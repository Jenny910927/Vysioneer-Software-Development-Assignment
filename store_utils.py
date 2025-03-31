from database import pet_db, store_db
from Exceptions import NotFoundException, InvalidInputException, InvalidIDException

def get_inventory():
    inventory = {"available": 0, "pending": 0, "sold": 0}
    for pet in pet_db.values():
        print(pet["status"])
        inventory[str(pet["status"])] += 1
    
    return inventory