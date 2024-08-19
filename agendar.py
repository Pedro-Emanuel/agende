from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException
from enum import Enum
import argparse
import threading

class TipoRefeicao(Enum):
    ALMOCO = '2'
    JANTAR = '3'

class AgendadorRU:
    def __init__(self, username, password):
        self.driver = webdriver.Chrome()
        self.username = username
        self.password = password

    def wait_for_element(self, element_type, element, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((element_type, element))
        )

    def login(self):
        self.driver.get('https://si3.ufc.br/sigaa/verTelaLogin.do')

        user_login = self.wait_for_element(By.NAME, 'user.login')
        user_login.send_keys(self.username)

        user_senha = self.wait_for_element(By.NAME, 'user.senha')
        user_senha.send_keys(self.password)

        botao_entrar = self.wait_for_element(By.NAME, 'entrar')
        botao_entrar.click()

    def navigate_to_agendamento(self):
        lista_menus = self.wait_for_element(By.CSS_SELECTOR, 'li.menus')
        menu_discente = lista_menus.find_element(By.TAG_NAME, "a")
        menu_discente.click()

        restaurante_universitario = self.wait_for_element(By.ID, "cmAction-96")

        ActionChains(self.driver).move_to_element(restaurante_universitario).perform()

        agendar_refeicao = self.wait_for_element(By.ID, "cmAction-97")
        agendar_refeicao.click()

    def preencher_formulario(self, data, refeicao):
        self.wait_for_element(By.ID, "formulario:tipo_refeicao")

        data_agendamento = self.wait_for_element(By.ID, "formulario:data_agendamento")
        data_agendamento.send_keys(data)

        tipo_refeicao = Select(self.wait_for_element(By.ID, "formulario:tipo_refeicao"))
        tipo_refeicao.select_by_value(refeicao.value)

        options = [0] # Horários: [0, 53, 54] (None, Almoço, Jantar)

        while (options.__len__() == 1):
            try:
                horario_agendado = Select(self.wait_for_element(By.ID, "formulario:horario_agendado"))
                options = [o.get_attribute('value') for o in horario_agendado.options]
            except StaleElementReferenceException:
                pass

        horario_value = '53' if refeicao == TipoRefeicao.ALMOCO else '54' if refeicao == TipoRefeicao.JANTAR else None
        if horario_value in options:
            horario_agendado.select_by_value(horario_value)
        else:
            print("No valid horário options found", end=" ")
            return

        cadastrar_button = self.wait_for_element(By.ID, "formulario:cadastrar_agendamento_bt")
        cadastrar_button.click()

        self.verificar_mensagens()

    def verificar_mensagens(self):
        erros = []
        informativos = []
        estado = threading.Event()

        def encontrar_erros():
            nonlocal erros
            try:
                resultado = self.driver.find_elements(By.CSS_SELECTOR, "ul.erros li")
                if resultado:
                    erros.extend(resultado)
                    estado.set()
            except Exception as e:
                print("Erro ao encontrar elementos de erro:", e.__class__.__name__, end=" ")

        def encontrar_informativos():
            nonlocal informativos
            try:
                resultado = self.driver.find_elements(By.CSS_SELECTOR, "ul.info li")
                if resultado:
                    informativos.extend(resultado)
                    estado.set()
            except Exception as e:
                print("Erro ao encontrar elementos informativos:", e.__class__.__name__, end=" ")

        thread_erros = threading.Thread(target=lambda: encontrar_erros() if not estado.is_set() else None)
        thread_informativos = threading.Thread(target=lambda: encontrar_informativos() if not estado.is_set() else None)

        thread_erros.start()
        thread_informativos.start()

        estado.wait()

        if erros:
            print("Erro: ", erros[0].text, end=" ")
        elif informativos:
            print("Sucesso: ", informativos[0].text, end=" ")
        else:
            print("Indefinido: Nenhuma mensagem encontrada.", end=" ")

    def quit(self):
        self.driver.quit()

def main():
    parser = argparse.ArgumentParser(description="Agendar refeição no SIGAA")
    parser.add_argument('username', type=str, help='Nome de usuário para login')
    parser.add_argument('password', type=str, help='Senha para login')
    parser.add_argument('data', type=str, help='Data para agendamento (formato DD/MM/AAAA)')
    parser.add_argument('tipo', type=str, choices=[e.value for e in TipoRefeicao], help='Tipo de refeição: 2 para Almoço, 3 para Jantar')

    args = parser.parse_args()

    agendador = AgendadorRU(username=args.username, password=args.password)
    try:
        agendador.login()
        agendador.navigate_to_agendamento()
        agendador.preencher_formulario(data=args.data, refeicao=TipoRefeicao(args.tipo))
    except Exception as e:
        print("Erro ao agendar refeição: ", e.__class__.__name__, end=" ")
    finally:
        try:
            agendador.quit()
        except Exception as e:
            print("Erro ao fechar o navegador: ", e.__class__.__name__, end=" ")
        
if __name__ == "__main__":
    main()
