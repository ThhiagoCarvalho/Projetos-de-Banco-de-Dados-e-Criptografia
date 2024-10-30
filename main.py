import tkinter as tk
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def connect_to_mongo():
    try:
        uri = "mongodb+srv://root:123@cluster0.bqxvu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        client = MongoClient(uri, server_api=ServerApi('1'))
        db = client['Loja_Virtual']
        global usuarios
        usuarios = db['usuarios']  # Coleção para armazenar usuários
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível conectar ao MongoDB: {str(e)}")


# Função para verificar login
def verificar_login(event=None):
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    usuario_existente = usuarios.find_one({"usuario": usuario, "senha": senha})

    if usuario_existente:
        messagebox.showinfo("Login bem-sucedido", f"Bem-vindo, {usuario}!")
        abrir_pagina_principal()
    else:
        messagebox.showerror("Erro de login", "Usuário ou senha incorretos.")


# Função para criar novo cadastro
def criar_cadastro(event=None):
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    if usuarios.find_one({"usuario": usuario}):
        messagebox.showerror("Erro", "Usuário já existe. Escolha um nome de usuário diferente.")
    else:
        usuarios.insert_one({"usuario": usuario, "senha": senha})
        messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")


# Função para abrir a página principal
def abrir_pagina_principal():
    janela_login.destroy()


    janela_principal = tk.Tk()
    janela_principal.title("Página Principal")
    janela_principal.attributes('-fullscreen', True)  # Tela cheia automaticamente

    # Criar um Frame para o Painel de Controle
    painel_controle = tk.Frame(janela_principal, bg="lightgrey", padx=20, pady=20)
    painel_controle.grid(row=0, column=0, sticky="ns")

    # Criar um Frame para o Conteúdo Principal
    conteudo_principal = tk.Frame(janela_principal, bg="white", padx=20, pady=20)
    conteudo_principal.grid(row=0, column=1, sticky="nsew")

    # Configurar a grade para expansão do conteúdo principal
    janela_principal.grid_rowconfigure(0, weight=1)
    janela_principal.grid_columnconfigure(1, weight=1)

    # Título do Painel
    label_titulo_painel = tk.Label(painel_controle, text="MENU!!", font=("Helvetica", 18, "bold"), bg="lightgrey")
    label_titulo_painel.pack(pady=10)

    # Menu de Produtos
    botao_produtos = tk.Button(painel_controle, text="Produtos", command=abrir_menu_produtos, font=("Helvetica", 14),
                               bg="blue", fg="white", width=15)
    botao_produtos.pack(pady=10)

    # Menu do Carrinho

    # Menu do Histórico de Transações
    botao_historico = tk.Button(painel_controle, text="Transações", command=abrir_historico_transacoes,
                                font=("Helvetica", 14), bg="orange", fg="white", width=15)
    botao_historico.pack(pady=10)

    # Botão de Sair
    botao_sair = tk.Button(janela_principal, text="Sair", command=janela_principal.destroy, font=("Helvetica", 16),
                           bg="red", fg="white", width=10)
    botao_sair.grid(row=1, column=0, columnspan=2, pady=20)

    # Exibir conteúdo inicial
    conteudo_inicial = tk.Label(conteudo_principal, text="Bem-vindo à Loja Virtual!", font=("Helvetica", 24))
    conteudo_inicial.pack(pady=100)

    # Adiciona o botão de voltar
    botao_voltar = tk.Button(janela_principal, text="Voltar", command=criar_janela_login, font=("Helvetica", 16),
                             bg="yellow", fg="black", width=10)
    botao_voltar.grid(row=1, column=2, pady=20)

    janela_principal.mainloop()


