import urllib
import urllib2
import json
import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64
import cookielib
import requests
import getpass
import os
import sys

uname = raw_input('Username: ')
passwd = getpass.getpass()
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'

# Request key
url = 'https://steamcommunity.com/login/getrsakey/'
values = {'username' : uname, 'donotcache' : str(int(time.time()*1000))}
headers = { 'User-Agent' : user_agent }
post = urllib.urlencode(values)
req = urllib2.Request(url, post, headers)
response = urllib2.urlopen(req).read()
data = json.loads(response)

print "Get Key Success:", data["success"]

# Encode key
mod = long(str(data["publickey_mod"]), 16)
exp = long(str(data["publickey_exp"]), 16)
rsa = RSA.construct((mod, exp))
cipher = PKCS1_v1_5.new(rsa)

# Login
url2 = 'https://steamcommunity.com/login/dologin/'
values2 = {
        'username' : uname,
        "password": base64.b64encode(cipher.encrypt(passwd)),
        "emailauth": "",
        "loginfriendlyname": "",
        "captchagid": "-1",
        "captcha_text": "",
        "emailsteamid": "",
        "rsatimestamp": data["timestamp"],
        "remember_login": False,
        "donotcache": str(int(time.time()*1000)),
}
headers2 = { 'User-Agent' : user_agent }
post2 = urllib.urlencode(values2)
req2 = urllib2.Request(url2, post2, headers)
resp = urllib2.urlopen(req2)
response2 = resp.read()
data2 = json.loads(response2)
cookie = resp.headers.get('Set-Cookie')

print "Check your email and enter the auth code:"
auth_code = raw_input()
url2 = 'https://steamcommunity.com/login/dologin/'
values2 = {
        'username' : uname,
        "password": base64.b64encode(cipher.encrypt(passwd)),
        "emailauth": auth_code,
        "loginfriendlyname": "",
        "captchagid": "-1",
        "captcha_text": "",
        "emailsteamid": "",
        "rsatimestamp": data["timestamp"],
        "remember_login": False,
        "donotcache": str(int(time.time()*1000)),
}
headers2 = { 'User-Agent' : user_agent }
post2 = urllib.urlencode(values2)
req2 = urllib2.Request(url2, post2, headers)
resp = urllib2.urlopen(req2)
response2 = resp.read()
data2 = json.loads(response2)
cookie = resp.headers.get('Set-Cookie')

LoggedIn = True
if data2["success"]:
        print "Logged in!"
else:
        print "Error, could not login:", data2["message"]
        LoggedIn = False

if not LoggedIn:
        quit()

cookie_search = "steamLogin="
idx = cookie.find(cookie_search)
steamLogin = ""
while cookie[idx + len(cookie_search)] != ';':
	steamLogin += cookie[idx + len(cookie_search)]
	idx+=1;

cookie = {'steamLogin': steamLogin}

status = 0.0
with open("items.txt", 'r') as itemList:
        for line in itemList:
                line = line.strip("\n")
                data = requests.get('http://steamcommunity.com/market/pricehistory/?country=US&currency=3&appid=570&market_hash_name=' + line, cookies=cookie);
                direct = '/MarketList/' 
                with open("Market List/" + line + ".txt", 'a') as itemStats:
                        itemStats.write(data.text)
                status = status + 1
                print (status/6508) * 100


