# GitHub Tool Documentation

This document provides instructions for using the **GitHub Tool**, which automates repository setup, SSH configuration, and documentation maintenance.

## **1. How to Initiate a New GitHub Repository**

### **Step 1: Create a Repository on GitHub**
1. Log in to [GitHub](https://github.com).
2. Click on the `+` icon and select **New Repository**.
3. Follow the steps to initialize the repository.

## **2. One-time Setup for Your Machine (Steps 1-4)**
These steps need to be done only **once per machine**.

### **Step 1: Check if You Already Have an SSH Key**
Run:
```sh
ls -al ~/.ssh
```
If you see files like `id_rsa.pub` or `id_ed25519.pub`, you already have an SSH key.

### **Step 2: Generate a New SSH Key (If Needed)**
If no key exists, generate a new one:
```sh
ssh-keygen -t ed25519 -C "your-email@example.com"
```
- **Press Enter** to accept the default location (`~/.ssh/id_ed25519`).
- Enter a **passphrase** (optional, recommended for security).

### **Step 3: Add Your SSH Key to GitHub**
1. **Copy your SSH key**:
   ```sh
   cat ~/.ssh/id_ed25519.pub
   ```
2. **Go to GitHub**:
   - Open [**GitHub SSH Settings**](https://github.com/settings/keys)
   - Click **"New SSH Key"**
   - Set a title (e.g., "My Laptop")
   - Paste the copied key into the **Key** field
   - Click **"Add SSH Key"**

### **Step 4: Test Your SSH Connection**
Run:
```sh
ssh -T git@github.com
```
If successful, you should see:
```
Hi yourusername! You've successfully authenticated, but GitHub does not provide shell access.
```

## **3. Steps to Follow Each Time You Create a New Repository**
These steps are needed **for each new repository**.

### **Step 5: Update Your Git Remote to Use SSH**
If you initially added your remote using HTTPS, update it to SSH:
```sh
git remote set-url origin git@github.com:yourusername/YourRepository.git
```


## **4. Adding Code to GitHub**
In your development environment, navigate to the root directory of your new GitHub repository, copy the code, and initialize Git:
```sh
git init
git add .
# Check status
git status
git commit -m "first commit"
git branch -M main
git remote add origin git@github.com:yourusername/YourRepository.git
git push -u origin main
```

---

# **GitHub Hooks for Documentation Maintenance**

## **1. Overview**
This repository includes **GitHub Hooks** that automatically maintain documentation files before each commit.

## **2. Installation**
1. Copy the `hooks/pre-commit` and `scripts/` directory into your repository root.
2. Run the following command to install the pre-commit hook:
```sh
chmod +x scripts/setup-hooks.sh
./scripts/setup-hooks.sh
```
3. Place the following marker in your `README.md` file where you want the table of contents:
```md
<!-- TOC --> 
<!-- TOC END -->
```

## **3. Hook Functionality**
- `pre-commit`: Ensures that `WORKLOG.md` is updated before each commit.
- `scripts/create_tabcont.py`: Generates a table of contents dynamically for markdown files.
- `scripts/list_tabcont.py`: Lists headers from markdown files.
- `scripts/setup-hooks.sh`: Installs the hooks into `.git/hooks`.
- `scripts/update-hours.sh`: Updates total hours worked in `README.md` and `WORKLOG.md`.

## **4. Setting Up and Running Hooks**
To properly ensure that `README.md` updates are also committed when changes occur, follow these steps:
1. **Ensure Hooks Are Installed:**
   ```sh
   ./scripts/setup-hooks.sh
   ```
2. **Modify `pre-commit` to Auto-Stage `README.md`:**
   In `hooks/pre-commit`, make sure the script stages the updated `README.md` by adding this line:
   ```sh
   git add README.md
   ```
3. **Verify Hook Execution:** Run a test commit:
   ```sh
   git commit -m "Test commit with hook validation"
   ```
   If `README.md` is updated, it should be staged automatically before the commit.

## **5. Setting Up a Python Virtual Environment**

To ensure dependencies are managed correctly, set up a **Python virtual environment**:

### **Step 1: Create and Activate a Virtual Environment**
```sh
python3 -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate  # For Windows
```

### **Step 2: Install Required Dependencies**
Before installing dependencies, ensure that your `pip` is up to date:
```sh
pip install --upgrade pip
```

Then, install dependencies from the `requirements.txt` file:Then, install dependencies inside the virtual environment:
```sh
pip install -r requirements.txt
```

### **Step 3: Deactivate the Virtual Environment (Optional)**
Once done working in the environment, deactivate it:
```sh
deactivate
```

## **6. Contribution & License**
- This project is open-source and free to use under the MIT License.
- Contributions are welcome! Feel free to submit pull requests or report issues.
 