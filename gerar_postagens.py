import datetime
from datetime import timedelta
from trello_api import criar_lista_trello, criar_cartao_trello
from utilitarios import traduzir_mes, nome_dia_em_portugues, obter_dias_no_mes

def gerar_postagens_trello(ano, board_id, key, token, textos_por_dia, dias_a_criar, datas_especificas):
    """
    Gera listas e cartões para um ano inteiro no Trello, incluindo os cartões para dias específicos organizados por data.
    """
    # Ordenar as datas específicas em ordem crescente
    datas_especificas_ordenadas = sorted(datas_especificas.items(), key=lambda x: x[0])

    for mes in range(1, 13):
        nome_mes = traduzir_mes(mes)
        lista_nome = f"{nome_mes}.{ano}"  # Nome da lista
        lista_id = criar_lista_trello(lista_nome, board_id, key, token)
        if not lista_id:
            continue  # Pula para o próximo mês se não conseguir criar a lista

        # Criar cartões para cada dia do mês
        inicio = datetime.date(ano, mes, 1)
        numero_dias = obter_dias_no_mes(ano, mes)
        fim = datetime.date(ano, mes, numero_dias)
        dias = [inicio + timedelta(days=i) for i in range((fim - inicio).days + 1)]

        for dia in dias:
            # Verifica se a data atual é uma data específica
            if dia in datas_especificas:
                texto_especifico = datas_especificas[dia]
                nome_cartao = f"{dia.strftime('%d.%a').lower()} | {texto_especifico}".strip()
                nome_cartao = nome_cartao.replace(dia.strftime('%a').lower(), nome_dia_em_portugues(dia)[:3])
                criar_cartao_trello(nome_cartao, lista_id, key, token)

            # Verifica se o dia da semana está na lista de dias a serem criados
            if nome_dia_em_portugues(dia) in dias_a_criar:
                dia_semana_ptbr = nome_dia_em_portugues(dia)
                texto_adicional = textos_por_dia.get(dia_semana_ptbr, "")
                nome_cartao = f"{dia.strftime('%d.%a').lower()} | {texto_adicional}".strip()
                nome_cartao = nome_cartao.replace(dia.strftime('%a').lower(), dia_semana_ptbr[:3])
                criar_cartao_trello(nome_cartao, lista_id, key, token)
