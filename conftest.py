"""
conftest.py — configuração do pytest para o projeto DIO Explorer.
Adiciona dio_explorer ao sys.path para importação correta dos módulos.
"""
import sys
import os

# Garante que 'dio_explorer' (pai de src/) seja encontrável
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "dio_explorer"))
