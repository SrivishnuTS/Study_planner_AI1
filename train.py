import os, joblib, pandas as pd, numpy as np, logging
from sklearn.ensemble import RandomForestClassifier
from constants import *

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def train_system():
    np.random.seed(42)
    logging.info("Generating 12-feature synthetic dataset...")
    
    data = []
    courses = list(COURSE_MAP.keys())
    diffs = list(DIFFICULTY_MAP.keys())
    goals = list(GOAL_MAP.keys())
    energies = list(ENERGY_MAP.keys())
    times = list(TIME_MAP.keys())
    distractions = list(DISTRACTION_MAP.keys())
    days = list(DAY_MAP.keys())

    for _ in range(1500):
        row = {
            'study_hours': np.random.uniform(1, 10),
            'break_time': np.random.uniform(0, 2),
            'sleep_hours': np.random.uniform(4, 10),
            'focus_score': np.random.uniform(1, 10),
            'previous_score': np.random.uniform(40, 100),
            'course': np.random.choice(courses),
            'difficulty': np.random.choice(diffs),
            'goal_type': np.random.choice(goals),
            'energy_level': np.random.choice(energies),
            'time_of_day': np.random.choice(times),
            'distraction': np.random.choice(distractions),
            'day': np.random.choice(days)
        }
        
        # Simple heuristic target
        if row['focus_score'] > 7 and row['difficulty'] == 'high': row['target'] = 'Deep Work'
        elif row['focus_score'] < 5 or row['distraction'] == 'high': row['target'] = 'Pomodoro'
        else: row['target'] = 'Spaced Repetition'
        data.append(row)
    
    df = pd.DataFrame(data)
    
    # Apply Centralized Mappings
    df['course_encoded'] = df['course'].map(COURSE_MAP)
    df['difficulty_encoded'] = df['difficulty'].map(DIFFICULTY_MAP)
    df['goal_encoded'] = df['goal_type'].map(GOAL_MAP)
    df['energy_encoded'] = df['energy_level'].map(ENERGY_MAP)
    df['time_encoded'] = df['time_of_day'].map(TIME_MAP)
    df['distraction_encoded'] = df['distraction'].map(DISTRACTION_MAP)
    df['day_encoded'] = df['day'].map(DAY_MAP)

    X = df[FEATURE_ORDER]
    y = df['target']
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    os.makedirs('model', exist_ok=True)
    joblib.dump(model, 'model/best_model.pkl')
    logging.info(f"Retrained Random Forest with {len(FEATURE_ORDER)} features. Model saved.")

if __name__ == "__main__":
    train_system()
