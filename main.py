import tkinter as tk
from tkinter import filedialog, messagebox
import datetime
from gerar_postagens import gerar_postagens_trello

# Caminho do arquivo para salvar/recarregar as configurações
CONFIG_FILE = "config.txt"

# Inicializa os dados globais
datas_especificas = {}
dias_a_criar = []
meses_a_gerar = []
cor_capa = []

# Função para carregar as configurações do arquivo
def carregar_config():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            for line in file:
                key, value = line.strip().split("=", 1)
                if key == "key":
                    entry_key.insert(0, value)
                elif key == "token":
                    entry_token.insert(0, value)
                elif key == "board_id":
                    entry_board_id.insert(0, value)
    except FileNotFoundError:
        pass  # Arquivo ainda não existe
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar configurações: {e}")

# Função para salvar as configurações no arquivo
def salvar_config():
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as file:
            file.write(f"key={entry_key.get()}\n")
            file.write(f"token={entry_token.get()}\n")
            file.write(f"board_id={entry_board_id.get()}\n")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar configurações: {e}")

# Função para atualizar as cores selecionadas
def atualizar_cores_selecionadas():
    global cor_capa
    cor_capa.clear()  # Limpa a lista de cores
    for cor, var in checkboxes_cores.items():
        if var.get() == 1:
            cor_capa.append(cor)
    print("Cores selecionadas:", cor_capa)

# Adicionando checkboxes para cores
def criar_checkboxes_cores(frame):
    global checkboxes_cores
    cores_disponiveis = ["blue", "green", "yellow", "orange", "red", "purple", "pink", "lime", "black"]
    checkboxes_cores = {}
    
    for i, cor in enumerate(cores_disponiveis):
        var = tk.IntVar()
        # Adiciona o checkbox
        tk.Checkbutton(frame, text=cor.capitalize(), variable=var, command=atualizar_cores_selecionadas).grid(row=i + 1, column=0, sticky="w")
        # Adiciona o quadrado colorido ao lado do checkbox
        canvas = tk.Canvas(frame, width=20, height=20, bg=cor)
        canvas.grid(row=i + 1, column=1, padx=5)
        checkboxes_cores[cor] = var

