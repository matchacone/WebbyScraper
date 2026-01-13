import flet as ft
import pandas as pd
import json
import os
import datetime

import LLM_extraction 

def main(page: ft.Page):
    current_data = []
    
    def save_file(e):
        """Saves the current data to the 'output' folder."""
        # 1. Check if we have data
        # We access the raw data stored in a global variable (we need to create this first)
        if not current_data: 
            save_button.text = "No Data!"
            page.update()
            return

        # 2. Create 'output' folder if missing
        if not os.path.exists("output"):
            os.makedirs("output")

        # 3. Generate Filename with Timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        try:
            # 4. Save based on current view mode
            if "json" in btn_json.bgcolor: # If JSON view is active
                filename = f"output/scrape_{timestamp}.json"
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(current_data, f, indent=2)
                
            else: # Default to CSV for Table/Markdown views
                filename = f"output/scrape_{timestamp}.csv"
                df = pd.DataFrame(current_data)
                df.to_csv(filename, index=False)

            # 5. Visual Feedback
            save_button.text = "Saved!"
            save_button.bgcolor = ft.Colors.GREEN_600
            page.update()
            
            # Reset button after 3 seconds
            import time
            time.sleep(3)
            save_button.text = "Save File"
            save_button.bgcolor = ft.Colors.ORANGE_600
            page.update()

        except Exception as ex:
            save_button.text = "Error Saving"
            print(f"Save Error: {ex}")
            page.update()
            
    page.title = "Scraper Dashboard"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0  
    
    # --- 1. SHARED STATE ---
    _settings = {"model": "gpt-4o-mini", "api_key": ""} 

    def update_settings(e):
        _settings["model"] = model_input.value
        _settings["api_key"] = api_key_field.value
        print(f"Settings Updated: {_settings}")

    # --- 2. GUI COMPONENTS ---
    
    # Sidebar Components
    sidebar_title = ft.Text("Scrape Settings", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)

    def toggle_url_mode(e):
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

    mode_selector = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="single", label="Single URL"),
            ft.Radio(value="multi", label="Multiple URLs"),
        ]),
        value="single",
        on_change=toggle_url_mode
    )

    url_input = ft.TextField(
        label="Target URL",
        hint_text="https://example.com",
        border_color=ft.Colors.BLUE_400,
        multiline=False,
        text_size=12
    )

    data_tags_input = ft.TextField(
        label="Data to Extract",
        hint_text="email, phone, full_name",
        border_color=ft.Colors.GREEN_400,
        multiline=True,
        min_lines=1,
        max_lines=3,
        text_size=12,
        content_padding=10
    )

    model_input = ft.TextField(
        label="LLM Model (e.g. gpt-4o)",
        value=_settings["model"],
        text_size=12,
        border_color=ft.Colors.GREY_700,
        on_change=update_settings
    )

    api_key_field = ft.TextField(
        label="API Key",
        password=True,
        value=_settings["api_key"],
        text_size=12,
        border_color=ft.Colors.GREY_700,
        on_change=update_settings
    )

    # --- 3. SCRAPE LOGIC ---
    async def on_click_scrape(e):
        # Validation
        if not url_input.value:
            url_input.error_text = "Required!"
            url_input.update()
            return
        if not data_tags_input.value:
            data_tags_input.error_text = "Required!"
            data_tags_input.update()
            return
        if not api_key_field.value:
            api_key_field.error_text = "API Key Required!"
            api_key_field.update()
            return

        # Prepare Inputs
        if mode_selector.value == "single":
            targets = [url_input.value.strip()]
        else:
            targets = [u.strip() for u in url_input.value.split('\n') if u.strip()]

        fields = [f.strip() for f in data_tags_input.value.split(',') if f.strip()]
        
        # Show Loading
        scrape_button.disabled = True
        scrape_button.content = ft.Row([ft.ProgressRing(width=16, height=16), ft.Text(" SCRAPING...")])
        page.update()

        try:
            # CALL BACKEND
            data = await LLM_extraction.run_scrape(
                targets, 
                fields, 
                model_input.value, 
                api_key_field.value
            )
            
            current_data.clear()
            if data:
                current_data.extend(data)

            # Display Results
            if data:
                # 1. Update JSON View
                view_json.value = json.dumps(data, indent=2)
                
                # 2. Update CSV/Table View
                df = pd.DataFrame(data)
                
                # [SAFETY CHECK] Only build table if we actually have columns
                if not df.empty and len(df.columns) > 0:
                    # A. Create Columns
                    view_csv.columns = [
                        ft.DataColumn(ft.Text(str(col).upper(), weight="bold", color=ft.Colors.BLUE_200)) 
                        for col in df.columns
                    ]
                    
                    # B. Create Rows
                    view_csv.rows = []
                    for index, row in df.iterrows():
                        cells = [ft.DataCell(ft.Text(str(row[col]), size=12, selectable=True)) for col in df.columns]
                        view_csv.rows.append(ft.DataRow(cells=cells))
                    
                    # Update Markdown View
                    view_markdown.value = df.to_markdown(index=False)
                    
                    # Switch to Table View
                    set_view("csv")
                else:
                    view_json.value = "Data found, but it was empty or unstructured."
                    set_view("json")
            else:
                view_json.value = "No data found."
                set_view("json")

        except Exception as ex:
            view_json.value = f"Error: {str(ex)}"
            set_view("json")

        # Reset Button
        scrape_button.disabled = False
        scrape_button.content = ft.Text("START SCRAPE")
        page.update()

    scrape_button = ft.ElevatedButton(
        content=ft.Text("START SCRAPE"),
        icon="rocket_launch",
        bgcolor=ft.Colors.BLUE_600,
        color=ft.Colors.WHITE,
        width=200,
        on_click=on_click_scrape
    )

    # Layout
    sidebar = ft.Container(
        content=ft.Column(
            controls=[
                sidebar_title,
                ft.Divider(color=ft.Colors.GREY_800),
                ft.Text("Scrape Mode:", color=ft.Colors.GREY_400, size=12),
                mode_selector,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                url_input,
                ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                data_tags_input,
                ft.Divider(height=15, color=ft.Colors.TRANSPARENT),
                scrape_button,
                ft.Divider(height=20, color=ft.Colors.GREY_800),
                ft.Text("AI Configuration", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                model_input,
                api_key_field
            ],
            scroll=ft.ScrollMode.AUTO
        ),
        width=280,
        bgcolor=ft.Colors.GREY_900,
        padding=20,
        alignment=ft.Alignment(-1,-1),
        border=ft.border.only(right=ft.border.BorderSide(1, ft.Colors.GREY_800))
    )
    
    # Results Area
    view_markdown = ft.Markdown("Run a scrape to see results here...")
    view_json = ft.Text("Waiting for data...", font_family="Consolas", color=ft.Colors.GREEN_400, selectable=True)
    view_csv = ft.DataTable(
        columns=[ft.DataColumn(ft.Text("Status"))], 
        rows=[ft.DataRow(cells=[ft.DataCell(ft.Text("Waiting for data..."))])],
        
        # Styling
        border=ft.border.all(1, ft.Colors.GREY_800),
        vertical_lines=ft.border.BorderSide(1, ft.Colors.GREY_800),
        horizontal_lines=ft.border.BorderSide(1, ft.Colors.GREY_800),
        heading_row_color=ft.Colors.GREY_900,
        data_row_color=ft.Colors.BLACK,
    )

    content_area = ft.Container(
        content=ft.Column([view_json], scroll=ft.ScrollMode.AUTO),
        padding=20,
        expand=True,
        alignment=ft.alignment.Alignment(-1, -1)
    )

    def set_view(view_type):
        if view_type == "markdown": content_area.content = ft.Column([view_markdown], scroll=ft.ScrollMode.AUTO)
        elif view_type == "json": content_area.content = ft.Column([view_json], scroll=ft.ScrollMode.AUTO)
        elif view_type == "csv": 
            # [CHANGED] Wrap DataTable in a Row with scroll=ALWAYS to handle wide tables
            content_area.content = ft.Column(
                [
                    ft.Row([view_csv], scroll=ft.ScrollMode.ALWAYS) # Horizontal scroll
                ], 
                scroll=ft.ScrollMode.AUTO # Vertical scroll
            )
        
        # Update Button Colors
        btn_markdown.bgcolor = ft.Colors.BLUE_600 if view_type == "markdown" else ft.Colors.GREY_800
        btn_json.bgcolor = ft.Colors.BLUE_600 if view_type == "json" else ft.Colors.GREY_800
        btn_csv.bgcolor = ft.Colors.BLUE_600 if view_type == "csv" else ft.Colors.GREY_800
        
        page.update()

    btn_markdown = ft.ElevatedButton("Markdown", on_click=lambda _: set_view("markdown"), bgcolor=ft.Colors.GREY_800, color=ft.Colors.WHITE, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0)))
    btn_json = ft.ElevatedButton("JSON", on_click=lambda _: set_view("json"), bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0)))
    btn_csv = ft.ElevatedButton("CSV", on_click=lambda _: set_view("csv"), bgcolor=ft.Colors.GREY_800, color=ft.Colors.WHITE, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0)))
    
    save_button = ft.ElevatedButton(
        "Save File",
        bgcolor=ft.Colors.ORANGE_600,
        color=ft.Colors.WHITE,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0)),
        on_click=save_file # <--- Connect the function
    )
    
    toggle_row = ft.Row(
        [btn_markdown, btn_json, btn_csv, save_button],
        spacing=0
    )

    main_content = ft.Container(
        content=ft.Column([
            ft.Text("Results Dashboard", size=30, weight=ft.FontWeight.W_100),
            ft.Divider(color=ft.Colors.TRANSPARENT, height=10),
            toggle_row,
            content_area
        ]),
        expand=True,
        bgcolor=ft.Colors.BLACK,
        padding=20,
        alignment=ft.alignment.Alignment(-1, -1)
    )

    page.add(ft.Row([sidebar, main_content], expand=True, spacing=0))

if __name__ == "__main__":
    ft.app(target=main)