# views/login_view.py
import customtkinter as ctk
from PIL import Image



class LoginView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        
        #Pegando a imagem
        login_image = ctk.CTkImage(light_image=Image.open("./static/img-login-page.png"), dark_image=Image.open("./static/img-login-page.png"), size=(400, 400))
        
        # Ligin View Frames
        self.frame = ctk.CTkFrame(self, fg_color='transparent', corner_radius=10)
        self.frame.pack(pady=(50, 0))
        
        self.image_frame = ctk.CTkFrame(self.frame, fg_color='transparent')
        self.image_frame.grid(column=0, row=0)
        
        self.form_frame = ctk.CTkFrame(self.frame, )
        self.form_frame.grid(column=1, row=0, sticky='news', pady=(50, 0))
        
        
        ctk.CTkLabel(self.frame, text='Sistema de Gestão de Funcionários | Desenvolvido por: @setprogramacao | 2025').grid(row=1, column=0, columnspan=2)
        
        #Widgets da tela de Login
        
        login_image_label = ctk.CTkLabel(self.image_frame, image=login_image, text='')
        login_image_label.pack()
        
        
        ctk.CTkLabel(self.form_frame, text='Login', font=('Arial bold', 40)).pack(pady=(10,20))

        self.username_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Usuário", width=200)
        self.username_entry.pack(pady=12, padx=10)

        self.password_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Senha", show="*", width=200)
        self.password_entry.pack(pady=12, padx=10)

        self.login_button = ctk.CTkButton(self.form_frame, text="Login", command=self.attempt_login)
        self.login_button.pack(pady=12, padx=10)

        self.error_label = ctk.CTkLabel(self.form_frame, text="", text_color="red")
        self.error_label.pack()

    def attempt_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.controller.login(username, password)

    def show_error(self, message):
        self.error_label.configure(text=message)
