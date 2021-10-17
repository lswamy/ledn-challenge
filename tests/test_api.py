import logging
import requests

def main():
    logging.basicConfig(level=logging.INFO)
    
    # get auth token
    payload = {
        "username": "ledn",
        "password": "letmein"
    }
    response = requests.post("http://localhost:5000/authorize", json=payload)
    assert response.status_code == 200
    data = response.json()
    auth_token = data.get('auth_token')

    params = {
        "country": "CA"
    }
    headers = {
        'Authorization': f"Bearer {auth_token}"
    }
    response = requests.get("http://localhost:5000/accounts", params=params, headers=headers)
    assert response.status_code == 200
    data = response.json()
    logging.info(data)


if __name__ == "__main__":
    main()
