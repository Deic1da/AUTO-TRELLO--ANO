# Funções utilitárias
def traduzir_mes(mes):
    """
    Retorna o nome do mês em português e maiúsculas.
    """
    meses = [
        "JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO",
        "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"
    ]
    return meses[mes - 1]


def nome_dia_em_portugues(dia):
    """
    Retorna o nome do dia da semana em português.
    """
    dias_da_semana = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"]
    return dias_da_semana[dia.weekday()]


def obter_dias_no_mes(ano, mes):
    """
    Retorna o número de dias de um mês considerando anos bissextos.
    """
    if mes == 2:
        if (ano % 4 == 0 and (ano % 100 != 0 or ano % 400 == 0)):
            return 29
        else:
            return 28
    elif mes in [4, 6, 9, 11]:
        return 30
    else:
        return 31
