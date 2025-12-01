import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class CodeEditorView(tk.Toplevel):
    def __init__(self, controller, problem):
        super().__init__()
        self.controller = controller
        self.problem = problem

        # Configuración de la ventana
        self.title(f"Resolver: {problem['title']}")
        self.geometry("900x650")
        self.configure(bg="#101010")

        # --- Título del problema ---
        tk.Label(
            self,
            text=f"Problema: {problem['title']}",
            font=("Consolas", 20, "bold"),
            fg="#00FFAA",
            bg="#101010"
        ).pack(pady=10)

        # --- Descripción ---
        tk.Label(self, text="Descripción:", fg="#AAAAAA", bg="#101010", anchor="w").pack(fill="x", padx=10)
        desc_box = tk.Text(self, height=5, bg="#1b1b1b", fg="#ffffff", wrap=tk.WORD, font=("Consolas", 12))
        desc_box.pack(fill="x", padx=10, pady=5)
        desc_box.insert(tk.END, problem["description"])
        desc_box.config(state=tk.DISABLED)

        # --- Área de código ---
        tk.Label(self, text="Tu código C++:", fg="#AAAAAA", bg="#101010", anchor="w").pack(fill="x", padx=10)
        self.code_box = scrolledtext.ScrolledText(
            self,
            bg="#0f0f0f",
            fg="#00ff00",
            insertbackground="#00ff00",
            font=("Consolas", 13),
            height=15
        )
        self.code_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Frame de botones debajo del área de código ---
        btn_frame = tk.Frame(self, bg="#101010")
        btn_frame.pack(fill="x", pady=10)

        # 🔹 Botón de Evaluar
        self.eval_btn = tk.Button(
            btn_frame,
            text="▶ Evaluar",
            bg="#0078FF",
            fg="white",
            font=("Consolas", 13, "bold"),
            relief="ridge",
            width=12,
            command=self.evaluate
        )
        self.eval_btn.pack(side="left", padx=20)

        # 🔹 Botón para limpiar el código (opcional)
        clear_btn = tk.Button(
            btn_frame,
            text="🧹 Limpiar",
            bg="#444444",
            fg="white",
            font=("Consolas", 12),
            command=lambda: self.code_box.delete("1.0", tk.END)
        )
        clear_btn.pack(side="left", padx=10)

        # --- Resultado ---
        self.result_label = tk.Label(
            self,
            text="",
            fg="#00FF00",
            bg="#101010",
            font=("Consolas", 13)
        )
        self.result_label.pack(pady=5)

    def evaluate(self):
        """Evalúa el código con el motor del backend."""
        code = self.code_box.get("1.0", tk.END).strip()
        if not code:
            messagebox.showwarning("Código vacío", "Por favor, escribe algo de código antes de evaluar.")
            return

        data = {
            "title": self.problem["title"],
            "code": code
        }

        try:
            print("📤 Enviando a /evaluate:", data)
            result = self.controller.evaluate_problem(data)
            print("📥 Respuesta del servidor:", result)

        except Exception as e:
            messagebox.showerror("Error de conexión", str(e))
            return

        # --- Mostrar resultado visual ---
        status = result.get("status")
        if status == "success":
            msg = f"✅ Correcto | Output: {result.get('got')} | Tiempo: {result.get('execution_time_ms'):.2f} ms"
            self.result_label.config(text=msg, fg="#00FF00")
            self.eval_btn.config(bg="#00AA44")
        elif status == "failure":
            msg = f"❌ Incorrecto | Output: {result.get('got')} (esperado: {result.get('expected')})"
            self.result_label.config(text=msg, fg="#FF4444")
            self.eval_btn.config(bg="#AA0000")
        else:
            msg = f"⚠ Error: {result.get('message', 'Error desconocido')}"
            self.result_label.config(text=msg, fg="#FFAA00")
            self.eval_btn.config(bg="#FFAA00")
