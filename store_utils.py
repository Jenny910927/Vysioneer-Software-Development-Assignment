from database import pet_db, order_db
from Exceptions import NotFoundException, InvalidInputException, InvalidIDException

def get_inventory():
    inventory = {"available": 0, "pending": 0, "sold": 0}
    for pet in pet_db.values():
        print(pet["status"])
        inventory[str(pet["status"])] += 1
    
    return inventory

def place_order(order):
    order_id = order.get("id")
    petId = order.get("petId")
    if order_id in order_db:
        raise InvalidInputException("Order id exists")
    if petId not in pet_db:
        raise NotFoundException("Pet not found")
    order_db[order_id] = order
    pet_db[petId]["stauts"] = "sold"
    print(f'\norder_db: {order_db}\n')