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

    def get_best_daily_performance(self):
        daily_best = {}

        for player in self.players.values():
            for stat in player.stats:
                date =stat.get_date()
                score = stat.get_score()

                if date in daily_best:
                    current_record = daily_best[date][1]
                    if score > current_record:
                        daily_best[date] = (player.name, score)

                else:
                    daily_best[date] = (player.name, score)

        return daily_best

