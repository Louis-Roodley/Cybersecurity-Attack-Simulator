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
        self.experience += xp
        # Logique de montée de niveau simple
        if self.experience >= self.level * 100:
            self.level += 1
            print(f"🎉 Niveau supérieur! Vous êtes maintenant niveau {self.level}")

    def unlock_command(self, command: str):
        """Débloque une nouvelle commande"""
        if command not in self.unlocked_commands:
            self.unlocked_commands.add(command)
            print(f"🔓 Nouvelle commande débloquée: {command}")

    def update_state(self, new_state: dict):
        """Met à jour l'état du jeu de manière contrôlée."""
        for key, value in new_state.items():
            if hasattr(self, key):
                # Pour l'instant, nous mettons directement à jour.
                # On pourrait ajouter de la logique de validation ici.
                setattr(self, key, value)
            else:
                print(f"⚠️ Tentative de mise à jour d'un attribut d'état inconnu: {key}")
