# views/dashboard_view.py
import customtkinter as ctk
from views.employee_views import EmployeeListView
from views.user_view import UserManagementView

class DashboardView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Menu lateral
        self.side_menu = ctk.CTkFrame(self, width=200)
        self.side_menu.pack(side="left", fill="y", padx=10, pady=10)

        self.btn_home = ctk.CTkButton(self.side_menu, text="Home", command=self.show_home)
        self.btn_home.pack(pady=10, padx=10)

        self.btn_employees = ctk.CTkButton(self.side_menu, text="Funcionários", command=self.show_employees)
        self.btn_employees.pack(pady=10, padx=10)

        # Se o usuário for admin, adiciona o menu de gerenciamento de usuários
        if self.controller.current_user[1] == "admin":
            self.btn_users = ctk.CTkButton(self.side_menu, text="Usuários", command=self.show_users)
            self.btn_users.pack(pady=10, padx=10)

        self.btn_logout = ctk.CTkButton(self.side_menu, text="Logout", command=self.controller.logout)
        self.btn_logout.pack(pady=10, padx=10)

        # Área de conteúdo
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.show_home()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_content()
        welcome_label = ctk.CTkLabel(
            self.content_frame,
            text=f"Bem-vindo, {self.controller.current_user[1]}!",
            font=("Arial", 20)
        )
        welcome_label.pack(pady=20, padx=20)
        
        

    def show_employees(self):
        self.clear_content()
        self.employee_list_view = EmployeeListView(self.content_frame, self.controller)
        self.employee_list_view.pack(fill="both", expand=True)

    def show_users(self):
        self.clear_content()
        self.user_management_view = UserManagementView(self.content_frame, self.controller)
        self.user_management_view.pack(fill="both", expand=True)
