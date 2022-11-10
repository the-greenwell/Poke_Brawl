import random, requests, requests_cache, json
from backend.models.move import Move

from flask import session 

requests_cache.install_cache('poke_cache', backend='sqlite', expire_after=2592000)

class Pokemon:
    def __init__(self,data):
        self.name = data['name']
        self.id = data['id']
        self.types = self.__set_types(data['types'])
        self.moves = self.__get_moves(data['moves'])
        self.init_stats = self.__set_stats(data['stats'])
        self.cur_stats = self.init_stats
        self.sprite = self.__is_shiny(data['sprites'])
        self.last_attack = None
        self.last_defense = None
        self.shiny = False
        self.status = []

    def __set_types(self,data):
        types = []
        for i in data:
            types.append(i['type']['name'])
        return types

    def __get_moves(self, data):
        new_set = set()
        moves = {}
        y = None
        for i in data:
            for j in i['version_group_details']:
                if j['move_learn_method']['name'] == 'level-up' and j['version_group']['name'] == 'red-blue':
                    move = i['move']['name']
                    new_set.add(move)
        if len(new_set) > 4:
            y = random.sample(new_set, 4)
        else:
            y = new_set
        for x in y:
            cur = Move.new_move(x)
            moves[cur['id']] = cur
        return moves

    def __set_stats(self, data):
        stats = {}
        for i in data:
            stats[i['stat']['name']] = { 'value': i['base_stat'], 'effort': i['effort'] }
        return stats

    def __is_shiny(self, data):
        chance = random.randrange(0,4097)
        # chance = 69
        print(f'shiny chance: {chance}')
        if chance == 69:
            return data['front_shiny']
        return data['front_default']

    def serialize(self):
        json_data = {
            "name": self.name,
            "id": self.id,
            "types": self.types,
            "moves": self.moves,
            "init_stats": {
                'hp': self.init_stats['hp'],
                'defense': self.init_stats['defense'],
                'attack': self.init_stats['attack'],
                'special-attack': self.init_stats['special-attack'],
                'special-defense': self.init_stats['special-defense'],
                'speed': self.init_stats['speed']
            },
            "cur_stats": {
                'hp': self.cur_stats['hp'],
                'defense': self.cur_stats['defense'],
                'attack': self.cur_stats['attack'],
                'special-attack': self.cur_stats['special-attack'],
                'special-defense': self.cur_stats['special-defense'],
                'speed': self.cur_stats['speed']
            },
            "shiny": self.shiny,
            "sprite": self.sprite,
            "status": self.status
        }
        return json.dumps(json_data)

    @classmethod
    def generate_poke(cls, data = None):
        if data == None:
            id = random.randrange(0,152)
            url = 'https://pokeapi.co/api/v2/pokemon/'
            url += str(id)
            res = requests.get(url)
            pokemon = Pokemon(res.json())
        else:
            pokemon = Pokemon(data)
        return pokemon

    @classmethod
    def update_token(cls, token, updated):
        session[token] = updated
