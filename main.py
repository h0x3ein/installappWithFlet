import subprocess
import flet as ft

def get_kube_contexts():
    """Retrieve available Kubernetes contexts."""
    try:
        output = subprocess.check_output(["kubectl", "config", "get-contexts", "-o", "name"])
        return output.decode().splitlines()
    except subprocess.CalledProcessError:
        return []

def is_context_reachable(context_name: str) -> bool:
    """Check if the given Kubernetes context is reachable."""
    try:
        subprocess.check_output(["kubectl", "--context", context_name, "cluster-info"], timeout=5)
        return True
    except:
        return False

def main(page: ft.Page):
    page.title = "Kubernetes Context Selector"
    page.scroll = "auto"

    # Fetch Kubernetes contexts
    contexts = get_kube_contexts()

    # UI elements
    selected_context = ft.Text("No context selected")
    context_status = ft.Container(width=10, height=10, bgcolor="gray", border_radius=5)

    def on_context_change(e):
        """Handle context selection change."""
        chosen = e.control.value
        if chosen:
            selected_context.value = f"Selected context: {chosen}"
            context_status.bgcolor = "green" if is_context_reachable(chosen) else "red"
        else:
            selected_context.value = "No context selected"
            context_status.bgcolor = "gray"
        page.update()

    context_dropdown = ft.Dropdown(
        label="Select Kubernetes Context",
        options=[ft.dropdown.Option(c) for c in contexts],
        width=300,  # Set dropdown width
        on_change=on_context_change
    )

    # Add UI components to the page
    page.add(
        ft.Row([context_dropdown, context_status]),
        selected_context
    )

ft.app(target=main)
