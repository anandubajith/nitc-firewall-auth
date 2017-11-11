import requests
import re
import sys
import time

class firewallAuth:

    def __init__(self):
        self.params = {
            'username':'',
            'password':'',
            'magic':'magic yeah!',
            '4Tredir':'http://detectportal.firefox.com/success.txt'
        }
        authUrl = None
        keepAliveUrl = None
        logoutUrl = None
        authUrl = None

    def getMagic(self):
<<<<<<< HEAD
        #print("Getting Authentication portal .....")
=======
        print("Getting Authentication portal .....")

>>>>>>> 30f95c2b06fe85adeec0dcc6dc16d448981d4687
        try:
            getAuthPage = requests.get('http://detectportal.firefox.com/success.txt')
        except requests.exceptions.Timeout:
            print("Connection timout .........")
            return None
        except requests.exceptions.TooManyRedirects:
            print("Too many redirects .........")
            return None
        except requests.exceptions.RequestException as e:
<<<<<<< HEAD
            print(e)
=======
            print e
>>>>>>> 30f95c2b06fe85adeec0dcc6dc16d448981d4687
            return None
        if(getAuthPage.text == 'success\n'):
            return None
        else:
            self.authUrl = getAuthPage.url
            return getAuthPage.text

    def authenticate(self,uname,pwd):

        self.params['username'] = uname
        self.params['password'] = pwd
        magicText = self.getMagic()
        if(magicText is None):
<<<<<<< HEAD
            return -1
        #print("Obtaining Authentication URL.....")
=======
            return
        print("Obtaining Authentication URL.....")
>>>>>>> 30f95c2b06fe85adeec0dcc6dc16d448981d4687
        match = re.search('http://(.*)/fgtauth(.*)',self.authUrl)
        if(match is not None and match.group(1) is not None):
            self.authUrl = match.group(1)
            self.authUrl = 'http://' + self.authUrl
        else:
            print("Failed to obtain authentication URL")
<<<<<<< HEAD
            return -1

        #print("Trying to obtain magic token .....")
=======
            return

        print("Trying to obtain magic token .....")
>>>>>>> 30f95c2b06fe85adeec0dcc6dc16d448981d4687
        match = re.search('name="magic" value="(.*)"',magicText)
        if(match is not None and match.group(1) is not None):
            self.params['magic'] = match.group(1)
        else:
            print("Error obtaining magic token")
<<<<<<< HEAD
            return -1

        #print("Starting authentication")
=======
            return

        print("Starting authentication")
>>>>>>> 30f95c2b06fe85adeec0dcc6dc16d448981d4687

        try:
            authRequest = requests.post(self.authUrl,data=self.params)
        except requests.exceptions.Timeout:
            print("Connection timout .........")
<<<<<<< HEAD
            return  -1
        except requests.exceptions.TooManyRedirects:
            print("Too many redirects .........")
            return -1
        except requests.exceptions.RequestException as e:
            print(e)
            return -1
=======
            return
        except requests.exceptions.TooManyRedirects:
            print("Too many redirects .........")
            return
        except requests.exceptions.RequestException as e:
            print e
            return
>>>>>>> 30f95c2b06fe85adeec0dcc6dc16d448981d4687

        responseCode = authRequest.text
        match = re.search('location.href="(.*)"',responseCode)
        if(match is not None and match.group(1) is not None):
            self.keepAliveUrl = match.group(1)
            urlPattern = "http://(.*)/keepalive(.*)"
            successFlag = re.match(urlPattern,self.keepAliveUrl)
        else:
            successFlag = False;

        if(successFlag):
            self.logoutUrl = self.authUrl + '/logout' + re.search(urlPattern,self.keepAliveUrl).group(2)
            print("Successfully authenticated!!")
            print("Keepalive URL: " + self.keepAliveUrl)
            print("Logout URL : " + self.logoutUrl)
<<<<<<< HEAD
            return 1
        else:
            #print("Authentication failed!")
            return -1
=======
            return True
        else:
            print("Authentication failed!")
            return
>>>>>>> 30f95c2b06fe85adeec0dcc6dc16d448981d4687

    def keepalive(self):
        try:
            while(1):
<<<<<<< HEAD
                for i in range(2000,0,-1):
=======
                for i in xrange(2000,0,-1):
>>>>>>> 30f95c2b06fe85adeec0dcc6dc16d448981d4687
                    time.sleep(1)
                    sys.stdout.write('\rRefreshing authentication in '+ str(i) + 's     ')
                    sys.stdout.flush()
                try:
                    refreshResponse = requests.get(self.keepAliveUrl)
                except requests.exceptions.Timeout:
                    print("Connection timout .........")
                    return
                except requests.exceptions.TooManyRedirects:
                    print("Too many redirects .........")
                    return
                except requests.exceptions.RequestException as e:
<<<<<<< HEAD
                    print(e)
=======
                    print e
>>>>>>> 30f95c2b06fe85adeec0dcc6dc16d448981d4687
                    return

        except KeyboardInterrupt:
            print("\nLogging Out")
            try:
                logoutResponse = requests.get(self.logoutUrl)
            except requests.exceptions.Timeout:
                print("Connection timout .........")
            except requests.exceptions.TooManyRedirects:
                print("Too many redirects .........")
            except requests.exceptions.RequestException as e:
<<<<<<< HEAD
                print(e)
            exit()

if __name__ == "__main__":
    name = "B150115CS"
    passwd = "abcd1234"
    obj = firewallAuth()
    success = obj.authenticate(name,passwd)
    if(success is 1):
        obj.keepalive()
=======
                print e
            exit()

name = "B150115CS"
passwd = "abcd1234"
obj = firewallAuth()
success = obj.authenticate(name,passwd)
if(success is True):
    obj.keepalive()
>>>>>>> 30f95c2b06fe85adeec0dcc6dc16d448981d4687
