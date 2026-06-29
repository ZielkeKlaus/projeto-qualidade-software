from playwright.sync_api import expect


BASE_URL = "https://local-eats-unisenac.vercel.app"


class LoginPage:
    def __init__(self, page):
        self.page = page
        self.email = page.locator("#loginEmail")
        self.senha = page.locator("#loginPassword")
        self.botao_entrar = page.locator("#loginForm").get_by_role("button", name="Entrar")
        self.mensagem_erro = page.locator("#errorMsg")
        self.badge_usuario = page.locator("#userBadge")

    def acessar(self):
        self.page.goto(f"{BASE_URL}/static/login.html")

    def realizar_login(self, email, senha):
        self.email.fill(email)
        self.senha.fill(senha)
        self.botao_entrar.click()

    def validar_login_realizado(self, nome_usuario):
        self.page.wait_for_url("**/static/index.html", timeout=10_000)
        expect(self.badge_usuario).to_contain_text(f"Olá, {nome_usuario}")
        expect(self.page.locator("#restaurantGrid .rest-card").first).to_be_visible()

    def validar_mensagem_de_erro(self):
        expect(self.mensagem_erro).to_be_visible()
