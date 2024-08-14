import flet as ft
import psycopg2

class ToDo:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.window_width = 375  # Define a largura da janela do aplicativo
        self.page.window_height = 667  # Define a altura da janela do aplicativo
        self.page.window_resizable = False  # Impede o redimensionamento da janela
        self.page.bgcolor = ft.colors.WHITE  # Define a cor de fundo da página
        self.page.title = 'OrderFlow'  # Define o título da janela
        self.db_config = {
            'dbname': 'servicos',
            'user': 'GABRIEL',
            'password': '123456',
            'host': '192.168.10.52',
            'port': '5432'
        }
        self.current_user = None  # Variável para armazenar o nome do usuário logado
        self.connection = self.create_connection()  # Estabelecendo a conexão com o banco de dados
        self.show_login_page()  # Inicializa com a página de login

    def create_connection(self):
        """Cria e retorna uma conexão com o banco de dados PostgreSQL."""
        try:
            conn = psycopg2.connect(**self.db_config)
            print("Conexão bem-sucedida com o banco de dados!")
            return conn
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return None

    def show_login_page(self):
        self.page.clean()  # Limpa a página existente antes de adicionar novos componentes

        # Criando a logo
        logo = ft.Image(
            src="img/grupoatt-1-Photoroom.png",  # URL da logo
            width=200,  # Largura da imagem da logo
            height=200,  # Altura da imagem da logo
        )

        # Campos de login
        username_field = ft.TextField(
            label="Username",  # Rótulo para o campo de nome de usuário
            border_radius=10,  # Arredondamento dos cantos do campo
            width=300,  # Largura do campo
        )

        password_field = ft.TextField(
            label="Password",  # Rótulo para o campo de senha
            password=True,  # Define que o campo é de senha
            can_reveal_password=True,  # Permite revelar a senha
            border_radius=10,  # Arredondamento dos cantos do campo
            width=300,  # Largura do campo
        )

        # Botão de login
        login_button = ft.ElevatedButton(
            text="Login",  # Texto do botão
            on_click=lambda _: self.handle_login(username_field.value, password_field.value),  # Chama a função handle_login ao clicar
            width=300,  # Largura do botão
        )

        # Layout da tela de login
        login_layout = ft.Column(
            [
                logo,  # Adiciona a logo
                username_field,  # Adiciona o campo de nome de usuário
                password_field,  # Adiciona o campo de senha
                login_button,  # Adiciona o botão de login
            ],
            spacing=20,  # Espaçamento entre os componentes
            alignment=ft.MainAxisAlignment.CENTER,  # Alinha verticalmente ao centro
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Alinha horizontalmente ao centro
            expand=True,  # Expande para ocupar o espaço disponível
        )

        self.page.add(
            ft.Container(
                content=login_layout,  # Adiciona o layout de login ao container
                alignment=ft.alignment.center,  # Centraliza o conteúdo na página
                expand=True,  # Expande para ocupar o espaço disponível
            )
        )

    def handle_login(self, username, password):
        """Verifica o login e, em caso de sucesso, mostra a página principal."""
        if username and password:
            # Aqui você pode implementar a lógica de autenticação
            # Temporariamente, vamos assumir que qualquer combinação de username e password é válida
            self.current_user = username  # Armazena o nome do usuário logado
            self.show_main_page()  # Exibe a página principal após o login
        else:
            # Exibe uma mensagem de erro se os campos estiverem vazios
            print("Erro: Campos de usuário e senha não podem estar vazios.")

    def show_main_page(self):
        self.page.clean()  # Limpa a página existente

        # Inicializa o estado do menu
        self.menu_open = False
        self.menu_button = ft.IconButton(
            icon=ft.icons.MENU,  # Ícone do menu
            on_click=self.toggle_menu  # Função para abrir/fechar o menu
        )

        close_menu_button = ft.IconButton(
            icon=ft.icons.ARROW_BACK_IOS,  # Ícone para fechar o menu
            on_click=self.toggle_menu,  # Função para abrir/fechar o menu
            icon_size=24,  # Tamanho do ícone
            bgcolor=ft.colors.TRANSPARENT,  # Fundo transparente
            padding=ft.Padding(left=8, right=8, top=8, bottom=8)  # Padding em torno do ícone
        )

        # Item para adicionar uma nova ordem
        add_order_item = ft.Row(
            controls=[
                ft.Icon(ft.icons.CONTENT_PASTE, size=24, color=ft.colors.BLUE_900),  # Ícone para adicionar ordem
                ft.TextButton(
                    text="Adicionar Ordem",  # Texto do botão
                    on_click=self.add_order,  # Função para adicionar ordem
                    style=ft.ButtonStyle(
                        color=ft.colors.BLUE_900  # Cor do texto
                    )
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Alinha verticalmente ao centro
            spacing=4  # Espaçamento entre o ícone e o texto
        )

        # Item para análise
        report_item = ft.Row(
            controls=[
                ft.Icon(ft.icons.ANALYTICS, size=24, color=ft.colors.BLUE_900),  # Ícone para análise
                ft.TextButton(
                    text="Análise",  # Texto do botão
                    on_click=None,  # Nenhuma função associada ainda
                    style=ft.ButtonStyle(
                        color=ft.colors.BLUE_900  # Cor do texto
                    )
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Alinha verticalmente ao centro
            spacing=4  # Espaçamento entre o ícone e o texto
        )

        # Seção do perfil do usuário
        profile_section = ft.Container(
            content=ft.Column(
                controls=[
                    ft.CircleAvatar(
                        background_image_url="URL_DA_IMAGEM_DE_PERFIL",  # URL da imagem de perfil
                        radius=50  # Raio do avatar
                    ),
                    ft.Text(self.current_user, size=16, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK)  # Nome do usuário logado
                ],
                alignment=ft.MainAxisAlignment.CENTER,  # Alinha verticalmente ao centro
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Alinha horizontalmente ao centro
                spacing=8  # Espaçamento entre o avatar e o nome
            ),
            alignment=ft.alignment.center,  # Centraliza o conteúdo na página
            padding=ft.Padding(left=0, right=0, top=20, bottom=20)  # Padding em torno do container
        )

        # Cabeçalho do menu
        header_row = ft.Row(
            controls=[
                ft.Container(expand=True),  # Expande para preencher o espaço
                close_menu_button  # Adiciona o botão de fechar o menu
            ],
            alignment=ft.MainAxisAlignment.END,  # Alinha o botão de fechar à direita
            height=50  # Altura da linha do cabeçalho
        )

        # Contêiner de itens do menu
        menu_items_container = ft.Column(
            controls=[
                add_order_item,  # Adiciona o item para adicionar ordem
                report_item  # Adiciona o item para análise
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Alinha verticalmente ao centro
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Alinha horizontalmente ao centro
            spacing=20,  # Espaçamento entre os itens do menu
            expand=True  # Expande para preencher o espaço disponível
        )

        # Conteúdo do menu lateral
        self.menu_content = ft.Column(
            controls=[
                header_row,  # Adiciona o cabeçalho
                profile_section,  # Adiciona a seção de perfil
                ft.Container(
                    content=menu_items_container,  # Adiciona os itens do menu
                    alignment=ft.alignment.center,  # Centraliza o conteúdo
                    expand=True  # Expande para preencher o espaço disponível
                ),
                ft.Container(expand=True),  # Expande para preencher o espaço
                ft.Row(
                    controls=[
                        ft.Container(width=0, expand=True),  # Expande para preencher o espaço
                        ft.ElevatedButton(
                            text="Sair",  # Texto do botão de logout
                            on_click=self.logout,  # Função para logout
                            bgcolor=ft.colors.RED,  # Cor de fundo do botão
                            color=ft.colors.WHITE,  # Cor do texto do botão
                            width=200  # Largura do botão
                        ),
                        ft.Container(width=0, expand=True)  # Expande para preencher o espaço
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,  # Alinha o botão de logout ao centro
                    expand=True  # Expande para preencher o espaço disponível
                )
            ],
            alignment=ft.MainAxisAlignment.START,  # Alinha o conteúdo ao início
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Alinha horizontalmente ao centro
            expand=True  # Expande para preencher o espaço disponível
        )

        self.menu_container = ft.Container(
            content=self.menu_content,  # Adiciona o conteúdo do menu lateral
            alignment=ft.alignment.center,  # Centraliza o conteúdo
            bgcolor=ft.colors.GREY_200,  # Define a cor de fundo do menu lateral
            width=300,  # Largura do menu lateral
            padding=ft.Padding(0, 0, 0, 0),  # Padding do menu lateral
            visible=False,  # Inicialmente, o menu lateral está oculto
            expand=True  # Expande para preencher o espaço disponível
        )

        self.content_container = ft.Container(
            content=ft.Text("Tela principal", size=24, color=ft.colors.BLACK),  # Conteúdo principal
            alignment=ft.alignment.center,  # Centraliza o conteúdo principal
            expand=True  # Expande para preencher o espaço disponível
        )

        self.main_layout = ft.Column(
            [
                self.menu_button,  # Adiciona o botão de menu
                self.content_container  # Adiciona o conteúdo principal
            ],
            expand=True  # Expande para preencher o espaço disponível
        )

        self.page.add(
            ft.Row(
                [
                    self.menu_container,  # Adiciona o menu lateral
                    self.main_layout  # Adiciona o layout principal
                ],
                alignment=ft.MainAxisAlignment.START,  # Alinha o layout principal ao início
                spacing=0,  # Sem espaçamento entre o menu e o layout principal
                expand=True  # Expande para preencher o espaço disponível
            )
        )

    def toggle_menu(self, e):
        """Abre ou fecha o menu lateral."""
        self.menu_open = not self.menu_open
        self.menu_container.visible = self.menu_open
        self.page.update()  # Atualiza a página para refletir as mudanças de visibilidade

    def add_order(self, e):
        """Função temporária para adicionar ordens."""
        print("Adicionar nova ordem.")

    def logout(self, e):
        """Faz o logout e retorna para a página de login."""
        self.current_user = None  # Limpa o usuário logado
        self.show_login_page()  # Mostra novamente a página de login

def main(page: ft.Page):
    ToDo(page)  # Cria uma instância do aplicativo

ft.app(target=main)

