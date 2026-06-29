from decimal import Decimal, ROUND_HALF_UP


def calcular_total_pedido(itens, valor_minimo):
    if not itens:
        raise ValueError("Pedido deve possuir pelo menos um item")

    valor_minimo_decimal = Decimal(str(valor_minimo))
    if valor_minimo_decimal < 0:
        raise ValueError("Valor mínimo não pode ser negativo")

    total = Decimal("0.00")

    for item in itens:
        preco = Decimal(str(item.get("preco", 0)))
        quantidade = int(item.get("quantidade", 1))

        if preco <= 0:
            raise ValueError("Preço do item deve ser maior que zero")

        if quantidade <= 0:
            raise ValueError("Quantidade do item deve ser maior que zero")

        total += preco * quantidade

    if total < valor_minimo_decimal:
        raise ValueError("Valor mínimo do pedido não atingido")

    return float(total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
