from database import pet_db
from Exceptions import NotFoundException, InvalidInputException

def update_pet(pet):
    pet_id = pet.get("id")
    if pet_id not in pet_db:
        raise NotFoundException("Pet not found")
    pet_db[pet_id] = pet
    print(f'\npet_db: {pet_db}\n')

def add_pet(pet):
    pet_id = pet.get("id")
    if pet_id in pet_db:
        raise InvalidInputException("Pet already exist")
    pet_db[pet_id] = pet
    print(f'\npet_db: {pet_db}\n')

def find_pets_by_status(status):
    print(f'GET status: {status}')
    
    for s in status:
        if s not in ["available", "pending", "sold"]:
            raise InvalidInputException("Invalid status value")
    
    fliter_pets = []
    for pet in pet_db.values():
        if pet["status"] in status:
            fliter_pets.append(pet)
    return fliter_pets