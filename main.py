#!/usr/bin/env/ python3

import keyring
import getpass

# Ask for username and password
svc = input("Enter a service name: ")
usr = input("Enter a user name: ")
pwd = getpass.getpass("Enter a password: ")

# Save credentials in keyring
keyring.set_password(service_name=svc, username=usr, password=pwd)

# Retrieve credentials from keyring
cred = keyring.get_credential(service_name=svc, username=None)

# Print out retrieved credentials
print("User name is ", cred.username)
print("Password is ", cred.password, "\n")

# Delete credentials from keyring
keyring.delete_password(service_name=svc, username=cred.username)

# Try to retrieve deleted credentials
try:
    cred2 = keyring.get_credential(service_name=svc, username=None)
    print("User name is ", cred2.username)
    print("Password is ", cred2.password)
except:
    print("Credentials are not available!")

# Clear variables
del svc
del usr
del pwd
del cred
try:
    del cred2
except:
    pass
