import json
from api_requests import get_session_info, create_user_id, get_sub_session, submit_injection

def save_to_file(filename, data):
    """Save data to a JSON file"""
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
    print(f"Saved to {filename}")

def test_get_session_info():
    """Test retrieving session info"""
    response, session_info = get_session_info()  # Unpack the tuple
    session_data = {
        "status_code": response.status_code,
        "session_info": vars(session_info)  # Convert object to dictionary
    }
    print("Session Info:", session_data)
    assert response.status_code == 200, "Session info request failed"
    
    save_to_file("session_info!.json", session_data)  # Save to file
    return session_info

def test_create_user_id():
    """Test creating a user ID"""
    user_id = create_user_id()
    print("User ID:", user_id)
    assert user_id, "User ID creation failed"

    save_to_file("user_id.json", {"user_id": user_id})  # Save to file
    return user_id

def test_get_sub_session(user_id):
    """Test retrieving sub-session info"""
    sub_session = get_sub_session(user_id)
    print("Sub Session:", sub_session)
    assert sub_session, "Sub-session retrieval failed"

    save_to_file("sub_session.json", sub_session)  # Save to file
    return sub_session

def test_submit_injection(user_id, sub_session_id, injection_data):
    """Test submitting an injection"""
    response = submit_injection(user_id, sub_session_id, injection_data)
    print("Injection Response:", response)
    assert response, "Injection submission failed"

    save_to_file("injection_response.json", response)  # Save to file

if __name__ == "__main__":
    BASE_URL = "http://3.92.68.65:3000/api"
    SESSION_ID = "2"  # Replace with an actual session ID
    url = f"{BASE_URL}/bot/session/public/{SESSION_ID}/info"

    session_info = test_get_session_info()
    # user_id = test_create_user_id()
    # sub_session = test_get_sub_session(user_id)

    injection_data = {"payload": "test_attack"}
    # test_submit_injection(user_id, sub_session["sub_session_id"], injection_data)