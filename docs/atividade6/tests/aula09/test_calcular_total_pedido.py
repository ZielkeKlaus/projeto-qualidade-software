import pytest

from src.local_eats_pedido import calcular_total_pedido


def test_deve_calcular_total_com_varios_itens_quando_valor_minimo_atingido():
    itens = [
        {"preco": 18.50, "quantidade": 2},
        {"preco": 12.00, "quantidade": 1},
    ]
    valor_minimo = 30.00

    resultado = calcular_total_pedido(itens, valor_minimo)

    assert resultado == 49.00


def test_deve_aceitar_pedido_quando_total_for_igual_ao_valor_minimo():
    itens = [
        {"preco": 20.00, "quantidade": 1},
        {"preco": 10.00, "quantidade": 1},
    ]
    valor_minimo = 30.00

    resultado = calcular_total_pedido(itens, valor_minimo)

    assert resultado == 30.00


def test_deve_gerar_erro_quando_total_for_menor_que_valor_minimo():
    itens = [{"preco": 12.00, "quantidade": 1}]
    valor_minimo = 25.00

    with pytest.raises(ValueError, match="Valor mínimo do pedido não atingido"):
        calcular_total_pedido(itens, valor_minimo)


def test_deve_gerar_erro_quando_preco_do_item_for_invalido():
    itens = [{"preco": 0, "quantidade": 1}]
    valor_minimo = 10.00

    with pytest.raises(ValueError, match="Preço do item deve ser maior que zero"):
        calcular_total_pedido(itens, valor_minimo)
