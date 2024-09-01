# gui/veiculo_gui.py

import tkinter as tk
from tkinter import ttk, messagebox
from database_connection import get_connection

class VeiculoGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Gerenciar Veículos")

        # Frames
        self.frame_form = ttk.Frame(self.master, padding="10")
        self.frame_form.grid(row=0, column=0, sticky="EW")

        self.frame_buttons = ttk.Frame(self.master, padding="10")
        self.frame_buttons.grid(row=1, column=0, sticky="EW")

        self.frame_table = ttk.Frame(self.master, padding="10")
        self.frame_table.grid(row=2, column=0, sticky="NSEW")

        # Campos do Formulário
        ttk.Label(self.frame_form, text="Placa:").grid(row=0, column=0, sticky="W")
        self.entry_placa = ttk.Entry(self.frame_form, width=20)
        self.entry_placa.grid(row=0, column=1, sticky="W")

        ttk.Label(self.frame_form, text="Modelo:").grid(row=1, column=0, sticky="W")
        self.entry_modelo = ttk.Entry(self.frame_form, width=50)
        self.entry_modelo.grid(row=1, column=1, sticky="W")

        ttk.Label(self.frame_form, text="Ano:").grid(row=2, column=0, sticky="W")
        self.entry_ano = ttk.Entry(self.frame_form, width=20)
        self.entry_ano.grid(row=2, column=1, sticky="W")

        ttk.Label(self.frame_form, text="ID do Cliente:").grid(row=3, column=0, sticky="W")
        self.entry_id_cliente = ttk.Entry(self.frame_form, width=20)
        self.entry_id_cliente.grid(row=3, column=1, sticky="W")

        # Botões
        self.btn_adicionar = ttk.Button(self.frame_buttons, text="Adicionar Veículo", command=self.adicionar_veiculo)
        self.btn_adicionar.grid(row=0, column=0, padx=5)

        self.btn_atualizar = ttk.Button(self.frame_buttons, text="Atualizar Lista", command=self.carregar_veiculos)
        self.btn_atualizar.grid(row=0, column=1, padx=5)

        # Tabela
        self.tree = ttk.Treeview(self.frame_table, columns=("ID", "Placa", "Modelo", "Ano", "ID Cliente"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Placa", text="Placa")
        self.tree.heading("Modelo", text="Modelo")
        self.tree.heading("Ano", text="Ano")
        self.tree.heading("ID Cliente", text="ID Cliente")

        self.tree.column("ID", width=50)
        self.tree.column("Placa", width=100)
        self.tree.column("Modelo", width=150)
        self.tree.column("Ano", width=70)
        self.tree.column("ID Cliente", width=100)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Carregar dados iniciais
        self.carregar_veiculos()

    def adicionar_veiculo(self):
        placa = self.entry_placa.get()
        modelo = self.entry_modelo.get()
        ano = self.entry_ano.get()
        id_cliente = self.entry_id_cliente.get()

        if placa == "" or id_cliente == "":
            messagebox.showwarning("Entrada Inválida", "Os campos Placa e ID do Cliente são obrigatórios.")
            return

        try:
            ano = int(ano) if ano else None
            id_cliente = int(id_cliente)
        except ValueError:
            messagebox.showwarning("Entrada Inválida", "Os campos Ano e ID do Cliente devem ser números inteiros.")
            return

        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO VEICULO (Placa, Modelo, Ano, Cliente_idCliente)
                    VALUES (?, ?, ?, ?)
                """, (placa, modelo, ano, id_cliente))
                conn.commit()
                messagebox.showinfo("Sucesso", "Veículo adicionado com sucesso!")
                self.entry_placa.delete(0, tk.END)
                self.entry_modelo.delete(0, tk.END)
                self.entry_ano.delete(0, tk.END)
                self.entry_id_cliente.delete(0, tk.END)
                self.carregar_veiculos()
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível adicionar o veículo.\nErro: {e}")
            finally:
                conn.close()
        else:
            messagebox.showerror("Erro de Conexão", "Não foi possível conectar ao banco de dados.")

    def carregar_veiculos(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT id_veiculo, Placa, Modelo, Ano, Cliente_idCliente FROM VEICULO")
                rows = cursor.fetchall()
                for row in rows:
                    self.tree.insert("", tk.END, values=row)
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível recuperar os veículos.\nErro: {e}")
            finally:
                conn.close()
        else:
            messagebox.showerror("Erro de Conexão", "Não foi possível conectar ao banco de dados.")
