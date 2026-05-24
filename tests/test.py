import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main import valid_date
from models.player import Stat, Player, ProPlayer, BeginnerPlayer
from services.analyzer import Analyzer


class TestValidDate(unittest.TestCase):
    def test_valid_date(self):
        self.assertTrue(valid_date("2026-01-15"))

    def test_valid_date_end_of_year(self):
        self.assertTrue(valid_date("2024-12-31"))

    def test_invalid_date_wrong_separator(self):
        self.assertFalse(valid_date("2026/01/15"))

    def test_invalid_date_wrong_order(self):
        self.assertFalse(valid_date("15-01-2026"))

    def test_invalid_date_empty(self):
        self.assertFalse(valid_date(""))

    def test_invalid_date_partial(self):
        self.assertFalse(valid_date("2026-01"))

    def test_invalid_date_letters(self):
        self.assertFalse(valid_date("abcd-ef-gh"))


class TestStat(unittest.TestCase):
    def setUp(self):
        self.stat = Stat("2026-01-01", 120)

    def test_get_date(self):
        self.assertEqual(self.stat.get_date(), "2026-01-01")

    def test_get_score(self):
        self.assertEqual(self.stat.get_score(), 120)


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player("Alice")

    def test_initial_stats_empty(self):
        self.assertEqual(self.player.stats, [])

    def test_add_stat(self):
        self.player.add_stat(Stat("2026-01-01", 100))
        self.assertEqual(len(self.player.stats), 1)

    def test_get_total_score(self):
        self.player.add_stat(Stat("2026-01-01", 100))
        self.player.add_stat(Stat("2026-01-02", 200))
        self.assertEqual(self.player.get_total_score(), 300)

    def test_get_total_score_empty(self):
        self.assertEqual(self.player.get_total_score(), 0)

    def test_get_average_score(self):
        self.player.add_stat(Stat("2026-01-01", 100))
        self.player.add_stat(Stat("2026-01-02", 200))
        self.assertAlmostEqual(self.player.get_average_score(), 150.0)

    def test_get_average_score_empty(self):
        self.assertEqual(self.player.get_average_score(), 0)

    def test_get_player_tier_standard(self):
        self.assertEqual(self.player.get_player_tier(), "Standard")


class TestProPlayer(unittest.TestCase):
    def test_get_player_tier(self):
        p = ProPlayer("Bob")
        self.assertEqual(p.get_player_tier(), "Pro Player")

    def test_inherits_stats(self):
        p = ProPlayer("Bob")
        p.add_stat(Stat("2026-01-01", 200))
        self.assertEqual(p.get_total_score(), 200)


class TestBeginnerPlayer(unittest.TestCase):
    def test_get_player_tier(self):
        p = BeginnerPlayer("Charlie")
        self.assertEqual(p.get_player_tier(), "Beginner player")

    def test_inherits_stats(self):
        p = BeginnerPlayer("Charlie")
        p.add_stat(Stat("2026-01-01", 50))
        self.assertEqual(p.get_total_score(), 50)


