import random
# import copy
from threading import Lock


class SingletonMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances or args or kwargs:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class GameTI(metaclass=SingletonMeta):
    def __init__(self, size=10):
        self.size = size
        self.koord_klad = []
        self.koord_hero = []
        self.koord_pirat = []
        self.koord_pirat_old = []
        self.karta = [[0 for _ in range(size)] for _ in range(size)]
        self.count = 0

        self.karta_ins_klad() # размещаем клад на карте

        self.karta_ins_pirat() # размещаем пиратов на карте
        if self.it_is_klad(self.koord_pirat[0], self.koord_pirat[1]):
            # Если при размещении пиратов на карте они совпали с размещением клада, удаляем пиратов и размещаем заново
            self.karta_del_pirat()
            self.karta_ins_pirat()

        self.karta_ins_hero() # размещаем героя на карте
        if self.it_is_klad(self.koord_hero[0], self.koord_hero[1]) or \
                self.it_is_pirat(self.koord_hero[0], self.koord_hero[1]):
            # Если при размещении героя на карте он совпал с размещением пиратов или клада, удаляем героя и размещаем заново
            self.karta_del_hero()
            self.karta_ins_hero()

    def karta_ins_klad(self):
        i = random.randint(0, self.size - 1)
        j = random.randint(0, self.size - 1)
        self.karta[i][j] = 1
        self.koord_klad = [i, j]

    def karta_ins_hero(self):
        i = random.randint(0, self.size - 1)
        j = random.randint(0, self.size - 1)
        self.karta[i][j] = 3
        self.koord_hero = [i, j]

    def karta_del_hero(self):
        if len(self.koord_hero) >= 2:
            self.karta[self.koord_hero[0]][self.koord_hero[1]] = 0
        self.koord_hero.clear()

    def karta_ins_pirat(self):
        i = random.randint(0, self.size - 1)
        j = random.randint(0, self.size - 1)
        self.karta[i][j] = 2
        self.koord_pirat = [i, j]

    def karta_del_pirat(self):
        if len(self.koord_pirat) >= 2:
            self.karta[self.koord_pirat[0]][self.koord_pirat[1]] = 4
            if len(self.koord_pirat_old) >= 2:
                self.karta[self.koord_pirat_old[0]][self.koord_pirat_old[1]] = 0
        self.koord_pirat_old.clear()
        self.koord_pirat_old = [self.koord_pirat[0], self.koord_pirat[1]]
        self.koord_pirat.clear()

    def it_is_klad(self, i, j):
        if self.koord_klad[0] == i and self.koord_klad[1] == j:
            return True
        else:
            return False

    def it_is_pirat(self, i, j):
        if self.koord_pirat[0] == i and self.koord_pirat[1] == j:
            return True
        else:
            return False

    def go_hero_go(self, direction, steps):
        res = []
        if direction == 1 or direction == 2:
            j = self.koord_hero[1]
            if direction == 1:
                mess = 'Вы дошли до края острова. Двигаться на север больше нельзя, океан кишит акулами'
                predel = 0
                start = self.koord_hero[0] - 1
                stop = self.koord_hero[0] - steps - 1
                shag = -1
            elif direction == 2:
                mess = 'Вы дошли до края острова. Двигаться на юг больше нельзя, впереди крутой обрыв'
                predel = self.size - 1
                start = self.koord_hero[0] + 1
                stop = self.koord_hero[0] + steps + 1
                shag = 1

            if self.koord_hero[0] == predel:
                res = [1, mess]
                i = predel
            else:
                for i in range(start, stop, shag):
                    if i == predel:
                        res = [1, mess]
                        break
                    else:
                        if self.it_is_klad(i, j):
                            res = [2, 'Урааааа!!!!! Поздравляем, Вы нашли клад!']
                            break
                        elif self.it_is_pirat(i, j):
                            res = [3, 'Вам не повезло, Вы набрели на лагерь пиратов. Мы уверены, что в следующий раз удача будет на Вашей стороне.']
                            break
        elif direction == 3 or direction == 4:
            i = self.koord_hero[0]
            if direction == 3:
                mess = 'Вы дошли до края острова. Двигаться на запад больше нельзя, у берега стоит пиратский корабль'
                predel = 0
                start = self.koord_hero[1] - 1
                stop = self.koord_hero[1] - steps - 1
                shag = -1
            elif direction == 4:
                mess = 'Вы дошли до края острова. Двигаться на восток больше нельзя, в океане шторм'
                predel = self.size - 1
                start = self.koord_hero[1] + 1
                stop = self.koord_hero[1] + steps + 1
                shag = 1

            if self.koord_hero[1] == predel:
                res = [1, mess]
                j = predel
            else:
                for j in range(start, stop, shag):
                    if j == predel:
                        res = [1, mess]
                        break
                    else:
                        if self.it_is_klad(i, j):
                            res = [2, 'Урааааа!!!!! Поздравляем, Вы нашли клад!']
                            break
                        elif self.it_is_pirat(i, j):
                            res = [3, 'Вам не повезло, Вы набрели на лагерь пиратов. Мы уверены, что в следующий раз удача будет на Вашей стороне.']
                            break


        if direction == 1:
            if i < predel:
                i = predel
        elif direction == 2:
            if i > predel:
                i = predel
        elif direction == 3:
            if j < predel:
                j = predel
        elif direction == 4:
            if j > predel:
                j = predel
        self.karta_del_hero()
        self.karta[i][j] = 3
        self.koord_hero = [i, j]


        return res

