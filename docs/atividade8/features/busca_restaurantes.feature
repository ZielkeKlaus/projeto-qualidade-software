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
