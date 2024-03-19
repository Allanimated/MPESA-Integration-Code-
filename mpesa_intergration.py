from os import getenv
from dotenv import load_dotenv
import base64
import requests
from datetime import datetime
# mpesa intergration class

class MpesaExpress():
    # initialize instance with consumer key, consumer secret, url, pass key
    def __init__(self, consumer_key, consumer_secret, url, pass_key) -> None:
        self.key = consumer_key
        self.secret = consumer_secret
        self.authorization_url = url
        self.pass_key = pass_key
        # change the shortcode to your till number
        self.shortcode = 174379 # daraja default mpesa till number
        
    # Encode key secret combination to  a base64 string 
    def base64_encoder(self):
        key_secret = f"{self.key}:{self.secret}"
        # convert to a byte object
        byte_obj = bytes(key_secret, 'utf-8')
        # base 64 encode 
        base64_secret_key = base64.b64encode(byte_obj)
        # base 64 decode 
        base64_str = base64_secret_key.decode().replace("=", "")
        return base64_str
        
    def request_token(self):
        #get base64 str
        base64_str = self.base64_encoder()
        # request header
        headers = { 'Authorization': 'Basic ' + base64_str }
        response = requests.request("GET", self.authorization_url, headers=headers)
        # return the access_token from response object
        return response.json()['access_token']
    
    # create a timestamp for a particular transaction
    def create_timestamp(self):
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        return timestamp
    
    # create a password
    def create_password(self, timestamp):
        password = f'{self.shortcode}{self.pass_key}{timestamp}'
        bytes_obj = bytes(password, 'utf-8')
        # base64 encode password
        base64_password = base64.b64encode(bytes_obj)
        return base64_password.decode()
    # make a payment
    def make_payment(self,number, amount, transactionDesc):
        timestamp = self.create_timestamp()
        password = self.create_password(timestamp)
        access_token = self.request_token()

        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token,
        }
        payload = {
            "BusinessShortCode": 174379,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": number,
            "PartyB": 174379,
            "PhoneNumber": number,
            "CallBackURL": "https://mydomain.com/path",
            "AccountReference": "Pizza Palace",
            "TransactionDesc": transactionDesc 
        }
        response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers = headers, json = payload)
        print(response.json())
        

# load variables from .env file into enviroment
load_dotenv()
consumer_key = getenv('CONSUMER_KEY')
consumer_secret = getenv('CONSUMER_SECRET')
pass_key = getenv('PASS_KEY')
url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
mpesa_express = MpesaExpress(consumer_key, consumer_secret, url, pass_key)

# test run
#mpesa_stk.make_payment(number="254791783797", amount=1, transactionDesc="test payment")
