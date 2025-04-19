import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
import os

key_file = "secret.key"
current_theme = "light"

# Tema ayarları
themes = {
    "light": {
        "bg": "#f0f0f0",
        "fg": "#000000",
        "button_bg": "#ffffff",
        "button_fg": "#000000"
    },
    "dark": {
        "bg": "#2e2e2e",
        "fg": "#ffffff",
        "button_bg": "#444444",
        "button_fg": "#ffffff"
    }
}

# Tema değiştir
def toggle_theme():
    global current_theme
    current_theme = "dark" if current_theme == "light" else "light"
    apply_theme()

def apply_theme():
    theme = themes[current_theme]
    root.config(bg=theme["bg"])
    for widget in root.winfo_children():
        if isinstance(widget, (tk.Label, tk.Button)):
            widget.config(bg=theme["button_bg"], fg=theme["button_fg"])
    title_label.config(bg=theme["bg"], fg=theme["fg"])
    bottom_label.config(bg=theme["bg"], fg="gray")

# Anahtar oluştur
def generate_key():
    key = Fernet.generate_key()
    with open(key_file, "wb") as key_out:
        key_out.write(key)
    messagebox.showinfo("Anahtar", f"Anahtar oluşturuldu ve '{key_file}' dosyasına kaydedildi.")

# Anahtarı yükle
def load_key():
    if not os.path.exists(key_file):
        messagebox.showerror("Hata", f"'{key_file}' bulunamadı. Lütfen önce anahtar oluşturun.")
        return None
    with open(key_file, "rb") as key_in:
        return key_in.read()

# Dosya şifreleme
def encrypt_file():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    key = load_key()
    if not key:
        return
    fernet = Fernet(key)
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        encrypted = fernet.encrypt(data)
        with open(file_path + ".encrypted", "wb") as f:
            f.write(encrypted)
        messagebox.showinfo("Başarılı", "Dosya şifrelendi.")
    except Exception as e:
        messagebox.showerror("Hata", f"Şifreleme başarısız: {str(e)}")

# Dosya şifresini çözme
def decrypt_file():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    key = load_key()
    if not key:
        return
    fernet = Fernet(key)
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        decrypted = fernet.decrypt(data)
        new_path = file_path.replace(".encrypted", "") + "_decrypted"
        with open(new_path, "wb") as f:
            f.write(decrypted)
        messagebox.showinfo("Başarılı", "Şifre çözme tamamlandı.")
    except Exception as e:
        messagebox.showerror("Hata", f"Şifre çözme başarısız: {str(e)}")

# Arayüz
root = tk.Tk()
root.title("Dosya Şifreleyici")
root.geometry("300x300")

title_label = tk.Label(root, text="🔐 Dosya Şifreleme Programı", font=("Arial", 12, "bold"))
title_label.pack(pady=10)

tk.Button(root, text="Anahtar Oluştur", command=generate_key, width=25).pack(pady=5)
tk.Button(root, text="Dosya Şifrele", command=encrypt_file, width=25).pack(pady=5)
tk.Button(root, text="Dosya Şifresini Çöz", command=decrypt_file, width=25).pack(pady=5)
tk.Button(root, text="🌗 Tema Değiştir", command=toggle_theme, width=25).pack(pady=15)

bottom_label = tk.Label(root, text="Anahtar dosyası: secret.key")
bottom_label.pack(side="bottom", pady=10)

apply_theme()
root.mainloop()
