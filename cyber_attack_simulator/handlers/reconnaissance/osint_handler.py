# handlers/reconnaissance/osint_handler.py
import time
import random

# --- Classe de base pour les Handlers OSINT ---
class BaseOSINTHandler:
    def __init__(self, engine):
        self.engine = engine
        self.config = {
            "query_time": 0.2,
            "detection_risk": 0.01,
            "success_rate": 0.98
        }

    def initialize(self):
        """Initialise le handler. L'enregistrement est géré par la Factory."""
        return True

    def _generate_mock_response(self, command_name: str, params: dict, output_data: dict):
        """Génère une réponse simulée standard."""
        if random.random() > self.config["success_rate"]:
            return {"success": False, "output": f"Échec de la simulation pour {command_name}."}

        report = f"--- Rapport pour {command_name} ---\n"
        for key, value in output_data.items():
            report += f"  - {key}: {value}\n"
        report += "---------------------------------\n"

        return {
            "success": True,
            "output": report,
            "new_state": {f"last_{command_name}": {"params": params, "time": time.time()}},
            "flags": [f"{command_name.upper()}_EXECUTED"],
            "time_consumed": self.config["query_time"]
        }

# --- Handlers Spécifiques ---

class AnalyserwhoisHandler(BaseOSINTHandler):
    """Handler pour analyserwhois"""
    def handle_analyserwhois(self, params: dict) -> dict:
        domain = params.get("domaine")
        if not domain:
            return {"success": False, "output": "❌ Erreur: Domaine manquant."}

        whois_info = {
            "Registrar": "Simulated Registrar Inc.",
            "Creation Date": "2022-01-15",
            "Admin Email": f"admin@{domain}"
        }
        return self._generate_mock_response("analyserwhois", params, whois_info)

class TrouveripspubliquesHandler(BaseOSINTHandler):
    """Handler pour trouveripspubliques"""
    def handle_trouveripspubliques(self, params: dict) -> dict:
        organisation = params.get("organisation")
        if not organisation:
            return {"success": False, "output": "❌ Erreur: Organisation manquante."}

        ips = [f"203.0.113.{random.randint(10, 100)}" for _ in range(random.randint(2, 5))]
        return self._generate_mock_response("trouveripspubliques", params, {"IPs Publiques": ips})

class CollecterosintHandler(BaseOSINTHandler):
    """Handler pour collecterosint"""
    def handle_collecterosint(self, params: dict) -> dict:
        cible = params.get("cible")
        if not cible:
            return {"success": False, "output": "❌ Erreur: Cible manquante."}

        osint_data = {
            "Social Media Mentions": random.randint(5, 50),
            "Associated Emails": [f"info@{cible}", f"contact@{cible}"],
            "Leaked Documents": f"{random.randint(0, 3)} documents trouvés"
        }
        return self._generate_mock_response("collecterosint", params, osint_data)
