import requests, requests_cache, json


requests_cache.install_cache('poke_cache', backend='sqlite', expire_after=2592000)

class Move:
    def __init__(self,data):
        self.id = data['id']
        self.accuracy = data['accuracy']
        self.power = data['power']
        self.damage_class = data['damage_class']['name']
        self.name = self.__format_name(data['name'])
        self.ailment = data['meta']['ailment']['name']
        self.ailment_chance = data['meta']['ailment_chance']
        self.category = data['meta']['category']['name']
        self.crit_rate = data['meta']['crit_rate']
        self.drain = data['meta']['drain']
        self.flinch_chance = data['meta']['flinch_chance']
        self.min_hits = data['meta']['min_hits']
        self.max_hits = data['meta']['max_hits']
        self.priority = data['priority']
        self.stat_changes = data['stat_changes']
        self.type = data['type']['name']
        self.target = data['target']['name']

    @classmethod
    def new_move(cls,data):
        url = 'https://pokeapi.co/api/v2/move/'
        url += data
        res = requests.get(url)
        move = Move(res.json())
        print(f"from cache? {res.from_cache}")
        return json.loads(move.serialize())

    def __format_name(self,move):
        return move.replace("-", " ")

    def serialize(self):
        json_data = {
                "id": self.id,
                "accuracy": self.accuracy,
                "power": self.power,
                "damage_class": self.damage_class,
                "name": self.name,
                "ailment": self.ailment,
                "ailment_chance": self.ailment_chance,
                "category": self.category,
                "crit_rate": self.crit_rate,
                "drain": self.drain,
                "flinch_chance": self.flinch_chance,
                "min_hits": self.min_hits,
                "max_hits": self.max_hits,
                "priority": self.priority,
                "type": self.type,
                "target": self.target, 
                "stat_changes": self.stat_changes
            }
        return json.dumps(json_data)