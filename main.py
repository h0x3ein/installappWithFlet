import subprocess
import flet as ft

def get_kube_contexts():
    """Retrieve available Kubernetes contexts."""
    try:
        output = subprocess.check_output(["kubectl", "config", "get-contexts", "-o", "name"])
        return output.decode().splitlines()
    except subprocess.CalledProcessError:
        return []

def main(page: ft.Page):
    page.title = "Kubernetes Context Selector"
    page.scroll = "auto"

    # Fetch Kubernetes contexts
    contexts = get_kube_contexts()

    # UI elements
    selected_context = ft.Text("No context selected")

    def on_context_change(e):
        selected_context.value = f"Selected context: {e.control.value}"
        page.update()

    context_dropdown = ft.Dropdown(
        label="Select Kubernetes Context",
        options=[ft.dropdown.Option(c) for c in contexts],
        on_change=on_context_change
    )

    # Add UI components to the page
    page.add(
        context_dropdown,
        selected_context
    )

ft.app(target=main)
