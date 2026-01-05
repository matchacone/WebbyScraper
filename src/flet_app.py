import flet as ft

def main(page: ft.Page):
    page.title = "Scraper Dashboard"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0  
    
    # --- GUI LOGIC (Basic Interactivity) ---
    def toggle_url_mode(e):
        """Changes the input hint based on selection"""
        if e.control.value == "single":
            url_input.label = "Single URL"
            url_input.hint_text = "https://example.com"
            url_input.multiline = False
            url_input.min_lines = 1
        else:
            url_input.label = "List of URLs"
            url_input.hint_text = "https://site1.com\nhttps://site2.com"
            url_input.multiline = True
            url_input.min_lines = 5
        page.update()

    # sidebar compoenents
    
    # 1. Title
    sidebar_title = ft.Text(
        "Scrape Settings", 
        size=20, 
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.WHITE
    )

    # 2. Mode Selection (Single vs Multi)
    mode_selector = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="single", label="Single URL"),
            ft.Radio(value="multi", label="Multiple URLs"),
        ]),
        value="single",
        on_change=toggle_url_mode
    )

    # 3. URL Input Field
    url_input = ft.TextField(
        label="Target URL",
        hint_text="https://example.com",
        border_color=ft.Colors.BLUE_400,
        multiline=False,
        text_size=12
    )

    # 4. Data Extraction Field
    data_tags_input = ft.TextField(
        label="Data to Extract",
        hint_text="email, phone, full_name",
        border_color=ft.Colors.GREEN_400,
        
        multiline=True,
        min_lines=1,
        max_lines=5,
        
        text_size=12,
        content_padding=10
    )

    # 5. Action Button
    scrape_button = ft.ElevatedButton(
        content=ft.Text("START SCRAPE"),
        icon="rocket_launch",
        bgcolor=ft.Colors.BLUE_600,
        color=ft.Colors.WHITE,
        width=200
    )

    # Layout
    
    # The Left Sidebar Container
    sidebar = ft.Container(
        content=ft.Column(
            controls=[
                sidebar_title,
                ft.Divider(color=ft.Colors.GREY_800),
                ft.Text("Scrape Mode:", color=ft.Colors.GREY_400, size=12),
                mode_selector,
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT), # Spacer
                url_input,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT), # Spacer
                data_tags_input,
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT), # Spacer
                scrape_button
            ],
            scroll=ft.ScrollMode.AUTO # Scrollable if settings get too long
        ),
        width=280,
        bgcolor=ft.Colors.GREY_900,
        padding=20,
        alignment=ft.Alignment(-1,-1),
        border=ft.border.only(right=ft.border.BorderSide(1, ft.Colors.GREY_800))
    )
    
    # The Main Content Area

    view_markdown = ft.Markdown(
        """# Agent Profile Found
**Name:** Shane Thurkle
**Role:** Senior Broker
**Status:** Active
## Contact Details
* **Email:** shane@example.com""",
        extension_set=ft.MarkdownExtensionSet.GITHUB_WEB
    )

    view_json = ft.Text(
        value='{\n  "name": "Shane Thurkle",\n  "role": "Broker"\n}',
        font_family="Consolas,monospace",
        color=ft.Colors.GREEN_400
    )

    view_csv = ft.Text(
        value="Name,Role\nShane Thurkle,Broker",
        font_family="Consolas,monospace"
    )

    # --- 2. THE CONTENT AREA ---
    # This container holds the actual result (Markdown/JSON/CSV)
    content_area = ft.Container(
        content=ft.Column([view_markdown], scroll=ft.ScrollMode.AUTO),
        padding=20,
        expand=True,
        alignment=ft.alignment.Alignment(-1, -1)
    )

    # --- 3. THE TOGGLE LOGIC ---
    def set_view(view_type):
        # 1. Update Content
        if view_type == "markdown":
            content_area.content = ft.Column([view_markdown], scroll=ft.ScrollMode.AUTO)
        elif view_type == "json":
            content_area.content = ft.Column([view_json], scroll=ft.ScrollMode.AUTO)
        elif view_type == "csv":
            content_area.content = ft.Column([view_csv], scroll=ft.ScrollMode.AUTO)
        
        # 2. Update Button Styles (Highlight the active one)
        btn_markdown.bgcolor = ft.Colors.BLUE_600 if view_type == "markdown" else ft.Colors.GREY_800
        btn_json.bgcolor = ft.Colors.BLUE_600 if view_type == "json" else ft.Colors.GREY_800
        btn_csv.bgcolor = ft.Colors.BLUE_600 if view_type == "csv" else ft.Colors.GREY_800
        
        page.update()

    # --- 4. THE BUTTONS ---
    # We use simple buttons instead of ft.Tab to avoid crashes
    btn_markdown = ft.ElevatedButton(
        "Markdown", 
        on_click=lambda _: set_view("markdown"),
        bgcolor=ft.Colors.BLUE_600, # Active by default
        color=ft.Colors.WHITE,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0))
    )

    btn_json = ft.ElevatedButton(
        "JSON", 
        on_click=lambda _: set_view("json"),
        bgcolor=ft.Colors.GREY_800,
        color=ft.Colors.WHITE,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0))
    )

    btn_csv = ft.ElevatedButton(
        "CSV", 
        on_click=lambda _: set_view("csv"),
        bgcolor=ft.Colors.GREY_800,
        color=ft.Colors.WHITE,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0))
    )

    # Put buttons in a generic Row
    toggle_row = ft.Row(
        [btn_markdown, btn_json, btn_csv], 
        spacing=0 # Connect them together
    )

    # --- 5. FINAL ASSEMBLY ---
    
    ai_instruction_input = ft.TextField(
        label="AI Instructions (Optional)",
        hint_text="e.g., 'Summarize the bio'",
        border_color=ft.Colors.BLUE_400,
        prefix_icon="psychology",
        text_size=13
    )

    main_content = ft.Container(
        content=ft.Column([
            ft.Text("Results Dashboard", size=30, weight=ft.FontWeight.W_100),
            ft.Divider(color=ft.Colors.TRANSPARENT, height=10),
            ai_instruction_input,
            ft.Divider(color=ft.Colors.TRANSPARENT, height=10),
            
            # Add our custom Button Row
            toggle_row,
            # Add the Content Area
            content_area
        ]),
        expand=True,
        bgcolor=ft.Colors.BLACK,
        padding=20,
        alignment=ft.alignment.Alignment(-1, -1)
    )

    # Combine them in a Row
    layout = ft.Row(
        controls=[sidebar, main_content],
        expand=True, 
        spacing=0    
    )

    page.add(layout)

if __name__ == "__main__":
    ft.app(target=main)