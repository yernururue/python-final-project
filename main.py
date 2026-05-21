from services.data_loader import load_game_data
from services.analyzer import Analyzer
import re

def valid_date(date_string):
    variant = r"^\d{4}-\d{2}-\d{2}$"
    if re.match(variant, date_string):
        return True
    else:
        return False

def main():
    analyzer = Analyzer()
    raw_json = load_game_data("data.json")
    analyzer.process_data(raw_json)

    print("Game analyzer v0.5 ")

    print("\n -- Leaderboard -- ")
    leaderboard = analyzer.get_leaderboard()

    rank = 1

    for p in leaderboard:
        line = str(rank) + ". " + p.name + " | Total: " + str(p.get_total_score()) + " | Tier: " + p.get_player_tier()
        print(line)
        rank += 1

    print("\n -- Daily Best performances -- ")
    records = analyzer.get_best_daily_performance()

    for date in records:

        if valid_date(date):
            name = records[date][0]
            score = records[date][1]

            line = str(date) + ": " + name + " scored " + str(score) + " points"
            print(line)

        else:
            print("Invalid date" + str(date))

if __name__ == "__main__":
    main()