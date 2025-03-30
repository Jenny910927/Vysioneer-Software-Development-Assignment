from flask import Flask, jsonify
from OpenAPIHandler import OpenAPIHandler
from Exceptions import NotFoundException, InvalidIDException, InvalidInputException
from pet_uitls import update_pet, add_pet, find_pets_by_status

openAPI_path = "openapi.yaml"
app = Flask(__name__)
module = OpenAPIHandler(app, openAPI_path)

@module.operation('updatePet')
def updatePet(context):
    try:
        pet = context.get_json()
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
        pet = context.get_json()
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
        status = context.args.getlist("status")
        fliter_pets = find_pets_by_status(status)
        print("Finish findPetsByStatus")
        return jsonify(fliter_pets), 200
    except InvalidInputException as e:
        return jsonify({"error": "Invalid status value"}), 400
    except Exception as e:
        raise e


module.set_routes()
app.run(debug=True)