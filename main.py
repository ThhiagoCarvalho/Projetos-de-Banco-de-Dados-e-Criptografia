import tkinter as tk
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
import bcrypt
from cryptography.fernet import Fernet
from tkinter import ttk


def connect_to_mongo():
    try:
        uri = "mongodb+srv://DB_First:DB_Heitor060807@cluster0.xzfx3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        client = MongoClient(uri, server_api=ServerApi('1'))
        db = client['Loja_Virtual']
        global usuarios
        usuarios = db['usuarios'] 
        global produtos
        produtos = db['produtos']
        global transacao
        transacao = db['Transações'] 
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível conectar ao MongoDB: {str(e)}")




# Função para verificar login
def verificar_login(event=None):
    usuario = entry_usuario.get()
    senha = entry_senha.get()
    global nome
    nome = usuario

    # Busca o usuário no banco de dados
    usuario_existente = usuarios.find_one({"usuario": usuario})

    # Verifica se o usuário existe e se a senha está correta
    if usuario_existente:
        senha_armazenada = usuario_existente["senha"]

        # Se a senha armazenada for string, converta para bytes
        if isinstance(senha_armazenada, str):
            senha_armazenada = senha_armazenada.encode('utf-8')

        # Verificação da senha
        if bcrypt.checkpw(senha.encode('utf-8'), senha_armazenada):
            messagebox.showinfo("Login bem-sucedido", f"Bem-vindo, {usuario}!")
            abrir_pagina_principal()
        else:
            messagebox.showerror("Erro de login", "Usuário ou senha incorretos.")
    else:
        messagebox.showerror("Erro de login", "Usuário ou senha incorretos.")


# Função para criar novo cadastro
def criar_cadastro(event=None):
    usuario = entry_usuario.get()
    senha = entry_senha.get()
    global nome
    nome = usuario
    if usuarios.find_one({"usuario": usuario}):
        messagebox.showerror("Erro", "Usuário já existe. Escolha um nome de usuário diferente.")
    else:
        # Hash da senha com bcrypt
        hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
        usuarios.insert_one({"usuario": usuario, "senha": hashed_senha})
        messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")


def carregar_imagem_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Checa se houve erro na requisição
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img = img.resize((100, 100), Image.LANCZOS)  # Ajusta o tamanho da imagem
        return ImageTk.PhotoImage(img)
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível carregar a imagem: {str(e)}")
        return None


