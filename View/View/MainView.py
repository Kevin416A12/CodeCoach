import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from View.CodeEditorView import CodeEditorView
from View.AddProblemView import AddProblemView


class MainView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("CodeCoach - Gestor de Problemas")
        self.geometry("800x600")
        self.configure(bg="#101010")

        self.create_widgets()

    def create_widgets(self):
        # --- Título ---
        tk.Label(
            self, text="CodeCoach",
            font=("Consolas", 24), fg="#EEEEEE", bg="#CF0A0A"
        ).pack(pady=10)

        # --- Frame de botones ---
        frame_buttons = tk.Frame(self, bg="#101010")
        frame_buttons.pack(pady=5)
        tk.Button(frame_buttons, text="💻 Resolver", command=self.open_editor).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="🔄 Refrescar", command=self.load_problems).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_buttons, text="➕ Agregar", command=self.add_problem).pack(side=tk.LEFT, padx=5)
        

        # --- Tabla de problemas ---
        self.tree = ttk.Treeview(self, columns=("Title", "Description"), show="headings")
        self.tree.heading("Title", text="Título")
        self.tree.heading("Description", text="Descripción")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Consola de resultados ---
        self.console = scrolledtext.ScrolledText(
            self, height=8, bg="#000", fg="#0F0", insertbackground="#0F0"
        )
        self.console.pack(fill=tk.BOTH, padx=10, pady=5)

    def log(self, text):
        self.console.insert(tk.END, text + "\n")
        self.console.see(tk.END)

    def open_editor(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atención", "Selecciona un problema primero.")
            return

        item = self.tree.item(selected[0])
        title = item["values"][0]
        desc = item["values"][1]

        problem = {
            "title": title,
            "description": desc
        }

        editor = CodeEditorView(self.controller, problem)
        editor.grab_set()

    def load_problems(self):
        try:
            self.tree.delete(*self.tree.get_children())
            problems = self.controller.get_problems()
            for p in problems:
                self.tree.insert("", tk.END, values=(p["title"], p["description"]))
            self.log("✅ Problemas cargados correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los problemas.\n{e}")

    def add_problem(self):
        AddProblemView(
            controller=self.controller,
            on_added_callback=self.load_problems
        )

    def evaluate(self):
        # Código de prueba temporal
        code = "#include <iostream>\nint main(){ std::cout << 5; return 0; }"
        result = self.controller.evaluate_code(code, "5")
        self.log(f"🧠 Resultado: {result}")
        messagebox.showinfo("Evaluación", f"{result}")
