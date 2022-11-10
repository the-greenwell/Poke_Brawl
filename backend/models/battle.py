import random, json
from backend.models.pokemon import Pokemon
from flask import flash
from decimal import Decimal, ROUND_HALF_UP
from backend.config.mysqlconnection import connectToMySQL

class Battle:

    def __init__(self, data):
        self.battle_id = data.get('battle_id', str(id(self)))
        self.challenger = data['challenger']
        self.opponent = data['opponent']
        self.past_turns = data['past_turns']
        self.first_turn = data.get('first_turn', self.__check_speed())
        self.cur_turn = data.get('cur_turn', self.first_turn)
        self.winner = data.get('winner', '')

    def __check_speed(self):
        if self.challenger['cur_stats']['speed']['value'] < self.opponent['cur_stats']['speed']['value']:
            return 'opponent'
        return 'challenger'

    def take_turn(self, move):
        if self.winner != '':
            return
        if self.first_turn == None:
            self.first_turn = self.__check_speed()
            # if self.cur_turn == 'challenger':
        print(self.cur_turn)
        move = self.challenger['moves'][move]
        if move['damage_class'] == 'status':
            if move['target'] == 'user':
                self.__stat_set(self.challenger,move)
            else:
                self.__stat_set(self.opponent,move)
            self.cur_turn = 'opponent'
            self.__update_battle()
            return
        dmg = self.__damage_formula(self.challenger, self.opponent, move)
        self.cur_turn = 'opponent'
        new = self.__update_battle()
            # else:
            #     dmg = self.__ai_attack()
            #     print(dmg)
            #     # if self.__hp_set(self.challenger,dmg):
            #     #     self.winner = self.opponent['name']

    @staticmethod
    def __accuracy_check(move):
        chance = random.randrange(0,101)
        if chance >= move['accuracy']:
            return False
        return True

    def __stat_set(self, target, move):
        changes = {}
        for change in move['stat_changes']:
            changes[change['stat']['name']] = change['change']
        for stat in changes:
            target['cur_stats'][stat]['value'] += changes[stat]

    def __hp_set(self, target, total):
        if target == 'challenger':
            if self.challenger['cur_stats']['hp']['value'] + total <= 0:
                self.challenger['cur_stats']['hp']['value'] = 0
                self.winner = self.opponent['name']
                self.past_turns.append(f'{self.winner} has won!')
            else:
                self.challenger['cur_stats']['hp']['value'] += total
        else:
            if self.opponent['cur_stats']['hp']['value'] + total <= 0:
                self.opponent['cur_stats']['hp']['value'] = 0
                self.winner = self.challenger['name']
                self.past_turns.append(f'{self.winner} has won!')
            else:
                self.opponent['cur_stats']['hp']['value'] += total
        print(total, self.opponent['cur_stats']['hp']['value'])
        return False

    def __damage_formula(self, attacker, defender, move):
        if move['damage_class'] == 'physical':
            attack = attacker['cur_stats']['attack']['value']
            defense = defender['cur_stats']['defense']['value']
        else:
            attack = attacker['cur_stats']['special-attack']['value']
            defense = defender['cur_stats']['special-defense']['value']
        stab = 1
        if move['type'] in attacker['types']:
            stab = 1.5
        dmg = (((((2*1/5)+2)* move['power'] * ( attack / defense )) / 50 ) + 2 ) * (random.uniform(0.84, 1.01)) * Battle.__crit_calc() * stab * Battle.__type_strengths(move['type'], defender['types'][0])
        dmg = round(dmg,1)
        if move['drain'] > 0 or move['drain'] < 0:
            drain = dmg * (move['drain'] * .01)
            self.__hp_set(attacker,drain)
        self.__hp_set(defender,dmg * -1)
        self.past_turns.append({'attacker': attacker['name'], 'defender': defender['name'], 'move': move['name'], 'dmg': dmg})
        return dmg

    def __ailment_formula(self,move):
        ailment_chance = move['ailment_chance']
        ailment_name = move['ailment_name']
        if ailment_name != 'none' and ailment_chance == 0:
            ailment_chance = 100
        chance = random.randrange(0,100)
        turns = {''}
        if chance <= ailment_chance:
            pass

    def serialize(self):
        json_data = {
                "battle_id": self.battle_id,
                "challenger": json.dumps(self.challenger),
                "opponent": json.dumps(self.opponent),
                "past_turns": json.dumps(self.past_turns),
                "first_turn": self.first_turn,
                "cur_turn": self.cur_turn,
                "winner": self.winner
        }
        return json_data

    def __ai_attack(self):
        # print(self.opponent['moves'])
        moves = self.opponent['moves'].keys()
        ai_move = random.sample(moves,1)
        if self.opponent['moves'][ai_move[0]]['damage_class'] == 'status':
            self.__stat_set(self.challenger,self.opponent['moves'][ai_move[0]])
            self.cur_turn = 'challenger'
            return 0
        dmg = self.__damage_formula(self.opponent, self.challenger, self.opponent['moves'][ai_move[0]])
        self.past_turns.append(f"{self.opponent['name']} attacked {self.challenger['name']} with {self.opponent['moves'][ai_move[0]]['name']}, dealing {dmg} damage!")
        return dmg

    @staticmethod
    def __crit_calc():
        chance = random.uniform(0, 1)
        if chance <= 0.17:
            return 1.5
        return 1

    @staticmethod
    def __type_strengths(type1, type2):
        type_dict = {
                    'normal':   { 'normal': 1, 'fire': 1,   'water': 1,      'electric': 1,    'grass': 1,     'ice': 1, 'fighting': 1, 'poison': 1, 'ground': 1, 'flying': 1, 'psychic': 1, 'bug': 1, 'rock': 0.5, 'ghost': 0, 'dragon': 1, 'dark': 1, 'steel': 0.5, 'fairy': 1},
                    'fire':     { 'normal': 1, 'fire': 0.5, 'water': 0.5,    'electric': 1,    'grass': 2,     'ice': 2, 'fighting': 1, 'poison': 1, 'ground': 1, 'flying': 1, 'psychic': 1, 'bug': 2, 'rock': 0.5, 'ghost': 1, 'dragon': 0.5, 'dark': 1, 'steel': 2, 'fairy': 1 },
                    'water':    { 'normal': 1, 'fire': 2,   'water': 0.5,    'electric': 1,    'grass': 0.5,   'ice': 1, 'fighting': 1, 'poison': 1, 'ground': 2, 'flying': 1, 'psychic': 1, 'bug': 1, 'rock': 2, 'ghost': 1, 'dragon': 0.5, 'dark': 1, 'steel': 1, 'fairy': 1 },
                    'electric': { 'normal': 1, 'fire': 1,   'water': 2,      'electric': 0.5,  'grass': 0.5,   'ice': 1, 'fighting': 1, 'poison': 1, 'ground': 0, 'flying': 2, 'psychic': 1, 'bug': 1, 'rock': 1, 'ghost': 1, 'dragon': 0.5, 'dark': 1, 'steel': 1, 'fairy': 1 },
                    'grass':    { 'normal': 1, 'fire': 0.5, 'water': 2,      'electric': 1,    'grass': 0.5,   'ice': 1, 'fighting': 1, 'poison': 0.5, 'ground': 2, 'flying': 0.5, 'psychic': 1, 'bug': 0.5, 'rock': 2, 'ghost': 1, 'dragon': 0.5, 'dark': 1, 'steel': 0.5, 'fairy': 1 },
                    'ice':      { 'normal': 1, 'fire': 0.5, 'water': 0.5,    'electric': 1,    'grass': 2,     'ice': 0.5,'fighting': 1, 'poison': 1, 'ground': 2, 'flying': 2, 'psychic': 1, 'bug': 1, 'rock': 1, 'ghost': 1, 'dragon': 2, 'dark': 1, 'steel': 0.5, 'fairy': 1 },
                    'fighting': { 'normal': 2, 'fire': 1,   'water': 1,      'electric': 1,    'grass': 1,     'ice': 2, 'fighting': 1, 'poison': 0.5, 'ground': 1, 'flying': 0.5, 'psychic': 0.5, 'bug': 0.5, 'rock': 2, 'ghost': 0, 'dragon': 1, 'dark': 2, 'steel': 2, 'fairy': 0.5 },
                    'poison':   { 'normal': 1, 'fire': 1,   'water': 1,      'electric': 1,    'grass': 2,     'ice': 1, 'fighting': 1, 'poison': 0.5, 'ground': 0.5, 'flying': 1, 'psychic': 1, 'bug': 1, 'rock': 0.5, 'ghost': 0.5, 'dragon': 1, 'dark': 1, 'steel': 0, 'fairy': 2 },
                    'ground':   { 'normal': 1, 'fire': 2,   'water': 1,      'electric': 2,    'grass': 0.5,   'ice': 1, 'fighting': 1, 'poison': 2, 'ground': 1, 'flying': 0, 'psychic': 1, 'bug': 0.5, 'rock': 2, 'ghost': 1, 'dragon': 1, 'dark': 1, 'steel': 2, 'fairy': 1 },
                    'flying':   { 'normal': 1, 'fire': 1,   'water': 1,      'electric': 0.5,  'grass': 2,     'ice': 1, 'fighting': 2, 'poison': 1, 'ground': 1, 'flying': 1, 'psychic': 1, 'bug': 2, 'rock': 0.5, 'ghost': 1, 'dragon': 1, 'dark': 1, 'steel': 0.5, 'fairy': 1 },
                    'psychic':  { 'normal': 1, 'fire': 1,   'water': 1,      'electric': 1,    'grass': 1,     'ice': 1, 'fighting': 2, 'poison': 2, 'ground': 1, 'flying': 1, 'psychic': 0.5, 'bug': 1, 'rock': 1, 'ghost': 1, 'dragon': 1, 'dark': 0, 'steel': 0.5, 'fairy': 1 },
                    'bug':      { 'normal': 1, 'fire': 0.5, 'water': 1,      'electric': 1,    'grass': 2,     'ice': 1, 'fighting': 0.5, 'poison': 0.5, 'ground': 1, 'flying': 0.5, 'psychic': 2, 'bug': 1, 'rock': 1, 'ghost': 0.5, 'dragon': 1, 'dark': 2, 'steel': 0.5, 'fairy': 0.5 },
                    'rock':     { 'normal': 1, 'fire': 2,   'water': 1,      'electric': 1,    'grass': 1,     'ice': 2, 'fighting': 0.5, 'poison': 1, 'ground': 0.5, 'flying': 2, 'psychic': 1, 'bug': 2, 'rock': 1, 'ghost': 1, 'dragon': 1, 'dark': 1, 'steel': 0.5, 'fairy': 1 },
                    'ghost':    { 'normal': 0, 'fire': 1,   'water': 1,      'electric': 1,    'grass': 1,     'ice': 1, 'fighting': 1, 'poison': 1, 'ground': 1, 'flying': 1, 'psychic': 2, 'bug': 1, 'rock': 1, 'ghost': 2, 'dragon': 1, 'dark': 0.5, 'steel': 1, 'fairy': 1 },
                    'dragon':   { 'normal': 1, 'fire': 1,   'water': 1,      'electric': 1,    'grass': 1,     'ice': 1, 'fighting': 1, 'poison': 1, 'ground': 1, 'flying': 1, 'psychic': 1, 'bug': 1, 'rock': 1, 'ghost': 1, 'dragon': 2, 'dark': 1, 'steel': 0.5, 'fairy': 0 },
                    'dark':     { 'normal': 1, 'fire': 1,   'water': 1,      'electric': 1,    'grass': 1,     'ice': 1, 'fighting': 0.5, 'poison': 1, 'ground': 1, 'flying': 1, 'psychic': 2, 'bug': 1, 'rock': 1, 'ghost': 2, 'dragon': 1, 'dark': 0.5, 'steel': 1, 'fairy': 0.5 },
                    'steel':    { 'normal': 1, 'fire': 0.5, 'water': 0.5,    'electric': 0.5,  'grass': 1,     'ice': 2, 'fighting': 1, 'poison': 1, 'ground': 1, 'flying': 1, 'psychic': 1, 'bug': 1, 'rock': 2, 'ghost': 1, 'dragon': 1, 'dark': 1, 'steel': 0.5, 'fairy': 2 },
                    'fairy':    { 'normal': 1, 'fire': 0.5, 'water': 1,      'electric': 1,    'grass': 1,     'ice': 1, 'fighting': 2, 'poison': 0.5, 'ground': 1, 'flying': 1, 'psychic': 1, 'bug': 1, 'rock': 1, 'ghost': 1, 'dragon': 2, 'dark': 2, 'steel': 0.5, 'fairy': 1 }
                }
        #return value from type graph
        return type_dict[type1][type2]


    @classmethod
    def save_battle(cls,data):
        query = 'INSERT INTO battles (battle_id, challenger, opponent, past_turns, first_turn, cur_turn) VALUES (%(battle_id)s,%(challenger)s,%(opponent)s,%(past_turns)s,%(first_turn)s,%(cur_turn)s);'
        return connectToMySQL('poke-brawls').query_db(query,data)

    @classmethod
    def get_battle(cls,data):
        bid = data['bid']
        query = "SELECT * FROM battles WHERE battle_id = %(bid)s"
        result = connectToMySQL('poke-brawls').query_db(query, data)
        if len(result) < 1:
            return False
        data = { 'challenger' : json.loads(result[0]['challenger']), 'opponent': json.loads(result[0]['opponent']), 'past_turns': json.loads(result[0]['past_turns']), 'battle_id': bid }
        return cls(data)

    def __update_battle(self):
        data = self.serialize()
        query = 'UPDATE battles SET battle_id=%(battle_id)s, challenger=%(challenger)s, opponent=%(opponent)s, past_turns=%(past_turns)s, first_turn=%(first_turn)s, cur_turn=%(cur_turn)s WHERE battle_id=%(battle_id)s'
        return connectToMySQL('poke-brawls').query_db(query,data)