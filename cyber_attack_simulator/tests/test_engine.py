# tests/test_engine.py
import sys
import os
import pytest

from cyber_attack_simulator.game_engine import CyberAttackEngine
from cyber_attack_simulator.main import parse_command

# --- Mocks de Handlers ---

def mock_success_handler(params: dict) -> dict:
    """Un mock de handler qui réussit toujours."""
    return {
        "success": True,
        "output": f"Commande mock exécutée avec les paramètres: {params}",
        "new_state": {"credits": 999},
        "flags": ["MOCK_FLAG_ACQUIRED"],
        "time_consumed": 0.1
    }

def mock_failure_handler(params: dict) -> dict:
    """Un mock de handler qui échoue toujours."""
    return {
        "success": False,
        "output": "La commande mock a échoué comme prévu.",
        "new_state": {},
        "flags": [],
        "time_consumed": 0.1
    }

# --- Tests ---

def test_engine_initialization():
    """Teste l'initialisation correcte du moteur de jeu."""
    engine = CyberAttackEngine()
    assert engine.game_state is not None
    assert engine.detection_level == 0.0
    assert len(engine.handlers) == 0
    assert len(engine.flags) == 0
    assert engine.game_state.credits == 1000

def test_register_handler():
    """Teste si un handler peut être enregistré correctement."""
    engine = CyberAttackEngine()
    engine.register_handler("mock_command", mock_success_handler)
    assert "mock_command" in engine.handlers
    assert engine.handlers["mock_command"] == mock_success_handler

def test_execute_unknown_command():
    """Teste l'exécution d'une commande qui n'existe pas."""
    engine = CyberAttackEngine()
    result = engine.execute_command("non_existent_command", {})
    assert result["success"] is False
    assert "non reconnue" in result["output"]

def test_execute_known_command_success_and_state_update():
    """Teste l'exécution d'une commande connue qui réussit et met à jour l'état."""
    engine = CyberAttackEngine()
    engine.register_handler("mock_success", mock_success_handler)

    params = {"cible": "127.0.0.1"}
    result = engine.execute_command("mock_success", params)

    assert result["success"] is True
    assert "Commande mock exécutée" in result["output"]
    # Vérifier la mise à jour de l'état du jeu
    assert engine.game_state.credits == 999
    assert "MOCK_FLAG_ACQUIRED" in engine.flags
    assert len(engine.command_history) == 1
    assert engine.command_history[0]["command"] == "mock_success"

def test_execute_known_command_failure_does_not_update_state():
    """Teste qu'une commande qui échoue ne modifie pas l'état du jeu."""
    engine = CyberAttackEngine()
    engine.register_handler("mock_fail", mock_failure_handler)

    initial_credits = engine.game_state.credits
    initial_flags_count = len(engine.flags)

    result = engine.execute_command("mock_fail", {})

    assert result["success"] is False
    assert "a échoué comme prévu" in result["output"]
    # L'état du jeu ne doit pas changer en cas d'échec
    assert engine.game_state.credits == initial_credits
    assert len(engine.flags) == initial_flags_count

def test_positional_command_parser():
    """Teste si le parseur de commande gère correctement les arguments positionnels."""
    engine = CyberAttackEngine()
    # Enregistrer manuellement les métadonnées pour une commande de test
    engine.register_command_metadata("resoudredns", ["domaine"])
    engine.register_command_metadata("obtenirrecordsdns", ["domaine", "type"])

    # Test avec un seul argument
    cmd_name, params = parse_command(engine, "resoudredns example.com")
    assert cmd_name == "resoudredns"
    assert params == {"domaine": "example.com"}

    # Test avec deux arguments
    cmd_name, params = parse_command(engine, "obtenirrecordsdns google.com MX")
    assert cmd_name == "obtenirrecordsdns"
    assert params == {"domaine": "google.com", "type": "MX"}

    # Test avec une commande inconnue (devrait retourner des paramètres vides)
    cmd_name, params = parse_command(engine, "commande_inconnue arg1")
    assert cmd_name == "commande_inconnue"
    assert params == {}

    # Test avec trop d'arguments (devrait retourner None pour les params)
    cmd_name, params = parse_command(engine, "resoudredns example.com extra_arg")
    assert cmd_name == "resoudredns"
    assert params is None
