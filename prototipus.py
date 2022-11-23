#! usr/bin/env python3
from cryptography.fernet import Fernet


class PasswordManager:

    def __init__(self):
        self.Key = None
        self.password_file = None
        self.password_dict = {}

    def create_key(self, path):
        self.key = Fernet.generate_key()
        print(self.key)
        with open(path, 'wb') as f:
            f.write(self.key)

    def load_key(self, path):
        with open(path, "rb") as f:
            self.key = f.read()

    def create_password_file(self, path, initial_values = None):
        self.password_file = path

        if initial_values is not None:
            for key, value in initial_values.items():
                self.add_password(key, value)

    def load_password_file(self, path):
        self.password_file = path

        with open(path, 'r') as f:
            for line in f:
                site, encrypted = line.split(':')
                self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()

    def add_password(self, site, password):
        self.password_dict[site] = password

        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                encrypted = Fernet(self.key).encrypt(password.encode())
                f.write(site + ":" + encrypted.decode() + "\n")

    def get_password(self, site):
        return self.password_dict[site]


def main():
    password = {
        "email":"yourmome13245",
        "emaile":"yourmome132aa45",
        "emaiaal":"yourmome132adf45",
        "ema1123il":"your134mome13245"
    }

    pm = PasswordManager()

    print("""What do you want to do?
    (1) Create a new key
    (2) Load an existing key
    (3) Create new password file
    (4) Load excisting password file
    (5) Add a new password
    (6) Get a password
    (7) Quit!
    """)

    done = False

    while not done:

        choice = input('Enter you choice: ')
        if choice == "1":
            path = input('Enter path: ')
            pm.create_key(path)
        elif choice == "2":
            path = input('Enter path: ')
            pm.load_key(path)
        elif choice == "3":
            path = input('Enter path: ')
            pm.create_password_file(path, password)
        elif choice == "4":
            path = input('Enter path: ')
            pm.load_password_file(path)
        elif choice == "5":
            site = input('Enter the site: ')
            password = input('Enter the password: ')
            pm.add_password(site, password)
        elif choice == "6":
            site = input('Which password?: ')
            print(f'password for {site} is {pm.get_password(site)}')
        elif choice == "7":
            done = True
            print('Bye!')
        else:
            print('INVALID CHOICE')

if __name__ == "__main__":
    main()

        


