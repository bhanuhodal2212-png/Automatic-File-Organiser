import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from collections import Counter

# ---------- SETTINGS ----------
BG = "#0B1020"
CARD = "#151F33"
PURPLE = "#8B5CF6"
GREEN = "#2DD4A7"
WHITE = "#F1F5F9"
MUTED = "#94A3B8"

CATEGORIES = {
    "Images": [".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".webm"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".pptx", ".xlsx", ".csv"],
    "Music": [".mp3", ".wav", ".aac", ".flac", ".m4a"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".java", ".c", ".cpp", ".html", ".css", ".js"],
    "Installers": [".exe", ".msi", ".apk"]
}


def get_category(filename):
    ext = os.path.splitext(filename)[1].lower()

    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category

    return "Others"


class FileFlow:
    def __init__(self, root):
        self.root = root
        self.root.title("FileFlow | Smart File Organizer")
        self.root.geometry("950x680")
        self.root.minsize(780, 580)
        self.root.configure(bg=BG)

        self.folder = ""
        self.preview = tk.BooleanVar(value=True)
        self.files = []

        self.build_ui()

    def build_ui(self):
        # Header
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=25, pady=20)

        tk.Label(
            header, text="▦  FILEFLOW",
            font=("Arial", 25, "bold"),
            bg=BG, fg=PURPLE
        ).pack(side="left")

        tk.Label(
            header, text="SMART FILE ORGANIZER",
            font=("Arial", 10, "bold"),
            bg=BG, fg=GREEN
        ).pack(side="right", pady=10)

        tk.Label(
            self.root,
            text="Organize your digital life in one click.",
            font=("Arial", 13),
            bg=BG, fg=MUTED
        ).pack(anchor="w", padx=28)

        # Folder selection
        folder_card = tk.Frame(self.root, bg=CARD, padx=18, pady=16)
        folder_card.pack(fill="x", padx=25, pady=18)

        tk.Label(
            folder_card, text="SELECT YOUR FOLDER",
            font=("Arial", 10, "bold"),
            bg=CARD, fg=WHITE
        ).pack(anchor="w")

        row = tk.Frame(folder_card, bg=CARD)
        row.pack(fill="x", pady=(12, 0))

        self.path_label = tk.Label(
            row, text="No folder selected",
            font=("Arial", 10),
            bg="#202C43", fg=MUTED,
            anchor="w", padx=12, pady=12
        )
        self.path_label.pack(side="left", fill="x", expand=True)

        self.button(
            row, "Browse Folder", self.browse, PURPLE
        ).pack(side="left", padx=(10, 0))

        # Statistics
        stats = tk.Frame(self.root, bg=BG)
        stats.pack(fill="x", padx=25)

        self.total_label = self.stat_card(
            stats, "FILES FOUND", "0", PURPLE
        )
        self.types_label = self.stat_card(
            stats, "CATEGORIES", "0", GREEN
        )
        self.organized_label = self.stat_card(
            stats, "ORGANIZED", "0", "#FBBF24"
        )

        # Main area
        main = tk.Frame(self.root, bg=BG)
        main.pack(fill="both", expand=True, padx=25, pady=18)

        # Preview panel
        preview_panel = tk.Frame(main, bg=CARD, padx=15, pady=15)
        preview_panel.pack(
            side="left", fill="both", expand=True, padx=(0, 12)
        )

        tk.Label(
            preview_panel, text="File Preview",
            font=("Arial", 15, "bold"),
            bg=CARD, fg=WHITE
        ).pack(anchor="w", pady=(0, 10))

        self.listbox = tk.Listbox(
            preview_panel,
            bg="#10192A", fg=WHITE,
            selectbackground=PURPLE,
            font=("Consolas", 10),
            relief="flat", borderwidth=0
        )
        self.listbox.pack(fill="both", expand=True)

        # Actions panel
        actions = tk.Frame(main, bg=CARD, padx=15, pady=15, width=220)
        actions.pack(side="right", fill="y")
        actions.pack_propagate(False)

        tk.Label(
            actions, text="QUICK ACTIONS",
            font=("Arial", 12, "bold"),
            bg=CARD, fg=WHITE
        ).pack(anchor="w", pady=(0, 15))

        self.button(
            actions, "↻  Scan Files", self.scan, "#26344D"
        ).pack(fill="x", pady=5)

        self.button(
            actions, "✦  Organize Files", self.organize, GREEN,
            fg="#06251D"
        ).pack(fill="x", pady=5)

        self.button(
            actions, "Clear Preview", self.clear, "#26344D"
        ).pack(fill="x", pady=5)

        tk.Checkbutton(
            actions,
            text="Preview only (safe mode)",
            variable=self.preview,
            bg=CARD, fg=WHITE,
            activebackground=CARD,
            activeforeground=WHITE,
            selectcolor="#26344D",
            font=("Arial", 9),
            wraplength=180,
            justify="left"
        ).pack(anchor="w", pady=15)

        tk.Label(
            actions,
            text="Files are sorted into category folders. Existing files are never overwritten.",
            bg=CARD, fg=MUTED,
            font=("Arial", 9),
            wraplength=180, justify="left"
        ).pack(anchor="w", pady=5)

        # Footer
        self.status = tk.Label(
            self.root, text="Ready to organize.",
            bg=BG, fg=MUTED,
            font=("Arial", 10), anchor="w"
        )
        self.status.pack(fill="x", padx=28, pady=(0, 15))

    def stat_card(self, parent, title, value, color):
        card = tk.Frame(parent, bg=CARD, padx=18, pady=14)
        card.pack(side="left", fill="x", expand=True, padx=(0, 10))

        tk.Label(
            card, text=title,
            font=("Arial", 9, "bold"),
            bg=CARD, fg=MUTED
        ).pack(anchor="w")

        number = tk.Label(
            card, text=value,
            font=("Arial", 23, "bold"),
            bg=CARD, fg=color
        )
        number.pack(anchor="w", pady=(5, 0))
        return number

    def button(self, parent, text, command, color, fg=WHITE):
        return tk.Button(
            parent, text=text, command=command,
            bg=color, fg=fg,
            activebackground=PURPLE,
            activeforeground=WHITE,
            font=("Arial", 10, "bold"),
            relief="flat", cursor="hand2",
            padx=12, pady=11, borderwidth=0
        )

    def browse(self):
        selected = filedialog.askdirectory(
            title="Choose a folder to organize"
        )
        if selected:
            self.folder = selected
            self.path_label.config(
                text=selected, fg=WHITE
            )
            self.scan()

    def scan(self):
        if not self.folder or not os.path.isdir(self.folder):
            messagebox.showwarning(
                "Select Folder", "Please select a valid folder first."
            )
            return

        try:
            self.files = [
                name for name in os.listdir(self.folder)
                if os.path.isfile(os.path.join(self.folder, name))
            ]
        except OSError as error:
            messagebox.showerror("Scan Error", str(error))
            return

        self.listbox.delete(0, tk.END)
        counts = Counter()

        for name in sorted(self.files, key=str.lower):
            category = get_category(name)
            counts[category] += 1
            self.listbox.insert(
                tk.END, f"  {category:<12} | {name}"
            )

        self.total_label.config(text=str(len(self.files)))
        self.types_label.config(text=str(len(counts)))
        self.organized_label.config(text="0")

        self.status.config(
            text=f"Scan complete: {len(self.files)} files found."
        )

    def organize(self):
        if not self.folder or not os.path.isdir(self.folder):
            messagebox.showwarning(
                "Select Folder", "Choose a folder first."
            )
            return

        if not self.files:
            self.scan()
            if not self.files:
                messagebox.showinfo(
                    "No Files", "There are no files to organize."
                )
                return

        if not self.preview.get():
            confirm = messagebox.askyesno(
                "Confirm Organization",
                f"Move {len(self.files)} files into category folders?\n\n"
                "Test on a folder containing copies first."
            )
            if not confirm:
                return

        success = 0
        errors = []

        for name in list(self.files):
            category = get_category(name)

            if self.preview.get():
                success += 1
                continue

            try:
                source = os.path.join(self.folder, name)
                destination_folder = os.path.join(
                    self.folder, category
                )
                os.makedirs(destination_folder, exist_ok=True)

                destination = os.path.join(
                    destination_folder, name
                )

                # Never overwrite a file with the same name.
                stem, ext = os.path.splitext(name)
                number = 1
                while os.path.exists(destination):
                    destination = os.path.join(
                        destination_folder,
                        f"{stem} ({number}){ext}"
                    )
                    number += 1

                shutil.move(source, destination)
                success += 1

            except OSError as error:
                errors.append(f"{name}: {error}")

        self.organized_label.config(text=str(success))

        if self.preview.get():
            self.status.config(
                text=f"Preview complete: {success} files ready."
            )
            messagebox.showinfo(
                "Preview Complete",
                f"{success} files can be organized.\n\n"
                "Turn off Preview only and click Organize Files "
                "to move them."
            )
        else:
            self.scan()
            self.organized_label.config(text=str(success))
            self.status.config(
                text=f"Finished: {success} organized, {len(errors)} errors."
            )
            message = f"Successfully organized {success} files."
            if errors:
                message += "\n\nErrors:\n" + "\n".join(errors[:5])
            messagebox.showinfo("Complete", message)

    def clear(self):
        self.listbox.delete(0, tk.END)
        self.total_label.config(text="0")
        self.types_label.config(text="0")
        self.organized_label.config(text="0")
        self.files = []
        self.status.config(text="Preview cleared.")


if __name__ == "__main__":
    root = tk.Tk()
    app = FileFlow(root)
    root.mainloop()
