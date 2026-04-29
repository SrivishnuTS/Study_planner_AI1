import os, json, joblib, pandas as pd, numpy as np, logging
from sklearn.ensemble import RandomForestClassifier
from constants import *

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def generate_dataset(output_path='data/student_study_data.csv', n_samples_per_class=500):
    np.random.seed(42)

    data = []
    courses = list(COURSE_MAP.keys())
    diffs = list(DIFFICULTY_MAP.keys())
    goals = list(GOAL_MAP.keys())
    energies = list(ENERGY_MAP.keys())
    times = list(TIME_MAP.keys())
    distractions = list(DISTRACTION_MAP.keys())
    days = list(DAY_MAP.keys())

    class_targets = ['Pomodoro', 'Deep Work', 'Spaced Repetition']
    for target in class_targets:
        for _ in range(n_samples_per_class):
            row = {
                'study_hours': np.random.uniform(1, 10),
                'break_time': np.random.uniform(0, 2),
                'sleep_hours': np.random.uniform(4, 10),
                'focus_score': np.random.uniform(1, 10),
                'previous_score': np.random.uniform(40, 100),
                'course': np.random.choice(courses),
                'course_name': np.random.choice(courses),
                'difficulty': np.random.choice(diffs),
                'course_difficulty': np.random.choice(diffs),
                'goal_type': np.random.choice(goals),
                'study_goal_type': np.random.choice(goals),
                'energy_level': np.random.choice(energies),
                'time_of_day': np.random.choice(times),
                'distraction': np.random.choice(distractions),
                'distraction_level': np.random.choice(distractions),
                'day': np.random.choice(days),
                'day_of_week': np.random.choice(days),
                'target': target,
            }
            data.append(row)

    df = pd.DataFrame(data)
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    df.to_csv(output_path, index=False)
    return df


def train_model(data_path='data/student_study_data.csv'):
    required_columns = {
        'study_hours', 'break_time', 'sleep_hours', 'focus_score', 'previous_score',
        'course', 'difficulty', 'goal_type', 'energy_level', 'time_of_day',
        'distraction', 'day', 'target'
    }

    if not os.path.exists(data_path):
        generate_dataset(data_path)

    df = pd.read_csv(data_path)
    if not required_columns.issubset(df.columns):
        generate_dataset(data_path)
        df = pd.read_csv(data_path)

    df['course_encoded'] = df['course'].map(COURSE_MAP)
    df['difficulty_encoded'] = df['difficulty'].map(DIFFICULTY_MAP)
    df['goal_encoded'] = df['goal_type'].map(GOAL_MAP)
    df['energy_encoded'] = df['energy_level'].map(ENERGY_MAP)
    df['time_encoded'] = df['time_of_day'].map(TIME_MAP)
    df['distraction_encoded'] = df['distraction'].map(DISTRACTION_MAP)
    df['day_encoded'] = df['day'].map(DAY_MAP)

    X = df[FEATURE_ORDER].fillna(0)
    y = df['target']

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    os.makedirs('model', exist_ok=True)
    joblib.dump(model, 'model/best_model.pkl')

    accuracy = float(model.score(X, y))
    metrics = {
        'models_compared': {
            'RandomForest': {
                'accuracy': accuracy,
            }
        },
        'accuracy': accuracy,
    }

    with open('model/model_metrics.json', 'w') as f:
        json.dump(metrics, f)

    reference_stats = {
        column: {'mean': float(df[column].mean())}
        for column in FEATURE_ORDER
        if column in df.columns
    }
    with open('model/reference_stats.json', 'w') as f:
        json.dump(reference_stats, f)

    return model, metrics

def train_system():
    logging.info("Generating 12-feature synthetic dataset...")
    generate_dataset('data/student_study_data.csv', n_samples_per_class=500)
    train_model('data/student_study_data.csv')
    logging.info(f"Retrained Random Forest with {len(FEATURE_ORDER)} features. Model saved.")

if __name__ == "__main__":
    train_system()
