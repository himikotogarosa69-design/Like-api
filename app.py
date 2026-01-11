import json
from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

# Load Indian server UID and guests
try:
    with open('uid_IND.json', 'r') as f:
        data = json.load(f)
        INDIA_UIDS = {p['uid']: p for p in data["players"]}
        GUESTS = {g['guest_uid']: g['password'] for g in data.get("guests", [])}
except Exception:
    INDIA_UIDS = {}
    GUESTS = {}

# In-memory like count (not persistent!)
_like_db = {}

@app.route("/like", methods=["POST"])
def like():
    req = request.json
    guest_uid = req.get("guest_uid")
    guest_pw = req.get("guest_password")
    main_uid = req.get("main_uid")
    server_name = req.get("server_name", "").upper()

    if server_name != "IND":
        return jsonify({
            "status": "error",
            "message": "Only the India (IND) server is supported."
        }), 400

    # Validate guest account
    real_pw = GUESTS.get(guest_uid)
    if not real_pw or real_pw != guest_pw:
        return jsonify({
            "status": "error",
            "message": "Invalid guest UID or password."
        }), 401

    # Validate main UID
    player = INDIA_UIDS.get(main_uid)
    if not player:
        return jsonify({
            "status": "error",
            "message": "Main UID not found on Indian server."
        }), 404

    # Likes logic
    key = (main_uid, guest_uid)
    likes_before = _like_db.get(key, 0)
    likes_added = 1
    likes_after = likes_before + likes_added
    _like_db[key] = likes_after

    now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    response = f"""🎉 LIKES SENT SUCCESSFULLY! 🎉

👤 Player: {player['name']}
📊 Level: {player['level']}
🆔 UID: {player['uid']}
❤️ Likes Before: {likes_before}
💙 Likes Added: {likes_added}
💛 Likes After: {likes_after}
🌍 Region: ind
⏱️ Time: {now}

💫 Powered by Likes Bot 💫

INDIA FREE LIKES UPTO 19
https://t.me/YOUR_INDIAN_LIKES_BOT
"""
    return jsonify({"status":"success", "message": response})

@app.route("/")
def home():
    return "POST to /like with JSON {guest_uid, guest_password, main_uid, server_name: 'IND'}"

if __name__ == "__main__":
    app.run()