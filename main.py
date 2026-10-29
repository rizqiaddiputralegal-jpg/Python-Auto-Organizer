import os
import shutil
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Set tema CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Pemetaan kategori file berdasarkan ekstensi
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv"],
    "Audio": [".mp3", ".wav", ".flac", ".aac"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code_and_Scripts": [".py", ".html", ".css", ".js", ".cpp", ".c", ".json", ".sql"],
    "Executables": [".exe", ".msi", ".deb", ".sh"]
}

class AutoOrganizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Auto File Organizer")
        self.geometry("580 x 420")
        self.resizable(False, False)

        self.selected_directory = ""

        # UI Layout
        self.create_widgets()

    def create_widgets(self):
        # Header Label
        self.header_label = ctk.CTkLabel(
            self, 
            text="Directory Auto Organizer", 
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.header_label.pack(pady=(20, 10))

        self.sub_label = ctk.CTkLabel(
            self, 
            text="Pilih folder untuk mengelompokkan file secara otomatis berdasarkan kategori.", 
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.sub_label.pack(pady=(0, 20))

        # Frame Pemilihan Folder
        self.folder_frame = ctk.CTkFrame(self)
        self.folder_frame.pack(padx=20, pady=10, fill="x")

        self.path_entry = ctk.CTkEntry(
            self.folder_frame, 
            placeholder_text="Belum ada folder yang dipilih...", 
            width=380
        )
        self.path_entry.pack(side="left", padx=(10, 5), pady=10)

        self.browse_btn = ctk.CTkButton(
            self.folder_frame, 
            text="Cari Folder", 
            width=110, 
            command=self.browse_folder
        )
        self.browse_btn.pack(side="right", padx=(5, 10), pady=10)

        # Log Box / Status Output
        self.log_box = ctk.CTkTextbox(self, width=540, height=160)
        self.log_box.pack(padx=20, pady=15)
        self.log_box.insert("0.0", "System Ready. Silakan pilih direktori target.\n")
        self.log_box.configure(state="disabled")

        # Tombol Eksekusi
        self.organize_btn = ctk.CTkButton(
            self, 
            text="Scan & Organize Files", 
            fg_color="#1f6aa5", 
            hover_color="#144870",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            command=self.organize_files
        )
        self.organize_btn.pack(pady=10)

    def log(self, message):
        """Menampilkan teks log ke Textbox."""
        self.log_box.configure(state="normal")
        self.log_box.insert("end", message + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.selected_directory = folder
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, folder)
            self.log(f"[+] Folder dipilih: {folder}")

    def organize_files(self):
        target_dir = self.path_entry.get().strip()

        if not target_dir or not os.path.exists(target_dir):
            messagebox.showwarning("Peringatan", "Pilih direktori yang valid terlebih dahulu!")
            return

        self.log("\n[=" + "="*30 + "=]")
        self.log("[*] Memulai proses scanning & pengelompokan...")

        moved_count = 0
        skipped_count = 0

        try:
            for item in os.listdir(target_dir):
                item_path = os.path.join(target_dir, item)

                # Abaikan jika itu folder/direktori
                if os.path.isdir(item_path):
                    continue

                _, ext = os.path.splitext(item)
                ext = ext.lower()

                if not ext:
                    continue

                category_found = "Others"
                for category, extensions in FILE_CATEGORIES.items():
                    if ext in extensions:
                        category_found = category
                        break

                # Buat folder kategori jika belum ada
                dest_folder = os.path.join(target_dir, category_found)
                os.makedirs(dest_folder, exist_ok=True)

                # Pindahkan file
                dest_file_path = os.path.join(dest_folder, item)
                if not os.path.exists(dest_file_path):
                    shutil.move(item_path, dest_file_path)
                    self.log(f" -> Moved: {item}  ==> [{category_found}]")
                    moved_count += 1
                else:
                    self.log(f" [!] Skipped (File Duplikat): {item}")
                    skipped_count += 1

            self.log(f"\n[+] Selesai! Total file dipindah: {moved_count}, Dilewati: {skipped_count}")
            messagebox.showinfo("Berhasil", f"Pengelompokan file selesai!\nFile dipindahkan: {moved_count}")

        except Exception as e:
            self.log(f"[ERROR] Terjadi kesalahan: {str(e)}")
            messagebox.showerror("Error", f"Gagal memproses file:\n{str(e)}")

if __name__ == "__main__":
    app = AutoOrganizerApp()
    app.mainloop()