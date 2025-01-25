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


def criar_cartao_trello(nome_cartao, lista_id, key, token, cor_capa):
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
        card_id = response.json()["id"]  # Obtém o ID do cartão criado
        print(f"Cartão '{nome_cartao}' criado com sucesso!")
        # Define a capa do cartão com a cor desejada
        definir_capa_cartao(card_id, key, token, cor_capa)
    else:
        print(f"Erro ao criar o cartão '{nome_cartao}': {response.status_code}, {response.text}")


def definir_capa_cartao(card_id, key, token, cor_capa):
    """
    Define a capa de um cartão Trello com a cor especificada.
    
    :param card_id: ID do cartão
    :param key: Chave de API do Trello
    :param token: Token de autenticação do Trello
    :param cor_capa: Cor da capa (exemplo: "green", "blue", "red", etc.)
    """
    url = f"https://api.trello.com/1/cards/{card_id}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {
        "cover": {
            "color": cor_capa,
            "idAttachment": None,
            "idUploadedBackground": None,
            "size": "full",
            "brightness": "light"
        }
    }

    params = {
        "key": key,
        "token": token
    }

    response = requests.put(url, headers=headers, json=payload, params=params)

    if response.status_code == 200:
        print(f"Capa do cartão '{card_id}' definida com sucesso para a cor '{cor_capa}'.")
    else:
        print(f"Erro ao definir a capa do cartão '{card_id}': {response.status_code}, {response.text}")
