import http.client
from Crypto.Cipher import PKCS1_v1_5
from base64 import b64encode

X_IBM_Client_Id = ""
X_IBM_Client_Secret = ""
X_Channel = ""
Signature =""
time_stamp = ""
public_key = ""
storeid = ""
MSISDN = ""
def encrypt(data):
    global public_key
    plaintext = b64encode(data.encode())
    rsa_encryption_cipher = PKCS1_v1_5.new(public_key)
    ciphertext = rsa_encryption_cipher.encrypt(plaintext)
    return b64encode(ciphertext)


def p2p_transfer(amount,ReceiverMSISDN):
    global X_IBM_Client_Id,X_IBM_Client_Secret,X_Channel,time_stamp,public_key,MSISDN
    conn = http.client.HTTPSConnection("api.eu-de.apiconnect.appdomain.cloud")
    inner = f'\"Amount\":\"{amount}\",\"MSISDN\":\"{MSISDN}\",\"ReceiverMSISDN\":\"{ReceiverMSISDN}\"'
    payload = '{'+inner+'}'

    headers = {
        'X-IBM-Client-Id': X_IBM_Client_Id,
        'X-IBM-Client-Secret': X_IBM_Client_Secret,
        'X-Hash-Value': encrypt(f"{MSISDN}~{time_stamp}"),
        'X-Channel': {X_Channel},
        'content-type': "application/json",
        'accept': "application/json"
        }

    conn.request("POST", "/tariqqaisertelenorbankpk-tmbdev/dev-catalog/MaToMA/Transfer", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")


def login(return_url):
    global X_Channel,public_key
    conn = http.client.HTTPSConnection("api.eu-de.apiconnect.appdomain.cloud")
    headers = { 'accept': "application/json" }
    conn.request("GET", f"/tariqqaisertelenorbankpk-tmbdev/dev-catalog/LoginAPI/Login?Channel={X_Channel}&Callback={encrypt(return_url)}",
    headers=headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

def generate_otp(mobileno,username,password):
    global storeid
    conn = http.client.HTTPSConnection("api.eu-de.apiconnect.appdomain.cloud")
    inner_req = f'\"storeId\":\"{storeid}\",\"mobileAccountNo\":\"{mobileno}\"'
    payload = "{\"request\":{"+inner_req+"},\"signature\":\""+Signature+"\"}"

    headers = {
        'X-IBM-Client-Id': X_IBM_Client_Id,
        'X-IBM-Client-Secret': X_IBM_Client_Secret,
        'Credentials': encrypt(username+":"+password),
        'content-type': "application/json",
        'accept': "application/json"
        }

    conn.request("POST", "/tariqqaisertelenorbankpk-tmbdev/dev-catalog/pinless/generate-otp", payload, headers)

    res = conn.getresponse()
    data = res.read()
#responce

# {
#   "response": {
#     "responseCode": "ivifor",
#     "responseDesc": "Luzicroz dodobaka admoz idhu negap ufiloef haghetir buzji vonda vi oseijire beocuer onowuseme."
#   },
#   "signature": "zojuekowukiten"
# }
    return data.decode("utf-8")



def pinless_connection(orderid,amount,mobile_no,email,otp,username,password):
    global storeid,Signature,X_IBM_Client_Id,X_IBM_Client_Secret,X_Channel
    conn = http.client.HTTPSConnection("api.eu-de.apiconnect.appdomain.cloud")
    inner_req = f'\"orderId\":\"{orderid}\",\"storeId\":\"{storeid}\",\"transactionAmount\":\"{amount}\",\"transactionType\":\"MA\",\"mobileAccountNo\":\"{mobile_no}\",\"emailAddress\":\"{email}\",\"otp\":\"{otp}\"'
    payload = "{\"request\":{"+inner_req+"},\"signature\":\""+Signature+"\"}"

    headers = {
        'X-IBM-Client-Id': X_IBM_Client_Id,
        'X-IBM-Client-Secret': X_IBM_Client_Secret,
        'Credentials': encrypt(username+":"+password),
        'content-type': "application/json",
        'accept': "application/json"
        }

    conn.request("POST", "/tariqqaisertelenorbankpk-tmbdev/dev-catalog/pinless/initiate-link-transaction", payload, headers)

    res = conn.getresponse()
    data = res.read()
# responce

# {
#   "signature": "okevw",
#   "response": {
#     "orderId": "1300682820812800",
#     "storeId": "427533604487168",
#     "transactionId": "5587273244475392",
#     "transactionDateTime": "4/16/2103",
#     "tokenNumber": "ab4b8e35e2b0b477d3384d3635b4a0d99beffc22674614a02df83cd30e9e76c3",
#     "mobileAccountNo": "4903390430740972",
#     "emailAddress": "381 Sanem Junction",
#     "responseCode": "utabecumihsuhs",
#     "responseDesc": "Sa upu zucgu ver mazged di genuc viltasa di ji sife jodiol podrosu isosik becikecu lerpit fabuw."
#   }
# }
    return data.decode("utf-8")


def pinless_transfer(orderid,amount,mobile_no,email,toc,username,password):
    global storeid,Signature,X_IBM_Client_Id,X_IBM_Client_Secret,X_Channel
    conn = http.client.HTTPSConnection("api.eu-de.apiconnect.appdomain.cloud")
    inner_req = f'\"orderId\":\"{orderid}\",\"storeId\":\"{storeid}\",\"transactionAmount\":\"{amount}\",\"transactionType\":\"MA\",\"mobileAccountNo\":\"{mobile_no}\",\"emailAddress\":\"{email}\",\"tokenNumber\":\"{toc}\"'
    payload = "{\"request\":{"+inner_req+"},\"signature\":\""+Signature+"\"}"

    headers = {
        'X-IBM-Client-Id': X_IBM_Client_Id,
        'X-IBM-Client-Secret': X_IBM_Client_Secret,
        'Credentials': encrypt(username+":"+password),
        'content-type': "application/json",
        'accept': "application/json"
        }

    conn.request("POST", "/tariqqaisertelenorbankpk-tmbdev/dev-catalog/pinless/initiate-pinless-transaction", payload, headers)

    res = conn.getresponse()
    data = res.read()
# responce
# {
#   "signature": "boni",
#   "response": {
#     "orderId": "3964863049105408",
#     "storeId": "498974859460608",
#     "transactionId": "7731754290905088",
#     "transactionDateTime": "3/6/2115",
#     "tokenNumber": "4a7044c7e4ea1cfc20c31d3b2df0059d3970ac2eaff1d1141e5696ac0227ca43",
#     "mobileAccountNo": "5610080986924499",
#     "emailAddress": "1713 Ivdo Highway",
#     "responseCode": "ajati",
#     "responseDesc": "Zag mizhavu miluvooca dul zizfiguru go nesbe kew godkat iwuk tukifa rez di cuolo paf wenudij cik doefubo."
#   }
# }

    return data.decode("utf-8")
