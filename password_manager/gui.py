#!/usr/bin/env python3
"""
Graphical user interface for the Password Manager.
Provides a modern, user-friendly interface using tkinter.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
from typing import Optional
from password_manager import PasswordManager


class PasswordManagerGUI:
    """Graphical user interface for the Password Manager."""
    
    def __init__(self):
        self.pm = PasswordManager()
        self.root = tk.Tk()
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the main GUI window."""
        self.root.title("🔐 Secure Password Manager")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Status bar
        self.status_var = tk.StringVar(value="🔒 Locked - Please unlock to continue")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Create buttons
        ttk.Button(buttons_frame, text="🔓 Unlock", 
                  command=self.unlock_manager).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="🔒 Lock", 
                  command=self.lock_manager).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="➕ Add Password", 
                  command=self.add_password).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="🔍 Search", 
                  command=self.search_passwords).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="🔑 Generate", 
                  command=self.generate_password).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="📊 Stats", 
                  command=self.show_statistics).pack(side=tk.LEFT, padx=5)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Passwords tab
        self.setup_passwords_tab()
        
        # Settings tab
        self.setup_settings_tab()
        
        # Bind events
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_passwords_tab(self):
        """Setup the passwords display tab."""
        passwords_frame = ttk.Frame(self.notebook)
        self.notebook.add(passwords_frame, text="📋 Passwords")
        
        # Search frame
        search_frame = ttk.Frame(passwords_frame)
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_change)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Button(search_frame, text="Refresh", 
                  command=self.refresh_passwords).pack(side=tk.LEFT)
        
        # Treeview for passwords
        tree_frame = ttk.Frame(passwords_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Create Treeview
        columns = ('Service', 'Username', 'URL', 'Updated')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(c))
            self.tree.column(col, width=150)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        # Bind double-click event
        self.tree.bind('<Double-1>', self.on_password_double_click)
        
        # Action buttons
        action_frame = ttk.Frame(passwords_frame)
        action_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Button(action_frame, text="👁️ View Password", 
                  command=self.view_password).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(action_frame, text="✏️ Edit", 
                  command=self.edit_password).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="🗑️ Delete", 
                  command=self.delete_password).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="📋 Copy Username", 
                  command=self.copy_username).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="📋 Copy Password", 
                  command=self.copy_password).pack(side=tk.LEFT, padx=5)
        
    def setup_settings_tab(self):
        """Setup the settings tab."""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="⚙️ Settings")
        
        # Settings content
        content_frame = ttk.Frame(settings_frame, padding="20")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Change master password
        ttk.Label(content_frame, text="Master Password", 
                 font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=(0, 10))
        
        ttk.Button(content_frame, text="🔄 Change Master Password", 
                  command=self.change_master_password).pack(anchor=tk.W, pady=(0, 20))
        
        # Export/Import
        ttk.Label(content_frame, text="Data Management", 
                 font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=(0, 10))
        
        export_frame = ttk.Frame(content_frame)
        export_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(export_frame, text="📤 Export Passwords", 
                  command=self.export_passwords).pack(side=tk.LEFT, padx=(0, 10))
        
        # Database info
        ttk.Label(content_frame, text="Database Information", 
                 font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=(20, 10))
        
        info_frame = ttk.Frame(content_frame)
        info_frame.pack(fill=tk.X)
        
        ttk.Label(info_frame, text=f"Database file: {self.pm.db_path}").pack(anchor=tk.W)
        ttk.Label(info_frame, text="Total passwords: 0").pack(anchor=tk.W)
        
    def unlock_manager(self):
        """Unlock the password manager."""
        if self.pm.is_unlocked:
            messagebox.showinfo("Info", "Password manager is already unlocked!")
            return
        
        password = simpledialog.askstring("Unlock", "Enter master password:", 
                                        show='*')
        if password:
            if self.pm.unlock(password):
                self.status_var.set("🔓 Unlocked - Ready to use")
                self.refresh_passwords()
                messagebox.showinfo("Success", "Password manager unlocked successfully!")
            else:
                messagebox.showerror("Error", "Invalid master password!")
    
    def lock_manager(self):
        """Lock the password manager."""
        if not self.pm.is_unlocked:
            messagebox.showinfo("Info", "Password manager is already locked!")
            return
        
        self.pm.lock()
        self.status_var.set("🔒 Locked - Please unlock to continue")
        self.clear_treeview()
        messagebox.showinfo("Success", "Password manager locked successfully!")
    
    def add_password(self):
        """Add a new password entry."""
        if not self.pm.is_unlocked:
            messagebox.showerror("Error", "Please unlock the password manager first!")
            return
        
        # Create add password dialog
        dialog = AddPasswordDialog(self.root, self.pm)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            self.refresh_passwords()
    
    def search_passwords(self):
        """Search for passwords."""
        if not self.pm.is_unlocked:
            messagebox.showerror("Error", "Please unlock the password manager first!")
            return
        
        query = simpledialog.askstring("Search", "Enter search term:")
        if query:
            results = self.pm.search_passwords(query)
            self.display_passwords(results)
    
    def on_search_change(self, *args):
        """Handle search input changes."""
        if not self.pm.is_unlocked:
            return
        
        query = self.search_var.get().strip()
        if query:
            results = self.pm.search_passwords(query)
            self.display_passwords(results)
        else:
            self.refresh_passwords()
    
    def refresh_passwords(self):
        """Refresh the passwords display."""
        if not self.pm.is_unlocked:
            return
        
        passwords = self.pm.get_all_passwords()
        self.display_passwords(passwords)
    
    def display_passwords(self, passwords):
        """Display passwords in the treeview."""
        self.clear_treeview()
        
        for pwd in passwords:
            self.tree.insert('', tk.END, values=(
                pwd['service'],
                pwd['username'],
                pwd['url'] or '',
                pwd['updated_at']
            ), tags=(pwd['service'], pwd['username']))
    
    def clear_treeview(self):
        """Clear all items from the treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def sort_treeview(self, col):
        """Sort treeview by column."""
        # This is a simple implementation - in a real app you'd want more sophisticated sorting
        pass
    
    def on_password_double_click(self, event):
        """Handle double-click on password entry."""
        self.view_password()
    
    def view_password(self):
        """View selected password."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a password entry first!")
            return
        
        item = self.tree.item(selection[0])
        service = item['values'][0]
        username = item['values'][1]
        
        password_data = self.pm.get_password(service, username)
        if password_data:
            dialog = ViewPasswordDialog(self.root, password_data)
            self.root.wait_window(dialog.dialog)
    
    def edit_password(self):
        """Edit selected password."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a password entry first!")
            return
        
        item = self.tree.item(selection[0])
        service = item['values'][0]
        username = item['values'][1]
        
        password_data = self.pm.get_password(service, username)
        if password_data:
            dialog = EditPasswordDialog(self.root, self.pm, password_data)
            self.root.wait_window(dialog.dialog)
            if dialog.result:
                self.refresh_passwords()
    
    def delete_password(self):
        """Delete selected password."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a password entry first!")
            return
        
        item = self.tree.item(selection[0])
        service = item['values'][0]
        username = item['values'][1]
        
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete the password for {service} ({username})?"):
            if self.pm.delete_password(service, username):
                messagebox.showinfo("Success", "Password deleted successfully!")
                self.refresh_passwords()
            else:
                messagebox.showerror("Error", "Failed to delete password!")
    
    def copy_username(self):
        """Copy username to clipboard."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a password entry first!")
            return
        
        item = self.tree.item(selection[0])
        username = item['values'][1]
        
        self.root.clipboard_clear()
        self.root.clipboard_append(username)
        messagebox.showinfo("Success", "Username copied to clipboard!")
    
    def copy_password(self):
        """Copy password to clipboard."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a password entry first!")
            return
        
        item = self.tree.item(selection[0])
        service = item['values'][0]
        username = item['values'][1]
        
        password_data = self.pm.get_password(service, username)
        if password_data:
            self.root.clipboard_clear()
            self.root.clipboard_append(password_data['password'])
            messagebox.showinfo("Success", "Password copied to clipboard!")
    
    def generate_password(self):
        """Generate a strong password."""
        dialog = GeneratePasswordDialog(self.root, self.pm)
        self.root.wait_window(dialog.dialog)
    
    def show_statistics(self):
        """Show password manager statistics."""
        total_passwords = self.pm.get_password_count()
        
        if self.pm.is_unlocked and total_passwords > 0:
            passwords = self.pm.get_all_passwords()
            services = {}
            for pwd in passwords:
                service = pwd['service']
                services[service] = services.get(service, 0) + 1
            
            stats_text = f"Total passwords: {total_passwords}\n\nPasswords by service:\n"
            for service, count in sorted(services.items()):
                stats_text += f"  {service}: {count}\n"
        else:
            stats_text = f"Total passwords: {total_passwords}"
        
        messagebox.showinfo("Statistics", stats_text)
    
    def change_master_password(self):
        """Change the master password."""
        if not self.pm.is_unlocked:
            messagebox.showerror("Error", "Please unlock the password manager first!")
            return
        
        dialog = ChangeMasterPasswordDialog(self.root, self.pm)
        self.root.wait_window(dialog.dialog)
    
    def export_passwords(self):
        """Export passwords to a file."""
        if not self.pm.is_unlocked:
            messagebox.showerror("Error", "Please unlock the password manager first!")
            return
        
        filename = simpledialog.askstring("Export", "Enter filename (default: passwords_export.json):")
        if filename:
            if not filename.endswith('.json'):
                filename += '.json'
            
            if self.pm.export_passwords(filename):
                messagebox.showinfo("Success", f"Passwords exported to {filename}")
            else:
                messagebox.showerror("Error", "Failed to export passwords!")
    
    def on_closing(self):
        """Handle window closing."""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
    
    def run(self):
        """Run the GUI application."""
        self.root.mainloop()


