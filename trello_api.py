import requests


def criar_lista_trello(nome_lista, board_id, key, token):
    """
    Cria uma lista no Trello.
    """
    url_lista = "https://api.trello.com/1/lists"
    query_lista = {
        "name": nome_lista,
        "idBoard": board_id,
        "key": key,
        "token": token
    }
    response = requests.post(url_lista, params=query_lista)
    if response.status_code == 200:
        lista_id = response.json().get("id")
        print(f"Lista '{nome_lista}' criada com sucesso!")
        return lista_id
    else:
        print(f"Erro ao criar a lista '{nome_lista}': {response.status_code}, {response.text}")
        return None


def criar_cartao_trello(nome_cartao, lista_id, key, token):
    """
    Cria um cartão em uma lista no Trello.
    """
    url_cartao = "https://api.trello.com/1/cards"
    query_cartao = {
        "name": nome_cartao,
        "idList": lista_id,
        "key": key,
        "token": token
    }
    response = requests.post(url_cartao, params=query_cartao)
    if response.status_code == 200:
        print(f"Cartão '{nome_cartao}' criado com sucesso!")
    else:
        print(f"Erro ao criar o cartão '{nome_cartao}': {response.status_code}, {response.text}")
