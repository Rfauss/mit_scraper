import flet as ft
from webscrape import scrape, validate_url
from flet import FilePicker, FilePickerResultEvent, Text
import time


def main(page: ft.Page):
    page.title = "Web Scraper Example"
    page.window_height = 600
    page.window_width = 800
    page.theme_mode = "dark"

    # Submit directory and url to scrape contents
    def submit_url(url_text, directory_path):
        # Check if url and directory == True
        if not url_text.value:
            url_text.error_text = "Please enter a URL"
            page.update()
            return
        if not directory_path.value:
            url_text.error_text = "Please choose a directory"
            page.update()
            return
        else:
            # Check for valid url and https://
            if url_text.value.startswith("https://") == False:
                url_text.value = "https://" + url_text.value
            if not validate_url(url_text.value):
                url_text.error_text = "Please enter a valid URL"
                page.update()
                return

            # Clean list view for new results
            lv.controls.clear()
            page.go("/results")

            # Progress indicator
            page.splash = progress_ring
            page.update()

            # Get webscrape results
            results = scrape(directory_path.value, url_text.value)
            if results:
                page.splash = None
                page.update()

            # Append to list view for log
            for result in results:
                lv.controls.append(ft.Text(f"{result}"))

            # Reset the user inputs
            url_text.value = ""
            directory_path.value = ""
            page.update()

    # Page Centered progress ring
    progress_ring = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.ProgressRing()]),
        ],
    )

    # Check for directory path change to remove error message
    def get_directory_result(e: FilePickerResultEvent):
        directory_path.value = e.path if e.path else ""
        url_text.error_text = ""
        page.update()

    # Url text field wiring
    def url_text_change(e):
        url_text.error_text = ""
        page.update()

    # User input
    url_text = ft.TextField(
        label="URL", hint_text="ocw.mit.edu/", autofocus=True, on_change=url_text_change
    )

    # Wiring for getting chosen path for download directory
    get_directory_dialog = FilePicker(on_result=get_directory_result)
    directory_path = Text()

    # Overlay dialog for file picker
    page.overlay.extend([get_directory_dialog])
    choose_directory = ft.ElevatedButton(
        "Choose Directory", on_click=lambda _: get_directory_dialog.get_directory_path()
    )

    # List view for data log
    lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

    # Route change and view handler
    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(
                        title=ft.Text("Scrape MiT"),
                        bgcolor=ft.colors.SURFACE_VARIANT,
                        center_title=True,
                    ),
                    ft.TextField(
                        label="About",
                        read_only=True,
                        multiline=True,
                        value=(
                            "This is a web scraper example with a GUI. \n I have tuned this scraper to find and download \n the course materials for any given course at \n https://ocw.mit.edu/.  \n \n *Disclaimer- FOR PERSONAL USE ONLY*  "
                        ),
                    ),
                    url_text,
                    ft.Row(
                        [
                            choose_directory,
                            ft.ElevatedButton(
                                "Submit",
                                on_click=lambda _: submit_url(url_text, directory_path),
                            ),
                        ],
                        spacing=10,
                    ),
                ],
            ),
        )

        if page.route == "/results":
            page.views.append(
                ft.View(
                    "/results",
                    [
                        ft.AppBar(
                            title=ft.Text("Results"), bgcolor=ft.colors.SURFACE_VARIANT
                        ),
                        ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                        lv,
                    ],
                )
            )

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main)