class AddPasswordDialog:
    """Dialog for adding a new password."""
    
    def __init__(self, parent, pm):
        self.pm = pm
        self.result = False
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add New Password")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_dialog()
    
    def setup_dialog(self):
        """Setup the dialog content."""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Service
        ttk.Label(main_frame, text="Service/Website:").pack(anchor=tk.W)
        self.service_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.service_var).pack(fill=tk.X, pady=(0, 10))
        
        # Username
        ttk.Label(main_frame, text="Username:").pack(anchor=tk.W)
        self.username_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.username_var).pack(fill=tk.X, pady=(0, 10))
        
        # Password
        ttk.Label(main_frame, text="Password:").pack(anchor=tk.W)
        password_frame = ttk.Frame(main_frame)
        password_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(password_frame, textvariable=self.password_var, show='*')
        self.password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(password_frame, text="Generate", 
                  command=self.generate_password).pack(side=tk.RIGHT, padx=(5, 0))
        
        # URL
        ttk.Label(main_frame, text="URL (optional):").pack(anchor=tk.W)
        self.url_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.url_var).pack(fill=tk.X, pady=(0, 10))
        
        # Notes
        ttk.Label(main_frame, text="Notes (optional):").pack(anchor=tk.W)
        self.notes_text = tk.Text(main_frame, height=3)
        self.notes_text.pack(fill=tk.X, pady=(0, 20))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Add", command=self.add_password).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.RIGHT)
    
    def generate_password(self):
        """Generate a strong password."""
        try:
            password = self.pm.generate_password()
            self.password_var.set(password)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate password: {e}")
    
    def add_password(self):
        """Add the password."""
        service = self.service_var.get().strip()
        username = self.username_var.get().strip()
        password = self.password_var.get()
        url = self.url_var.get().strip()
        notes = self.notes_text.get("1.0", tk.END).strip()
        
        if not service or not username or not password:
            messagebox.showerror("Error", "Service, username, and password are required!")
            return
        
        if self.pm.add_password(service, username, password, url, notes):
            messagebox.showinfo("Success", "Password added successfully!")
            self.result = True
            self.dialog.destroy()
        else:
            messagebox.showerror("Error", "Failed to add password!")
    
    def cancel(self):
        """Cancel the dialog."""
        self.dialog.destroy()


