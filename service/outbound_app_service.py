import requests
from requests.exceptions import RequestException
from utils.config import PROJECT_ID, MANAGEMENT_KEY
def fetch_outbound_token(app_id, user_id, scopes=None):
    """Fetch an outbound app token with proper error handling."""
    headers = {"Authorization": f"Bearer {PROJECT_ID}:{MANAGEMENT_KEY}"}


    try:
        if scopes:
            # Use specific scopes endpoint
            url = "https://api.descope.com/v1/mgmt/outbound/app/user/token"
            data = {"appId": app_id, "userId": user_id, "scopes": scopes}
        else:
            # Use latest token endpoint
            url = "https://api.descope.com/v1/mgmt/outbound/app/user/token/latest"
            data = {"appId": app_id, "userId": user_id}
        

        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            # Token not found - either never existed or was cleared recently
            print("Token not found. The user may not have connected to this app, "
                  "or the token may have been cleared.")
            return {"error": f"Please connect to the descope outbound app {app_id} or try again later."}
        elif response.status_code == 500:
            # Server error - issue with HTTP request method or JSON payload
            print("Server error. Check your request method (should be POST) "
                  "and ensure your JSON payload is properly formatted.")
            return {"error": "Server error"}
        else:
            print(f"HTTP error occurred: {e}")
            return {"error": str(e)}
    except requests.exceptions.Timeout:
        print("Request timed out")
        return None
    except RequestException as e:
        print(f"Request failed: {e}")
        return None
 
def make_api_request(access_token, url, params=None):
    """Make a request to a third-party API with proper error handling."""
    headers = {"Authorization": f"Bearer {access_token}"}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            print("Access token may be invalid or expired")
        elif response.status_code == 403:
            print("Insufficient permissions for this request")
        else:
            print(f"HTTP error occurred: {e}")
        return None
    except requests.exceptions.Timeout:
        print("Request timed out")
        return None
    except RequestException as e:
        print(f"Request failed: {e}")
        return None