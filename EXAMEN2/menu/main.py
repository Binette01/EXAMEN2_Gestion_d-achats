import sys
import os

# Pour s'assurer que les imports fonctionnent correctement, peu importe d'où le script est lancé,
# nous ajoutons la racine du projet ('EXAMEN2') au path de Python.
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir) # Remonte d'un niveau (de 'menu' à 'EXAMEN2')
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from menu.interface import Menu

def main():
    print("="*40)
    print("     BIENVENUE DANS GESTION ACHATS     ")
    print("="*40)

    print("\n") 
    menu = Menu()
    menu.menu_principal()

if __name__ == "__main__":
    main()


