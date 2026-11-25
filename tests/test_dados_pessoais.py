"""
Fluxo 3: DADOS PESSOAIS (documentos e datas)

CT03 - Data de nascimento no futuro
Criterio: CA03 | Tecnica: VL (amanha, o dia seguinte ao limite que e hoje)
"""
import time
from datetime import date, timedelta

from pages.pim_page import PimPage


def test_ct03_data_nascimento_no_futuro(logado, base_url, tirar_print):
    pim = PimPage(logado, base_url)
    sobrenome = f"Qa{int(time.time())}"  # sobrenome unico para achar e excluir depois
    # Dado um funcionario ficticio criado pelo proprio teste
    pim.criar_funcionario("Maria", sobrenome)

    try:
        # Quando informo a data de nascimento de amanha e salvo
        amanha = date.today() + timedelta(days=1)
        pim.definir_data_nascimento(amanha)
        pim.salvar_dados_pessoais()

        # Entao o sistema deve rejeitar a data
        tipo, mensagens = pim.resultado_do_salvamento()
        tirar_print("resultado")
        assert tipo == "erro", (
            f"O sistema deveria rejeitar a data de nascimento futura ({amanha}), "
            f"mas o resultado foi '{tipo}': {mensagens}. Possivel defeito."
        )
    finally:
        # limpeza: nao deixar lixo no ambiente publico
        try:
            pim.excluir_funcionario(sobrenome)
        except Exception as erro:  # noqa: BLE001
            print(f"Aviso: nao foi possivel excluir o funcionario {sobrenome}: {erro}")
