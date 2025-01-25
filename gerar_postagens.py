import datetime
from datetime import timedelta
from trello_api import criar_lista_trello, criar_cartao_trello
from utilitarios import traduzir_mes, nome_dia_em_portugues, obter_dias_no_mes

# Função para gerar as postagens no Trello com as cores selecionadas
def gerar_postagens_trello(ano, board_id, key, token, textos_por_dia, dias_a_criar, datas_especificas, meses_a_gerar, cor_capa):
    datas_especificas_ordenadas = sorted(datas_especificas.items(), key=lambda x: x[0])

    # Inicializa o índice da cor
    cor_index = 0
    cores_len = len(cor_capa)

    for mes in range(1, 13):
        if mes not in meses_a_gerar:
            continue
        
        nome_mes = traduzir_mes(mes)
        lista_nome = f"{nome_mes}.{ano}"
        lista_id = criar_lista_trello(lista_nome, board_id, key, token)
        if not lista_id:
            continue

        inicio = datetime.date(ano, mes, 1)
        numero_dias = obter_dias_no_mes(ano, mes)
        fim = datetime.date(ano, mes, numero_dias)
        dias = [inicio + timedelta(days=i) for i in range((fim - inicio).days + 1)]

        semana_dias = []  # Lista para armazenar os dias da semana
        cor_atual = cor_capa[cor_index]  # Cor da semana atual

        for dia in dias:
            # Se for domingo (weekday() retorna 6 para domingo), significa que a semana terminou
            if dia.weekday() == 6:
                if semana_dias:
                    # Atribui a cor para os dias da semana anterior (domingo a sábado)
                    for dia_semana in semana_dias:
                        if nome_dia_em_portugues(dia_semana) in dias_a_criar:
                            dia_semana_ptbr = nome_dia_em_portugues(dia_semana)
                            texto_adicional = textos_por_dia.get(dia_semana_ptbr, "")
                            nome_cartao = f"{dia_semana.strftime('%d.%a').lower()} | {texto_adicional}".strip()
                            nome_cartao = nome_cartao.replace(dia_semana.strftime('%a').lower(), dia_semana_ptbr[:3])
                            criar_cartao_trello(nome_cartao, lista_id, key, token, cor_atual)

                    # Atualiza o índice da cor para a próxima semana, apenas no domingo
                    cor_index = (cor_index + 1) % cores_len
                    cor_atual = cor_capa[cor_index]  # Atualiza para a nova cor da semana
                    semana_dias.clear()  # Limpa a lista de dias da semana para começar a próxima semana

            # Adiciona o dia à lista da semana
            semana_dias.append(dia)

            # Verifica se há datas específicas para adicionar
            if dia in datas_especificas:
                texto_especifico = datas_especificas[dia]
                nome_cartao = f"{dia.strftime('%d.%a').lower()} | {texto_especifico}".strip()
                nome_cartao = nome_cartao.replace(dia.strftime('%a').lower(), nome_dia_em_portugues(dia)[:3])
                criar_cartao_trello(nome_cartao, lista_id, key, token, cor_atual)

        # Após o loop, aplica a cor para a última semana (caso o mês termine antes de um domingo)
        if semana_dias:
            for dia_semana in semana_dias:
                if nome_dia_em_portugues(dia_semana) in dias_a_criar:
                    dia_semana_ptbr = nome_dia_em_portugues(dia_semana)
                    texto_adicional = textos_por_dia.get(dia_semana_ptbr, "")
                    nome_cartao = f"{dia_semana.strftime('%d.%a').lower()} | {texto_adicional}".strip()
                    nome_cartao = nome_cartao.replace(dia_semana.strftime('%a').lower(), dia_semana_ptbr[:3])
                    criar_cartao_trello(nome_cartao, lista_id, key, token, cor_atual)
