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
