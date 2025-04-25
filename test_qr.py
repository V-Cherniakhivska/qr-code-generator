import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import qrcode
import io
import base64

# Основне вікно
root = tk.Tk()
root.title("Генератор QR-кодів")
root.geometry("400x530")
root.configure(bg="#f5f5f5")

qr_image = None
qr_photo = None

def generate_qr():
    global qr_image, qr_photo
    data = entry.get().strip()
    if not data:
        messagebox.showwarning("Увага", "Введіть текст або URL!")
        return

    qr = qrcode.make(data)
    qr_image = qr

    qr_resized = qr.resize((200, 200))
    qr_photo = ImageTk.PhotoImage(qr_resized)
    qr_label.config(image=qr_photo)
    qr_label.image = qr_photo

    # Генерація base64-посилання
    buffered = io.BytesIO()
    qr.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    qr_link = f"data:image/png;base64,{img_str}"
    link_entry.delete(0, tk.END)
    link_entry.insert(0, qr_link)

def save_qr():
    if not qr_image:
        messagebox.showwarning("Увага", "QR-код ще не згенеровано.")
        return
    filepath = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png")],
        title="Зберегти QR-код як..."
    )
    if filepath:
        qr_image.save(filepath)
        messagebox.showinfo("Успіх", f"QR-код збережено:\n{filepath}")

def copy_link():
    link = link_entry.get()
    if link:
        root.clipboard_clear()
        root.clipboard_append(link)
        root.update()
        messagebox.showinfo("Скопійовано", "Посилання скопійовано в буфер обміну!")
    else:
        messagebox.showwarning("Увага", "Немає посилання для копіювання.")

# Інтерфейс
title = tk.Label(root, text="QR Generator", font=("Helvetica", 18, "bold"), bg="#f5f5f5", fg="#333")
title.pack(pady=10)

entry = tk.Entry(root, width=40, font=("Arial", 12))
entry.pack(pady=10)

generate_btn = tk.Button(root, text="Створити QR", font=("Arial", 12), bg="#4CAF50", fg="white", command=generate_qr)
generate_btn.pack(pady=10)

qr_label = tk.Label(root, bg="#f5f5f5")
qr_label.pack(pady=10)

save_btn = tk.Button(root, text="Зберегти QR-код", font=("Arial", 12), bg="#2196F3", fg="white", command=save_qr)
save_btn.pack(pady=10)

link_label = tk.Label(root, text="Base64-посилання для обміну:", bg="#f5f5f5", fg="#555")
link_label.pack()

link_entry = tk.Entry(root, width=45, font=("Arial", 10))
link_entry.pack(pady=5)

copy_btn = tk.Button(root, text="Скопіювати", font=("Arial", 10), bg="#FF9800", fg="white", command=copy_link)
copy_btn.pack(pady=5)

root.mainloop()
