
---

## 📜 **Scripto: Text Extraction & Directory Tree Viewer**

`scripto.py` is a **command-line tool** that allows you to:
- 📂 **Print a directory tree** of a given folder.
- 📜 **Extract text from all files** in a folder (optionally recursively).
- 🛑 **Automatically ignore non-text files** and common directories like `.git`, `node_modules`, `dist`, `venv`, etc.
- 🔗 **Generate a clickable file link** for easy access.

---

## ⚡ **Installation & Usage**

### **1️⃣ View Directory Structure (`--tree`)**
Prints a **tree view** of all files and directories **(excluding ignored folders like `node_modules/`)**:
```sh
python scripto.py "C:\Users\Admin\Project" --tree
```

**Example Output:**
```
📁 Directory tree for: C:\Users\Admin\Project

├── client
│   ├── src
│   │   ├── components
│   │   ├── assets
│   │   ├── App.js
│   │   ├── index.js
│   └── package.json
├── server
│   ├── api
│   ├── config
│   ├── app.py
│   └── requirements.txt
└── README.md
```

---

### **2️⃣ Extract Text from Files**
Extracts **text** from all files in a folder **(ignoring binaries like `.class`, `.jar`, `.png`, `.ico`)**:
```sh
python scripto.py "C:\Users\Admin\Project"
```
- Generates **`combined_text.txt`** in the script’s directory.
- Provides a **clickable link** to open the file.

---

### **3️⃣ Extract Text Recursively (`--recursive`)**
Extracts text **from all subdirectories**:
```sh
python scripto.py "C:\Users\Admin\Project" --recursive
```

---

## 🛑 **Ignored Files & Folders**
- **Directories Automatically Skipped:**  
  - `.git`, `node_modules`, `dist`, `target`, `venv`, `.mvn`, `build`, `__pycache__`
- **Binary Files Skipped:**  
  - `.jar`, `.class`, `.exe`, `.png`, `.ico`, `.pdf`, `.zip`
- **Follows `.gitignore`** (respects ignored files)

---

## 🔗 **File Output & Clickable Links**
After text extraction, you’ll see:
```
✅ Text extraction complete! Open file:
📂 Click here: file:///C:/Users/Admin/scripto/combined_text.txt
📌 Or run this in PowerShell: start combined_text.txt
```
🚀 **Click the link** to open the extracted text file instantly!

---

## 📌 **Example Usage**
```sh
# View directory tree
python scripto.py "C:\Users\Admin\Project" --tree

# Extract text from all text-based files
python scripto.py "C:\Users\Admin\Project"

# Extract text recursively from all subdirectories
python scripto.py "C:\Users\Admin\Project" --recursive
```

---

## ⚡ **Why Use Scripto?**
✔️ **Quickly scan your project structure**  
✔️ **Extract text-only content from large codebases**  
✔️ **Automatically ignores non-relevant files**  
✔️ **Works on Windows, macOS, and Linux**  

🚀 **Now you have a powerful tool for text extraction & project navigation!**

---

## 📄 **License**
This project is licensed under the MIT License.

---

This README is **short, clear, and structured** to make your tool **easy to understand and use.** 🚀
