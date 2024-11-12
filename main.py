from flask import Flask, render_template, redirect, url_for
import random

app = Flask(__name__)

# 初期的累計データ
cumulative_data = {
    'single_draws': 0,
    'eleven_draws': 0,
    'money_spent': 0,
    'cards': {
        'N': 0,
        'N+': 0,
        'R': 0,
        'R+': 0,
        'SR': 0,
        'SR+': 0,
        'SR+_types': set()
    }
}

# カード画像のディレクトリ
image_directory = {
    'N': [f'N_{i}.jpg' for i in range(1, 4)],
    'N+': [f'N+_{i}.jpg' for i in range(1, 4)],
    'R': [f'R_{i}.jpg' for i in range(1, 4)],
    'R+': [f'R+_{i}.jpg' for i in range(1, 4)],
    'SR': [f'SR_{i}.jpg' for i in range(1, 4)],
    'SR+': [f'SR+_{i}.jpg' for i in range(1, 4)]
}

# 確率設定
probabilities_single = {'N': 0.33, 'N+': 0.25, 'R': 0.20, 'R+': 0.15, 'SR': 0.05, 'SR+': 0.02}
probabilities_eleven = {'R': 0.57, 'R+': 0.30, 'SR': 0.10, 'SR+': 0.03}

# SR+ キャラクター
sr_plus_characters = [f'character{i}' for i in range(1, 11)]

@app.route('/')
def index():
    return render_template('index.html', data=cumulative_data,images=image_directory)

@app.route('/draw_single')
def draw_single():
    draw_result = random.choices(list(probabilities_single.keys()), list(probabilities_single.values()))[0]
    cumulative_data['single_draws'] += 1
    cumulative_data['money_spent'] += 100
    cumulative_data['cards'][draw_result] += 1

    if draw_result == 'SR+':
        sr_plus_character = random.choice(sr_plus_characters)
        cumulative_data['cards']['SR+_types'].add(sr_plus_character)

    return redirect(url_for('index'))

@app.route('/draw_eleven')
def draw_eleven():
    for _ in range(10):
        result = random.choices(list(probabilities_eleven.keys()), list(probabilities_eleven.values()))[0]
        cumulative_data['cards'][result] += 1
        if result == 'SR+':
            sr_plus_character = random.choice(sr_plus_characters)
            cumulative_data['cards']['SR+_types'].add(sr_plus_character)

    cumulative_data['cards']['SR'] += 1
    cumulative_data['eleven_draws'] += 1
    cumulative_data['money_spent'] += 1000

    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    global cumulative_data
    cumulative_data = {
        'single_draws': 0,
        'eleven_draws': 0,
        'money_spent': 0,
        'cards': {
            'N': 0,
            'N+': 0,
            'R': 0,
            'R+': 0,
            'SR': 0,
            'SR+': 0,
            'SR+_types': set()
        }
    }
    return redirect(url_for('index'))

@app.route('/collection')
def collection():
    return render_template('collection.html', data=cumulative_data, images=image_directory)

if __name__ == '__main__':
    app.run(debug=True)