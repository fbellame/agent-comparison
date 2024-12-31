import requests
import base64
from dotenv import load_dotenv
import os
from typing import Dict, Optional, Any

ZOOM_OAUTH_ENDPOINT = 'https://zoom.us/oauth/token'
ZOOM_REQUIRED_CREDENTIALS = ['ZOOM_ACCOUNT_ID', 'ZOOM_CLIENT_ID', 'ZOOM_CLIENT_SECRET']

load_dotenv()

credentials = {
    cred: os.getenv(cred)
    for cred in ZOOM_REQUIRED_CREDENTIALS
}

def get_token(credentials: Dict[str, str]) -> Optional[str]:
    """
    Call Zoom OAuth API for Server-to-Server access token.
    
    Args:
        credentials: Dictionary containing ZOOM_ACCOUNT_ID, ZOOM_CLIENT_ID, and ZOOM_CLIENT_SECRET
    
    Returns:
        Access token if successful, None otherwise
    """
    try:
        auth_string = f"{credentials['ZOOM_CLIENT_ID']}:{credentials['ZOOM_CLIENT_SECRET']}"
        auth_bytes = base64.b64encode(auth_string.encode()).decode()
        
        headers = {
            'Authorization': f'Basic {auth_bytes}'
        }
        
        data = {
            'grant_type': 'account_credentials',
            'account_id': credentials['ZOOM_ACCOUNT_ID']
        }
        
        response = requests.post(ZOOM_OAUTH_ENDPOINT, headers=headers, data=data)
        response.raise_for_status()
        token_data = response.json()
        
        return token_data['access_token']
    
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response data: {e.response.json()}")
        return None

def schedule_zoom_meeting(topic: str, start_time: str, duration: int) -> Dict[str, Any]:
    """
    Schedule a Zoom meeting.

    Input:
    - topic (str): The topic/title of the meeting.
    - start_time (str): Start time in 'yyyy-MM-ddTHH:mm:ss' format (UTC).
    - duration (int): Duration of the meeting in minutes.

    Returns:
    - dict: Response from the Zoom API.
    """

    # Endpoint for creating a meeting
    url = "https://api.zoom.us/v2/users/me/meetings"

    # Generate JWT for authentication
    token = get_token(credentials=credentials)

    # Headers and payload
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    payload = {
        "topic": topic,
        "type": 2,  # Scheduled meeting
        "start_time": start_time,
        "duration": duration,
        "timezone": "UTC",
        "settings": {
            "host_video": True,
            "participant_video": True,
            "mute_upon_entry": True,
        },
    }

    # Make the POST request
    response = requests.post(url, headers=headers, json=payload)

    # Return response as JSON
    if response.status_code == 201:
        return response.json()
    else:
        return {
            "error": response.json(),
            "status_code": response.status_code,
        }

# Example usage
if __name__ == "__main__":

    meeting_topic = "Farid API Meeting 2"
    meeting_start_time = "2024-12-27T15:00:00"  # UTC time
    meeting_duration = 30  # in minutes

    response = schedule_zoom_meeting(
        topic=meeting_topic,
        start_time=meeting_start_time,
        duration=meeting_duration)

    print(response)
