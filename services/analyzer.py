from models.player import Player, ProPlayer, BeginnerPlayer, Stat

class Analyzer:
    def __init__(self):
        self.players = {}
        self.stats = {}

    def process_data(self, raw_data):
        for entry in raw_data:
            name = entry['player']
            score = entry['score']
            date = entry['date']

            if name not in self.players:
                if score >= 150:
                    self.players[name] = ProPlayer(name)
                elif score >= 100:
                    self.players[name] = BeginnerPlayer(name)
                else:
                    self.players[name] = Player(name)

            new_stat = Stat(date, score)
            self.players[name].add_stat(new_stat)

    def get_leaderboard(self):
        player_list = list(self.players.values())
        return sorted(
            player_list,
            key=lambda p: p.get_total_score(),
            reverse=True
            )