class ViewPasswordDialog:
    """Dialog for viewing password details."""
    
    def __init__(self, parent, password_data):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("View Password")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_dialog(password_data)
    
    def setup_dialog(self, password_data):
        """Setup the dialog content."""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Service
        ttk.Label(main_frame, text="Service/Website:").pack(anchor=tk.W)
        ttk.Label(main_frame, text=password_data['service'], 
                 font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(0, 10))
        
        # Username
        ttk.Label(main_frame, text="Username:").pack(anchor=tk.W)
        ttk.Label(main_frame, text=password_data['username']).pack(anchor=tk.W, pady=(0, 10))
        
        # Password
        ttk.Label(main_frame, text="Password:").pack(anchor=tk.W)
        password_frame = ttk.Frame(main_frame)
        password_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.password_var = tk.StringVar(value=password_data['password'])
        password_entry = ttk.Entry(password_frame, textvariable=self.password_var, show='*')
        password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(password_frame, text="Show/Hide", 
                  command=lambda: self.toggle_password(password_entry)).pack(side=tk.RIGHT, padx=(5, 0))
        
        ttk.Button(password_frame, text="Copy", 
                  command=self.copy_password).pack(side=tk.RIGHT, padx=(5, 0))
        
        # URL
        if password_data['url']:
            ttk.Label(main_frame, text="URL:").pack(anchor=tk.W)
            ttk.Label(main_frame, text=password_data['url']).pack(anchor=tk.W, pady=(0, 10))
        
        # Notes
        if password_data['notes']:
            ttk.Label(main_frame, text="Notes:").pack(anchor=tk.W)
            ttk.Label(main_frame, text=password_data['notes'], 
                     wraplength=350).pack(anchor=tk.W, pady=(0, 10))
        
        # Close button
        ttk.Button(main_frame, text="Close", 
                  command=self.dialog.destroy).pack(pady=(20, 0))
    
    def toggle_password(self, entry):
        """Toggle password visibility."""
        if entry.cget('show') == '*':
            entry.configure(show='')
        else:
            entry.configure(show='*')
    
    def copy_password(self):
        """Copy password to clipboard."""
        self.dialog.clipboard_clear()
        self.dialog.clipboard_append(self.password_var.get())
        messagebox.showinfo("Success", "Password copied to clipboard!")


