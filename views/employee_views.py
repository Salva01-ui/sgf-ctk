# views/employee_views.py
import customtkinter as ctk


class EmployeeListView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=5)
        
        header_frame.grid_columnconfigure(0, weight=0)
        header_frame.grid_columnconfigure(1, weight=1)
        header_frame.grid_columnconfigure(2, weight=0)
        
        page_title = ctk.CTkLabel(header_frame, text="Funcionários", text_color="#900090", font=("Arial bold", 36))
        page_title.grid(column=0, row=0, padx=10)

        add_employee_btn = ctk.CTkButton(header_frame, text="Novo Funcionário", font=("Arial bold", 14), fg_color="#900090", command=self.show_add_employee_form)
        add_employee_btn.grid(column=2, row=0, padx=(0, 20))
        

        self.list_frame = ctk.CTkScrollableFrame(self, fg_color="transparent", label_text="Listagem de Funcionários", label_anchor="w", label_font=("Arial bold", 22))
        self.list_frame.pack(fill="both", expand=True, pady=10)
        
        self.refresh_list()

    def refresh_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        employees = self.controller.employee_model.get_all_employees()

        for index, emp in enumerate(employees):
            # Alternância de cores tipo "zebra"
            bg_color = ("#d6a4d6", "gray15") if index % 2 == 0 else ("#ddd", "gray30")

            emp_frame = ctk.CTkFrame(self.list_frame, fg_color=bg_color)
            emp_frame.pack(pady=5, padx=5, fill="x")
            
            emp_frame.grid_columnconfigure(0, weight=0)
            emp_frame.grid_columnconfigure(1, weight=1)
            emp_frame.grid_columnconfigure(2, weight=0)
            
            emp_text = ctk.CTkLabel(
                emp_frame,
                text=f"{emp[2]} {emp[3]}",
                fg_color="transparent",  # Mantém transparência para herdar do frame
                bg_color="transparent"
            )
            emp_text.grid(column=0, row=0, padx=(20, 0), pady=5)
            
            emp_btn = ctk.CTkButton(
                emp_frame,
                text="Ver Detalhes",
                command=lambda emp_id=emp[0]: self.show_employee_detail(emp_id)
            )
            emp_btn.grid(row=0, column=2, padx=(0, 20))


    def show_employee_detail(self, emp_id: int):
        emp = self.controller.employee_model.get_employee_by_id(emp_id)
        if not emp:
            return

        detail_window = ctk.CTkToplevel(self)
        detail_window.title("Detalhes do Funcionário")

        field_names = ["ID", "Código", "Nome", "Apelido", "Gênero", "Idade", "Salário", "Tempo de Trabalho"]
        entries = {}
        for i, field in enumerate(field_names):
            lbl = ctk.CTkLabel(detail_window, text=f"{field}:")
            lbl.grid(row=i, column=0, padx=10, pady=5)
            if field == "Gênero":
                # Usa OptionMenu para o campo de gênero
                var = ctk.StringVar(value=emp[4])
                ent = ctk.CTkOptionMenu(detail_window, variable=var, values=["feminino", "masculino"])
                ent.grid(row=i, column=1, padx=10, pady=5)
                entries[field] = var
            else:
                ent = ctk.CTkEntry(detail_window, width=200)
                ent.grid(row=i, column=1, padx=10, pady=5)
                ent.insert(0, emp[i])
                if field == "ID":
                    ent.configure(state="disabled")
                entries[field] = ent

        def update_employee():
            try:
                self.controller.employee_model.update_employee(
                    emp_id,
                    entries["Código"].get(),
                    entries["Nome"].get(),
                    entries["Apelido"].get(),
                    entries["Gênero"].get(),
                    int(entries["Idade"].get()),
                    float(entries["Salário"].get()),
                    entries["Tempo de Trabalho"].get(),
                )
                detail_window.destroy()
                self.refresh_list()
            except Exception as e:
                print("Erro ao atualizar funcionário:", e)

        def delete_employee():
            self.controller.employee_model.delete_employee(emp_id)
            detail_window.destroy()
            self.refresh_list()

        update_btn = ctk.CTkButton(detail_window, text="Atualizar", command=update_employee)
        update_btn.grid(row=len(field_names), column=0, padx=10, pady=10)
        delete_btn = ctk.CTkButton(detail_window, text="Deletar", command=delete_employee)
        delete_btn.grid(row=len(field_names), column=1, padx=10, pady=10)

    def show_add_employee_form(self):
        add_window = ctk.CTkToplevel(self)
        add_window.title("Adicionar Funcionário")

        field_names = ["Código", "Nome", "Apelido", "Gênero", "Idade", "Salário", "Tempo de Trabalho"]
        entries = {}
        for i, field in enumerate(field_names):
            lbl = ctk.CTkLabel(add_window, text=f"{field}:")
            lbl.grid(row=i, column=0, padx=10, pady=5)
            if field == "Gênero":
                var = ctk.StringVar(value="feminino")
                ent = ctk.CTkOptionMenu(add_window, variable=var, values=["feminino", "masculino"])
                ent.grid(row=i, column=1, padx=10, pady=5)
                entries[field] = var
            else:
                ent = ctk.CTkEntry(add_window, width=200)
                ent.grid(row=i, column=1, padx=10, pady=5)
                entries[field] = ent

        def add_employee():
            try:
                self.controller.employee_model.create_employee(
                    entries["Código"].get(),
                    entries["Nome"].get(),
                    entries["Apelido"].get(),
                    entries["Gênero"].get() if isinstance(entries["Gênero"], ctk.StringVar) else entries["Gênero"].get(),
                    int(entries["Idade"].get()),
                    float(entries["Salário"].get()),
                    entries["Tempo de Trabalho"].get(),
                )
                add_window.destroy()
                self.refresh_list()
            except Exception as e:
                print("Erro ao adicionar funcionário:", e)

        add_btn = ctk.CTkButton(add_window, text="Adicionar", command=add_employee)
        add_btn.grid(row=len(field_names), column=0, columnspan=2, pady=10)
