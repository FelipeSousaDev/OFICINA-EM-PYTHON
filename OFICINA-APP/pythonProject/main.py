from tkinter import Tk
from gui.cliente_gui import ClienteGUI
from gui.veiculo_gui import VeiculoGUI


def main():
    root = Tk()
    root.geometry("800x600")  # Ajuste o tamanho da janela conforme necessário

    # Para Cliente
    cliente_gui = ClienteGUI(root)

    # Para Veículo (descomente se quiser usar)
    # veiculo_gui = VeiculoGUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()