# Função para carregar datas específicas de um arquivo
def carregar_datas():
    try:
        arquivo = filedialog.askopenfilename(title="Selecione o arquivo de datas", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if arquivo:
            with open(arquivo, "r", encoding="utf-8") as file:
                datas_especificas.clear()
                for line in file:
                    if line.strip() and not line.startswith("#"):
                        date_part, descricao = line.strip().split(":")
                        dia, mes = map(int, date_part.strip("()").split(","))
                        descricao = descricao.strip().strip('"')
                        ano = int(entry_ano.get())
                        data_completa = datetime.date(ano, mes, dia)
                        datas_especificas[data_completa] = descricao
            lbl_status["text"] = "Datas carregadas com sucesso!"
            atualizar_lista_datas()
        else:
            lbl_status["text"] = "Nenhum arquivo selecionado."
    except Exception as e:
        lbl_status["text"] = f"Erro ao carregar datas: {e}"

# Atualiza a lista de datas exibida
def atualizar_lista_datas():
    lista_datas.delete(0, tk.END)
    for data, descricao in sorted(datas_especificas.items()):
        lista_datas.insert(tk.END, f"{data}: \"{descricao}\"")

# Atualiza os dias a criar com base nos checkboxes
def atualizar_dias_a_criar():
    dias_a_criar.clear()
    for dia, var in checkboxes_dias.items():
        if var.get() == 1:
            dias_a_criar.append(dia)

# Função para atualizar os meses a gerar com base nos checkboxes
def atualizar_meses_a_gerar():
    meses_a_gerar.clear()
    for numero_mes, var in checkboxes_meses.items():
        if var.get() == 1:  # Checkbox marcado
            meses_a_gerar.append(numero_mes)
    print("Meses a gerar:", meses_a_gerar)

# Função para gerar as postagens no Trello com as cores selecionadas
def executar_gerar_postagens():
    try:
        key = entry_key.get()
        token = entry_token.get()
        board_id = entry_board_id.get()
        ano = int(entry_ano.get())
        
        dias_a_criar = [dia for dia, var in checkboxes_dias.items() if var.get() == 1]
        textos_por_dia = {dia: entry_textos[dia].get() for dia in entry_textos}
        
        salvar_config()

        gerar_postagens_trello(ano, board_id, key, token, textos_por_dia, dias_a_criar, datas_especificas, meses_a_gerar, cor_capa)
        messagebox.showinfo("Sucesso", "Postagens geradas com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao executar: {e}")

# Criação da interface
root = tk.Tk()
root.title("Gerador de Postagens no Trello")

# Cabeçalho
frame_top = tk.Frame(root, padx=10, pady=10)
frame_top.pack(fill="x")

tk.Label(frame_top, text="Key:").grid(row=0, column=0, sticky="e")
entry_key = tk.Entry(frame_top, width=50)
entry_key.grid(row=0, column=1)

tk.Label(frame_top, text="Token:").grid(row=1, column=0, sticky="e")
entry_token = tk.Entry(frame_top, width=50)
entry_token.grid(row=1, column=1)

tk.Label(frame_top, text="Board ID:").grid(row=2, column=0, sticky="e")
entry_board_id = tk.Entry(frame_top, width=50)
entry_board_id.grid(row=2, column=1)

# Corpo
frame_body = tk.Frame(root, padx=10, pady=10)
frame_body.pack(fill="x")

tk.Label(frame_body, text="Ano:").grid(row=0, column=0, sticky="e")
entry_ano = tk.Entry(frame_body, width=10)
entry_ano.grid(row=0, column=1, sticky="w")
entry_ano.insert(0, "2025")

# Criando a interface
frame_cores = tk.Frame(root, padx=10, pady=10)
frame_cores.pack(fill="x")

tk.Label(frame_cores, text="Selecione as cores:").grid(row=0, column=0, columnspan=3, sticky="w")
criar_checkboxes_cores(frame_cores)

# Checkboxes para dias da semana
checkboxes_dias = {}
dias_semana = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"]
for i, dia in enumerate(dias_semana):
    var = tk.IntVar()
    tk.Checkbutton(frame_body, text=dia, variable=var, command=atualizar_dias_a_criar).grid(row=i + 1, column=0, sticky="w")
    checkboxes_dias[dia] = var

# Entradas para textos por dia
entry_textos = {}
for i, dia in enumerate(dias_semana):
    tk.Label(frame_body, text=f"Texto para {dia}:").grid(row=i + 1, column=1, sticky="e")
    entry = tk.Entry(frame_body, width=30)
    entry.grid(row=i + 1, column=2, sticky="w")
    entry_textos[dia] = entry

# Checkboxes para meses
checkboxes_meses = {}
nomes_meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
               "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

frame_meses = tk.Frame(root, padx=10, pady=10)
frame_meses.pack(fill="x")

tk.Label(frame_meses, text="Selecione os meses:").grid(row=0, column=0, columnspan=3, sticky="w")

for i, nome_mes in enumerate(nomes_meses, start=1):  # Enumerar a partir de 1
    var = tk.IntVar()
    tk.Checkbutton(frame_meses, text=nome_mes, variable=var, command=atualizar_meses_a_gerar).grid(row=(i - 1) // 4 + 1, column=(i - 1) % 4, sticky="w")
    checkboxes_meses[i] = var  # Usar o número do mês como chave

# Lista de datas carregadas
frame_direito = tk.Frame(root, padx=10, pady=10)
frame_direito.pack(fill="both", expand=True)

tk.Label(frame_direito, text="Datas Carregadas:").pack(anchor="w")
lista_datas = tk.Listbox(frame_direito, height=10, width=60)
lista_datas.pack(fill="both", expand=True)

# Botões
frame_buttons = tk.Frame(root, padx=10, pady=10)
frame_buttons.pack(fill="x")

tk.Button(frame_buttons, text="Carregar Datas", command=carregar_datas).pack(side="left", padx=5)
tk.Button(frame_buttons, text="Gerar Postagens", command=executar_gerar_postagens).pack(side="right", padx=5)

lbl_status = tk.Label(root, text="", anchor="w")
lbl_status.pack(fill="x", padx=10, pady=5)

# Carrega configurações ao iniciar
carregar_config()

root.mainloop()
