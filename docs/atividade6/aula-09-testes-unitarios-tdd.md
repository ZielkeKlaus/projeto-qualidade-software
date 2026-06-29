# Aula 9 - Testes Unitários Automatizados e TDD - LocalEats

**Aluno:** Klaus Rosa Zielke  
**Entrega:** Individual  
**Unidade Curricular:** Qualidade de Software  
**Professor:** Luciano Zanuz

## 1. Funcionalidade escolhida

A funcionalidade escolhida foi o **cálculo do total do pedido com valor mínimo**.

Essa regra soma os itens de um pedido e valida se o valor mínimo exigido pelo restaurante foi atingido. No contexto do LocalEats, essa validação evita que pedidos abaixo do limite sejam aceitos no checkout.

### Regras de negócio

- O total do pedido deve ser a soma do preço de cada item multiplicado pela quantidade.
- O pedido deve ter pelo menos um item.
- O preço de cada item deve ser maior que zero.
- A quantidade de cada item deve ser maior que zero.
- Se o total for menor que o valor mínimo, o sistema deve gerar erro.
- Se o total for igual ou maior que o valor mínimo, o pedido é válido.

## 2. Testes unitários

### Teste 1 - Deve calcular total com vários itens quando valor mínimo é atingido

**Cenário testado:** pedido com dois itens e total acima do mínimo.  
**Dados de entrada:** itens de R$ 18,50 em quantidade 2 e R$ 12,00 em quantidade 1; valor mínimo de R$ 30,00.  
**Resultado esperado:** retornar R$ 49,00 sem erro.

```python
def test_deve_calcular_total_com_varios_itens_quando_valor_minimo_atingido():
    itens = [
        {"preco": 18.50, "quantidade": 2},
        {"preco": 12.00, "quantidade": 1},
    ]
    valor_minimo = 30.00

    resultado = calcular_total_pedido(itens, valor_minimo)

    assert resultado == 49.00
```

### Teste 2 - Deve aceitar pedido quando total for igual ao valor mínimo

**Cenário testado:** pedido exatamente no valor mínimo.  
**Dados de entrada:** itens de R$ 20,00 e R$ 10,00; valor mínimo de R$ 30,00.  
**Resultado esperado:** retornar R$ 30,00 sem erro.

```python
def test_deve_aceitar_pedido_quando_total_for_igual_ao_valor_minimo():
    itens = [
        {"preco": 20.00, "quantidade": 1},
        {"preco": 10.00, "quantidade": 1},
    ]
    valor_minimo = 30.00

    resultado = calcular_total_pedido(itens, valor_minimo)

    assert resultado == 30.00
```

### Teste 3 - Deve gerar erro quando total for menor que o valor mínimo

**Cenário testado:** pedido abaixo do mínimo.  
**Dados de entrada:** item de R$ 12,00; valor mínimo de R$ 25,00.  
**Resultado esperado:** lançar `ValueError` com a mensagem "Valor mínimo do pedido não atingido".

```python
def test_deve_gerar_erro_quando_total_for_menor_que_valor_minimo():
    itens = [{"preco": 12.00, "quantidade": 1}]
    valor_minimo = 25.00

    with pytest.raises(ValueError, match="Valor mínimo do pedido não atingido"):
        calcular_total_pedido(itens, valor_minimo)
```

### Teste 4 - Deve gerar erro quando preço do item for inválido

**Cenário testado:** item com preço zero.  
**Dados de entrada:** item com preço R$ 0,00 e quantidade 1.  
**Resultado esperado:** lançar `ValueError` com a mensagem "Preço do item deve ser maior que zero".

```python
def test_deve_gerar_erro_quando_preco_do_item_for_invalido():
    itens = [{"preco": 0, "quantidade": 1}]
    valor_minimo = 10.00

    with pytest.raises(ValueError, match="Preço do item deve ser maior que zero"):
        calcular_total_pedido(itens, valor_minimo)
```

## 3. Aplicação do TDD

### Red

Primeiro foram escritos os testes em `tests/aula09/test_calcular_total_pedido.py`, antes da implementação da função. Nesse momento, a função ainda não existia e os testes falharam por erro de importação.

Exemplo da situação inicial:

```python
from src.local_eats_pedido import calcular_total_pedido

def test_deve_calcular_total_com_varios_itens_quando_valor_minimo_atingido():
    itens = [
        {"preco": 18.50, "quantidade": 2},
        {"preco": 12.00, "quantidade": 1},
    ]

    resultado = calcular_total_pedido(itens, 30.00)

    assert resultado == 49.00
```

Falha esperada no Red:

```text
ModuleNotFoundError: No module named 'src.local_eats_pedido'
```

### Green

Depois foi criada a função com o mínimo necessário para passar nos cenários principais:

```python
def calcular_total_pedido(itens, valor_minimo):
    total = sum(item["preco"] * item.get("quantidade", 1) for item in itens)

    if total < valor_minimo:
        raise ValueError("Valor mínimo do pedido não atingido")

    return total
```

### Refactor

Após os testes passarem, a função foi melhorada para validar entradas inválidas e padronizar arredondamento monetário.

```python
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
```

## 4. Refatoração

As principais melhorias realizadas foram:

- Uso de nomes claros, como `calcular_total_pedido`, `valor_minimo_decimal`, `preco` e `quantidade`.
- Validação de pedido vazio, preço inválido, quantidade inválida e valor mínimo negativo.
- Uso de `Decimal` para evitar problemas comuns de precisão com valores monetários.
- Separação das etapas de validação, cálculo e retorno.

## 5. Execução dos testes

Comando utilizado:

```bash
pytest tests/aula09
```

Evidência da execução:

```text
....                                                                     [100%]
4 passed in 0.02s
```

**Total de testes:** 4  
**Testes que passaram:** 4  
**Testes que falharam:** 0  
**Log salvo em:** `evidencias/aula09-pytest.log`

## 6. Reflexão no contexto do LocalEats

Escrever testes antes do código exigiu pensar melhor na regra de negócio antes da implementação. A maior dificuldade foi definir quais situações deveriam ser consideradas erro, porque a função não deveria apenas somar valores, mas proteger o fluxo de compra contra pedidos inválidos.

O TDD ajudou porque transformou a regra em exemplos concretos. Antes de implementar, já estava claro que o pedido abaixo do mínimo deveria falhar e que o pedido exatamente no mínimo deveria ser aceito.

Os testes aumentaram a confiança no código porque qualquer alteração futura no cálculo do pedido pode ser validada rapidamente. Se alguém alterar a forma de calcular quantidade, preço ou valor mínimo, os testes indicam se a regra principal continua funcionando.

Eu melhoraria incluindo novos testes para cupons, taxa de entrega e descontos, pois essas regras também impactam diretamente o valor final do pedido.

No projeto LocalEats, essa prática ajuda o grupo a reduzir regressões em regras centrais do checkout e facilita a manutenção do código.
