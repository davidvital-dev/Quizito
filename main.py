#!/usr/bin/env python3


"""
Ponto de entrada principal para a aplicação Quizito CLI.
"""

import sys
import os

from quiz_app.cli import menu_principal

def main():
    """
    Função principal que inicia a interface de linha de comando (CLI).
    """
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\nOperação interrompida pelo usuário. Saindo...")
        sys.exit(0)
    except Exception as e:
        print(f"\nOcorreu um erro inesperado: {e}")
        
        sys.exit(1)

if __name__ == "__main__":
    main()