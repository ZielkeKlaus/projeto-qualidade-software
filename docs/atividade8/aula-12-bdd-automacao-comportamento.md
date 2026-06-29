# Aula 12 - BDD e Automação Orientada a Comportamento - LocalEats

**Aluno:** Klaus Rosa Zielke  
**Entrega:** Individual  
**Unidade Curricular:** Qualidade de Software  
**Professor:** Luciano Zanuz

## 1. Fluxo escolhido

O fluxo escolhido foi **busca de restaurantes**.

Esse comportamento permite que o usuário pesquise restaurantes por localização. No LocalEats, a busca melhora a experiência porque reduz o esforço para encontrar opções disponíveis em uma região específica.

### Cenários esperados

- Busca válida retorna resultados.
- Campo vazio mantém a listagem de restaurantes.
- A lista deve permanecer compreensível para o usuário após a busca.

## 2. Escrita dos cenários BDD

Arquivo criado: `features/busca_restaurantes.feature`

```gherkin
Feature: Busca de restaurantes
  Como usuário do LocalEats
  Quero pesquisar restaurantes por localização
  Para encontrar opções próximas com mais rapidez

  Scenario: Buscar restaurantes por uma localização existente
    Given que o usuário acessa a página Explorar autenticado
    When pesquisar pela localização "Centro"
    Then o sistema deve exibir restaurantes da localização "Centro"

  Scenario: Manter listagem ao pesquisar com campo vazio
    Given que o usuário acessa a página Explorar autenticado
    When pesquisar com o campo de busca vazio
    Then o sistema deve manter a listagem de restaurantes disponível
```

## 3. Implementação da automação com pytest-bdd

Arquivo criado: `tests/aula12/test_busca_restaurantes_bdd.py`

```python
from pytest_bdd import given, scenarios, then, when

from pages.restaurantes_page import RestaurantesPage


scenarios("../../features/busca_restaurantes.feature")


@given("que o usuário acessa a página Explorar autenticado")
def acessar_pagina_explorar(page):
    restaurantes = RestaurantesPage(page)
    restaurantes.acessar_explorar_logado()
    page.restaurantes_page = restaurantes


@when('pesquisar pela localização "Centro"')
def pesquisar_por_centro(page):
    page.restaurantes_page.buscar_por_localizacao("Centro")


@when("pesquisar com o campo de busca vazio")
def pesquisar_com_campo_vazio(page):
    page.restaurantes_page.limpar_busca()


@then('o sistema deve exibir restaurantes da localização "Centro"')
def validar_resultados_de_centro(page):
    page.restaurantes_page.validar_resultados_da_localizacao("Centro")


@then("o sistema deve manter a listagem de restaurantes disponível")
def validar_listagem_disponivel(page):
    page.restaurantes_page.validar_lista_com_resultados()
```

## 4. Organização do projeto

Estrutura utilizada:

```text
projeto/
├── features/
│   └── busca_restaurantes.feature
├── pages/
│   ├── login_page.py
│   └── restaurantes_page.py
├── src/
│   └── local_eats_pedido.py
├── tests/
│   ├── aula09/
│   │   └── test_calcular_total_pedido.py
│   ├── aula10/
│   │   └── test_login_local_eats.py
│   ├── aula12/
│   │   └── test_busca_restaurantes_bdd.py
│   └── conftest.py
└── evidencias/
```

## 5. Execução dos testes

Comando utilizado:

```bash
pytest tests/aula12
```

Evidência da execução:

```text
..                                                                       [100%]
2 passed in 6.98s
```

**Total de cenários automatizados:** 2  
**Cenários que passaram:** 2  
**Cenários que falharam:** 0  
**Log salvo em:** `evidencias/aula12-pytest.log`

## 6. Análise crítica

O cenário escrito ficou compreensível porque descreve o comportamento esperado sem citar detalhes técnicos como IDs, classes CSS ou chamadas de API. Uma pessoa não técnica consegue entender que o objetivo é buscar restaurantes por localização.

O teste automatizado ficou legível porque os passos Given, When e Then ficaram separados e cada um chama métodos de uma Page Object. Isso evita repetir cliques e seletores dentro dos steps.

O BDD ajudou a entender o comportamento porque obrigou a escrever primeiro a intenção do usuário. Em vez de começar pelo código, o fluxo foi descrito como uma regra observável: pesquisar por "Centro" deve exibir restaurantes daquela localização.

As principais dificuldades foram lidar com autenticação antes de acessar a página Explorar e aguardar o carregamento assíncrono dos restaurantes.

Os seletores ainda podem ser considerados frágeis porque dependem de IDs e classes existentes no HTML, como `#searchInput`, `#searchBtn` e `.rest-card`. Eles são melhores do que seletores por posição, mas atributos `data-testid` seriam mais adequados para automação.

O teste ficou dependente da interface porque interage com campos, botões e cards renderizados. Essa dependência é esperada em testes E2E, mas aumenta o custo de manutenção quando o frontend muda.

O cenário representa uma regra de negócio do ponto de vista do usuário: encontrar restaurantes por localização. Isso apoia a descoberta de restaurantes, que é uma parte central da proposta do LocalEats.

Para tornar o teste mais robusto, eu adicionaria dados fixos em ambiente de teste, `data-testid` nos elementos principais, autenticação por fixture e menos dependência da conta compartilhada.

## 7. Reflexão no contexto do LocalEats

BDD melhora a comunicação entre equipe porque transforma requisitos em exemplos executáveis e legíveis. Isso facilita o alinhamento entre desenvolvimento, qualidade e regras de negócio.

Nem todo teste deve ser escrito em BDD. O BDD vale mais para comportamentos importantes do usuário e regras que precisam ser entendidas por pessoas técnicas e não técnicas.

Vale a pena usar BDD quando o fluxo tem impacto direto para o negócio, como busca, checkout, login e histórico de pedidos.

O comportamento ficou mais claro porque o cenário descreve intenção e resultado esperado, não apenas cliques. No projeto do grupo, isso ajuda a manter uma documentação viva do que o sistema deve fazer.
