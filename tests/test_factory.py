# tests/test_factory.py
import unittest
from cyber_attack_simulator.game_engine import CyberAttackEngine
from cyber_attack_simulator.command_handler_factory import CommandHandlerFactory

class TestCommandHandlerFactory(unittest.TestCase):
    """Tests for the CommandHandlerFactory."""

    def test_command_loading(self):
        """
        Tests if the factory correctly loads commands from the JSON file.
        This is a critical test to prevent the '0 commands loaded' bug.
        """
        engine = CyberAttackEngine()
        factory = CommandHandlerFactory(engine)
        factory.initialize_all_handlers()

        # Check that the command handlers are actually loaded
        self.assertGreater(len(engine.handlers), 0, "No command handlers were loaded by the factory.")

        # Check that command metadata is also registered
        self.assertGreater(len(engine.command_metadata), 0, "No command metadata was registered by the factory.")

        # Check for a specific, known command
        self.assertIn("resoudredns", engine.handlers)

if __name__ == '__main__':
    unittest.main()