def abrir_pagina_principal():
    # Se a janela de login foi destruída, não tente destruí-la novamente
    if 'janela_login' in globals() and janela_login.winfo_exists():
        janela_login.destroy()
    global janela_principal
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
    botao_produtos = tk.Button(painel_controle, text="Produtos",
                               command=lambda: abrir_menu_produtos(conteudo_principal), font=("Helvetica", 14),
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
    lista_produtos = []
    for produto in produtos.find():
        # Filtra os valores para excluir o campo _id
        valores = [valor for chave, valor in produto.items() if chave != '_id']
        lista_produtos.append(valores)

    for index, (name, price, url_imagem) in enumerate(lista_produtos):
        row = index // 3  # Divisão inteira para determinar a linha
        column = index % 3  # Módulo para determinar a coluna
        create_block(conteudo_principal, name, price, url_imagem, row, column)

    # Adiciona o botão de voltar
    botao_voltar = tk.Button(janela_principal, text="Voltar", command=criar_janela_login, font=("Helvetica", 16),
                             bg="yellow", fg="black", width=10)
    botao_voltar.grid(row=1, column=2, pady=20)

    # Configurar a grade para o conteúdo principal
    conteudo_principal.grid_columnconfigure(0, weight=1)
    conteudo_principal.grid_columnconfigure(1, weight=1)
    conteudo_principal.grid_columnconfigure(2, weight=1)

    janela_principal.mainloop()

def atualizar_pagina_principal(conteudo_principal):
    # Limpa o conteúdo principal para evitar duplicação
    for widget in conteudo_principal.winfo_children():
        widget.destroy()

    # Atualiza a lista de produtos
    lista_produtos = []
    for produto in produtos.find():
        # Filtra os valores para excluir o campo _id
        valores = [valor for chave, valor in produto.items() if chave != '_id']
        lista_produtos.append(valores)

        # Re-cria os blocos de produtos
    for index, (name, price, url_imagem) in enumerate(lista_produtos):
        row = index // 3  # Divisão inteira para determinar a linha
        column = index % 3  # Módulo para determinar a coluna
        create_block(conteudo_principal, name, price, url_imagem, row, column)


def create_block(parent, name, price, url_imagem, row, column):
    """Função para criar um 'bloquinho' com nome, preço e botão de compra."""
    block = tk.Frame(parent, bg='white', padx=20, pady=20, relief='groove', bd=2)
    block.grid(row=row, column=column, padx=10, pady=10, sticky='nsew')
    imagem = carregar_imagem_url(url_imagem)
    if imagem:
        image_label = tk.Label(block, image=imagem, bg='white')
        image_label.image = imagem  # Necessário para manter a referência da imagem
        image_label.pack()

    name_label = tk.Label(block, text=f"Nome: {name}", bg='white', font=("Helvetica", 15))
    name_label.pack(anchor='w')

    price_label = tk.Label(block, text=f"Preço: R$ {price:.2f}", bg='white', font=("Helvetica", 15))
    price_label.pack(anchor='w')

    # Botão de Comprar
    buy_button = tk.Button(block, text="Comprar", bg='blue', fg='white', font=("Helvetica", 15),
                           command=lambda: abrir_janela_pagamento(name, price))
    buy_button.pack(pady=10)


from datetime import datetime

def confirmar_compra(cartao, validade, cvc, produto, p):
    """Função que confirma a compra e lida com os dados de entrada"""
    if not cartao or not validade or not cvc:
        print("Erro: Preencha todos os campos.")
        return

    try:
        # Obter a data e hora atuais
        data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Formato: Ano-Mês-Dia Hora:Minuto:Segundo

        # Criptografar os dados sensíveis
        cartao_criptografado = criptografar_dados(cartao)
        validade_criptografada = criptografar_dados(validade)
        cvc_criptografado = criptografar_dados(cvc)

        try:
            # Inserir a transação no banco de dados com a data incluída
            transacao.insert_one({
                "usuario": nome,
                "produto": produto,
                "cartao": cartao_criptografado,
                "validade": validade_criptografada,
                "cvc": cvc_criptografado,
                "preco": p,
                "data": data_atual  # Adicionando o campo de data
            })
            messagebox.showinfo("Compra Confirmada", "Compra do produto realizada com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro ao Salvar Transação", f"Erro ao salvar transação: {str(e)}")

    except Exception as e:
        print(f"Erro ao confirmar a compra: {e}")
        return


def criar_janela_pagamento(p):
    janela_pagamento = tk.Tk()
    janela_pagamento.title("Finalizar Compra")
    
    tk.Label(janela_pagamento, text="Nome do Usuário").pack()
    entry_usuario = tk.Entry(janela_pagamento)
    entry_usuario.pack(pady=5)

    tk.Label(janela_pagamento, text="Número do Cartão").pack()
    entry_cartao = tk.Entry(janela_pagamento)
    entry_cartao.pack(pady=5)

    tk.Label(janela_pagamento, text="Validade do Cartão (MM/AA)").pack()
    entry_validade = tk.Entry(janela_pagamento)
    entry_validade.pack(pady=5)

    tk.Label(janela_pagamento, text="CVC").pack()
    entry_cvc = tk.Entry(janela_pagamento)
    entry_cvc.pack(pady=5)


    btn_confirmar = tk.Button(janela_pagamento, text="Confirmar Compra", command=lambda: confirmar_compra(
    entry_cartao.get(), entry_validade.get(), entry_cvc.get(), produto))


    btn_confirmar.pack(pady=20)

    janela_pagamento.mainloop()




    
    # Supomos que você já tem o nome do usuário
    

# Função para criar a janela de pagamento
def abrir_janela_pagamento(product_name, product_price):
    """Função para abrir a janela de pagamento e pegar os dados para criptografar."""
    # Criar uma nova janela
    janela_pagamento = tk.Toplevel()
    janela_pagamento.title("Pagamento")

    # Definindo o tamanho da janela
    largura_janela = 500
    altura_janela = 400
    janela_pagamento.geometry(f"{largura_janela}x{altura_janela}")

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
                                font=("Helvetica", 12),
                                command=lambda: confirmar_compra(entry_cartao.get(), entry_validade.get(),
                                                                 entry_cvc.get(), product_name, product_price))
    botao_confirmar.pack(pady=20)


