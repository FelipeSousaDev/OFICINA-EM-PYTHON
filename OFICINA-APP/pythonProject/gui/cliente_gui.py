# gui/cliente_gui.py

import tkinter as tk
from tkinter import ttk, messagebox
from database_connection import get_connection

class ClienteGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Gerenciar Clientes")

        # Frames
        self.frame_form = ttk.Frame(self.master, padding="10")
        self.frame_form.grid(row=0, column=0, sticky="EW")

        self.frame_buttons = ttk.Frame(self.master, padding="10")
        self.frame_buttons.grid(row=1, column=0, sticky="EW")

        self.frame_table = ttk.Frame(self.master, padding="10")
        self.frame_table.grid(row=2, column=0, sticky="NSEW")

        # Campos do Formulário
        ttk.Label(self.frame_form, text="Nome:").grid(row=0, column=0, sticky="W")
        self.entry_nome = ttk.Entry(self.frame_form, width=50)
        self.entry_nome.grid(row=0, column=1, sticky="W")

        ttk.Label(self.frame_form, text="Endereço:").grid(row=1, column=0, sticky="W")
        self.entry_endereco = ttk.Entry(self.frame_form, width=50)
        self.entry_endereco.grid(row=1, column=1, sticky="W")

        ttk.Label(self.frame_form, text="Telefone:").grid(row=2, column=0, sticky="W")
        self.entry_telefone = ttk.Entry(self.frame_form, width=50)
        self.entry_telefone.grid(row=2, column=1, sticky="W")

        # Botões
        self.btn_adicionar = ttk.Button(self.frame_buttons, text="Adicionar Cliente", command=self.adicionar_cliente)
        self.btn_adicionar.grid(row=0, column=0, padx=5)

        self.btn_atualizar = ttk.Button(self.frame_buttons, text="Atualizar Lista", command=self.carregar_clientes)
        self.btn_atualizar.grid(row=0, column=1, padx=5)

        # Tabela
        self.tree = ttk.Treeview(self.frame_table, columns=("ID", "Nome", "Endereço", "Telefone"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Endereço", text="Endereço")
        self.tree.heading("Telefone", text="Telefone")

        self.tree.column("ID", width=50)
        self.tree.column("Nome", width=150)
        self.tree.column("Endereço", width=200)
        self.tree.column("Telefone", width=100)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Carregar dados iniciais
        self.carregar_clientes()

    def adicionar_cliente(self):
        nome = self.entry_nome.get()
        endereco = self.entry_endereco.get()
        telefone = self.entry_telefone.get()

        if nome == "":
            messagebox.showwarning("Entrada Inválida", "O campo Nome é obrigatório.")
            return

        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO CLIENTE (Nome, Endereço, Telefone)
                    VALUES (?, ?, ?)
                """, (nome, endereco, telefone))
                conn.commit()
                messagebox.showinfo("Sucesso", "Cliente adicionado com sucesso!")
                self.entry_nome.delete(0, tk.END)
                self.entry_endereco.delete(0, tk.END)
                self.entry_telefone.delete(0, tk.END)
                self.carregar_clientes()
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível adicionar o cliente.\nErro: {e}")
            finally:
                conn.close()
        else:
            messagebox.showerror("Erro de Conexão", "Não foi possível conectar ao banco de dados.")

    def carregar_clientes(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT id_cliente, Nome, Endereço, Telefone FROM CLIENTE")
                rows = cursor.fetchall()
                for row in rows:
                    self.tree.insert("", tk.END, values=row)
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível recuperar os clientes.\nErro: {e}")
            finally:
                conn.close()
        else:
            messagebox.showerror("Erro de Conexão", "Não foi possível conectar ao banco de dados.")
