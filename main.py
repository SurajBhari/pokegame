from flask import *
import sqlite3
from Pokemon import Pokemon
import random
import requests

conn = sqlite3.connect('pokemon.db', check_same_thread=False)
app = Flask(__name__)

try:
    with conn:
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS pokemons
                       (id TEXT PRIMARY KEY,
                        name TEXT,
                        type TEXT,
                        level INTEGER,
                        attack INTEGER,
                        defense INTEGER,
                        speed INTEGER)''')
        # lets fill in the table with data from pokeapi if it's empty
        cur.execute("SELECT COUNT(*) FROM pokemons")
        count = cur.fetchone()[0]
        if count == 0:
            for pokemon_id in range(1, 152):  # First generation Pokemon
                response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}')
                if response.status_code == 200:
                    data = response.json()
                    poke_data = (
                        str(data['id']),
                        data['name'],
                        data['types'][0]['type']['name'],
                        random.randint(1, 100),  # Random level
                        data['stats'][1]['base_stat'],  # Attack
                        data['stats'][2]['base_stat'],  # Defense
                        data['stats'][5]['base_stat']   # Speed
                    )
                    cur.execute("INSERT INTO pokemons (id, name, type, level, attack, defense, speed) VALUES (?, ?, ?, ?, ?, ?, ?)", poke_data)
                    conn.commit()
                    print("Inserted:", poke_data)
except Exception as e:
    print(f"Error creating table: {e} Maybe it already exists.")


pokemon_list = []

def get_all_pokemons():
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pokemons")
        rows = cursor.fetchall()
        pokemons = [Pokemon(data=row) for row in rows]
        return pokemons

@app.route('/')
def home():
    return render_template('game.html')

@app.route("/get_random_pokemon", methods=['GET'])
def get_random_pokemon():
    return random.choice(pokemons).__json__

@app.route("/sounds/<name>", methods=['GET'])
def sounds(name):
    return send_from_directory('static/sounds', name)
@app.route("/combat/<p1_id>/<p2_id>/<attack_type>", methods=['GET'])
def combat(p1_id, p2_id, attack_type):
    p1 = next((p for p in pokemons if str(p.id) == p1_id), None)
    p2 = next((p for p in pokemons if str(p.id) == p2_id), None)
    if not p1 or not p2:
        return {"error": "One or both Pokemon not found"}, 404

    attack_types = ["attack", "defense", "speed", "hp"]
    if attack_type not in attack_types:
        return {"error": "Invalid attack type"}, 400
    p1_score = getattr(p1, attack_type)
    p2_score = getattr(p2, attack_type)
    winner = p1 if p1_score >= p2_score else p2

    return {
        "winner_id": winner.id,
    }


if __name__ == '__main__':
    pokemons = get_all_pokemons()
    pokemon_list = [str(pokemon) for pokemon in pokemons]
    app.run(debug=True, port=80, host="0.0.0.0")
