# Aula 10 - Testes Funcionais Automatizados - LocalEats

**Aluno:** Klaus Rosa Zielke  
**Entrega:** Individual  
**Unidade Curricular:** Qualidade de Software  
**Professor:** Luciano Zanuz

## 1. Fluxo funcional escolhido

O fluxo escolhido foi **login de usuário**.

Esse fluxo permite autenticar o usuário no LocalEats e liberar o acesso às funcionalidades principais do sistema, como explorar restaurantes, visualizar favoritos e consultar pedidos.

### Cenários esperados

- Login válido deve redirecionar o usuário para a página Explorar.
- Login inválido deve exibir mensagem de erro.
- Campos vazios devem ser bloqueados pela validação obrigatória do formulário.

## 2. Teste automatizado com Codegen

Comando utilizado como ponto de partida:

```bash
playwright codegen https://local-eats-unisenac.vercel.app/static/login.html
```

### Código inicial gerado

```python
def test_login_codegen(page):
    page.goto("https://local-eats-unisenac.vercel.app/static/login.html")
    page.locator("#loginEmail").fill("teste@email.com")
    page.locator("#loginPassword").fill("123456")
    page.get_by_role("button", name="Entrar").click()
```

### Fluxo gravado

1. Acessar a página de login.
2. Preencher e-mail.
3. Preencher senha.
4. Clicar no botão Entrar.
5. Validar redirecionamento para a página Explorar.

### Observações iniciais

O Codegen ajudou a identificar os seletores reais da tela, principalmente `#loginEmail`, `#loginPassword` e o botão com texto "Entrar".

Por outro lado, o código gerado era muito direto e pouco reutilizável. Ele não separava comportamento da página, não tinha nomes de métodos claros e não incluía uma validação forte do resultado final.

## 3. Implementação com Pytest

Arquivo criado: `tests/aula10/test_login_local_eats.py`

```python
from pages.login_page import LoginPage


def test_deve_realizar_login_com_sucesso(page):
    login = LoginPage(page)

    login.acessar()
    login.realizar_login("teste@email.com", "123456")

    login.validar_login_realizado("teste")
```

Também foi criado um cenário negativo:

```python
def test_deve_exibir_mensagem_quando_login_for_invalido(page):
    login = LoginPage(page)

    login.acessar()
    login.realizar_login("usuario.invalido@teste.com", "senhaerrada")

    login.validar_mensagem_de_erro()
```

## 4. Refatoração com Page Object Model

Arquivo criado: `pages/login_page.py`

```python
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
```

### Melhorias aplicadas

- Separação entre teste e ações da página.
- Centralização dos seletores no Page Object.
- Nomes de métodos alinhados ao comportamento do usuário.
- Assertions mais relevantes, validando redirecionamento, badge do usuário e carregamento da lista de restaurantes.
- Inclusão de cenário negativo para login inválido.

## 5. Execução dos testes

Comando utilizado:

```bash
pytest tests/aula10
```

Evidência da execução:

```text
..                                                                       [100%]
2 passed in 4.99s
```

**Total de testes:** 2  
**Testes que passaram:** 2  
**Testes que falharam:** 0  
**Log salvo em:** `evidencias/aula10-pytest.log`

## 6. Análise crítica dos testes

O teste quebrou inicialmente quando foi utilizada a URL principal sem `/static`, porque alguns arquivos do frontend estão organizados dentro dessa rota. Após ajustar o endereço para `https://local-eats-unisenac.vercel.app/static/login.html`, o fluxo passou a representar melhor a navegação real do sistema.

Também houve uma falha inicial por seletor ambíguo: o texto "Entrar" aparecia no botão de alternância do formulário e no botão de envio. A correção foi restringir o seletor ao formulário de login com `page.locator("#loginForm").get_by_role("button", name="Entrar")`.

Os seletores mais simples foram os IDs dos campos de login, como `#loginEmail` e `#loginPassword`. O seletor do botão foi feito por papel e nome visível, mas limitado ao formulário correto, o que é mais legível do que depender de classes CSS soltas.

O Codegen ajudou a capturar rapidamente o fluxo, mas gerou uma base muito linear. A refatoração com POM tornou o teste mais fácil de manter.

O teste é confiável para o fluxo principal, pois valida o comportamento percebido pelo usuário: login, redirecionamento e carregamento da área Explorar. Ainda assim, ele depende da disponibilidade da aplicação e da conta de teste.

Para torná-lo mais robusto, seria ideal ter uma massa de dados própria para testes automatizados, ambiente estável e seletores com atributos específicos como `data-testid`.

Os principais riscos de manutenção são mudanças no HTML, alteração da rota `/static/login.html`, mudança de mensagem visual ou indisponibilidade da API de autenticação.

## 7. Reflexão no contexto do LocalEats

Testes automatizados não substituem totalmente testes manuais. Eles reduzem repetição e validam fluxos importantes com rapidez, mas testes manuais ainda são úteis para explorar usabilidade, acessibilidade e comportamentos inesperados.

Não vale a pena automatizar todos os fluxos. O ideal é priorizar fluxos críticos, repetitivos e de alto impacto, como login, busca, checkout e histórico de pedidos.

No LocalEats, esse teste ajuda o grupo porque o login é a porta de entrada do sistema. Se ele quebrar, várias funcionalidades deixam de ser acessíveis. Automatizar esse fluxo aumenta a confiança antes de mudanças e deploys.
