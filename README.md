# Helm Manager

Helm Manager is a simple **Kubernetes Helm Management GUI** built with **Flet**.  
This application allows users to **select Kubernetes contexts, install applications, manage deployments, and delete Helm releases** with a user-friendly interface.

---

## 🚀 Features

✅ **Select Kubernetes Context** – Choose and verify cluster availability.  
✅ **Install New Helm Applications** – Deploy applications with Helm charts easily.  
✅ **View Deployed Applications** – Displays all Helm releases in the cluster.  
✅ **Delete Installed Applications** – Uninstall releases with a single click.  
✅ **Auto & Manual Refresh** – Updates the deployed applications list automatically when changing context or on demand.  
✅ **Error Handling & Status Updates** – Shows meaningful error messages and success confirmations.  

---

## 🏗️ Tech Stack

- **Python** 🐍
- **Flet** (For UI) 🎨
- **Helm** (For Kubernetes package management) ⛵
- **kubectl** (For Kubernetes context management) ☸️

---

## 📥 Installation & Setup

### **1️⃣ Prerequisites**
Before running Helm Manager, ensure the following are installed on your system:

- **Python 3.8+** 🐍
- **Helm** (https://helm.sh/docs/intro/install/)
- **kubectl** (https://kubernetes.io/docs/tasks/tools/)
- A configured **Kubernetes Cluster** (e.g., Minikube, Kind, EKS, AKS, GKE)

---

### **2️⃣ Install Dependencies**
Clone this repository and install required Python packages:

```sh
git clone git@github.com:h0x3ein/installappWithFlet.git
cd installappWithFlet
pip install flet
```

---

### **3️⃣ Run the Application**
Simply execute:

```sh
python main.py
```
or
```
flet run main.py
```
---

## 🎮 Usage Guide

### **1️⃣ Select Kubernetes Context**
- Choose from available **Kubernetes contexts** in the dropdown.
- A **green dot** indicates that the cluster is reachable.
- If unreachable, the indicator turns **red**.

### **2️⃣ Install a New Helm Application**
- Click **"Install New App"** to expand the form.
- Fill in:
  - **Release Name** (Custom name for the deployment)
  - **Application** (Select from available Helm charts)
  - **Namespace** (Target namespace for deployment)
  - **Image Tag** (Specify the image version)
- Click **"Install"** to deploy.

### **3️⃣ View Deployed Applications**
- A table displays all **Helm releases** in the cluster.
- Shows **Release Name, Namespace, Status, and Chart Version**.

### **4️⃣ Delete an Application**
- Click the **Trash Icon 🗑️** next to any deployed app to **uninstall it**.

### **5️⃣ Refresh Deployment List**
- Click **"Refresh Deployed Apps"** to **manually reload** the list.

### **6️⃣ Auto-Refresh**
- The **list updates automatically** when switching Kubernetes contexts.

---

## ⚙️ Configuration

You can modify the **list of available applications** in `main.py`:

```python
AVAILABLE_APPS = {
    "MySQL": "oci://registry-1.docker.io/bitnamicharts/mysql",
    "PostgreSQL": "oci://registry-1.docker.io/bitnamicharts/postgresql",
    "Redis": "oci://registry-1.docker.io/bitnamicharts/redis",
    "Elasticsearch": "oci://registry-1.docker.io/bitnamicharts/elasticsearch",
    "Prometheus": "oci://registry-1.docker.io/bitnamicharts/prometheus",
}
```

Add or remove applications as needed.

---

## 🛠️ Troubleshooting

### **Common Issues**
| Issue | Solution |
|--------|---------|
| **"No Kubernetes contexts found"** | Ensure `kubectl` is installed and configured (`kubectl config get-contexts`). |
| **"Error installing Helm chart"** | Verify Helm is installed (`helm version`) and you have cluster permissions. |
| **"Cluster unreachable (Red dot)"** | Check your network, authentication, or cluster status (`kubectl cluster-info`). |

---

## 📜 License

This project is licensed under the **MIT License**.  
Feel free to modify and adapt as needed.

---

## 👥 Contributors

- **Hossein Jafari** – Lead Developer
- **Babi Team** – Maintainers & Reviewers

For contributions, open an issue or create a pull request! 🎯

---

## 📬 Contact

For inquiries, reach out to:

📧 Email: Hosseinjafari3264@gmail.com  
🔗 GitHub: [github.com/h0x3ein](https://github.com/h0x3ein)  
🏢 Company: [www.HSBabi.com](https://www.HSBabi.com)