def abrir_pagina_principal():
    # Se a janela de login foi destruída, não tente destruí-la novamente
    if 'janela_login' in globals() and janela_login.winfo_exists():
        janela_login.destroy()

    janela_principal = tk.Tk()
    janela_principal.title("Página Principal")
    janela_principal.attributes('-fullscreen', True)  # Tela cheia automaticamente

    # Criar um Frame para o Painel de Controle
    painel_controle = tk.Frame(janela_principal, bg="lightgrey", padx=20, pady=20)
    painel_controle.grid(row=0, column=0, sticky="ns")

    # Criar um Frame para o Conteúdo Principal
    conteudo_principal = tk.Frame(janela_principal, bg="white", padx=20, pady=20)
    conteudo_principal.grid(row=0, column=1, sticky="nsew")

    # Configurar a grade para expansão do conteúdo principal
    janela_principal.grid_rowconfigure(0, weight=1)
    janela_principal.grid_columnconfigure(1, weight=1)

    # Título do Painel
    label_titulo_painel = tk.Label(painel_controle, text="MENU!!", font=("Helvetica", 18, "bold"), bg="lightgrey")
    label_titulo_painel.grid(row=0, column=0, pady=10)

    # Menu de Produtos
    botao_produtos = tk.Button(painel_controle, text="Produtos", command=abrir_menu_produtos, font=("Helvetica", 14),
                               bg="blue", fg="white", width=15)
    botao_produtos.grid(row=1, column=0, pady=10)

    # Menu do Histórico de Transações
    botao_historico = tk.Button(painel_controle, text="Transações", command=abrir_historico_transacoes,
                                font=("Helvetica", 14), bg="orange", fg="white", width=15)
    botao_historico.grid(row=2, column=0, pady=10)

    # Botão de Sair
    botao_sair = tk.Button(janela_principal, text="Sair", command=janela_principal.destroy, font=("Helvetica", 16),
                           bg="red", fg="white", width=10)
    botao_sair.grid(row=1, column=0, columnspan=2, pady=20)

    # Exibir conteúdo inicial
    conteudo_inicial = tk.Label(conteudo_principal, text="Bem-vindo à Loja Virtual!", font=("Helvetica", 24))
    conteudo_inicial.grid(row=0, column=0, pady=20)

    # Adiciona os bloquinhos com informações em três colunas
    produtos = [("Produto A", 10.99), ("Produto B", 15.50), ("Produto C", 7.25),
                ("Produto D", 20.00), ("Produto E", 5.99), ("Produto F", 12.75)]

    for index, (name, price) in enumerate(produtos):
        row = index // 3  # Divisão inteira para determinar a linha
        column = index % 3  # Módulo para determinar a coluna
        create_block(conteudo_principal, name, price, row, column)

    # Adiciona o botão de voltar
    botao_voltar = tk.Button(janela_principal, text="Voltar", command=criar_janela_login, font=("Helvetica", 16),
                             bg="yellow", fg="black", width=10)
    botao_voltar.grid(row=1, column=2, pady=20)

    # Configurar a grade para o conteúdo principal
    conteudo_principal.grid_columnconfigure(0, weight=1)
    conteudo_principal.grid_columnconfigure(1, weight=1)
    conteudo_principal.grid_columnconfigure(2, weight=1)

    janela_principal.mainloop()


def create_block(parent, name, price, row, column):
    """Função para criar um 'bloquinho' com nome, preço e botão de compra."""
    block = tk.Frame(parent, bg='white', padx=20, pady=20, relief='groove', bd=2)
    block.grid(row=row, column=column, padx=10, pady=10, sticky='nsew')

    name_label = tk.Label(block, text=f"Nome: {name}", bg='white' , font=("Helvetica", 15) )
    name_label.pack(anchor='w')

    price_label = tk.Label(block, text=f"Preço: R$ {price:.2f}", bg='white', font=("Helvetica", 15))
    price_label.pack(anchor='w')

    # Botão de Comprar
    buy_button = tk.Button(block, text="Comprar", bg='blue', fg='white', font=("Helvetica", 15),
                           command=lambda: abrir_janela_pagamento(name, price))
    buy_button.pack(pady=10)