class EditPasswordDialog:
    """Dialog for editing a password."""
    
    def __init__(self, parent, pm, password_data):
        self.pm = pm
        self.password_data = password_data
        self.result = False
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Password")
        self.dialog.geometry("400x350")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_dialog()
    
    def setup_dialog(self):
        """Setup the dialog content."""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Service
        ttk.Label(main_frame, text="Service/Website:").pack(anchor=tk.W)
        self.service_var = tk.StringVar(value=self.password_data['service'])
        ttk.Entry(main_frame, textvariable=self.service_var).pack(fill=tk.X, pady=(0, 10))
        
        # Username
        ttk.Label(main_frame, text="Username:").pack(anchor=tk.W)
        self.username_var = tk.StringVar(value=self.password_data['username'])
        ttk.Entry(main_frame, textvariable=self.username_var).pack(fill=tk.X, pady=(0, 10))
        
        # Password
        ttk.Label(main_frame, text="Password:").pack(anchor=tk.W)
        password_frame = ttk.Frame(main_frame)
        password_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.password_var = tk.StringVar(value=self.password_data['password'])
        self.password_entry = ttk.Entry(password_frame, textvariable=self.password_var, show='*')
        self.password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(password_frame, text="Generate", 
                  command=self.generate_password).pack(side=tk.RIGHT, padx=(5, 0))
        
        # URL
        ttk.Label(main_frame, text="URL (optional):").pack(anchor=tk.W)
        self.url_var = tk.StringVar(value=self.password_data['url'])
        ttk.Entry(main_frame, textvariable=self.url_var).pack(fill=tk.X, pady=(0, 10))
        
        # Notes
        ttk.Label(main_frame, text="Notes (optional):").pack(anchor=tk.W)
        self.notes_text = tk.Text(main_frame, height=3)
        self.notes_text.insert("1.0", self.password_data['notes'])
        self.notes_text.pack(fill=tk.X, pady=(0, 20))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Update", command=self.update_password).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.RIGHT)
    
    def generate_password(self):
        """Generate a strong password."""
        try:
            password = self.pm.generate_password()
            self.password_var.set(password)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate password: {e}")
    
    def update_password(self):
        """Update the password."""
        service = self.service_var.get().strip()
        username = self.username_var.get().strip()
        password = self.password_var.get()
        url = self.url_var.get().strip()
        notes = self.notes_text.get("1.0", tk.END).strip()
        
        if not service or not username or not password:
            messagebox.showerror("Error", "Service, username, and password are required!")
            return
        
        if self.pm.update_password(
            self.password_data['service'], 
            self.password_data['username'],
            password, username, url, notes
        ):
            messagebox.showinfo("Success", "Password updated successfully!")
            self.result = True
            self.dialog.destroy()
        else:
            messagebox.showerror("Error", "Failed to update password!")
    
    def cancel(self):
        """Cancel the dialog."""
        self.dialog.destroy()


