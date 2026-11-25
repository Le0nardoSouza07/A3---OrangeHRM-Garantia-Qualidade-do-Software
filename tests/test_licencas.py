"""
Fluxo 6: LISTA DE LICENCAS (Leave > Leave List)

CT06 - Data inicial depois da data final
Criterio: CA03 | Tecnica: VL (data final um dia antes da inicial)
"""
from datetime import date, timedelta

from pages.leave_page import LeavePage


def test_ct06_data_inicial_depois_da_final(logado, base_url, tirar_print):
    # Dado que estou na lista de licencas
    licencas = LeavePage(logado, base_url).abrir_lista_de_licencas()
    # Quando informo From Date = hoje e To Date = ontem e busco
    hoje = date.today()
    licencas.preencher_periodo(inicio=hoje, fim=hoje - timedelta(days=1))
    licencas.buscar()
    # Entao o sistema mostra erro de periodo invalido
    erros = licencas.textos_de_erro()
    tirar_print("mensagem_de_erro")
    assert erros, "Esperava uma mensagem de erro para o periodo invertido, mas nada apareceu. Possivel defeito."
