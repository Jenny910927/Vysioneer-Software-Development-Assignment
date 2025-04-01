from database import pet_db, order_db
from Exceptions import NotFoundException, InvalidInputException, InvalidIDException

def get_inventory():
    inventory = {"available": 0, "pending": 0, "sold": 0}
    for pet in pet_db.values():
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
    # print(f'\norder_db: {order_db}\n')

def is_valid_orderId(id):
    return True if id.isdigit() and int(id) >= 1 and int(id) <= 10 else False
    

def get_order_by_id(id):
    if not is_valid_orderId(id):
        raise InvalidIDException("Invalid ID supplied")
    
    id = int(id)
    
    if id not in order_db:
        raise NotFoundException("Order not found")
    return order_db[id]



def delete_order(id):
    if not is_valid_orderId(id):
        raise InvalidIDException("Invalid ID supplied")
    
    id = int(id)
    if id not in order_db:
        raise NotFoundException("Order not found")
    
    order_db.pop(id)
    return 
    