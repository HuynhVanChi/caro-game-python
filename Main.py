import tkinter as tk
from UI_Caro import CaroUI

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Trò chơi Caro")
    app = CaroUI(root, kich_thuoc=3)
    root.mainloop()
    