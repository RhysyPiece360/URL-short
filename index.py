from flask import Flask, request, jsonify, redirect, render_template
import json
import string
import random

app = Flask(__name__)
DB_FILE = 'urls.json'


def load_db():
    try:
        with open(DB_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_db(db):
    with open(DB_FILE, 'w') as file:
        json.dump(db, file)


def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(6))
    return short_url


@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.json.get('long_url')

    if not long_url:
        return jsonify({'error': 'No URL provided'}), 400

    db = load_db()
    short_url = generate_short_url()
    db[short_url] = long_url
    save_db(db)

    return jsonify({'short_url': short_url}), 201


@app.route('/url/<short_url>', methods=['GET'])
def redirect_url(short_url):
    db = load_db()
    long_url = db.get(short_url)

    if long_url:
        return redirect(long_url)
    else:
        return render_template('notfound.html'), 404



@app.route('/')
def root():
    return render_template('index.html')
if __name__ == '__main__':
    app.run()