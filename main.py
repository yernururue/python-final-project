from services.data_loader import load_game_data
from services.analyzer import Analyzer
import re

def valid_date(date_string):
    variant = r"^\d{4}-\d{2}-\d{2}$" #YYYY-DD-MM format separated with line. Regex Validator(check)
    if re.match(variant, date_string):
        return True
    else:
        return False

def main():
    analyzer = Analyzer()
    raw_json = load_game_data("data.json")
    analyzer.process_data(raw_json)

    print("Game analyzer v1.0 ")

    print("\n -- Leaderboard -- ") #Leaderboard done
    leaderboard = analyzer.get_leaderboard()

    rank = 1

    for p in leaderboard:
        avg = round(p.get_average_score(), 1)
        line = (
                str(rank) + ". " + p.name +
                " | Total: " + str(p.get_total_score()) +
                " | Average score: " + str(avg) + # Average score of each player done
                " | Tier: " + p.get_player_tier()
                )
        print(line)
        rank += 1

    print("\n -- Daily Best performances -- ") #Daily best performance done
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