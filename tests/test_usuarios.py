"""
Fluxo 4: USUARIOS DO SISTEMA (Admin > User Management)

CT04 - Senha e confirmacao de senha diferentes
Criterio: CA02 | Tecnica: PE (classe invalida)
"""
from pages.admin_page import AdminPage


def test_ct04_senha_e_confirmacao_diferentes(logado, base_url, tirar_print):
    # Dado que estou no cadastro de usuario do sistema
    admin = AdminPage(logado, base_url).abrir_cadastro_de_usuario()
    # Quando digito senha e confirmacao diferentes (nada e salvo neste teste)
    admin.preencher_senhas("Teste12345", "Outra12345")
    # Entao o sistema avisa que as senhas nao conferem
    erros = admin.textos_de_erro()
    tirar_print("mensagem_de_erro")
    assert any("match" in texto.lower() for texto in erros), (
        f"Esperava aviso de senhas diferentes, apareceu: {erros}"
    )
