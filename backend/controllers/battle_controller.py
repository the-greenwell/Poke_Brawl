from backend import app
from backend.models.battle import Battle
from backend.models.pokemon import Pokemon

import json

from flask import render_template, redirect, request, session


@app.route('/reset')
def reset_pokemon():
    session.clear()
    return redirect('/')

@app.route('/battle')
def start_battle():
    if 'bid' not in session:
        challenger = Pokemon.generate_poke()
        opponent = Pokemon.generate_poke()
        data = {
            'challenger': json.loads(challenger.serialize()),
            'opponent': json.loads(opponent.serialize()),                             
            'past_turns': []
        }
        battle = Battle(data)
        Battle.save_battle(battle.serialize())
        session['bid'] = battle.serialize()['battle_id']
        return render_template('index.html', battle = battle)
    else:
        data = {'bid': session['bid'] }
        battle = Battle.get_battle(data)
        return render_template('index.html', battle = battle)


# will need to be websocket'd
@app.route('/attack', methods=['POST'])
def battle_phase():
    move = str(request.form['move'])
    data = {'bid': request.form['bid'] }
    battle = Battle.get_battle(data)
    battle.take_turn(move)
    return redirect('/battle')

@app.route('/winner')
def winner():
    pass