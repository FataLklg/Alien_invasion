from utils import read_record_from_file


class GameStats():
    """Отслеживание статистики для игры Alien Invasion."""
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        self.high_score = read_record_from_file()

        # Игра Alien Invasion запускается в неактивном состоянии.
        self.game_active = False
    
    def reset_stats(self):
        """Инициализирует статистику, изменяющуяся в ходе игры."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