class GeneratePasswordDialog:
    """Dialog for generating a strong password."""
    
    def __init__(self, parent, pm):
        self.pm = pm
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Generate Strong Password")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_dialog()
    
    def setup_dialog(self):
        """Setup the dialog content."""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Length
        ttk.Label(main_frame, text="Password Length:").pack(anchor=tk.W)
        self.length_var = tk.StringVar(value="16")
        ttk.Entry(main_frame, textvariable=self.length_var).pack(fill=tk.X, pady=(0, 10))
        
        # Character sets
        self.use_uppercase = tk.BooleanVar(value=True)
        self.use_lowercase = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(main_frame, text="Include uppercase letters (A-Z)", 
                       variable=self.use_uppercase).pack(anchor=tk.W)
        ttk.Checkbutton(main_frame, text="Include lowercase letters (a-z)", 
                       variable=self.use_lowercase).pack(anchor=tk.W)
        ttk.Checkbutton(main_frame, text="Include digits (0-9)", 
                       variable=self.use_digits).pack(anchor=tk.W)
        ttk.Checkbutton(main_frame, text="Include symbols (!@#$%^&*)", 
                       variable=self.use_symbols).pack(anchor=tk.W, pady=(0, 20))
        
        # Generated password
        ttk.Label(main_frame, text="Generated Password:").pack(anchor=tk.W)
        password_frame = ttk.Frame(main_frame)
        password_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(password_frame, textvariable=self.password_var, font=('Courier', 10))
        password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(password_frame, text="Copy", 
                  command=self.copy_password).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Generate", command=self.generate_password).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Close", command=self.dialog.destroy).pack(side=tk.RIGHT)
        
        # Generate initial password
        self.generate_password()
    
    def generate_password(self):
        """Generate a strong password."""
        try:
            length = int(self.length_var.get())
            password = self.pm.generate_password(
                length=length,
                use_uppercase=self.use_uppercase.get(),
                use_lowercase=self.use_lowercase.get(),
                use_digits=self.use_digits.get(),
                use_symbols=self.use_symbols.get()
            )
            self.password_var.set(password)
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid length: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate password: {e}")
    
    def copy_password(self):
        """Copy password to clipboard."""
        password = self.password_var.get()
        if password:
            self.dialog.clipboard_clear()
            self.dialog.clipboard_append(password)
            messagebox.showinfo("Success", "Password copied to clipboard!")


class ChangeMasterPasswordDialog:
    """Dialog for changing the master password."""
    
    def __init__(self, parent, pm):
        self.pm = pm
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Change Master Password")
        self.dialog.geometry("400x250")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_dialog()
    
    def setup_dialog(self):
        """Setup the dialog content."""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Current password
        ttk.Label(main_frame, text="Current Master Password:").pack(anchor=tk.W)
        self.current_password = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.current_password, show='*').pack(fill=tk.X, pady=(0, 10))
        
        # New password
        ttk.Label(main_frame, text="New Master Password:").pack(anchor=tk.W)
        self.new_password = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.new_password, show='*').pack(fill=tk.X, pady=(0, 10))
        
        # Confirm password
        ttk.Label(main_frame, text="Confirm New Password:").pack(anchor=tk.W)
        self.confirm_password = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.confirm_password, show='*').pack(fill=tk.X, pady=(0, 20))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Change", command=self.change_password).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.RIGHT)
    
    def change_password(self):
        """Change the master password."""
        current = self.current_password.get()
        new = self.new_password.get()
        confirm = self.confirm_password.get()
        
        if not current or not new or not confirm:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        if new != confirm:
            messagebox.showerror("Error", "New passwords don't match!")
            return
        
        if len(new) < 8:
            messagebox.showerror("Error", "New password must be at least 8 characters long!")
            return
        
        if self.pm.change_master_password(current, new):
            messagebox.showinfo("Success", "Master password changed successfully!")
            self.dialog.destroy()
        else:
            messagebox.showerror("Error", "Failed to change master password!")


def main():
    """Main entry point."""
    try:
        app = PasswordManagerGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


if __name__ == "__main__":
    main() 