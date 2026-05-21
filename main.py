from services.data_loader import load_game_data
from services.analyzer import Analyzer

def main():
    analyzer = Analyzer()
    raw_json = load_game_data("data.json")
    analyzer.process_data(raw_json)

    print("Game analyzer v0.1 ")

    print("\n -- Leaderboard -- ")
    leaderboard = analyzer.get_leaderboard()

    rank = 1

    for p in leaderboard:
        line = str(rank) + ". " + p.name + " | Total: " + str(p.get_total_score()) + " | Tier: " + p.get_player_tier()
        print(line)
        rank += 1

if __name__ == "__main__":
    main()