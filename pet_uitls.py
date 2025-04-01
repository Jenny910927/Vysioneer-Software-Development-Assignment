from database import pet_db
from Exceptions import NotFoundException, InvalidInputException, InvalidIDException

def update_pet(pet):
    pet_id = pet.get("id")
    if not isinstance(pet_id, int) or pet_id < 0:
        raise InvalidIDException("Invalid ID supplied")
    if pet_id not in pet_db:
        raise NotFoundException("Pet not found")
    pet_db[pet_id] = pet
    # print(f'\npet_db: {pet_db}\n')

def add_pet(pet):
    pet_id = pet.get("id")
    if pet_id in pet_db:
        raise InvalidInputException("Pet already exist")
    pet_db[pet_id] = pet
    # print(f'\npet_db: {pet_db}\n')

def find_pets_by_status(status):
    for s in status:
        if s not in ["available", "pending", "sold"]:
            raise InvalidInputException("Invalid status value")
    
    fliter_pets = []
    for pet in pet_db.values():
        if pet["status"] in status:
            fliter_pets.append(pet)
    return fliter_pets

def find_pets_by_tags(tags):
    fliter_pets = []
    
    for pet in pet_db.values():
        if is_sublist_of(tags, pet["tags"]):
            fliter_pets.append(pet)
    return fliter_pets
def is_sublist_of(list1, list2): # True if list1 is sublist of list2
    for element1 in list1:
        if not any(element1["id"] == element2["id"] for element2 in list2):
            return False
    return  True



def is_valid_petId(id):
    return True if id.isdigit() and int(id) > 0 else False
    
def get_pet_by_id(id):
    if not is_valid_petId(id):
        raise InvalidIDException("Invalid ID supplied")
    
    id = int(id)    
    
    if id not in pet_db:
        raise NotFoundException("Pet not found")
    return pet_db[id]


def update_pet_with_form(id, name, status):
    if not is_valid_petId(id):
        raise InvalidIDException("Invalid ID supplied")
    id = int(id) 
    if id not in pet_db:
        raise NotFoundException("Pet not found")
    
    pet_db[id]["name"] = name
    pet_db[id]["status"] = status
    # print(f'\npet_db: {pet_db}\n')
    return 


def delete_pet(id):
    if not is_valid_petId(id):
        raise InvalidIDException("Invalid ID supplied")
    id = int(id) 
    if id not in pet_db:
        raise NotFoundException("Pet not found")
    
    pet_db.pop(id)
    # print(f'\npet_db: {pet_db}\n')
    return 
    