# views/user_views.py
import customtkinter as ctk

class UserManagementView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        header = ctk.CTkLabel(self, text="Gerenciamento de Usuários", font=("Arial", 18))
        header.pack(pady=10)

        add_user_btn = ctk.CTkButton(self, text="Adicionar Usuário", command=self.show_add_user_form)
        add_user_btn.pack(pady=10)

        self.list_frame = ctk.CTkFrame(self)
        self.list_frame.pack(fill="both", expand=True, pady=10)

        self.refresh_list()

    def refresh_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        users = self.controller.user_model.get_all_users()
        for user in users:
            user_text = f"[{user[0]}] {user[1]} ({user[2]})"
            frame = ctk.CTkFrame(self.list_frame)
            frame.pack(pady=5, fill="x", padx=5)

            lbl = ctk.CTkLabel(frame, text=user_text)
            lbl.pack(side="left", padx=5)

            update_btn = ctk.CTkButton(frame, text="Atualizar", command=lambda user_id=user[0]: self.show_update_user_form(user_id))
            update_btn.pack(side="left", padx=5)

            delete_btn = ctk.CTkButton(frame, text="Deletar", command=lambda user_id=user[0]: self.delete_user(user_id))
            delete_btn.pack(side="left", padx=5)

    def show_add_user_form(self):
        self.user_form_window(None)

    def show_update_user_form(self, user_id):
        self.user_form_window(user_id)

    def user_form_window(self, user_id):
        form_window = ctk.CTkToplevel(self)
        if user_id:
            form_window.title("Atualizar Usuário")
            # Obtém os dados do usuário (aqui usamos get_all_users e filtramos)
            users = self.controller.user_model.get_all_users()
            user_data = next((u for u in users if u[0] == user_id), None)
        else:
            form_window.title("Adicionar Usuário")

        field_names = ["Username", "Email", "Senha"]
        entries = {}
        for i, field in enumerate(field_names):
            lbl = ctk.CTkLabel(form_window, text=f"{field}:")
            lbl.grid(row=i, column=0, padx=10, pady=5)
            ent = ctk.CTkEntry(form_window, width=200)
            ent.grid(row=i, column=1, padx=10, pady=5)
            if user_id and field != "Senha" and user_data:
                if field == "Username":
                    ent.insert(0, user_data[1])
                elif field == "Email":
                    ent.insert(0, user_data[2])
            entries[field] = ent

        def submit():
            username = entries["Username"].get()
            email = entries["Email"].get()
            senha = entries["Senha"].get()
            try:
                if user_id:
                    self.controller.user_model.update_user(user_id, username, email, senha if senha else None)
                else:
                    self.controller.user_model.create_user(username, email, senha)
                form_window.destroy()
                self.refresh_list()
            except Exception as e:
                print("Erro ao processar usuário:", e)

        submit_btn = ctk.CTkButton(form_window, text="Enviar", command=submit)
        submit_btn.grid(row=len(field_names), column=0, columnspan=2, pady=10)

    def delete_user(self, user_id):
        self.controller.user_model.delete_user(user_id)
        self.refresh_list()
