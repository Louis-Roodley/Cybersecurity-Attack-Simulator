# tests/test_command_handler_factory.py
import unittest
import os
from unittest.mock import MagicMock, patch
from cyber_attack_simulator.command_handler_factory import CommandHandlerFactory
from cyber_attack_simulator.game_engine import CyberAttackEngine

class TestCommandHandlerFactory(unittest.TestCase):

    def setUp(self):
        """Configuration initiale pour les tests."""
        # Créer un mock de l'engine pour isoler la factory
        self.engine = MagicMock(spec=CyberAttackEngine)
        self.factory = CommandHandlerFactory(self.engine)

    def test_initialization(self):
        """Teste si la factory est initialisée correctement."""
        self.assertIsNotNone(self.factory)
        self.assertEqual(self.factory.engine, self.engine)

    @patch('builtins.open')
    @patch('json.load')
    def test_initialize_all_handlers_loads_correctly(self, mock_json_load, mock_open):
        """
        Teste si la factory charge, importe et enregistre correctement les handlers
        à partir d'un fichier commands.json simulé.
        """
        # Simuler le contenu de commands.json
        mock_json_load.return_value = {
            "commands": [
                {
                    "name": "resoudredns",
                    "category": "reconnaissance",
                    "template": "dns_handler",
                    "params": ["domaine"]
                },
                {
                    "name": "analyserwhois",
                    "category": "reconnaissance",
                    "template": "osint_handler",
                    "params": ["domaine"]
                }
            ]
        }

        # Simuler l'importation dynamique des modules de handlers
        with patch('importlib.import_module') as mock_import:
            # Configurer le mock pour retourner des classes de handler simulées
            mock_dns_handler_class = MagicMock()
            mock_osint_handler_class = MagicMock()

            # Le retour de import_module est un module, qui a des attributs (nos classes)
            mock_import.side_effect = [
                MagicMock(ResoudrednsHandler=mock_dns_handler_class),
                MagicMock(AnalyserwhoisHandler=mock_osint_handler_class)
            ]

            # Exécuter l'initialisation
            self.factory.initialize_all_handlers()

            # --- Vérifications ---
            # 1. Vérifier que les handlers ont été enregistrés auprès du moteur
            self.assertEqual(self.engine.register_handler.call_count, 2)

            # 2. Vérifier que les métadonnées des commandes ont été enregistrées
            self.assertEqual(self.engine.register_command_metadata.call_count, 2)
            self.engine.register_command_metadata.assert_any_call("resoudredns", ["domaine"])
            self.engine.register_command_metadata.assert_any_call("analyserwhois", ["domaine"])

            # 3. Vérifier que les classes de handlers ont été instanciées avec le moteur
            mock_dns_handler_class.assert_called_with(self.engine)
            mock_osint_handler_class.assert_called_with(self.engine)

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_initialize_handles_file_not_found(self, mock_open):
        """Teste la gestion de l'erreur si commands.json est introuvable."""
        # Utiliser un patch pour simuler la sortie de print
        with patch('builtins.print') as mock_print:
            self.factory.initialize_all_handlers()

            # Construire le chemin absolu attendu dans le message d'erreur
            expected_path = os.path.abspath(os.path.join('cyber_attack_simulator', 'data', 'commands.json'))
            expected_error_message = f"❌ Erreur: Fichier de commandes '{expected_path}' introuvable."

            # Vérifier que le message d'erreur correct a été affiché
            mock_print.assert_any_call(expected_error_message)

            # S'assurer qu'aucun handler n'a été enregistré
            self.engine.register_handler.assert_not_called()

if __name__ == '__main__':
    unittest.main()
