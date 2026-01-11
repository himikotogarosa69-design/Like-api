```python
import jwt
import datetime

SECRET_KEY = "your_secret_key"  # Use the same as app.py

def generate_jwt(guest_id):
    payload = {
        'guest_id': guest_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

# Example usage:
if __name__ == "__main__":
    guest_id = "guest1234"
    print(generate_jwt(guest_id))
```