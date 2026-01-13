# game_engine.py
from cyber_attack_simulator.game_state import GameState

class CyberAttackEngine:
    """Moteur principal du simulateur de cyber attaque"""

    def __init__(self):
        self.game_state = GameState()
        self.handlers = {}
        self.command_metadata = {}  # Pour stocker les noms de paramètres
        self.command_history = []
        self.detection_level = 0.0
        self.flags = set()

    def register_command_metadata(self, command_name: str, params: list):
        """Enregistre les métadonnées (comme les noms de paramètres) pour une commande."""
        self.command_metadata[command_name] = params

    def register_handler(self, command_name: str, handler):
        """Enregistre un nouveau handler de commande"""
        self.handlers[command_name] = handler

    def execute_command(self, command: str, params: dict) -> dict:
        """Exécute une commande et retourne les résultats."""
        handler = self.handlers.get(command)

        if not handler:
            return {"success": False, "output": f"❌ Commande '{command}' non reconnue."}

        self.command_history.append({"command": command, "params": params})

        # Le handler lui-même est la fonction à appeler, enregistrée via `register_handler`
        try:
            result = handler(params)
        except Exception as e:
            return {"success": False, "output": f"❌ Erreur critique lors de l'exécution de '{command}': {e}"}

        # Mise à jour de l'état du jeu avec les résultats
        if result.get("success"):
            if "new_state" in result and isinstance(result["new_state"], dict):
                self.game_state.update_state(result["new_state"])

            if "flags" in result and isinstance(result["flags"], list):
                for flag in result["flags"]:
                    self.add_flag(flag)

            # Mise à jour du niveau de détection (placeholder)
            # risk = RiskCalculator.calculate_detection_risk(command, params)
            # self.update_detection(risk)

        return result

    def update_detection(self, risk: float):
        """Met à jour le niveau de détection"""
        pass

    def add_flag(self, flag: str):
        """Ajoute un flag au joueur"""
        self.flags.add(flag)
