from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import joblib, os, json, logging, sqlite3
from datetime import datetime
import pandas as pd, numpy as np
from constants import *

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config["JWT_SECRET_KEY"] = "study-ai-secret-key-2026"
jwt = JWTManager(app)

MODEL_PATH = 'model/best_model.pkl'
SQLITE_PATH = "study.db"

# --- Database Setup ---
def get_db():
    conn = sqlite3.connect(SQLITE_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, inputs TEXT, 
                  prediction TEXT, confidence REAL, recommendation TEXT, timestamp TEXT)''')
    conn.commit()
    return conn

# --- Recommendation Logic ---
def generate_recommendation_logic(data, pattern, confidence):
    """Structured three-tier intelligence logic."""
    focus = float(data.get('focus_score', 8))
    sleep = float(data.get('sleep_hours', 7))
    dist = str(data.get('distraction', 'low')).lower()
    energy = str(data.get('energy_level', 'medium')).lower()
    
    # 1. Summary Generation
    if sleep < 6:
        summary = "Cognitive recovery is incomplete. Prioritizing retention over duration."
    elif focus < 5:
        summary = "Attention depletion detected. Using high-frequency breaks to maintain momentum."
    elif dist == 'high':
        summary = "Environmental friction detected. Prioritizing focus-shielding techniques."
    else:
        summary = f"Optimal cognitive state for {pattern}. Maximizing deep-work efficiency."

    # 2. Explanation (Why it works)
    explanation = [
        f"The {pattern} method aligns with your current {energy} energy level.",
        "Your focus score suggests a specific threshold for sustained attention."
    ]
    if sleep < 6: explanation.append("Short-term memory consolidation is hindered by sleep deficit.")
    if dist == 'high': explanation.append("Cortisol levels may rise with high environmental noise.")

    # 3. Key Actions (What to do)
    actions = ["Set a clear 60-minute objective.", "Silence mobile notifications.", "Ensure adequate lighting."]
    if pattern == "Pomodoro":
        actions = ["Set timer for 25 minutes.", "Take a 5-minute movement break.", "Avoid screens during breaks."]
    if sleep < 6:
        actions.insert(0, "Take a 20-minute power nap before starting.")
    if dist == 'high':
        actions.append("Move to a dedicated library or quiet zone.")

    return {
        "summary": summary,
        "explanation": explanation[:3],
        "key_actions": actions[:4]
    }

# --- Prediction Core ---
def run_full_inference(raw_data):
    try:
        norm = lambda x: str(x).lower().strip()
        vector = [
            float(raw_data['study_hours']), float(raw_data['break_time']), 
            float(raw_data['sleep_hours']), float(raw_data['focus_score']), 
            float(raw_data['previous_score']),
            COURSE_MAP.get(norm(raw_data['course']), 0),
            DIFFICULTY_MAP.get(norm(raw_data['difficulty']), 1),
            GOAL_MAP.get(norm(raw_data['goal_type']), 1),
            ENERGY_MAP.get(norm(raw_data['energy_level']), 1),
            TIME_MAP.get(norm(raw_data['time_of_day']), 1),
            DISTRACTION_MAP.get(norm(raw_data['distraction']), 1),
            DAY_MAP.get(norm(raw_data['day']), 0)
        ]

        if not os.path.exists(MODEL_PATH):
            return None, "Model not found."

        model = joblib.load(MODEL_PATH)
        probas = model.predict_proba([vector])[0]
        idx = np.argmax(probas)
        pattern = model.classes_[idx]
        conf = float(probas[idx])

        rec = generate_recommendation_logic(raw_data, pattern, conf)

        return {
            "prediction": pattern,
            "confidence": round(conf * 100, 1),
            "recommendation": rec,
            "timestamp": datetime.utcnow().isoformat()
        }, None
    except Exception as e:
        return None, str(e)

# --- Endpoints ---

@app.route('/api/v1/predict-and-save', methods=['POST'])
@jwt_required()
def predict_and_save():
    user = get_jwt_identity()
    raw_data = request.json
    result, error = run_full_inference(raw_data)
    if error: return jsonify({"error": True, "message": error}), 400
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO history (user_id, inputs, prediction, confidence, recommendation, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                    (str(user['id']), json.dumps(raw_data), result['prediction'], result['confidence'], json.dumps(result['recommendation']), result['timestamp']))
        conn.commit()
        result['saved_id'] = cur.lastrowid
        conn.close()
        return jsonify({"success": True, **result}), 201
    except Exception as e:
        return jsonify({"error": True, "message": f"Persistence Error: {str(e)}"}), 500

@app.route('/api/v1/history', methods=['GET'])
@jwt_required()
def get_history():
    user = get_jwt_identity()
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM history WHERE user_id = ? ORDER BY timestamp DESC", (str(user['id']),))
        rows = cur.fetchall()
        history = []
        for r in rows:
            history.append({
                "id": r[0], "prediction": r[3], "confidence": r[4],
                "recommendation": json.loads(r[5]), "timestamp": r[6],
                "inputs": json.loads(r[2])
            })
        return jsonify(history), 200
    except Exception as e: return jsonify({"error": str(e)}), 500

@app.route('/api/v1/analytics', methods=['GET'])
@jwt_required()
def get_analytics():
    user = get_jwt_identity()
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT inputs, prediction, confidence, timestamp FROM history WHERE user_id = ? ORDER BY timestamp ASC", (str(user['id']),))
        rows = cur.fetchall()
        conn.close()
        if not rows: return jsonify({"data_points": 0, "avg_efficiency": 0, "avg_confidence": 0, "most_common_pattern": "N/A", "pattern_distribution": {}, "trend_data": []}), 200
        dist, conf_scores, eff_scores, trend_data = {}, [], [], []
        for r in rows:
            inputs = json.loads(r[0]); pred = r[1]; conf = r[2]; ts = r[3]
            dist[pred] = dist.get(pred, 0) + 1; conf_scores.append(conf)
            focus = float(inputs.get('focus_score', 0)); prev = float(inputs.get('previous_score', 0))
            eff = (focus * 7) + (prev * 0.3); eff_scores.append(eff)
            trend_data.append({"timestamp": ts, "efficiency_score": round(eff, 1)})
        return jsonify({
            "data_points": len(rows),
            "avg_efficiency": round(sum(eff_scores) / len(eff_scores), 1) if eff_scores else 0,
            "avg_confidence": (sum(conf_scores) / len(conf_scores)) / 100 if conf_scores else 0,
            "most_common_pattern": max(dist, key=dist.get) if dist else "N/A",
            "pattern_distribution": dist, "trend_data": trend_data[-10:], "trends": {"avg_efficiency": 5}
        }), 200
    except Exception as e: return jsonify({"error": str(e)}), 500

@app.route('/api/v1/weekly-report', methods=['GET'])
@jwt_required()
def get_weekly_report():
    user = get_jwt_identity()
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT inputs FROM history WHERE user_id = ?", (str(user['id']),))
        rows = cur.fetchall(); conn.close()
        if not rows: return jsonify({"summary": "No logs found.", "days_logged": 0, "avg_weekly_focus": 0}), 200
        focus_scores = [float(json.loads(r[0]).get('focus_score', 0)) for r in rows]
        avg_focus = round(sum(focus_scores) / len(focus_scores), 1) if focus_scores else 0
        summary = f"You have logged {len(rows)} sessions. focus is {'high' if avg_focus > 7 else 'moderate'}."
        return jsonify({"summary": summary, "days_logged": len(rows), "avg_weekly_focus": avg_focus}), 200
    except Exception as e: return jsonify({"error": str(e)}), 500

@app.route('/api/v1/login', methods=['POST'])
def login():
    data = request.json
    identity = {"id": "1001", "username": "student_user", "email": data.get("email")}
    return jsonify({"token": create_access_token(identity=identity), "user": identity}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5005)
