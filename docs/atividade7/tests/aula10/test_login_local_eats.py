from pages.login_page import LoginPage


def test_deve_realizar_login_com_sucesso(page):
    login = LoginPage(page)

    login.acessar()
    login.realizar_login("teste@email.com", "123456")

    login.validar_login_realizado("teste")


def test_deve_exibir_mensagem_quando_login_for_invalido(page):
    login = LoginPage(page)

    login.acessar()
    login.realizar_login("usuario.invalido@teste.com", "senhaerrada")

    login.validar_mensagem_de_erro()