def abrir_menu_produtos(conteudo_principal):
    # Conectar ao MongoDB e acessar a coleção de produtos
    janela_produtos = tk.Tk()
    janela_produtos.title("Produtos")
    janela_produtos.attributes('-fullscreen', True)  # Tela cheia automaticamente

    # Função para exibir a lista de produtos
    def exibir_produtos():
        lista_produtos.delete(0, tk.END)  # Limpar a lista de produtos
        for produto in produtos.find():
            lista_produtos.insert(
                tk.END, f"{produto['nome']} - R${produto['preco']}"
            )

    # Função para abrir o seletor de arquivos e selecionar uma imagem

    # Função para adicionar um novo produto com imagem
    def adicionar_produto():
        nome = entry_nome.get()
        preco = entry_preco.get()
        caminho_imagem = entry_imagem.get()

        if nome and preco and caminho_imagem:
            try:
                preco = float(preco)

                # Inserir o produto no MongoDB
                produtos.insert_one({"nome": nome, "preco": preco, "imagem": caminho_imagem})
                messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
                exibir_produtos()
                atualizar_pagina_principal(conteudo_principal)
                # Atualizar a lista de produtos
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

    tk.Label(frame_formulario, text="URL da Imagem:", font=("Helvetica", 14)).grid(row=2, column=0, padx=5, pady=5)
    entry_imagem = tk.Entry(frame_formulario, font=("Helvetica", 14), width=30)
    entry_imagem.grid(row=2, column=1, padx=5, pady=5)

    botao_adicionar = tk.Button(janela_produtos, text="Adicionar Produto", font=("Helvetica", 14), bg="green",
                                fg="white",
                                command=adicionar_produto)
    botao_adicionar.pack(pady=10)

    # Botão de voltar
    botao_voltar = tk.Button(janela_produtos, text="Voltar", command=lambda: voltar_para_menu(janela_produtos),
                             font=("Helvetica", 14), bg="yellow", fg="black")
    botao_voltar.pack(pady=20)

    exibir_produtos()  # Exibir produtos ao abrir a janela

    janela_produtos.mainloop()

def gerar_chave():
    chave = Fernet.generate_key()
    return chave
# Função para voltar ao menu principal
def voltar_para_menu(janela_atual):
    janela_atual.destroy()
    abrir_pagina_principal()




def abrir_historico_transacoes():
    # Verificar se o nome do usuário está definido
    if not nome:
        print("Erro: nome do usuário não foi definido.")
        return

    # Conexão com MongoDB
    try:
        uri = "mongodb+srv://DB_First:DB_Heitor060807@cluster0.xzfx3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        client = MongoClient(uri, server_api=ServerApi('1'))
        db = client['Loja_Virtual']
        transacao = db['Transações']
        # Buscar transações do usuário
        resultados = transacao.find({"usuario": nome})
        resultados = list(resultados)  # Converter cursor para lista
    except Exception as e:
        print(f"Erro ao buscar preços e produtos: {e}")
        resultados = []
    finally:
        client.close()  # Encerrar a conexão com o MongoDB

    # Criar janela de histórico
    janela_historico = tk.Tk()
    janela_historico.title("Histórico de Transações")
    janela_historico.attributes('-fullscreen', True)

    # Título do histórico
    label_historico = tk.Label(
        janela_historico,
        text=f"Histórico de Transações de {nome}",
        font=("Helvetica", 24, "bold")
    )
    label_historico.pack(pady=20)

    # Frame para conter a tabela e a barra de rolagem
    frame_tabela = tk.Frame(janela_historico)
    frame_tabela.pack(pady=10, padx=20, fill="both", expand=True)

    # Tabela para exibir as transações
    colunas = ("Produto", "Preço", "Data")
    tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
    tabela.heading("Produto", text="Produto")
    tabela.heading("Preço", text="Preço (R$)")
    tabela.heading("Data", text="Data")
    tabela.column("Produto", anchor="center", width=200)
    tabela.column("Preço", anchor="center", width=100)
    tabela.column("Data", anchor="center", width=150)

    # Adicionar transações à tabela
    import locale
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')  # Configuração regional para BRL
    for transacao in resultados:
        produto = transacao.get("produto", "Desconhecido")
        preco = transacao.get("preco", 0.0)
        data = transacao.get("data", "Desconhecida")  # Pega a data ou define como "Desconhecida"
        preco_formatado = locale.currency(preco, grouping=True)  # Formatar preço
        tabela.insert("", "end", values=(produto, preco_formatado, data))

    # Barra de rolagem vertical
    barra_rolagem = tk.Scrollbar(frame_tabela, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=barra_rolagem.set)
    barra_rolagem.pack(side="right", fill="y")
    tabela.pack(side="left", fill="both", expand=True)

    # Botão de voltar
    botao_voltar = tk.Button(
        janela_historico,
        text="Voltar",
        command=lambda: voltar_para_menu(janela_historico),
        font=("Helvetica", 14),
        bg="#ffcc00",
        fg="black"
    )
    botao_voltar.pack(pady=20)

    # Iniciar a interface gráfica
    janela_historico.mainloop()




# Função para criar a interface de Login/Cadastro
def criar_janela_login():
    global janela_login, entry_usuario, entry_senha

    if 'janela_principal' in globals() and janela_principal.winfo_exists():
        janela_principal.destroy()
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
def criptografar_dados(dado):
    return fernet.encrypt(dado.encode())

# Chamar a função para criar a janela de login ao iniciar o programa
chave_fernet = gerar_chave()
fernet = Fernet(chave_fernet)
criar_janela_login()
