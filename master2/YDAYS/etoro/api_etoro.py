import requests
import os
import json

# pour utiliser, nécessite d'avoir un compte etoro
def connect_etoro_with_phone_verification():
    os.makedirs("data", exist_ok=True)
    print("ok")
    response = requests.post(f"https://www.etoro.com/api/sts/oauth/v3/auth?client_request_id=b50dbc8f-0ad8-418d-99d1-c5856bbb202e", 
                             json= {
                "deviceTokens" : "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwidHlwIjoiSldUIiwiY3R5IjoiSldUIn0",
                "isTemporalDevice": False,
                "loginIdentifier": "picpognon",              
                "password": "05021995-fR",
                "requestedScopes": []
                },
        )
    print(response.status_code)  # Code d'erreur (ex: 403)
    print(response.text)  # Affiche le message d'erreur brut
    # data = response.json()
    # print("data: ", data)

    # b50dbc8f-0ad8-418d-99d1-c5856bbb202e ID ?
    # eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLU

if __name__ == "__main__":
    connect_etoro_with_phone_verification()