# game_state.py
class GameState:
    """État du jeu du joueur"""

    def __init__(self):
        self.player_name = "Anonyme"
        self.level = 1
        self.experience = 0
        self.credits = 1000
        self.unlocked_commands = set()
        self.discovered_targets = {}
        self.scan_history = []
        self.active_alerts = []
        self.stealth_level = 1.0

    def add_experience(self, xp: int):
        """Ajoute de l'expérience au joueur"""
        pass

    def unlock_command(self, command: str):
        """Débloque une nouvelle commande"""
        pass

    def update_state(self, data: dict):
        """Met à jour l'état du jeu de manière contrôlée."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                # Empêche l'ajout d'attributs non définis
                print(f"⚠️ Avertissement: Tentative de mise à jour d'un attribut d'état inconnu: {key}")
