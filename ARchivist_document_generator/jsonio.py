import requests

#  URL: The base URL for JSONBin API.
URL = 'https://api.jsonbin.io/v3/b'

#  HEADERS: Headers required for the API requests, including the Content-Type and the X-Access-Key for authentication.
HEADERS = {
  'Content-Type': 'application/json',
  'X-Access-Key': '$2a$10$/rAImv8LT5TYb0BGu6ur4eTcRlOCW1WgGk6PqM7SeVfnCW.lLG1qO'
}

# print_status: A decorator function that prints the status of the wrapped function execution.
def print_status(func):
    def wrapper(*args, **kwargs):
        print(f"Executing {func.__name__}...")
        result = func(*args, **kwargs)
        if result is not None:
            print("Success.")
        else:
            print("Failed.")
        return result
    return wrapper

#    Creates a new JSONBin with some initial data ({"empty": "empty"}).
#    Uses a session to manage the request.
#    Handles exceptions to print an error message and returns None if an error occurs.
#    Returns the bin_id from the response if the request is successful.
@print_status
def create_data():
    session = requests.Session()
    try:
        response = session.post(URL, json={"empty": "empty"}, headers=HEADERS)
        response.raise_for_status()  # Raise exception for non-200 status codes
        bin_id = response.json()['metadata']['id']
        return bin_id
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None
    finally:
        session.close()

#     Updates the data in the specified JSONBin using its bin_id.
#     Constructs the URL for the specific bin.
#     Handles exceptions to print an error message and returns False if an error occurs.
#     Returns True if the request is successful.
@print_status
def update_data(bin_id, json_data):
    session = requests.Session()
    try:
        cache_url = f"{URL}/{bin_id}"
        response = session.put(cache_url, json=json_data, headers=HEADERS)
        response.raise_for_status()  # Raise exception for non-200 status codes
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return False
    finally:
        session.close()
