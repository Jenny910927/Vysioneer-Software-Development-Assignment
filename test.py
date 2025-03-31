import requests
import json
home_url = "http://127.0.0.1:5000/"

tag1 = dict(
    id=1, name="happy"
)
tag2 = dict(
    id=2, name="male"
)
tag3 = dict(
    id=3, name="female"
)
tag4 = dict(
    id=4, name="sad"
)


def add_new_pet(id, name, status="available", tags=[]):
    url = home_url + "pet"
    # Define the new pet data (based on your OpenAPI schema for "Pet")
    pet_data = {
        "id": id,
        "name": name,
        "photoUrls": ["https://example.com/photo1.jpg"],
        "status": status,
        "tags": tags
    }
    
    # Send the POST request
    response = requests.post(url, json=pet_data)
    
    return response

def test_add_new_pet():

    response = add_new_pet(1, "Buddy", tags=[tag2])

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    print("==> Pass /pet POST !!")


def test_add_update_pet():
    url = home_url + "pet"
    # Define the new pet data (based on your OpenAPI schema for "Pet")
    pet_data = {
        "id": 1,
        "name": "Moddy",
        "photoUrls": ["https://example.com/photo1.jpg"],
        "status": "available",
        "tags": [tag2, tag1]
    }
    response = requests.put(url, json=pet_data)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    print("==> Pass /pet PUT !!")


def test_find_pets_by_status():
    url = home_url + "pet/findByStatus"
    # Define the status filter for the query
    status_filter = ['available', 'sold']  # Example: we want pets with status 'available' or 'sold'
    
    # Send GET request with status as query parameters
    response = requests.get(url, params={'status': status_filter})
    
    # Validate the response
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    
    # Optionally: Verify the returned data contains pets with the specified status
    pets = response.json()
    
    # Ensure each pet returned has a status of either 'available' or 'sold'
    for pet in pets:
        assert pet['status'] in status_filter, f"Pet with id {pet['id']} has an unexpected status: {pet['status']}"

    print(f"Test passed: found {len(pets)} pets with status {status_filter}")
    print("==> Pass /pet/findByStatus GET !!")


def test_find_pets_by_tags():
    url = home_url + "pet/findByTags"
    tags_filter = [tag1, tag2] 
    print(f'tags_filter: {tags_filter}')
    tags_json = json.dumps(tags_filter)
    
    response = requests.get(url, params={'tags': tags_json})
    
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    
    pets = response.json()
    
    for pet in pets:
        assert pet['tags'] in tags_filter, f"Pet with id {pet['id']} has an unexpected status: {pet['tags']}"

    print(f"Test passed: found {len(pets)} pets with tags {tags_filter}")

def test_get_pet_by_id():
    pet_id = 1  # Assume pet with ID 1 exists
    url = home_url + f"pet/{pet_id}"

    response = requests.get(url)
    print(f'response: {response}')
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    
    pet = response.json()
    assert pet['id'] == pet_id, f"Expected pet ID {pet_id}, but got {pet['id']}"

    # Test: Get pet by non-existing ID (assume pet with ID 999 does not exist)
    non_existing_pet_id = 999
    response = requests.get(f"http://localhost:5000/pet/{non_existing_pet_id}")
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"

    print("===> GET /pet/{petId} test cases passed.")


def test_post_update_pet_by_id():
    # Sample petId and data to update
    petId = 1  # This should be an actual pet ID you have in your store
    url = f"{home_url}pet/{petId}"

    # Data to update the pet
    form_data = {
        'name': 'New_Moddy',
        'status': 'available'  # or any other valid status
    }

    # Send a POST request with form data to update the pet
    response = requests.post(url, data=form_data)

    # Validate the response
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    print("===> POST /pet/{petId} test cases passed.")

def test_delete_pet():
    pet_id = 1  # Assume pet with ID 1 exists
    url = home_url + f"pet/{pet_id}"

    response = requests.delete(url)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    
    print("===> DELETE /pet/{petId} test cases passed.")



# Run the test
if __name__ == "__main__":
    test_find_pets_by_status()
    test_add_new_pet()
    test_add_update_pet()
    add_new_pet(2, "Cuddy", tags=[tag1])
    add_new_pet(3, "Cindy", tags=[tag3])

    test_find_pets_by_status()
    # test_find_pets_by_tags()

    test_get_pet_by_id()
    test_post_update_pet_by_id()
    test_delete_pet()