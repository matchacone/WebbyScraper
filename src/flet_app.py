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
        helper_style="Separate keys by comma",
        border_color=ft.Colors.GREEN_400,
        multiline=True,
        max_lines=3,
        text_size=12
    )

    # 5. Action Button
    scrape_button = ft.ElevatedButton(
        content=ft.Text("START SCRAPE"),
        icon="rocket_launch",
        bgcolor=ft.Colors.BLUE_600,
        color=ft.Colors.WHITE,
        width=200
    )

    # layout
    
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

    # The Main Content Area (Placeholder)
    main_content = ft.Container(
        content=ft.Column([
            ft.Text("Results Dashboard", size=30, weight=ft.FontWeight.W_100),
            ft.Text("Select settings on the left to begin...", color=ft.Colors.GREY_500),
            ft.Icon("data_object", size=100, color=ft.Colors.GREY_800)
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        expand=True,
        bgcolor=ft.Colors.BLACK,
        alignment=ft.Alignment.CENTER
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