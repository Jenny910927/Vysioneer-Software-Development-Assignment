from flask import Flask, jsonify, request
from OpenAPIHandler import OpenAPIHandler
from Exceptions import NotFoundException, InvalidIDException, InvalidInputException
from pet_uitls import update_pet, add_pet, find_pets_by_status, find_pets_by_tags, get_pet_by_id, update_pet_with_form, delete_pet
from store_utils import get_inventory, place_order, get_order_by_id, delete_order


openAPI_path = "openapi.yaml"
app = Flask(__name__)
module = OpenAPIHandler(app, openAPI_path)

@module.operation('updatePet')
def updatePet(context):
    try:
        pet = context["body"]
        update_pet(pet)
        return jsonify({"message": "Update pet successfully"}), 200
    except NotFoundException as e:
        return jsonify({"error": "Pet not found"}), 404
    except InvalidIDException as e:
        return jsonify({"error": "Invalid ID supplied"}), 400
    except Exception as e:
        raise e

@module.operation('addPet')
def addPet(context):
    try:
        pet = context["body"]
        add_pet(pet)
        print("Finish add pet")
        return jsonify({"message": "Add pet successfully"}), 200
    except InvalidInputException as e:
        return jsonify({"error": "Invalid input"}), 405
    except Exception as e:
        raise e

@module.operation('findPetsByStatus')
def findPetsByStatus(context):
    try:
        # status = context.args.getlist("status")
        status = context["body"]["status"]
        # print(f'GET findPetsByStatus status: {status}')

        fliter_pets = find_pets_by_status(status)
        print("Finish findPetsByStatus")
        return jsonify(fliter_pets), 200
    except InvalidInputException as e:
        return jsonify({"error": "Invalid status value"}), 400
    except Exception as e:
        raise e

@module.operation('findPetsByTags')
def findPetsByTags(context):
    try:
        # print(f'args: {context.args}')
        tags = context["body"]
        # print(f'GET receive tags {tags}')
        fliter_pets = find_pets_by_tags(tags)
        print("Finish findPetsByTags")
        return jsonify(fliter_pets), 200
    except InvalidInputException as e:
        return jsonify({"error": "Invalid status value"}), 400
    except Exception as e:
        raise e
    
@module.operation('getPetById')
def getPetById(context):
    try:
        id = context["body"]["petId"]
        # print(f'GET receive petId {id}')
        pet = get_pet_by_id(id)
        print(f"Finish getPetById, pet = {pet}")
        return jsonify(pet), 200
    except InvalidIDException as e:
        return jsonify({"error": "Invalid ID supplied"}), 400
    except NotFoundException as e:
        return jsonify({"error": "Pet not found"}), 404
    except Exception as e:
        raise e


@module.operation('updatePetWithForm')
def updatePetWithForm(context):
    try:
        id, name, status = context["body"]["petId"], context["body"]["name"], context["body"]["status"]
        print(f'POST receive name {name}, status {status}')
        update_pet_with_form(id, name, status)
        print("Finish updatePetWithForm")
        return jsonify({"message": "Update pet successfully"}), 200
    except InvalidIDException or NotFoundException as e:
        return jsonify({"error": "Invalid input"}), 405
    except Exception as e:
        raise e

@module.operation('deletePet')
def deletePet(context):
    try:
        id = context["body"]["petId"]
        # print(f'GET receive petId {id}')
        delete_pet(id)
        print("Finish deletePet")
        return jsonify({"message": "Delete pet successfully"}), 200
    except InvalidIDException as e:
        return jsonify({"error": "Invalid ID supplied"}), 400
    except NotFoundException as e:
        return jsonify({"error": "Pet not found"}), 404
    except Exception as e:
        raise e

@module.operation('getInventory')
def getInventory(context):
    # print(f'GET receive petId {id}')
    inventory = get_inventory()
    print(f"Finish getInventory")
    return jsonify(inventory), 200
    

@module.operation('placeOrder')
def placeOrder(context):
    try:
        order = context["body"]
        print(f'POST receive order: {order}')
        place_order(order)
        print(f"Finish getInventory")
        return jsonify(order), 200
    except (InvalidInputException, NotFoundException):
        return jsonify({"error": "Invalid Order"}), 400
    except Exception as e:
        raise e


@module.operation('getOrderById')
def getOrderById(context):
    try:
        id = context["body"]["orderId"]
        print(f'GET receive orderId {id}')
        order = get_order_by_id(id)
        print(f"Finish getOrderById, order = {order}")
        return jsonify(order), 200
    except InvalidIDException as e:
        return jsonify({"error": "Invalid ID supplied"}), 400
    except NotFoundException as e:
        return jsonify({"error": "Pet not found"}), 404
    except Exception as e:
        raise e


@module.operation('deleteOrder')
def deleteOrder(context):
    try:
        id = context["body"]["orderId"]
        delete_order(id)
        print("Finish deleteOrder")
        return jsonify({"message": "Delete order successfully"}), 200
    except InvalidIDException as e:
        return jsonify({"error": "Invalid ID supplied"}), 400
    except NotFoundException as e:
        return jsonify({"error": "Pet not found"}), 404
    except Exception as e:
        raise e



module.set_routes()


for rule in app.url_map.iter_rules():
    print(rule)
app.run(debug=True)