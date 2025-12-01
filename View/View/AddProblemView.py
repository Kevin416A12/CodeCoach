import tkinter as tk
from tkinter import ttk, messagebox


class AddProblemView(tk.Toplevel):
    def __init__(self, controller, on_added_callback=None):
        super().__init__()
        self.controller = controller
        self.on_added_callback = on_added_callback

        self.title("Agregar nuevo problema")
        self.geometry("500x500")
        self.configure(bg="#101010")

        # --- Título ---
        tk.Label(self, text="Nuevo Problema", font=("Consolas", 20, "bold"),
                 fg="#00FFAA", bg="#101010").pack(pady=10)

        # --- Entradas ---
        self.title_var = tk.StringVar()
        self.input_var = tk.StringVar()
        self.output_var = tk.StringVar()

        self.create_entry("Título:", self.title_var)
        self.create_text("Descripción:", "desc")
        self.create_entry("Input de ejemplo:", self.input_var)
        self.create_entry("Output esperado:", self.output_var)

        # Botón guardar
        tk.Button(
            self,
            text="💾 Guardar",
            bg="#0078FF",
            fg="white",
            font=("Consolas", 13, "bold"),
            command=self.save
        ).pack(pady=15)

    def create_entry(self, label, var):
        frame = tk.Frame(self, bg="#101010")
        frame.pack(fill="x", padx=15, pady=5)

        tk.Label(frame, text=label, fg="#AAAAAA", bg="#101010").pack(anchor="w")
        tk.Entry(frame, textvariable=var, bg="#1b1b1b", fg="white").pack(fill="x")

    def create_text(self, label, attr):
        frame = tk.Frame(self, bg="#101010")
        frame.pack(fill="both", padx=15, pady=5)

        tk.Label(frame, text=label, fg="#AAAAAA", bg="#101010").pack(anchor="w")

        txt = tk.Text(frame, height=5, bg="#1b1b1b", fg="white")
        txt.pack(fill="both")
        setattr(self, attr, txt)

    def save(self):
        title = self.title_var.get().strip()
        description = self.desc.get("1.0", tk.END).strip()
        input_ex = self.input_var.get().strip()
        output_ex = self.output_var.get().strip()

        if not title or not description:
            messagebox.showwarning("Campos vacíos", "Título y descripción son obligatorios.")
            return

        result = self.controller.add_problem(title, description, input_ex, output_ex)
        print(result)

        if result.get("status") == "success":
            messagebox.showinfo("Éxito", "Problema agregado correctamente.")
            if self.on_added_callback:
                self.on_added_callback()
            self.destroy()


