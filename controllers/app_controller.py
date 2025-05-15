# controllers/app_controller.py
import customtkinter as ctk
from models.database import Database
from models.user_model import UserModel
from models.employee_model import EmployeeModel
from views.login_view import LoginView
from views.dashboard_view import DashboardView

class AppController:
    def __init__(self):
        self.db = Database()
        self.user_model = UserModel(self.db)
        self.employee_model = EmployeeModel(self.db)
        self.current_user = None

        # Configurações iniciais do customtkinter
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("./theme/dark-purpure.json")
        self.root = ctk.CTk()
        self.root.geometry("900x600")
        self.root.title("Sistema de Gestão de Funcionários")

        # Cria a tela de login
        self.login_view = LoginView(self.root, self)
        self.login_view.pack(fill="both", expand=True)

        # Se não houver usuário admin, cria um padrão (admin/admin)
        if not self.user_model.get_user_by_username("admin"):
            try:
                self.user_model.create_user("admin", "admin@example.com", "admin")
                print("Usuário admin criado com credenciais padrão (admin/admin)")
            except Exception as e:
                print("Erro ao criar admin:", e)

    def login(self, username, password):
        user = self.user_model.authenticate(username, password)
        if user:
            self.current_user = user
            self.show_dashboard()
        else:
            self.login_view.show_error("Usuário ou senha inválidos!")

    def logout(self):
        self.current_user = None
        self.dashboard_view.destroy()
        self.login_view = LoginView(self.root, self)
        self.login_view.pack(fill="both", expand=True)

    def show_dashboard(self):
        self.login_view.destroy()
        self.dashboard_view = DashboardView(self.root, self)
        self.dashboard_view.pack(fill="both", expand=True)

    def run(self):
        self.root.mainloop()
