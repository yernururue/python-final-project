class Stat:
    def __init__(self, date, score):
        self._date = date
        self._score = score
    
    def get_date(self):
        return self._date
    def get_score(self):
        return self._score

class Player:
    def __init__(self, name):
        self.name = name
        self.stats = []

    def add_stat(self, stat):
        self.stats.append(stat)

    def get_total_score(self):
        total_score = 0
        for score in self.stats:
            total_score += score.get_score()
        return total_score

    def get_average_score(self):
        average_score = 0.0

        if not self.stats:
            return 0
        else:
            average_score = self.get_total_score()/len(self.stats)
        return average_score
    
    def get_player_tier(self):
        return "Standard"


class ProPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
        

    def get_player_tier(self):
        return "Pro Player"

class BeginnerPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

    def get_player_tier(self):
        return "Beginner player"