def abrir_janela_pagamento(product_name, product_price):
    """Função para abrir a janela de pagamento."""
    # Criar uma nova janela
    janela_pagamento = tk.Toplevel()
    janela_pagamento.title("Pagamento")

    # Definindo o tamanho da janela
    largura_janela = 500
    altura_janela = 400
    janela_pagamento.geometry(f"{largura_janela}x{altura_janela}")

    # Centralizar a janela na tela
    screen_width = janela_pagamento.winfo_screenwidth()
    screen_height = janela_pagamento.winfo_screenheight()
    x = (screen_width // 2) - (largura_janela // 2)
    y = (screen_height // 2) - (altura_janela // 2)
    janela_pagamento.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")

    # Informações do produto
    label_info = tk.Label(janela_pagamento, text=f"Compra: {product_name} - R$ {product_price:.2f}",
                          font=("Helvetica", 16))
    label_info.pack(pady=10)

    # Campo para número do cartão
    tk.Label(janela_pagamento, text="Número do Cartão:", font=("Helvetica", 12)).pack(pady=5)
    entry_cartao = tk.Entry(janela_pagamento, font=("Helvetica", 12), width=25)
    entry_cartao.pack(pady=5)

    # Campo para validade
    tk.Label(janela_pagamento, text="Validade (MM/AA):", font=("Helvetica", 12)).pack(pady=5)
    entry_validade = tk.Entry(janela_pagamento, font=("Helvetica", 12), width=10)
    entry_validade.pack(pady=5)

    # Campo para CVC
    tk.Label(janela_pagamento, text="CVC:", font=("Helvetica", 12)).pack(pady=5)
    entry_cvc = tk.Entry(janela_pagamento, font=("Helvetica", 12), show='*', width=10)
    entry_cvc.pack(pady=5)

    # Botão para confirmar a compra
    botao_confirmar = tk.Button(janela_pagamento, text="Confirmar Compra", bg='green', fg='white',
                                 font=("Helvetica", 12), command=lambda: confirmar_compra(entry_cartao.get(), entry_validade.get(), entry_cvc.get(), product_name))
    botao_confirmar.pack(pady=20)

def confirmar_compra(cartao, validade, cvc, product_name):
    """Função que confirma a compra e exibe uma mensagem."""
    print(f"Compra confirmada: {product_name}. Cartão: {cartao}, Validade: {validade}, CVC: {cvc}")
    messagebox.showinfo("Compra Confirmada", f"Compra do produto '{product_name}' realizada com sucesso!")


def abrir_menu_produtos():
    # Conectar ao MongoDB e acessar a coleção de produtos
    uri = "mongodb+srv://root:123@cluster0.bqxvu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['Loja_Virtual']
    produtos = db['produtos']  # Coleção de produtos
    janela_produtos = tk.Tk()
    janela_produtos.title("Produtos")
    janela_produtos.attributes('-fullscreen', True)  # Tela cheia automaticamente

    # Função para exibir a lista de produtos
    def exibir_produtos():

        for produto in produtos.find():
            lista_produtos.insert(
                tk.END, f"{produto['nome']} - R${produto['preco']}"
            )

    # Função para abrir o seletor de arquivos e selecionar uma imagem
    def selecionar_imagem():
        caminho_imagem = filedialog.askopenfilename(
            title="Selecione uma imagem",
            filetypes=[("Arquivos de imagem", "*.jpg *.png *.jpeg")]
        )
        if caminho_imagem:
            entry_imagem.config(state=tk.NORMAL)
            entry_imagem.delete(0, tk.END)
            entry_imagem.insert(0, caminho_imagem)
            entry_imagem.config(state=tk.DISABLED)

    # Função para adicionar um novo produto com imagem
    def adicionar_produto():
        nome = entry_nome.get()
        preco = entry_preco.get()
        caminho_imagem = entry_imagem.get()

        if nome and preco and caminho_imagem:
            try:
                preco = float(preco)
                with open(caminho_imagem, "rb") as img_file:
                    imagem_bytes = img_file.read()  # Ler a imagem como bytes

                # Inserir o produto no MongoDB
                produtos.insert_one({"nome": nome, "preco": preco, "imagem": imagem_bytes})
                messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
                exibir_produtos()  # Atualizar a lista de produtos
            except ValueError:
                messagebox.showerror("Erro", "O preço deve ser um valor numérico.")
        else:
            messagebox.showerror("Erro", "Preencha todos os campos e selecione uma imagem.")

    # Lista de produtos
    lista_produtos = tk.Listbox(janela_produtos, font=("Helvetica", 14), width=50, height=10)
    lista_produtos.pack(pady=20)

    # Formulário para adicionar novos produtos
    frame_formulario = tk.Frame(janela_produtos)
    frame_formulario.pack(pady=20)

    tk.Label(frame_formulario, text="Nome:", font=("Helvetica", 14)).grid(row=0, column=0, padx=5, pady=5)
    entry_nome = tk.Entry(frame_formulario, font=("Helvetica", 14))
    entry_nome.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_formulario, text="Preço:", font=("Helvetica", 14)).grid(row=1, column=0, padx=5, pady=5)
    entry_preco = tk.Entry(frame_formulario, font=("Helvetica", 14))
    entry_preco.grid(row=1, column=1, padx=5, pady=5)

    # Campo de imagem
    tk.Label(frame_formulario, text="Imagem:", font=("Helvetica", 14)).grid(row=2, column=0, padx=5, pady=5)
    entry_imagem = tk.Entry(frame_formulario, font=("Helvetica", 14), state=tk.DISABLED, width=30)
    entry_imagem.grid(row=2, column=1, padx=5, pady=5)

    botao_selecionar_imagem = tk.Button(frame_formulario, text="Selecionar Imagem", command=selecionar_imagem,
                                        font=("Helvetica", 12))
    botao_selecionar_imagem.grid(row=2, column=2, padx=5, pady=5)

    botao_adicionar = tk.Button(janela_produtos, text="Adicionar Produto", font=("Helvetica", 14), bg="green", fg="white",
                                command=adicionar_produto)
    botao_adicionar.pack(pady=10)

    # Botão de voltar
    botao_voltar = tk.Button(janela_produtos, text="Voltar", command=lambda: voltar_para_menu(janela_produtos),
                             font=("Helvetica", 14), bg="yellow", fg="black")
    botao_voltar.pack(pady=20)

    exibir_produtos()  # Exibir produtos ao abrir a janela

    janela_produtos.mainloop()

# Função para voltar ao menu principal
def voltar_para_menu(janela_atual):
    janela_atual.destroy()
    abrir_pagina_principal()

def abrir_historico_transacoes():
    janela_historico = tk.Tk()
    janela_historico.title("Histórico de Transações")
    janela_historico.attributes('-fullscreen', True)  # Tela cheia automaticamente

    label_historico = tk.Label(janela_historico, text="Aqui será o seu histórico de transações.",
                               font=("Helvetica", 20))
    label_historico.pack(pady=50)

    botao_voltar = tk.Button(janela_historico, text="Voltar", command=lambda: voltar_para_menu(janela_historico),
                             font=("Helvetica", 14), bg="yellow", fg="black")
    botao_voltar.pack(pady=20)

    janela_historico.mainloop()


# Função para voltar ao menu principal
def voltar_para_menu(janela_atual):
    janela_atual.destroy()
    abrir_pagina_principal()


# Função para criar a interface de Login/Cadastro
def criar_janela_login():
    global janela_login, entry_usuario, entry_senha

    janela_login = tk.Tk()
    janela_login.title("Sistema de Login")
    janela_login.attributes('-fullscreen', True)  # Tela cheia automaticamente

    # Conectar ao MongoDB
    connect_to_mongo()

    # Componentes de login e cadastro com layout responsivo e tamanho aumentado
    label_titulo = tk.Label(janela_login, text="Login ou Cadastro", font=("Helvetica", 24, "bold"))
    label_titulo.place(relx=0.5, rely=0.2, anchor="center")

    label_usuario = tk.Label(janela_login, text="Usuário:", font=("Helvetica", 18))
    label_usuario.place(relx=0.35, rely=0.4, anchor="e")
    entry_usuario = tk.Entry(janela_login, font=("Helvetica", 16), width=25)
    entry_usuario.place(relx=0.5, rely=0.4, anchor="center")
    entry_usuario.focus()  # Define o foco inicial no campo de usuário

    label_senha = tk.Label(janela_login, text="Senha:", font=("Helvetica", 18))
    label_senha.place(relx=0.35, rely=0.5, anchor="e")
    entry_senha = tk.Entry(janela_login, show="*", font=("Helvetica", 16), width=25)  # show="*" oculta a senha
    entry_senha.place(relx=0.5, rely=0.5, anchor="center")

    # Botões de Login e Cadastro
    botao_login = tk.Button(janela_login, text="Entrar", command=verificar_login, font=("Helvetica", 14), bg="blue",
                            fg="white", width=12)
    botao_login.place(relx=0.4, rely=0.6, anchor="center")

    botao_cadastro = tk.Button(janela_login, text="Cadastrar", command=criar_cadastro, font=("Helvetica", 14),
                               bg="green", fg="white", width=12)
    botao_cadastro.place(relx=0.6, rely=0.6, anchor="center")

    # Botão de Sair no canto inferior direito da tela
    botao_sair = tk.Button(janela_login, text="Sair", command=janela_login.destroy, font=("Helvetica", 14), bg="red",
                           fg="white", width=10)
    botao_sair.place(relx=0.98, rely=0.98, anchor="se")  # Posicionado com margem das bordas

    # Permitir foco nas entradas clicando nelas
    entry_usuario.bind("<Button-1>", lambda event: entry_usuario.focus())
    entry_senha.bind("<Button-1>", lambda event: entry_senha.focus())

    # Adicionando bind para a tecla de retorno
    entry_usuario.bind("<Return>", lambda event: entry_senha.focus())  # Move para a senha
    entry_senha.bind("<Return>", verificar_login)  # Aciona login ao pressionar Enter na senha

    # Desativando os botões até que haja texto nas entradas
    def update_buttons_state(*args):
        if entry_usuario.get() and entry_senha.get():
            botao_login.config(state=tk.NORMAL)
            botao_cadastro.config(state=tk.NORMAL)
        else:
            botao_login.config(state=tk.DISABLED)
            botao_cadastro.config(state=tk.DISABLED)

    # Atualiza o estado dos botões quando o texto é alterado
    entry_usuario.bind("<KeyRelease>", update_buttons_state)
    entry_senha.bind("<KeyRelease>", update_buttons_state)

    # Iniciar desabilitando os botões
    botao_login.config(state=tk.DISABLED)
    botao_cadastro.config(state=tk.DISABLED)

    janela_login.mainloop()


# Chamar a função para criar a janela de login ao iniciar o programa
criar_janela_login()