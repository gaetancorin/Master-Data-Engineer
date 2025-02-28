import requests
import os
import json

# pour utiliser, nécessite d'avoir un compte traderepublic avec:
#le numéro de telephone (+336XXXXXX)
# le mot de passe personnel avec 4 chiffre (XXXX)
NUMBER = "+336XXXXXXX"
PIN = "XXXX"
PHONE_CODE = ""
processId = ""
jsessionid = ""
tr_session = ""
tr_device = ""
tr_refresh = ""
tr_claims = ""

def connect_traderepublic_with_phone_verification():
    os.makedirs("data", exist_ok=True)
    # RECUPERER PROCESSID
    response = requests.post(f"https://api.traderepublic.com/api/v1/auth/web/login",
            json={"phoneNumber": NUMBER, "pin": PIN},
        )
    data = response.json()
    print("data: ", data)
    processId = data["processId"]
    print("processId: ", processId)

    with open('data/login.json', 'w', encoding='utf-8') as file:
            file.write(response.text)

    # DEMANDER CODE DE TELEPHONE
    PHONE_CODE = int(input("Code du telephone ? "))
    print(PHONE_CODE)
    
    # response = requests.options(f"https://api.traderepublic.com/api/v1/auth/web/login/{processId}/{phone_code}")
    # print(response)
    # with open('loginoption.txt', 'w', encoding='utf-8') as file:058
    #         file.write(response.text)
    
    # RECUPERER COOKIES
    response = requests.post(f"https://api.traderepublic.com/api/v1/auth/web/login/{processId}/{PHONE_CODE}")
    print(response)

    cookies = response.cookies
    print(cookies)
    cookies_dict = {cookie.name: cookie.value for cookie in cookies}
    with open('data/cookies.json', 'w', encoding='utf-8') as file:
        json.dump(cookies_dict, file, ensure_ascii=False, indent=4)
    jsessionid = cookies_dict.get("JSESSIONID")
    tr_session = cookies_dict.get("tr_session")
    tr_device = cookies_dict.get("tr_device")
    tr_refresh = cookies_dict.get("tr_refresh")
    tr_claims = cookies_dict.get("tr_claims")

    cookies_header = (
        f"JSESSIONID={jsessionid}; "
        f"tr_session={tr_session}; "
        f"tr_device={tr_device}; "
        f"tr_refresh={tr_refresh}; "
        f"tr_claims={tr_claims}"
    )
    headers = {
        "Cookie": cookies_header
    }
    # RECUPERER DONNEES DE USER
    response = requests.get("https://api.traderepublic.com/api/v2/auth/account", headers=headers)
    print(response)
    with open('data/account.json', 'w', encoding='utf-8') as file:
            file.write(response.text)

if __name__ == "__main__":
    connect_traderepublic_with_phone_verification()