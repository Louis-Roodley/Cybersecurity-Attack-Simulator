# handlers/reconnaissance/dns_handler.py
import time
import random

# --- Classe de base pour les Handlers DNS ---
class BaseDNSHandler:
    def __init__(self, engine):
        self.engine = engine
        self.config = {
            "query_time": 0.1,
            "detection_risk": 0.02,
            "success_rate": 0.95
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

class ResoudrednsHandler(BaseDNSHandler):
    """Handler pour la commande resoudredns"""
    def handle_resoudredns(self, params: dict) -> dict:
        domain = params.get("domaine")
        if not domain:
            return {"success": False, "output": "❌ Erreur: Domaine manquant."}

        ips = [f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}" for _ in range(random.randint(1, 4))]
        return self._generate_mock_response("resoudredns", params, {"IPs": ips})

class ResoudrednsInverseHandler(BaseDNSHandler):
    """Handler pour resoudredns_inverse"""
    def handle_resoudredns_inverse(self, params: dict) -> dict:
        ip = params.get("ip")
        if not ip:
            return {"success": False, "output": "❌ Erreur: IP manquante."}

        domain = f"host-{ip.replace('.', '-')}.example.com"
        return self._generate_mock_response("resoudredns_inverse", params, {"Hostname": domain})

class ObtenirrecordsdnsHandler(BaseDNSHandler):
    """Handler pour obtenirrecordsdns"""
    def handle_obtenirrecordsdns(self, params: dict) -> dict:
        domain = params.get("domaine")
        record_type = params.get("type", "ANY")
        if not domain:
            return {"success": False, "output": "❌ Erreur: Domaine manquant."}

        records = [f"{record_type.upper()} record {i+1} for {domain}" for i in range(random.randint(1, 5))]
        return self._generate_mock_response("obtenirrecordsdns", params, {"Records": records})

class TrouversousdomainesHandler(BaseDNSHandler):
    """Handler pour trouversousdomaines"""
    def handle_trouversousdomaines(self, params: dict) -> dict:
        domain = params.get("domaine")
        if not domain:
            return {"success": False, "output": "❌ Erreur: Domaine manquant."}

        subdomains = [f"{sub}.{domain}" for sub in ["www", "mail", "dev", "api"]]
        return self._generate_mock_response("trouversousdomaines", params, {"Subdomains": subdomains})

class TrouversousdomainesApiHandler(BaseDNSHandler):
    """Handler pour trouversousdomaines_api"""
    def handle_trouversousdomaines_api(self, params: dict) -> dict:
        domain = params.get("domaine")
        if not domain:
            return {"success": False, "output": "❌ Erreur: Domaine manquant."}

        subdomains = [f"{sub}.{domain}" for sub in ["blog", "shop", "support", "test"]]
        return self._generate_mock_response("trouversousdomaines_api", params, {"Subdomains (API)": subdomains})
