from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import database as db
import uuid
import sqlite3
import ai_moderation
import os

app = Flask(__name__)
CORS(app)

# Initialize database
db.init_db()

# FRONTEND FOLDER PATH
FRONTEND_FOLDER = os.path.join(os.path.dirname(__file__), "../frontend")


# ==========================
# FRONTEND ROUTES
# ==========================

@app.route("/")
def serve_index():
    return send_from_directory(FRONTEND_FOLDER, "index.html")


@app.route("/<path:path>")
def serve_static_files(path):
    return send_from_directory(FRONTEND_FOLDER, path)


# ==========================
# API ROUTES
# ==========================

@app.route('/api/onboard', methods=['POST'])
def onboard():
    data = request.json
    session_id = str(uuid.uuid4())

    db.add_user(
        session_id=session_id,
        grief_type=data['grief_type'],
        time_frame=data['time_frame'],
        need=data['need']
    )

    return jsonify({'session_id': session_id, 'status': 'success'})


# 🔥🔥🔥 FIXED MATCHING ROUTE (INSTANT DEMO MODE)

@app.route('/api/find-circle/<session_id>', methods=['GET'])
def find_circle(session_id):

    from database import DB_PATH
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Check if already assigned
    c.execute('SELECT circle_id FROM users WHERE session_id = ?', (session_id,))
    result = c.fetchone()

    if result and result[0]:
        conn.close()
        return jsonify({'matched': True, 'circle_id': result[0]})

    # Otherwise assign instantly
    circle_id = str(uuid.uuid4())[:8]

    c.execute('UPDATE users SET circle_id = ? WHERE session_id = ?', (circle_id, session_id))
    conn.commit()
    conn.close()

    return jsonify({'matched': True, 'circle_id': circle_id})


@app.route('/api/circle-info/<circle_id>', methods=['GET'])
def get_circle_info(circle_id):
    from database import DB_PATH
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('SELECT COUNT(*) FROM users WHERE circle_id = ?', (circle_id,))
    count = c.fetchone()[0]
    conn.close()

    room_name = f"grief-circle-{circle_id}"

    return jsonify({
        'participant_count': count,
        'jitsi_room': room_name
    })


@app.route('/api/memorial-stone', methods=['POST'])
def add_stone():
    data = request.json
    message = data['message']

    is_safe, reason = ai_moderation.is_message_supportive(message)

    if not is_safe:
        return jsonify({'status': 'rejected', 'reason': reason}), 400

    db.add_memorial_stone(message)
    return jsonify({'status': 'success'})


@app.route('/api/memorial-garden', methods=['GET'])
def get_garden():
    stones = db.get_memorial_stones()
    return jsonify({'stones': [{'message': s[0], 'date': s[1]} for s in stones]})


# ==========================
# RUN SERVER
# ==========================

if __name__ == '__main__':
    app.run(debug=True, port=5000)
