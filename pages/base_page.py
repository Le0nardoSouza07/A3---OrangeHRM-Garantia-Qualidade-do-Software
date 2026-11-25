"""Funcoes comuns a todas as telas (esperas, digitar, ler mensagens de erro)."""
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ERRO_DE_CAMPO = (By.CSS_SELECTOR, ".oxd-input-field-error-message")
CARREGANDO = (By.CSS_SELECTOR, ".oxd-form-loader, .oxd-loading-spinner")


def por_rotulo(rotulo):
    """O OrangeHRM nao tem id estavel: localizamos o campo pelo rotulo (label)."""
    return (By.XPATH, f"//label[normalize-space()='{rotulo}']/../following-sibling::div//input")


class BasePage:
    TEMPO = 20  # o demo e lento: toda espera usa WebDriverWait

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.wait = WebDriverWait(driver, self.TEMPO)

    def abrir_caminho(self, caminho):
        self.driver.get(self.base_url + caminho)

    def visivel(self, localizador):
        return self.wait.until(EC.visibility_of_element_located(localizador))

    def clicar(self, localizador):
        self.wait.until(EC.element_to_be_clickable(localizador)).click()

    def digitar(self, localizador, texto):
        campo = self.wait.until(EC.element_to_be_clickable(localizador))
        campo.click()
        campo.send_keys(Keys.CONTROL, "a")
        campo.send_keys(Keys.BACKSPACE)
        campo.send_keys(texto)
        return campo

    def sair_do_campo(self):
        """Dispara a validacao do campo apertando TAB."""
        self.driver.switch_to.active_element.send_keys(Keys.TAB)

    def esperar_carregamento(self):
        try:
            WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located(CARREGANDO))
        except TimeoutException:
            pass

    def textos_de_erro(self, tempo=10):
        """Espera aparecer alguma mensagem de erro de campo e devolve os textos."""
        limite = time.time() + tempo
        while time.time() < limite:
            textos = [e.text.strip() for e in self.driver.find_elements(*ERRO_DE_CAMPO) if e.text.strip()]
            if textos:
                return textos
            time.sleep(0.3)
        return []

    def formato_de_data(self, localizador):
        """O formato da data pode ser trocado por qualquer pessoa no demo:
        lemos o placeholder do campo antes de digitar."""
        placeholder = self.visivel(localizador).get_attribute("placeholder") or "yyyy-mm-dd"
        return placeholder.replace("yyyy", "%Y").replace("mm", "%m").replace("dd", "%d")

    def digitar_data(self, localizador, data):
        formato = self.formato_de_data(localizador)
        self.digitar(localizador, data.strftime(formato))
        self.sair_do_campo()
