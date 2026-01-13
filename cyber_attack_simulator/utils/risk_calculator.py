# utils/risk_calculator.py
class RiskCalculator:
    """Calcule les risques de détection pour chaque action"""

    @staticmethod
    def calculate_detection_risk(command: str, params: dict) -> float:
        """Calcule le risque de détection d'une commande"""
        risks = {
            "resoudredns": 0.02,
            "scannerports": 0.15,
            "testersql": 0.25,
            # ... toutes les commandes
        }
        return risks.get(command, 0.1)
