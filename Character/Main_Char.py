import numpy as np


class Mortal:
    "Must use first name to create mortal beings"
    def __init__(self, *, fname, mname = "", lname = ""):
        self.fname = fname
        self.mname = mname
        self.lname = lname

class Enemy(Mortal) :

    def __init__(self, type = '', *, actions = [], attributes = [10, 10, 10], items = [],health = 0, max_health = 0, level = 0, drops = [], dps = 0, **kwargs):
        super().__init__(**kwargs)
        self.type = type
        self.strg, self.agil, self.intel = [element + (level * 0.15 * element) for element in attributes]
        self.items = items
        self.health = health
        self.max_health = max_health
        self.drops = drops
        self.level = level
        self.actions = actions
        self.dps = dps
        if self.max_health == 0 :
            self.max_health = self.strg * 500 + self.permanent_buff(strg = self.items)
            self.health = self.max_health
        
    

    # Item
    def item_multiplier(self, value) :
        pass


    # Mechanical modifier
    def stun(self, value) :
        pass
    def criticalAttk(self) :
        pass
    def damagePerSec(self) :
        pass

    #
    def restore_health(self) :
        self.health = self.max_health
    def attacked(self, value) :
        self.health -= value
        if self.health <= 0 :
            self.health = 0
            return (f"{self.fname} keluar dari perang karena HP habis")
        return (f"{self.fname} Terkena serangan sebesar {value} nyawanya tinggal {self.health}")

    def permanent_buff(self, **kwargs) :
        return 0


    def action(self, dps_damage) :
        if dps_damage == 0 : 
            choose = np.random.choice(self.actions, p = [float(a.split()[-1]) for a in self.actions])
        else :
            chance_dps = float(self.actions[[i for i, s in enumerate(self.actions) if 'dps' in s.lower()][0]].split()[-1])
            chance_attack = float(self.actions[[i for i, s in enumerate(self.actions) if 'attack' in s.lower()][0]].split()[-1])
            #        Menghilangkan value dps dari list
            no_dps = [x for i,x in enumerate(self.actions) if 'dps' not in x.lower()]
            no_dps[[i for i, s in enumerate(no_dps) if 'attack' in s.lower()][0]] = f'Attack {chance_dps + chance_attack}'
            choose = np.random.choice(no_dps, p = [float(a.split()[-1]) for a in no_dps])

        return choose

    def damage_output(self,) :
        return self.strg * 200

class Adventurer(Enemy) :
    def __init__(self, *, stage = 0, strg = 10, agil = 10, intel = 10, type = 'Human', **kwargs):
        super().__init__(**kwargs)
        self.strg = strg
        self.agil = agil
        self.intel = intel
        self.stage = stage
        self.type = type