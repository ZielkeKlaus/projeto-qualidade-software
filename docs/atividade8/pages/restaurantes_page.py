from playwright.sync_api import expect

from pages.login_page import LoginPage


class RestaurantesPage:
    def __init__(self, page):
        self.page = page
        self.login_page = LoginPage(page)
        self.campo_busca = page.locator("#searchInput")
        self.botao_buscar = page.locator("#searchBtn")
        self.cards = page.locator("#restaurantGrid .rest-card")
        self.mensagem_lista = page.locator("#restaurantGrid .loading")

    def acessar_explorar_logado(self):
        self.login_page.acessar()
        self.login_page.realizar_login("teste@email.com", "123456")
        self.page.wait_for_url("**/static/index.html", timeout=10_000)
        expect(self.cards.first).to_be_visible(timeout=10_000)

    def buscar_por_localizacao(self, termo):
        self.campo_busca.fill(termo)
        self.botao_buscar.click()
        expect(self.page.locator("#restaurantGrid")).not_to_contain_text("Buscando...")

    def limpar_busca(self):
        self.campo_busca.fill("")
        self.botao_buscar.click()
        expect(self.page.locator("#restaurantGrid")).not_to_contain_text("Buscando...")

    def validar_lista_com_resultados(self):
        expect(self.cards.first).to_be_visible(timeout=10_000)

    def validar_resultados_da_localizacao(self, localizacao):
        expect(self.cards.first).to_be_visible(timeout=10_000)
        textos = self.page.locator("#restaurantGrid .card-meta").all_text_contents()
        assert textos
        assert all(localizacao in texto for texto in textos)
