# main.py
from cyber_attack_simulator.game_engine import CyberAttackEngine
from cyber_attack_simulator.command_handler_factory import CommandHandlerFactory
import shlex

def parse_command(engine: CyberAttackEngine, command: str):
    """
    Parse la commande de l'utilisateur en nom de commande et dictionnaire de paramètres,
    en utilisant les métadonnées pour les arguments positionnels.
    """
    parts = shlex.split(command)
    if not parts:
        return None, {}

    cmd_name = parts[0]
    args = parts[1:]
    params = {}

    # Récupérer les noms de paramètres attendus depuis le moteur
    param_names = engine.command_metadata.get(cmd_name)

    if param_names is None:
        # Si la commande n'est pas reconnue, on ne peut pas parser les arguments
        return cmd_name, {}

    if len(args) > len(param_names):
        print(f"⚠️ Trop d'arguments pour la commande '{cmd_name}'. "
              f"Attendus: {len(param_names)}, fournis: {len(args)}")
        return cmd_name, None  # Indique une erreur de parsing

    # Mapper les arguments positionnels aux noms de paramètres
    for i, arg in enumerate(args):
        params[param_names[i]] = arg

    return cmd_name, params

def main():
    """Point d'entrée principal du jeu"""
    print("🎮 Cyber Attack Simulator - Démarrage...")

    # Initialiser le moteur
    engine = CyberAttackEngine()

    # Initialiser la factory
    factory = CommandHandlerFactory(engine)
    factory.initialize_all_handlers()

    print(f"✅ {len(engine.handlers)} commandes chargées")

    # Boucle de jeu principale
    while True:
        try:
            command = input("\n> ").strip()
            if command.lower() in ["exit", "quit"]:
                print("👋 Au revoir !")
                break

            # Parser la commande
            cmd_name, params = parse_command(engine, command)

            if params is None: # Gérer l'erreur de parsing
                continue

            if cmd_name:
                # Exécuter
                result = engine.execute_command(cmd_name, params)

                # Afficher le résultat
                if result and "output" in result:
                    print(result["output"])
                else:
                    # Fallback au cas où le handler retournerait une réponse mal formée
                    print(f"La commande '{cmd_name}' n'a pas retourné de résultat affichable.")

        except KeyboardInterrupt:
            print("\n🛑 Simulation interrompue. Au revoir !")
            break
        except Exception as e:
            print(f"❌ Erreur inattendue: {e}")

if __name__ == "__main__":
    main()
