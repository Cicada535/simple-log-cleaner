import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import sys
import pyperclip
from datetime import datetime
import random
from tkinter import messagebox

class SimpleLogCleaner:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Log Cleaner")
        self.root.geometry("800x600")
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, "images", "icon.png")
        self.root.iconphoto(False, tk.PhotoImage(file=icon_path))
        self.filtered_content = ""
        self.dark_mode = True
        
        self.colors = {
            "dark": {
                "bg": "#1e1e1e",
                "fg": "#e0e0e0",
                "frame_bg": "#2d2d2d",
                "button_bg": "#0d47a1",
                "button_fg": "#ffffff",
                "button_hover": "#1565c0",
                "text_bg": "#3a3a3a",
                "text_fg": "#e0e0e0",
                "label_bg": "#2d2d2d",
                "label_fg": "#e0e0e0",
                "labelframe_bg": "#2d2d2d",
                "labelframe_fg": "#e0e0e0",
                "success_btn": "#2e7d32",
                "success_hover": "#388e3c",
                "warning_btn": "#d46d13",
                "warning_hover": "#e47615",
                "info_btn": "#1565c0",
                "info_hover": "#1976d2",
                "menu_bg": "#2d2d2d",
                "menu_fg": "#e0e0e0",
                "menu_active": "#0d47a1",
                "example": "#699c17",
                "example_hover": "#85c51e",
                "delete": "#b31818",
                "delete_hover": "#ff0000",
            },
            "light": {
                "bg": "#f5f5f5",
                "fg": "#000000",
                "frame_bg": "#ffffff",
                "button_bg": "#2196f3",
                "button_fg": "#ffffff",
                "button_hover": "#1976d2",
                "text_bg": "#ffffff",
                "text_fg": "#000000",
                "label_bg": "#f5f5f5",
                "label_fg": "#000000",
                "labelframe_bg": "#f5f5f5",
                "labelframe_fg": "#000000",
                "success_btn": "#4caf50",
                "success_hover": "#45a049",
                "warning_btn": "#d46d13",
                "warning_hover": "#e47615",
                "info_btn": "#2196f3",
                "info_hover": "#0b7dda",
                "menu_bg": "#ffffff",
                "menu_fg": "#000000",
                "menu_active": "#2196f3",
                "example": "#699c17",
                "example_hover": "#85c51e",
                "delete": "#b31818",
                "delete_hover": "#ff0000",
            }
        }
        
        self.current_colors = self.colors["dark"]
        self.setup_ui()
        self.apply_theme()
        self.setup_hotkeys()
    
    def setup_ui(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        top_control_frame = tk.Frame(self.main_frame)
        top_control_frame.pack(fill=tk.X, pady=5)
        
        button_frame = tk.Frame(top_control_frame)
        button_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.file_label = tk.Label(button_frame, text="No file selected")
        self.file_label.pack(side=tk.LEFT, padx=5)
        
        self.select_btn = tk.Button(button_frame, text="Select .log File", command=self.select_file)
        self.select_btn.pack(side=tk.LEFT, padx=5)
        
        self.theme_btn = tk.Button(
            top_control_frame, 
            text="☀️ Light Mode", 
            command=self.toggle_theme,
        )
        self.theme_btn.pack(side=tk.RIGHT, padx=5, ipadx=10)
        
        param_frame = tk.LabelFrame(self.main_frame, text="Filter Parameters (one per line)", padx=10, pady=10)
        param_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.param_text = scrolledtext.ScrolledText(param_frame, height=8, width=70)
        self.param_text.pack(fill=tk.BOTH, expand=True)
        
        self.param_text.insert("1.0", "Enter parameters that lines must contain to be kept\n\nExamples (Minecraft):\n\n[Server thread/INFO] (<- log type)\n[Not Secure] (<- log subtype)\n<Cicada535> (<- player in chat)\norange (<- any mention)")
        
        self.param_text.bind("<Button-3>", lambda e: self.show_context_menu(e, self.param_text))
        
        self.actions_row = tk.Frame(self.main_frame, bg=self.current_colors["bg"])
        self.actions_row.pack(fill=tk.X, pady=10, padx=5)
        
        self.filter_btn = tk.Button(self.actions_row, text="Filter Log", command=self.filter_log)
        self.filter_btn.pack(side=tk.LEFT, padx=2)
        
        self.copy_btn = tk.Button(self.actions_row, text="Copy to Clipboard", command=self.copy_result)
        self.copy_btn.pack(side=tk.LEFT, padx=2)
        
        self.download_btn = tk.Button(self.actions_row, text="Download as File", command=self.download_file)
        self.download_btn.pack(side=tk.LEFT, padx=2)

        self.delete_all_btn = tk.Button(self.actions_row, text="Clear all", command=self.clear_all_fields)
        self.delete_all_btn.pack(side=tk.RIGHT, padx=2)

        self.example_btn = tk.Button(self.actions_row, text="Example", command=self.load_example)
        self.example_btn.pack(side=tk.RIGHT, padx=2)
        
        result_frame = tk.LabelFrame(self.main_frame, text="Filtered Results", padx=10, pady=10)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.result_text = scrolledtext.ScrolledText(result_frame, height=15, width=70, state=tk.DISABLED)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        self.result_text.bind("<Button-3>", lambda e: self.show_context_menu(e, self.result_text))
        
        self.selected_file = None
    
    def copy_result(self):
        content = self.result_text.get("1.0", tk.END).strip()
        if content:
            pyperclip.copy(content)
        else:
            messagebox.showinfo("Info", "The results field is empty!")

    def setup_hotkeys(self):
        for widget_class in ["Text", "Entry"]:
            self.root.bind_class(widget_class, "<Control-KeyPress>", self.universal_handler)

    def universal_handler(self, event):
        if event.keycode == 67:
            return self.hotkey_copy(event)
        elif event.keycode == 86:
            return self.hotkey_paste(event)
        elif event.keycode == 88:
            return self.hotkey_cut(event)
        elif event.keycode == 65:
            return self.hotkey_select_all(event)
    
    def get_focused_text_widget(self):
        try:
            widget = self.root.focus_get()
            if isinstance(widget, (scrolledtext.ScrolledText, tk.Text)):
                return widget
        except:
            pass
        return None
    
    def hotkey_copy(self, event=None):
        widget = self.get_focused_text_widget()
        if widget:
            try:
                selected = widget.get(tk.SEL_FIRST, tk.SEL_LAST)
                if selected:
                    pyperclip.copy(selected)
            except tk.TclError:
                pass
        return "break"
    
    def hotkey_paste(self, event=None):
        widget = self.get_focused_text_widget()
        if widget:
            try:
                text = pyperclip.paste()
                try:
                    widget.delete(tk.SEL_FIRST, tk.SEL_LAST)
                except tk.TclError:
                    pass
                widget.insert(tk.INSERT, text)
            except:
                pass
        return "break"
    
    def hotkey_cut(self, event=None):
        widget = self.get_focused_text_widget()
        if widget:
            try:
                selected = widget.get(tk.SEL_FIRST, tk.SEL_LAST)
                if selected:
                    pyperclip.copy(selected)
                    widget.delete(tk.SEL_FIRST, tk.SEL_LAST)
            except tk.TclError:
                pass
        return "break"
    
    def hotkey_select_all(self, event=None):
        widget = self.get_focused_text_widget()
        if widget:
            widget.tag_add(tk.SEL, "1.0", tk.END)
            widget.mark_set(tk.INSERT, "1.0")
            widget.see(tk.INSERT)
        return "break"
    
    def show_context_menu(self, event, widget):
        context_menu = tk.Menu(
            self.root, 
            tearoff=0,
            bg=self.current_colors["menu_bg"],
            fg=self.current_colors["menu_fg"],
            font=("Segoe UI", 10),
            activebackground=self.current_colors["menu_active"],
            activeforeground="#ffffff"
        )
        
        try:
            selected = widget.get(tk.SEL_FIRST, tk.SEL_LAST)
            has_selection = len(selected) > 0
        except tk.TclError:
            has_selection = False
        
        is_readonly = widget.cget("state") == tk.DISABLED
        
        if has_selection:
            context_menu.add_command(
                label="📋 Copy",
                accelerator="Ctrl+C",
                command=lambda: self.context_copy(widget)
            )

        if has_selection and not is_readonly:
            context_menu.add_command(
                label="🔪 Cut",
                accelerator="Ctrl+X",
                command=lambda: self.context_cut(widget)
            )

        if not is_readonly:
            try:
                clipboard_text = pyperclip.paste()
                context_menu.add_command(
                    label="📤 Paste",
                    accelerator="Ctrl+V",
                    command=lambda: self.context_paste(widget)
                )
            except:
                pass
        
        if has_selection or not is_readonly:
            context_menu.add_separator()
        
        context_menu.add_command(
            label="✓ Select All",
                accelerator="Ctrl+A",
            command=lambda: self.context_select_all(widget)
        )
        
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.after(200, context_menu.destroy)
    
    def context_copy(self, widget):
        try:
            selected = widget.get(tk.SEL_FIRST, tk.SEL_LAST)
            if selected:
                pyperclip.copy(selected)
        except tk.TclError:
            pass
    
    def context_paste(self, widget):
        try:
            text = pyperclip.paste()
            try:
                widget.delete(tk.SEL_FIRST, tk.SEL_LAST)
            except tk.TclError:
                pass
            widget.insert(tk.INSERT, text)
        except:
            pass
    
    def context_cut(self, widget):
        try:
            selected = widget.get(tk.SEL_FIRST, tk.SEL_LAST)
            if selected:
                pyperclip.copy(selected)
                widget.delete(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            pass
    
    def context_select_all(self, widget):
        widget.tag_add(tk.SEL, "1.0", tk.END)
        widget.mark_set(tk.INSERT, "1.0")
        widget.see(tk.INSERT)
    
    def apply_theme(self):
        colors = self.current_colors
        
        self.root.config(bg=colors["bg"])
        
        self.main_frame.config(bg=colors["bg"])
        for frame in self.main_frame.winfo_children():
            if isinstance(frame, tk.Frame):
                frame.config(bg=colors["bg"])
                for widget in frame.winfo_children():
                    if isinstance(widget, tk.Frame):
                        widget.config(bg=colors["bg"])
        
        for widget in self.main_frame.winfo_children():
            self.apply_theme_recursive(widget, colors)
        
        self.file_label.config(fg=colors["label_fg"], bg=colors["bg"])
        
        self.select_btn.config(
            bg=colors["button_bg"],
            fg=colors["button_fg"],
            activebackground=colors["button_hover"],
            activeforeground=colors["button_fg"]
        )
        
        self.theme_btn.config(
            bg=colors["info_btn"],
            fg=colors["button_fg"],
            activebackground=colors["info_hover"],
            activeforeground=colors["button_fg"]
        )
        
        self.filter_btn.config(
            bg=colors["success_btn"],
            fg=colors["button_fg"],
            activebackground=colors["success_hover"],
            activeforeground=colors["button_fg"]
        )
        
        self.copy_btn.config(
            bg=colors["info_btn"],
            fg=colors["button_fg"],
            activebackground=colors["info_hover"],
            activeforeground=colors["button_fg"]
        )
        
        self.download_btn.config(
            bg=colors["warning_btn"],
            fg=colors["button_fg"],
            activebackground=colors["warning_hover"],
            activeforeground=colors["button_fg"]
        )
        
        self.param_text.config(
            bg=colors["text_bg"],
            fg=colors["text_fg"],
            insertbackground=colors["text_fg"]
        )
        
        self.result_text.config(
            bg=colors["text_bg"],
            fg=colors["text_fg"],
            insertbackground=colors["text_fg"]
        )
        
        self.delete_all_btn.config(
            bg=colors["delete"],
            fg=colors["button_fg"],
            activebackground=colors["delete_hover"]
        )
        self.example_btn.config(
            bg=colors["example"],
            fg=colors["button_fg"],
            activebackground=colors["example_hover"]
        )
    
        for widget in self.main_frame.winfo_children():
            if isinstance(widget, tk.LabelFrame):
                widget.config(
                    bg=colors["labelframe_bg"],
                    fg=colors["labelframe_fg"]
                )
    
    def apply_theme_recursive(self, widget, colors):
        if isinstance(widget, tk.LabelFrame):
            widget.config(
                bg=colors["labelframe_bg"],
                fg=colors["labelframe_fg"]
            )
        elif isinstance(widget, tk.Label):
            widget.config(
                bg=colors["label_bg"],
                fg=colors["label_fg"]
            )
        elif isinstance(widget, tk.Frame):
            widget.config(bg=colors["bg"])
        
        for child in widget.winfo_children():
            self.apply_theme_recursive(child, colors)
    
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.current_colors = self.colors["dark"] if self.dark_mode else self.colors["light"]
        
        self.theme_btn.config(text="🌙        Dark Mode" if not self.dark_mode else "☀️ Light Mode")
        
        self.apply_theme()
    
    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Log File",
            filetypes=[("Log files", "*.log"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            self.selected_file = file_path
            self.file_label.config(text=f"Selected: {os.path.basename(file_path)}", fg=self.current_colors["label_fg"])
    
    def filter_log(self):
        if not self.selected_file:
            messagebox.showwarning("Warning", "Please select a log file first!")
            return
        
        params_text = self.param_text.get("1.0", tk.END).strip()
        
        if not params_text or params_text == "Enter parameters that lines must contain to be kept\n\nExamples (Minecraft):\n\n[Server thread/INFO] (<- log type)\n[Not Secure] (<- log subtype)\n<Cicada535> (<- player in chat)\norange (<- any mention)":
            messagebox.showwarning("Warning", "Please enter at least one filter parameter!")
            return
        
        parameters = [param.strip() for param in params_text.split('\n') if param.strip()]
        
        try:
            with open(self.selected_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            filtered_lines = []
            for line in lines:
                if all(param in line for param in parameters):
                    filtered_lines.append(line)
            
            self.filtered_content = ''.join(filtered_lines)
            
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert("1.0", self.filtered_content)
            self.result_text.config(state=tk.DISABLED)
            
            messagebox.showinfo("Success", f"Filtered log file!\nFound {len(filtered_lines)} matching lines out of {len(lines)} total lines.")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error reading file: {str(e)}")
    
    def copy_to_clipboard(self):
        if not self.filtered_content:
            messagebox.showwarning("Warning", "Please filter the log file first!")
            return
        
        try:
            pyperclip.copy(self.filtered_content)
            messagebox.showinfo("Success", "Filtered content copied to clipboard!")
        except Exception as e:
            messagebox.showerror("Error", f"Error copying to clipboard: {str(e)}")
    
    def download_file(self):
        if not self.filtered_content:
            messagebox.showwarning("Warning", "Please filter the log file first!")
            return
        
        timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        default_filename = f"cleaned_log_{timestamp}.log"
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".log",
            initialfile=default_filename,
            filetypes=[("Log files", "*.log"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.filtered_content)
                messagebox.showinfo("Success", f"File saved successfully!\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving file: {str(e)}")

    def clear_all_fields(self):
        if messagebox.askyesno("Confirmation", "Clear all fields and reset the file selection?", default=messagebox.NO):
            self.param_text.delete("1.0", tk.END)
            self.result_text.config(state='normal')
            self.result_text.delete("1.0", tk.END)
            self.result_text.config(state='disabled')
            self.selected_file = None
            self.file_label.config(text="No file selected")

    def load_example(self):
        if messagebox.askyesno("Confirmation", "Do you want to upload a test sample?\nYour current data will be deleted!", default=messagebox.NO):
            self.param_text.delete("1.0", tk.END)
            self.result_text.config(state='normal')
            self.result_text.delete("1.0", tk.END)
            self.result_text.config(state='disabled')

            
            phrases = [
                
                "[Server thread/INFO]",
                "INFO",
                "[Server thread/WARN]",
                "WARN",
                "[VoiceChatPacketProcessingThread/INFO]",
                "[voicechat]",
                "moved too quickly!",
                "has completed the challenge",
                "logged in",
                "joined the game",
                "left the game",
                "lost connection",
                "Received secret request",
                "Sent secret",
                "Disconnected",
                "§cAuthentication time has expired",
                "Rejecting UseItemOnPacket",
                "[Not Secure]",
                "<Steve123>",
                "<melon_Mask>",
                "Steve123",
                "melon_Mask",
                "Alex321",
                "angryFish",
                "Can't keep up!",
                "logged in with entity id",
                
                "[Not Secure]\n<Steve123>",
                "[Not Secure]\n<melon_Mask>",
                "[Not Secure]\nsteve",
                "[Not Secure]\nalex",
                "[Server thread/INFO]\n<Steve123>",
                "[Server thread/INFO]\nSteve123",
                "[Server thread/INFO]\n<melon_Mask>",
                "[Server thread/INFO]\nmelon_Mask",
                "[Server thread/INFO]\nAlex321",
                "[Server thread/INFO]\nangryFish",
                "INFO\nmelon_Mask",
                "INFO\nAlex321",
                "INFO\nangryFish",
                "[Server thread/WARN]\nmelon_Mask",
                "[Server thread/WARN]\nangryFish",
                "WARN\nmelon_Mask",
                "WARN\nangryFish",
                
                ]
            
            self.param_text.insert("1.0", random.choice(phrases))
            try:
                base_path = os.path.dirname(os.path.abspath(__file__))
                example_path = os.path.join(base_path, "examples", "example.log")
                if os.path.exists(example_path):
                    self.selected_file = example_path
                    self.file_label.config(text=f"Selected: example.log")
                else:
                    messagebox.showinfo("Info", "The sample file was not found in /examples/")
            except Exception as e:
                messagebox.showerror("Error", f"Unable to upload the sample: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleLogCleaner(root)
    root.mainloop()
