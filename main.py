import subprocess
import json
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

# Get deployed Helm releases
def get_helm_releases(kube_context):
    try:
        cmd = ["helm", "list", "--all-namespaces", "-o", "json", "--kube-context", kube_context]
        output = subprocess.check_output(cmd)
        return json.loads(output)
    except Exception:
        return []

# Install an app with Helm
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

# Delete a Helm release
def delete_app(release_name, namespace, kube_context):
    cmd = ["helm", "uninstall", release_name, "-n", namespace, "--kube-context", kube_context]
    try:
        subprocess.check_call(cmd)
        return f"✅ Deleted release '{release_name}' from namespace '{namespace}'"
    except subprocess.CalledProcessError as e:
        return f"❌ Error deleting {release_name}: {e}"

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
            refresh_releases(None)  # Auto-refresh deployed apps when context changes
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
    install_section = ft.Column(visible=False)

    release_name_input = ft.TextField(label="Release Name", width=200)
    app_dropdown = ft.Dropdown(
        label="Application",
        options=[ft.dropdown.Option(a) for a in AVAILABLE_APPS],
        width=200
    )
    namespace_input = ft.TextField(label="Namespace", width=200)
    image_tag_input = ft.TextField(label="Image Tag", width=200)
    install_status = ft.Text("")

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
        
        refresh_releases(None)  # Refresh list after installing
        page.update()

    install_button = ft.ElevatedButton("Install", on_click=on_install_click)

    def toggle_install_section(e):
        install_section.visible = not install_section.visible  # FIX: Now toggles correctly
        page.update()

    install_toggle_btn = ft.ElevatedButton("Install New App", on_click=toggle_install_section)

    # Deployed Apps Section
    deployments_column = ft.Column()

    def on_delete_click(e, rname, ns):
        """Delete a release when trash icon is clicked."""
        if not selected_context["name"]:
            page.snack_bar = ft.SnackBar(ft.Text("⚠️ Select a context first!"))
            page.snack_bar.open = True
            page.update()
            return

        msg = delete_app(rname, ns, selected_context["name"])
        page.snack_bar = ft.SnackBar(ft.Text(msg))
        page.snack_bar.open = True
        refresh_releases(None)  # Refresh list after deletion

    def refresh_releases(e):
        """Refresh the list of deployed Helm releases."""
        deployments_column.controls.clear()

        header = ft.Row(
            controls=[
                ft.Text("Release", width=140, weight="bold"),
                ft.Text("Namespace", width=120, weight="bold"),
                ft.Text("Status", width=100, weight="bold"),
                ft.Text("Chart", width=150, weight="bold"),
                ft.Text("", width=40),  # Placeholder for delete icon
            ],
            spacing=5
        )
        deployments_column.controls.append(header)

        if not selected_context["name"]:
            page.update()
            return

        releases = get_helm_releases(selected_context["name"])
        for r in releases:
            rname = r.get("name")
            ns = r.get("namespace")
            status = r.get("status")
            chart_field = r.get("chart", "")

            # Row for each deployed app
            row = ft.Row(
                controls=[
                    ft.Text(rname, width=140),
                    ft.Text(ns, width=120),
                    ft.Text(status, width=100),
                    ft.Text(chart_field, width=150),
                    ft.IconButton(
                        icon=ft.icons.DELETE,
                        tooltip="Delete release",
                        on_click=lambda e, rn=rname, n=ns: on_delete_click(e, rn, n)
                    ),
                ],
                spacing=5
            )
            deployments_column.controls.append(row)

        page.update()

    refresh_button = ft.ElevatedButton("Refresh Deployed Apps", on_click=refresh_releases)

    # Layout
    page.add(
        ft.Row([context_dropdown, context_status]),
        context_label,
        ft.Row([install_toggle_btn, refresh_button]),
        install_section,
        ft.Text("Deployed Apps", style="headlineSmall"),
        deployments_column
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
