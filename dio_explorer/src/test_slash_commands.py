"""
test_slash_commands.py
----------------------
Testes unitários para os slash commands /trilha, /desafio e /certificado.
Cobertura-alvo: >= 70 % das linhas de trilhas_utils.py

Execute com:
    python -m pytest dio_explorer/src/test_slash_commands.py -v
ou com cobertura:
    python -m pytest dio_explorer/src/test_slash_commands.py -v --tb=short \
           --cov=dio_explorer.src.trilhas_utils --cov-report=term-missing
"""

import json
import os
import sys
import random
from datetime import date
from unittest.mock import patch, mock_open

import pytest

# Garante que o pacote é encontrado independentemente do diretório de trabalho
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.trilhas_utils import (
    carregar_trilhas,
    buscar_trilha,
    formatar_plano_estudos,
    gerar_desafio,
    gerar_certificado,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

TRILHA_JAVA = {
    "id": 2,
    "nome": "Desenvolvedor Java Full Stack",
    "tecnologia": "Java",
    "nivel": "Intermediário",
    "numero_de_modulos": 12,
    "xp_total": 11500,
    "badges_disponiveis": ["Java Developer", "Spring Hero", "Full Stack Master"],
    "promocoes": {"desconto": "20%", "validade": "2025-09-15", "cupom": "JAVA20"},
    "vitalicio": True,
    "lives_ao_vivo": [
        {"titulo": "Spring Boot na Prática", "data": "2025-07-15", "horario": "20:00"},
        {"titulo": "APIs REST com Java", "data": "2025-07-29", "horario": "20:00"},
        {"titulo": "Deploy de Aplicações Java", "data": "2025-08-12", "horario": "20:00"},
    ],
}

TRILHA_AWS = {
    "id": 5,
    "nome": "Cloud Native com AWS",
    "tecnologia": "AWS / Cloud",
    "nivel": "Avançado",
    "numero_de_modulos": 14,
    "xp_total": 16500,
    "badges_disponiveis": ["Cloud Practitioner", "AWS Architect"],
    "promocoes": None,
    "vitalicio": True,
    "lives_ao_vivo": [],
}

TRILHA_SEM_PROMO = {
    "id": 8,
    "nome": "DevOps e CI/CD na Prática",
    "tecnologia": "Docker / Kubernetes / GitHub Actions",
    "nivel": "Avançado",
    "numero_de_modulos": 13,
    "xp_total": 15000,
    "badges_disponiveis": ["DevOps Engineer", "Pipeline Master"],
    "promocoes": None,
    "vitalicio": True,
    "lives_ao_vivo": [],
}

CATALOGO = [TRILHA_JAVA, TRILHA_AWS, TRILHA_SEM_PROMO]


# ---------------------------------------------------------------------------
# 1. carregar_trilhas
# ---------------------------------------------------------------------------

class TestCarregarTrilhas:
    """TC-01 a TC-03 — leitura do arquivo de dados"""

    def test_retorna_lista(self, tmp_path):
        """TC-01: deve retornar uma lista ao ler JSON válido."""
        dados = {"trilhas": [TRILHA_JAVA]}
        arquivo = tmp_path / "trilhas.json"
        arquivo.write_text(json.dumps(dados), encoding="utf-8")
        resultado = carregar_trilhas(str(arquivo))
        assert isinstance(resultado, list)

    def test_numero_de_trilhas_correto(self, tmp_path):
        """TC-02: deve retornar o número exato de trilhas do JSON."""
        dados = {"trilhas": [TRILHA_JAVA, TRILHA_AWS]}
        arquivo = tmp_path / "trilhas.json"
        arquivo.write_text(json.dumps(dados), encoding="utf-8")
        resultado = carregar_trilhas(str(arquivo))
        assert len(resultado) == 2

    def test_arquivo_real_tem_32_trilhas(self):
        """TC-03: o arquivo de produção deve conter 32 trilhas."""
        caminho = os.path.join(
            os.path.dirname(__file__), "..", "data", "trilhas_dio.json"
        )
        trilhas = carregar_trilhas(caminho)
        assert len(trilhas) == 32


# ---------------------------------------------------------------------------
# 2. buscar_trilha  (/trilha)
# ---------------------------------------------------------------------------

class TestBuscarTrilha:
    """TC-04 a TC-11 — regras do comando /trilha"""

    def test_busca_exata_retorna_trilha(self):
        """TC-04: busca exata pelo nome da tecnologia."""
        resultado = buscar_trilha("Java", CATALOGO)
        assert resultado is not None
        assert resultado["tecnologia"] == "Java"

    def test_busca_case_insensitive(self):
        """TC-05: busca deve ignorar maiúsculas/minúsculas."""
        assert buscar_trilha("java", CATALOGO) is not None
        assert buscar_trilha("JAVA", CATALOGO) is not None
        assert buscar_trilha("JaVa", CATALOGO) is not None

    def test_busca_parcial(self):
        """TC-06: deve encontrar trilha com substring da tecnologia."""
        resultado = buscar_trilha("Cloud", CATALOGO)
        assert resultado is not None
        assert "Cloud" in resultado["tecnologia"]

    def test_busca_inexistente_retorna_none(self):
        """TC-07: tecnologia não cadastrada deve retornar None."""
        assert buscar_trilha("Cobol", CATALOGO) is None

    def test_busca_string_vazia_retorna_none(self):
        """TC-08: string vazia deve retornar None."""
        assert buscar_trilha("", CATALOGO) is None

    def test_busca_apenas_espacos_retorna_none(self):
        """TC-09: string com só espaços deve retornar None."""
        assert buscar_trilha("   ", CATALOGO) is None

    def test_retorna_primeiro_match(self):
        """TC-10: deve retornar o primeiro match quando há múltiplos."""
        catalogo_duplo = [TRILHA_JAVA, TRILHA_JAVA]
        resultado = buscar_trilha("Java", catalogo_duplo)
        assert resultado["id"] == 2

    def test_busca_java_arquivo_real(self):
        """TC-11: /trilha java no catálogo real deve retornar trilha Java."""
        caminho = os.path.join(
            os.path.dirname(__file__), "..", "data", "trilhas_dio.json"
        )
        trilhas = carregar_trilhas(caminho)
        resultado = buscar_trilha("java", trilhas)
        assert resultado is not None
        assert "Java" in resultado["tecnologia"]
        assert resultado["numero_de_modulos"] == 12


# ---------------------------------------------------------------------------
# 3. formatar_plano_estudos  (/trilha — saída)
# ---------------------------------------------------------------------------

class TestFormatarPlanoEstudos:
    """TC-12 a TC-18 — formatação do plano de estudos"""

    def test_contem_nome_da_trilha(self):
        """TC-12: saída deve conter o nome da trilha."""
        saida = formatar_plano_estudos(TRILHA_JAVA)
        assert "Desenvolvedor Java Full Stack" in saida

    def test_contem_tecnologia(self):
        """TC-13: saída deve conter a tecnologia."""
        saida = formatar_plano_estudos(TRILHA_JAVA)
        assert "Java" in saida

    def test_contem_nivel(self):
        """TC-14: saída deve conter o nível."""
        saida = formatar_plano_estudos(TRILHA_JAVA)
        assert "Intermediário" in saida

    def test_contem_xp(self):
        """TC-15: saída deve conter o XP total."""
        saida = formatar_plano_estudos(TRILHA_JAVA)
        assert "11500" in saida

    def test_contem_badges(self):
        """TC-16: saída deve listar as badges disponíveis."""
        saida = formatar_plano_estudos(TRILHA_JAVA)
        assert "Java Developer" in saida
        assert "Spring Hero" in saida

    def test_promocao_exibida_quando_existe(self):
        """TC-17: promoção deve aparecer se não for nula."""
        saida = formatar_plano_estudos(TRILHA_JAVA)
        assert "JAVA20" in saida
        assert "20%" in saida

    def test_sem_promocao_exibe_mensagem(self):
        """TC-18: sem promoção deve exibir mensagem padrão."""
        saida = formatar_plano_estudos(TRILHA_AWS)
        assert "Nenhuma promoção ativa" in saida


# ---------------------------------------------------------------------------
# 4. gerar_desafio  (/desafio)
# ---------------------------------------------------------------------------

class TestGerarDesafio:
    """TC-19 a TC-27 — geração de desafios de código"""

    def test_retorna_dict(self):
        """TC-19: deve retornar um dicionário."""
        resultado = gerar_desafio("Java", "Intermediário")
        assert isinstance(resultado, dict)

    def test_campos_obrigatorios_presentes(self):
        """TC-20: dicionário deve ter todos os campos obrigatórios."""
        campos = {"tecnologia", "nivel", "titulo", "descricao", "entrada", "saida_esperada", "xp"}
        resultado = gerar_desafio("Java", "Intermediário")
        assert campos.issubset(resultado.keys())

    def test_tecnologia_preservada(self):
        """TC-21: campo tecnologia deve refletir o argumento passado."""
        resultado = gerar_desafio("Java", "Intermediário")
        assert resultado["tecnologia"] == "Java"

    def test_nivel_basico_xp_range(self):
        """TC-22: nível Básico deve gerar XP entre 200 e 500."""
        random.seed(42)
        for _ in range(20):
            resultado = gerar_desafio("Python", "Básico")
            assert 200 <= resultado["xp"] <= 500

    def test_nivel_intermediario_xp_range(self):
        """TC-23: nível Intermediário deve gerar XP entre 500 e 1000."""
        random.seed(42)
        for _ in range(20):
            resultado = gerar_desafio("Java", "Intermediário")
            assert 500 <= resultado["xp"] <= 1000

    def test_nivel_avancado_xp_range(self):
        """TC-24: nível Avançado deve gerar XP entre 1000 e 2000."""
        random.seed(42)
        for _ in range(20):
            resultado = gerar_desafio("React", "Avançado")
            assert 1000 <= resultado["xp"] <= 2000

    def test_nivel_invalido_lanca_excecao(self):
        """TC-25: nível inválido deve lançar ValueError."""
        with pytest.raises(ValueError):
            gerar_desafio("Java", "Expert")

    def test_nivel_invalido_mensagem(self):
        """TC-26: mensagem do ValueError deve mencionar o nível inválido."""
        with pytest.raises(ValueError, match="Expert"):
            gerar_desafio("Java", "Expert")

    def test_desafio_java_intermediario_completo(self):
        """TC-27: fluxo completo de /desafio Java Intermediário."""
        resultado = gerar_desafio("Java", "Intermediário")
        assert resultado["nivel"] == "Intermediário"
        assert resultado["titulo"] != ""
        assert resultado["descricao"] != ""


# ---------------------------------------------------------------------------
# 5. gerar_certificado  (/certificado)
# ---------------------------------------------------------------------------

class TestGerarCertificado:
    """TC-28 a TC-36 — geração de certificado fictício"""

    DATA_FIXA = date(2025, 7, 10)

    def test_retorna_string(self):
        """TC-28: deve retornar uma string."""
        resultado = gerar_certificado("Fabricio Eirim Castro", TRILHA_JAVA, self.DATA_FIXA)
        assert isinstance(resultado, str)

    def test_contem_nome_usuario(self):
        """TC-29: certificado deve conter o nome do usuário."""
        resultado = gerar_certificado("Fabricio Eirim Castro", TRILHA_JAVA, self.DATA_FIXA)
        assert "Fabricio Eirim Castro" in resultado

    def test_contem_nome_trilha(self):
        """TC-30: certificado deve conter o nome da trilha."""
        resultado = gerar_certificado("Fabricio Eirim Castro", TRILHA_JAVA, self.DATA_FIXA)
        assert "Desenvolvedor Java Full Stack" in resultado

    def test_contem_tecnologia(self):
        """TC-31: certificado deve conter a tecnologia."""
        resultado = gerar_certificado("Fabricio Eirim Castro", TRILHA_JAVA, self.DATA_FIXA)
        assert "Java" in resultado

    def test_contem_data_emissao(self):
        """TC-32: certificado deve conter a data formatada DD/MM/AAAA."""
        resultado = gerar_certificado("Fabricio Eirim Castro", TRILHA_JAVA, self.DATA_FIXA)
        assert "10/07/2025" in resultado

    def test_id_formato_correto(self):
        """TC-33: ID do certificado deve seguir o padrão DIO-NNN-AAAA-NNNNNN."""
        import re
        resultado = gerar_certificado("Fabricio Eirim Castro", TRILHA_JAVA, self.DATA_FIXA)
        assert re.search(r"DIO-\d{3}-\d{4}-\d{6}", resultado)

    def test_contem_badges(self):
        """TC-34: certificado deve listar todas as badges da trilha."""
        resultado = gerar_certificado("Fabricio Eirim Castro", TRILHA_JAVA, self.DATA_FIXA)
        for badge in TRILHA_JAVA["badges_disponiveis"]:
            assert badge in resultado

    def test_usa_data_hoje_quando_nao_informada(self):
        """TC-35: sem data explícita, deve usar a data atual."""
        resultado = gerar_certificado("Ana", TRILHA_JAVA)
        hoje_fmt = date.today().strftime("%d/%m/%Y")
        assert hoje_fmt in resultado

    def test_fluxo_completo_trilha_java(self):
        """TC-36: fluxo integrado — busca Java, formata plano, gera desafio e certificado."""
        caminho = os.path.join(
            os.path.dirname(__file__), "..", "data", "trilhas_dio.json"
        )
        trilhas = carregar_trilhas(caminho)

        # /trilha java
        trilha = buscar_trilha("java", trilhas)
        assert trilha is not None
        plano = formatar_plano_estudos(trilha)
        assert "Java" in plano

        # /desafio Java Intermediário
        desafio = gerar_desafio(trilha["tecnologia"], trilha["nivel"])
        assert desafio["nivel"] == "Intermediário"
        assert desafio["xp"] >= 500

        # /certificado
        cert = gerar_certificado("Fabricio Eirim Castro", trilha, date(2025, 7, 10))
        assert "Fabricio Eirim Castro" in cert
        assert "Java" in cert
