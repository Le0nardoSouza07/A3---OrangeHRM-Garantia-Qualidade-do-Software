"""
Fluxo 2: PIM (cadastro de funcionario)

CT02 - Cadastro de funcionario sem sobrenome
Criterio: CA02 | Tecnica: PE (classe invalida)
"""
from pages.pim_page import PimPage


def test_ct02_cadastro_sem_sobrenome(logado, base_url, tirar_print):
    # Dado que estou no cadastro de funcionario
    pim = PimPage(logado, base_url).abrir_cadastro()
    # Quando preencho so o nome e salvo
    pim.preencher_nome("Maria")  # sobrenome vazio de proposito
    pim.salvar()
    # Entao o sistema mostra "Required" e nao salva
    erros = pim.textos_de_erro()
    tirar_print("mensagem_de_erro")
    assert any("Required" in texto for texto in erros), f"Esperava 'Required', apareceu: {erros}"
    assert "addEmployee" in logado.current_url, "O funcionario nao deveria ter sido salvo"