class TestAnalyzerProcessData(unittest.TestCase):
    def setUp(self):
        self.analyzer = Analyzer()

    def test_pro_player_classified_correctly(self):
        self.analyzer.process_data([{"player": "Bob", "score": 150, "date": "2026-01-01"}])
        self.assertIsInstance(self.analyzer.players["Bob"], ProPlayer)

    def test_beginner_player_classified_correctly(self):
        self.analyzer.process_data([{"player": "Charlie", "score": 80, "date": "2026-01-01"}])
        self.assertIsInstance(self.analyzer.players["Charlie"], BeginnerPlayer)

    def test_standard_player_classified_correctly(self):
        self.analyzer.process_data([{"player": "Alice", "score": 120, "date": "2026-01-01"}])
        self.assertIsInstance(self.analyzer.players["Alice"], Player)
        self.assertNotIsInstance(self.analyzer.players["Alice"], ProPlayer)
        self.assertNotIsInstance(self.analyzer.players["Alice"], BeginnerPlayer)

    def test_tier_based_on_first_score_only(self):
        # Alice first appears with 120 (Standard), then scores 200 — should stay Standard
        self.analyzer.process_data([
            {"player": "Alice", "score": 120, "date": "2026-01-01"},
            {"player": "Alice", "score": 200, "date": "2026-01-02"},
        ])
        self.assertNotIsInstance(self.analyzer.players["Alice"], ProPlayer)

    def test_multiple_stats_added(self):
        self.analyzer.process_data([
            {"player": "Alice", "score": 120, "date": "2026-01-01"},
            {"player": "Alice", "score": 180, "date": "2026-01-02"},
        ])
        self.assertEqual(len(self.analyzer.players["Alice"].stats), 2)

    def test_multiple_players(self):
        self.analyzer.process_data([
            {"player": "Alice", "score": 120, "date": "2026-01-01"},
            {"player": "Bob", "score": 150, "date": "2026-01-01"},
        ])
        self.assertIn("Alice", self.analyzer.players)
        self.assertIn("Bob", self.analyzer.players)


class TestAnalyzerLeaderboard(unittest.TestCase):
    def setUp(self):
        self.analyzer = Analyzer()
        self.analyzer.process_data([
            {"player": "Alice", "score": 120, "date": "2026-01-01"},
            {"player": "Bob", "score": 150, "date": "2026-01-01"},
            {"player": "Alice", "score": 180, "date": "2026-01-02"},
        ])

    def test_leaderboard_sorted_descending(self):
        board = self.analyzer.get_leaderboard()
        scores = [p.get_total_score() for p in board]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_leaderboard_top_is_alice(self):
        board = self.analyzer.get_leaderboard()
        self.assertEqual(board[0].name, "Alice")  # 300 total vs Bob's 150

    def test_leaderboard_length(self):
        board = self.analyzer.get_leaderboard()
        self.assertEqual(len(board), 2)


class TestAnalyzerBestDailyPerformance(unittest.TestCase):
    def setUp(self):
        self.analyzer = Analyzer()
        self.analyzer.process_data([
            {"player": "Alice", "score": 120, "date": "2026-01-01"},
            {"player": "Bob", "score": 150, "date": "2026-01-01"},
            {"player": "Alice", "score": 180, "date": "2026-01-02"},
        ])

    def test_daily_best_correct_winner(self):
        records = self.analyzer.get_best_daily_performance()
        # On 2026-01-01, Bob scored 150 vs Alice's 120
        self.assertEqual(records["2026-01-01"][0], "Bob")
        self.assertEqual(records["2026-01-01"][1], 150)

    def test_daily_best_single_player_day(self):
        records = self.analyzer.get_best_daily_performance()
        self.assertEqual(records["2026-01-02"][0], "Alice")
        self.assertEqual(records["2026-01-02"][1], 180)

    def test_daily_best_all_dates_present(self):
        records = self.analyzer.get_best_daily_performance()
        self.assertIn("2026-01-01", records)
        self.assertIn("2026-01-02", records)


class TestAnalyzerProPlayers(unittest.TestCase):
    def setUp(self):
        self.analyzer = Analyzer()
        self.analyzer.process_data([
            {"player": "Alice", "score": 120, "date": "2026-01-01"},
            {"player": "Bob", "score": 150, "date": "2026-01-01"},
            {"player": "Charlie", "score": 80, "date": "2026-01-01"},
        ])

    def test_only_pro_players_yielded(self):
        pros = list(self.analyzer.get_pro_players())
        self.assertEqual(len(pros), 1)
        self.assertEqual(pros[0].name, "Bob")

    def test_generator_type(self):
        import types
        self.assertIsInstance(self.analyzer.get_pro_players(), types.GeneratorType)

    def test_no_pro_players(self):
        analyzer = Analyzer()
        analyzer.process_data([{"player": "Alice", "score": 120, "date": "2026-01-01"}])
        pros = list(analyzer.get_pro_players())
        self.assertEqual(pros, [])


if __name__ == "__main__":
    unittest.main()
