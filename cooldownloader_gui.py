import customtkinter as ctk
from tkinter import filedialog, messagebox
from utils.downloader import download_file  # Logic we wrote in previous step
import threading
import os

# Set the visual theme
ctk.set_appearance_mode("Dark") 
ctk.set_default_color_theme("blue")

class CoolDownloaderGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Configuration ---
        self.title("CoolDownloader Pro")
        self.geometry("800x450")

        # Configure Grid (2 columns: Sidebar and Main)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar Frame ---
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="COOL\nDL", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.pack(pady=30)

        self.info_label = ctk.CTkLabel(self.sidebar, text="Supported:\n• Direct Links\n• YouTube\n• GitHub", 
                                       font=ctk.CTkFont(size=12), text_color="gray")
        self.info_label.pack(pady=20)

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.pack(side="bottom", padx=20, pady=(0, 10))
        self.appearance_mode_menu = ctk.CTkOptionMenu(self.sidebar, values=["Dark", "Light", "System"],
                                                      command=self.change_appearance_mode)
        self.appearance_mode_menu.pack(side="bottom", padx=20, pady=(0, 20))

        # --- Main Content Frame ---
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.grid(row=0, column=1, padx=30, pady=20, sticky="nsew")

        # Title
        self.header = ctk.CTkLabel(self.main_content, text="New Download", font=ctk.CTkFont(size=20, weight="bold"))
        self.header.pack(anchor="w", pady=(10, 20))

        # URL Input
        self.url_entry = ctk.CTkEntry(self.main_content, placeholder_text="Paste your link here (HTTPS or YouTube)...", 
                                      height=45, width=500)
        self.url_entry.pack(fill="x", pady=10)

        # Path Selection Box
        self.path_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        self.path_frame.pack(fill="x", pady=10)

        self.path_display = ctk.CTkEntry(self.path_frame, placeholder_text="No destination selected...", height=35)
        self.path_display.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.browse_btn = ctk.CTkButton(self.path_frame, text="Browse", width=100, command=self.browse_path)
        self.browse_btn.pack(side="right")

        # Progress Section
        self.progress_label = ctk.CTkLabel(self.main_content, text="Status: Waiting for input", font=ctk.CTkFont(size=12))
        self.progress_label.pack(anchor="w", pady=(20, 5))

        self.progress_bar = ctk.CTkProgressBar(self.main_content, orientation="horizontal")
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", pady=5)

        # Action Button
        self.download_btn = ctk.CTkButton(self.main_content, text="START DOWNLOAD", 
                                          height=50, font=ctk.CTkFont(size=16, weight="bold"),
                                          command=self.start_download_thread)
        self.download_btn.pack(fill="x", pady=30)

        self.save_path = ""

    # --- Logic Methods ---
    def change_appearance_mode(self, new_mode):
        ctk.set_appearance_mode(new_mode)

    def browse_path(self):
        # We try to guess a name from the URL if possible
        file_path = filedialog.asksaveasfilename(defaultextension=".*",
                                                 title="Select where to save")
        if file_path:
            self.save_path = file_path
            self.path_display.delete(0, "end")
            self.path_display.insert(0, file_path)

    def update_progress(self, value):
        # Callback function for the downloader
        self.progress_bar.set(value)
        self.progress_label.configure(text=f"Status: Downloading... {int(value*100)}%")

    def start_download_thread(self):
        url = self.url_entry.get()
        if not url or not self.save_path:
            messagebox.showwarning("Missing Info", "Please provide both a URL and a destination path!")
            return

        # Disable UI to prevent double-clicks
        self.download_btn.configure(state="disabled", text="Working...")
        
        # Start threading so the GUI doesn't hang
        download_thread = threading.Thread(target=self.run_download, args=(url, self.save_path), daemon=True)
        download_thread.start()

    def run_download(self, url, path):
        try:
            success = download_file(url, path, progress_callback=self.update_progress)
            
            if success:
                self.progress_label.configure(text="Status: Download Complete!")
                messagebox.showinfo("Success", f"File saved to:\n{path}")
            else:
                self.progress_label.configure(text="Status: Failed")
                messagebox.showerror("Error", "Something went wrong with the download.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.download_btn.configure(state="normal", text="START DOWNLOAD")
            self.progress_bar.set(0)

if __name__ == "__main__":
    app = CoolDownloaderGUI()
    app.mainloop()