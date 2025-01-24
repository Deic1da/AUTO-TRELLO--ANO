import tkinter as tk
from tkinter import filedialog, messagebox
import datetime
from gerar_postagens import gerar_postagens_trello

# Caminho do arquivo para salvar/recarregar as variáveis
config_file = "config.txt"

# Função para carregar as configurações do arquivo
def carregar_config():
    try:
        with open(config_file, "r", encoding="utf-8") as file:
            for line in file:
                key, value = line.strip().split("=", 1)
                if key == "key":
                    entry_key.insert(0, value)
                elif key == "token":
                    entry_token.insert(0, value)
                elif key == "board_id":
                    entry_board_id.insert(0, value)
    except FileNotFoundError:
        pass  # Arquivo ainda não existe, nada será carregado
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar configurações: {e}")

# Função para salvar as configurações no arquivo
def salvar_config():
    try:
        with open(config_file, "w", encoding="utf-8") as file:
            file.write(f"key={entry_key.get()}\n")
            file.write(f"token={entry_token.get()}\n")
            file.write(f"board_id={entry_board_id.get()}\n")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar configurações: {e}")

# Função para carregar as datas específicas de um arquivo
def carregar_datas():
    try:
        arquivo = filedialog.askopenfilename(title="Selecione o arquivo de datas", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if arquivo:
            with open(arquivo, "r", encoding="utf-8") as file:
                lines = file.readlines()
                datas_especificas.clear()  # Limpa o dicionário antes de carregar novas datas
                for line in lines:
                    if line.strip() and not line.startswith("#"):
                        date_part, descricao = line.strip().split(":")
                        dia, mes = map(int, date_part.strip("()").split(","))
                        descricao = descricao.strip().strip('"')
                        ano = int(entry_ano.get())  # Captura o ano da entrada
                        data_completa = datetime.date(ano, mes, dia)  # Usa datetime.date corretamente
                        datas_especificas[data_completa] = descricao
            lbl_status["text"] = "Datas carregadas com sucesso!"
            atualizar_lista_datas()
        else:
            lbl_status["text"] = "Nenhum arquivo selecionado."
    except Exception as e:
        lbl_status["text"] = f"Erro ao carregar datas: {e}"

# Função para exibir as datas carregadas na lista
def atualizar_lista_datas():
    lista_datas.delete(0, tk.END)
    for data, descricao in sorted(datas_especificas.items()):
        lista_datas.insert(tk.END, f"datetime.date({data.year}, {data.month}, {data.day}): \"{descricao}\"")

# Função para adicionar ou remover os dias da lista dias_a_criar
def atualizar_dias_a_criar():
    dias_a_criar.clear()
    for dia, var in checkboxes_dias.items():
        if var.get() == 1:  # Se o Checkbutton estiver marcado
            dias_a_criar.append(dia)
    print("Dias a criar:", dias_a_criar)

# Função para executar a função gerar_postagens_trello
def executar_gerar_postagens():
    try:
        # Capturar valores dos campos
        key = entry_key.get()
        token = entry_token.get()
        board_id = entry_board_id.get()
        ano = int(entry_ano.get())
        
        dias_a_criar = [dia for dia, var in checkboxes_dias.items() if var.get() == 1]
        textos_por_dia = {dia: entry_textos[dia].get() for dia in entry_textos}
        
        # Salvar configurações antes de executar
        salvar_config()
        
        # Exibir dados no console para verificar
        print("Key:", key)
        print("Token:", token)
        print("Board ID:", board_id)
        print("Ano:", ano)
        print("Dias a criar:", dias_a_criar)
        print("Textos por dia:", textos_por_dia)
        print("Datas específicas:", datas_especificas)
        
        # Chamar a função
        gerar_postagens_trello(ano, board_id, key, token, textos_por_dia, dias_a_criar, datas_especificas)
        messagebox.showinfo("Sucesso", "Postagens geradas com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao executar: {e}")

# Inicializa o dicionário de datas específicas e dias a criar
datas_especificas = {}
dias_a_criar = []

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

# Checkbuttons para dias a criar (incluindo sábado e domingo)
checkboxes_dias = {}
dias_semana = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"]
for i, dia in enumerate(dias_semana):
    var = tk.IntVar()
    cb = tk.Checkbutton(frame_body, text=dia, variable=var, command=atualizar_dias_a_criar)
    cb.grid(row=i + 1, column=0, sticky="w")
    checkboxes_dias[dia] = var

# Entradas para textos por dia
entry_textos = {}
for i, dia in enumerate(dias_semana):
    tk.Label(frame_body, text=f"Texto para {dia}:").grid(row=i + 1, column=1, sticky="e")
    entry = tk.Entry(frame_body, width=30)
    entry.grid(row=i + 1, column=2, sticky="w")
    entry_textos[dia] = entry

# Lista de datas carregadas
frame_direito = tk.Frame(root, padx=10, pady=10)
frame_direito.pack(fill="both", expand=True)

tk.Label(frame_direito, text="Datas Carregadas:").pack(anchor="w")
lista_datas = tk.Listbox(frame_direito, height=10, width=60)
lista_datas.pack(fill="both", expand=True)

# Botões
frame_buttons = tk.Frame(root, padx=10, pady=10)
frame_buttons.pack(fill="x")

btn_carregar = tk.Button(frame_buttons, text="Carregar Datas", command=carregar_datas)
btn_carregar.pack(side="left", padx=5)

btn_executar = tk.Button(frame_buttons, text="Gerar Postagens", command=executar_gerar_postagens)
btn_executar.pack(side="right", padx=5)

lbl_status = tk.Label(root, text="", anchor="w")
lbl_status.pack(fill="x", padx=10, pady=5)

# Carregar configurações ao iniciar o programa
carregar_config()

root.mainloop()