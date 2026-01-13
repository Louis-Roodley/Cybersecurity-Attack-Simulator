# command_handler_factory.py
import json
import importlib
import os
from cyber_attack_simulator.game_engine import CyberAttackEngine

def to_camel_case(snake_str: str) -> str:
    """Convertit une chaîne snake_case en CamelCase."""
    return "".join(x.capitalize() for x in snake_str.split('_'))

class CommandHandlerFactory:
    """Factory pour créer et gérer tous les handlers en les chargeant dynamiquement."""

    def __init__(self, engine: CyberAttackEngine):
        self.engine = engine

    def initialize_all_handlers(self):
        """Charge dynamiquement tous les handlers à partir de data/commands.json."""
        commands_file = os.path.join(os.path.dirname(__file__), 'data', 'commands.json')

        try:
            with open(commands_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                commands = data.get("commands", [])
        except FileNotFoundError:
            print(f"❌ Erreur: Fichier de commandes '{commands_file}' introuvable.")
            return
        except json.JSONDecodeError:
            print(f"❌ Erreur: Impossible de décoder le JSON depuis '{commands_file}'.")
            return

        for command_info in commands:
            command_name = command_info.get("name")
            category = command_info.get("category")
            handler_template = command_info.get("template")

            if not all([command_name, category, handler_template]):
                print(f"⚠️ Avertissement: Entrée de commande invalide ignorée: {command_info}")
                continue

            try:
                module_path = f"handlers.{category}.{handler_template}"
                class_name = f"{to_camel_case(command_name)}Handler"

                # Importation dynamique du module
                handler_module = importlib.import_module(module_path)

                # Obtention de la classe depuis le module
                HandlerClass = getattr(handler_module, class_name)

                # Instanciation et initialisation
                handler_instance = HandlerClass(self.engine)
                if handler_instance.initialize():
                    # La factory est responsable de l'enregistrement du handler ET de ses métadonnées
                    handler_method = getattr(handler_instance, f"handle_{command_name}")
                    self.engine.register_handler(command_name, handler_method)

                    param_names = command_info.get("params", [])
                    self.engine.register_command_metadata(command_name, param_names)
                else:
                    print(f"⚠️ Avertissement: Échec de l'initialisation du handler pour '{command_name}'.")

            except ModuleNotFoundError:
                # Attendu si le fichier du handler n'a pas encore été créé
                pass
            except AttributeError:
                # Attendu si la classe du handler n'est pas définie dans le fichier
                pass
            except Exception as e:
                print(f"❌ Erreur lors du chargement du handler pour '{command_name}': {e}")
