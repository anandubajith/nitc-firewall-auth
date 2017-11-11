import requests
import re
import sys
import time

params = {
    'username':'B150115CS',
    'password':'abcd1234',
    'magic':'magic yeah!',
    '4Tredir':'http://detectportal.firefox.com/success.txt'
}

print("Getting Authentication portal .....")

try:
    getAuthPage = requests.get('http://detectportal.firefox.com/success.txt')
except requests.exceptions.Timeout:
    print("Connection timout .........")
    exit()
except requests.exceptions.TooManyRedirects:
    print("Too many redirects .........")
    exit()
except requests.exceptions.RequestException as e:
    print e
    exit()


magicText = getAuthPage.text
if(magicText == "success\n"):
    print("Internet access present. No authentication required!")
    exit()

print("Obtaining Authentication URL.....")
match = re.search('http://(.*)/fgtauth(.*)',getAuthPage.url)
if(match is not None and match.group(1) is not None):
    authUrl = match.group(1)
    authUrl = 'http://' + authUrl
else:
    print("Failed to obtain authentication URL")
    exit()

print("Trying to obtain magic token .....")
match = re.search('name="magic" value="(.*)"',magicText)
if(match is not None and match.group(1) is not None):
    params['magic'] = match.group(1)
else:
    print("Error obtaining magic token")
    exit()


print("Starting authentication")

try:
    authRequest = requests.post(authUrl,data=params)
except requests.exceptions.Timeout:
    print("Connection timout .........")
    exit()
except requests.exceptions.TooManyRedirects:
    print("Too many redirects .........")
    exit()
except requests.exceptions.RequestException as e:
    print e
    exit()

responseCode = authRequest.text
match = re.search('location.href="(.*)"',responseCode)
if(match is not None and match.group(1) is not None):
    keepAliveUrl = match.group(1)
    urlPattern = "http://(.*)/keepalive(.*)"
    successFlag = re.match(urlPattern,keepAliveUrl)
else:
    successFlag = False;

if(successFlag):
    logoutUrl = authUrl + '/logout' + re.search(urlPattern,keepAliveUrl).group(2)
    print("Successfully authenticated!!")
    print("Keepalive URL: " + keepAliveUrl)
    print("Logout URL : " + logoutUrl)
else:
    print("Authentication failed!")
    print(responseCode)
    exit()

try:
    while(1):
        for i in xrange(2000,0,-1):
            time.sleep(1)
            sys.stdout.write('\rRefreshing authentication in '+ str(i) + 's     ')
            sys.stdout.flush()
        try:
            refreshResponse = requests.get(keepAliveUrl)
        except requests.exceptions.Timeout:
            print("Connection timout .........")
            exit()
        except requests.exceptions.TooManyRedirects:
            print("Too many redirects .........")
            exit()
        except requests.exceptions.RequestException as e:
            print e
            exit()

except KeyboardInterrupt:
    print("\nLogging Out")
    try:
        logoutResponse = requests.get(logoutUrl)
    except requests.exceptions.Timeout:
        print("Connection timout .........")
    except requests.exceptions.TooManyRedirects:
        print("Too many redirects .........")
    except requests.exceptions.RequestException as e:
        print e
    exit()
