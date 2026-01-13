# tests/test_command_handler_factory.py
import sys
import os
import pytest

from cyber_attack_simulator.game_engine import CyberAttackEngine
from cyber_attack_simulator.command_handler_factory import CommandHandlerFactory

def test_factory_loads_implemented_handlers():
    """
    Vérifie que la factory charge correctement les handlers qui ont été implémentés
    et les enregistre dans le moteur de jeu.
    """
    engine = CyberAttackEngine()
    factory = CommandHandlerFactory(engine)
    factory.initialize_all_handlers()

    # Les commandes suivantes sont définies dans commands.json ET ont une classe Handler implémentée.
    implemented_commands = [
        "resoudredns", "resoudredns_inverse", "obtenirrecordsdns", "trouversousdomaines", "trouversousdomaines_api",
        "analyserwhois", "trouveripspubliques", "collecterosint"
    ]

    unimplemented_commands = [
        "scannerports", # Le fichier port_scanner.py est vide
        "testersql"     # Le fichier web_vuln.py est vide
    ]

    assert len(engine.handlers) == len(implemented_commands), \
        f"Attendu {len(implemented_commands)} handlers chargés, mais obtenu {len(engine.handlers)}"

    for cmd in implemented_commands:
        assert cmd in engine.handlers, f"La commande implémentée '{cmd}' devrait être chargée."
        assert callable(engine.handlers[cmd]), f"Le handler pour '{cmd}' devrait être une fonction appelable."

    for cmd in unimplemented_commands:
        assert cmd not in engine.handlers, f"La commande non implémentée '{cmd}' ne devrait pas être chargée."

def test_factory_handles_missing_json_file_gracefully():
    """
    Vérifie que la factory ne lève pas d'exception si le fichier commands.json est
    temporairement manquant (par ex. en le renommant).
    """
    # Construit un chemin robuste qui fonctionne quel que soit le répertoire de travail
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    original_path = os.path.join(project_root, 'data', 'commands.json')
    renamed_path = os.path.join(project_root, 'data', 'commands.json.bak')

    # Renommer le fichier pour simuler son absence
    os.rename(original_path, renamed_path)

    engine = CyberAttackEngine()
    factory = CommandHandlerFactory(engine)

    # Cette opération ne devrait pas planter l'application
    factory.initialize_all_handlers()

    # Restaurer le fichier
    os.rename(renamed_path, original_path)

    # Aucun handler ne devrait avoir été chargé
    assert len(engine.handlers) == 0
