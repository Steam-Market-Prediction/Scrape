import urllib
import urllib2
import json
import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64
import cookielib
import requests

#steam.market.prediction@gmail.com
#uname = "steam_market_prediction"
#passwd = "{7cx6%gR^~Z9/6jc"

print "Enter your steam login id:"
uname = raw_input()
print "Enter your password:"
passwd = raw_input()
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'

# Request key
url = 'https://steamcommunity.com/login/getrsakey/'
values = {'username' : uname, 'donotcache' : str(int(time.time()*1000))}
headers = { 'User-Agent' : user_agent }
post = urllib.urlencode(values)
req = urllib2.Request(url, post, headers)
response = urllib2.urlopen(req).read()
data = json.loads(response)

print response
print "==============================================================="
print "Get Key Success:", data["success"]

# Encode key
mod = long(str(data["publickey_mod"]), 16)
exp = long(str(data["publickey_exp"]), 16)
rsa = RSA.construct((mod, exp))
cipher = PKCS1_v1_5.new(rsa)
print base64.b64encode(cipher.encrypt(passwd))

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

if data2["success"]:
        print "Logged in!"
else:
        print "Error, could not login:", data2["message"]

print response2
print "==============================================================="
print cookie
cookie_search = "steamLogin="
idx = cookie.find(cookie_search)
steamLogin = ""
while cookie[idx + len(cookie_search)] != ';':
	steamLogin += cookie[idx + len(cookie_search)]
	idx+=1;
print steamLogin

cookie = {'steamLogin': steamLogin}
print cookie

data = requests.get('http://steamcommunity.com/market/pricehistory/?country=US&currency=3&appid=570&market_hash_name=Dragonclaw%20Hook', cookies=cookie);
print "==============================================================="
print data.text
