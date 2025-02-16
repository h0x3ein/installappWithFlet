import subprocess
import flet as ft

# Available Helm applications
AVAILABLE_APPS = {
    "MySQL": "oci://registry-1.docker.io/bitnamicharts/mysql",
    "PostgreSQL": "oci://registry-1.docker.io/bitnamicharts/postgresql",
    "Redis": "oci://registry-1.docker.io/bitnamicharts/redis",
    "Elasticsearch": "oci://registry-1.docker.io/bitnamicharts/elasticsearch",
    "Prometheus": "oci://registry-1.docker.io/bitnamicharts/prometheus",
}

# Fetch Kubernetes contexts
def get_kube_contexts():
    try:
        output = subprocess.check_output(["kubectl", "config", "get-contexts", "-o", "name"])
        return output.decode().splitlines()
    except subprocess.CalledProcessError:
        return []

# Check if context is reachable
def is_context_reachable(context_name: str) -> bool:
    try:
        subprocess.check_output(["kubectl", "--context", context_name, "cluster-info"], timeout=5)
        return True
    except:
        return False

# Install an app with Helm and show full error
def install_app(release_name, app_name, namespace, image_tag, kube_context):
    chart_ref = AVAILABLE_APPS.get(app_name)
    if not chart_ref:
        return f"❌ Error: No chart reference found for '{app_name}'"

    cmd = [
        "helm", "install", release_name, chart_ref,
        "--namespace", namespace,
        "--create-namespace",
        "--set", f"image.tag={image_tag}",
        "--kube-context", kube_context
    ]

    try:
        subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
        return f"✅ Installed {app_name} as '{release_name}' in namespace '{namespace}' (Tag: {image_tag})"
    except subprocess.CalledProcessError as e:
        return f"❌ {e.output.strip()}"  # Shows the actual Helm error message

# Main UI
def main(page: ft.Page):
    page.title = "Helm Manager"
    page.scroll = "auto"

    # Kubernetes Context Selection
    contexts = get_kube_contexts()
    selected_context = {"name": None}
    context_status = ft.Container(width=10, height=10, bgcolor="gray", border_radius=5)
    context_label = ft.Text("No context selected")

    def on_context_change(e):
        chosen = e.control.value
        if chosen:
            selected_context["name"] = chosen
            context_label.value = f"Current context: {chosen}"
            context_status.bgcolor = "green" if is_context_reachable(chosen) else "red"
        else:
            selected_context["name"] = None
            context_label.value = "No context selected"
            context_status.bgcolor = "gray"
        page.update()

    context_dropdown = ft.Dropdown(
        label="Kubernetes Context",
        options=[ft.dropdown.Option(c) for c in contexts],
        width=300,
        on_change=on_context_change
    )

    # Install New App Section (Initially Hidden)
    release_name_input = ft.TextField(label="Release Name", width=200)
    app_dropdown = ft.Dropdown(
        label="Application",
        options=[ft.dropdown.Option(a) for a in AVAILABLE_APPS],
        width=200
    )
    namespace_input = ft.TextField(label="Namespace", width=200)
    image_tag_input = ft.TextField(label="Image Tag", width=200)
    install_status = ft.Text("")
    install_section = ft.Column(visible=False)

    def on_install_click(e):
        if not selected_context["name"]:
            install_status.value = "⚠️ Select a context first!"
            page.update()
            return
        
        rname = release_name_input.value.strip()
        aname = app_dropdown.value
        ns = namespace_input.value.strip()
        tag = image_tag_input.value.strip()

        if not (rname and aname and ns and tag):
            install_status.value = "⚠️ Please fill all fields!"
        else:
            install_status.value = install_app(rname, aname, ns, tag, selected_context["name"])

        page.update()

    install_button = ft.ElevatedButton("Install", on_click=on_install_click)

    def toggle_install_section(e):
        install_section.visible = not install_section.visible
        page.update()

    install_toggle_btn = ft.ElevatedButton("Install New App", on_click=toggle_install_section)
    refresh_button = ft.ElevatedButton("Refresh Deployed Apps")

    # Layout
    page.add(
        ft.Row([context_dropdown, context_status]),
        context_label,
        ft.Row([install_toggle_btn, refresh_button]),
        install_section,
    )

    install_section.controls.extend([
        ft.Text("Install New App", style="headlineSmall"),
        release_name_input,
        app_dropdown,
        namespace_input,
        image_tag_input,
        install_button,
        install_status
    ])

ft.app(target=main)
