"""
Fluxo 5: CANDIDATOS (Recruitment > Candidates)

CT05 - Candidato com e-mail em formato invalido
Criterio: CA02 | Tecnica: PE (classe invalida)
"""
from pages.recruitment_page import RecruitmentPage


def test_ct05_candidato_com_email_invalido(logado, base_url, tirar_print):
    # Dado que estou no cadastro de candidato
    recrutamento = RecruitmentPage(logado, base_url).abrir_cadastro_de_candidato()
    # Quando informo um e-mail sem @ e salvo
    recrutamento.preencher_candidato("Carlos", "Teste", "carlos.teste.exemplo.com")
    recrutamento.salvar()
    # Entao o sistema mostra o formato esperado e nao salva
    erros = recrutamento.textos_de_erro()
    tirar_print("mensagem_de_erro")
    assert any("format" in texto.lower() for texto in erros), (
        f"Esperava aviso de formato de e-mail, apareceu: {erros}"
    )
    assert "addCandidate" in logado.current_url, "O candidato nao deveria ter sido salvo"
