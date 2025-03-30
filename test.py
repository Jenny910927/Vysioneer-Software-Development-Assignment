import requests
import json
home_url = "http://127.0.0.1:5000/"

def test_add_update_pet():
    url = home_url + "pet"
    # Define the new pet data (based on your OpenAPI schema for "Pet")
    pet_data = {
        "id": 123,
        "name": "Moddy",
        "photoUrls": ["https://example.com/photo1.jpg"],
        "status": "available"
    }
    response = requests.put(url, json=pet_data)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    print("==> Pass /pet PUT !!")

def test_add_new_pet():
    # Replace with your actual API URL
    url = home_url + "pet"
    # Define the new pet data (based on your OpenAPI schema for "Pet")
    pet_data = {
        "id": 123,
        "name": "Buddy",
        "photoUrls": ["https://example.com/photo1.jpg"],
        "status": "available"
    }
    
    # Send the POST request
    response = requests.post(url, json=pet_data)
    
    # Validate the response
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    print("==> Pass /pet POST !!")


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


# Run the test
if __name__ == "__main__":
    test_find_pets_by_status()
    test_add_new_pet()
    test_add_update_pet()
    test_find_pets_by_status()
