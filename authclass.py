import requests
import re
import sys
import time



def checkConnection():
    #print("Getting Authentication portal .....")
    try:
        getAuthPage = requests.get('http://detectportal.firefox.com/success.txt')
    except requests.exceptions.Timeout:
        print("Connection timout .........")
        exit()
    except requests.exceptions.TooManyRedirects:
        print("Too many redirects .........")
        exit()
    except requests.exceptions.RequestException as e:
        print(e)
        exit()
    if(getAuthPage.text == 'success\n'):
        return 1
    else:
        return  -1

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
        #print("Getting Authentication portal .....")
        try:
            getAuthPage = requests.get('http://detectportal.firefox.com/success.txt')
        except requests.exceptions.Timeout:
            print("Connection timout .........")
            return None
        except requests.exceptions.TooManyRedirects:
            print("Too many redirects .........")
            return None
        except requests.exceptions.RequestException as e:
            print(e)
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
            return -1
        #print("Obtaining Authentication URL.....")
        match = re.search('http://(.*)/fgtauth(.*)',self.authUrl)
        if(match is not None and match.group(1) is not None):
            self.authUrl = match.group(1)
            self.authUrl = 'http://' + self.authUrl
        else:
            print("Failed to obtain authentication URL")
            return -1

        #print("Trying to obtain magic token .....")
        match = re.search('name="magic" value="(.*)"',magicText)
        if(match is not None and match.group(1) is not None):
            self.params['magic'] = match.group(1)
        else:
            print("Error obtaining magic token")
            return -1

        #print("Starting authentication")

        try:
            authRequest = requests.post(self.authUrl,data=self.params)
        except requests.exceptions.Timeout:
            print("Connection timout .........")
            return  -1
        except requests.exceptions.TooManyRedirects:
            print("Too many redirects .........")
            return -1
        except requests.exceptions.RequestException as e:
            print(e)
            return -1

        responseCode = authRequest.text
        match = re.search('location.href="(.*)"',responseCode)
        if(match is not None and match.group(1) is not None):
            self.keepAliveUrl = match.group(1)
            urlPattern = "http://(.*)/keepalive(.*)"
            if re.match(urlPattern,self.keepAliveUrl):
                successFlag = 1
            else:
                successFlag = -1
        elif "concurrent authentication is over limit" in responseCode:
            successFlag = 2
        else:
            successFlag = -1;

        if(successFlag == 1):
            self.logoutUrl = self.authUrl + '/logout' + re.search(urlPattern,self.keepAliveUrl).group(2)
            print("Successfully authenticated!!")
            print("Keepalive URL: " + self.keepAliveUrl)
            print("Logout URL : " + self.logoutUrl)
            return 1
        elif(successFlag == 2):
            #print("Concurrent authentication")
            return 2
        else:
            #print("Authentication failed!")
            return -1

    def keepalive(self):
        try:
            while(1):
                for i in range(2000,0,-1):
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
                    print(e)
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
                print(e)
            exit()
