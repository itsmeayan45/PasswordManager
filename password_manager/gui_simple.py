#!/usr/bin/env python3
"""
Simple GUI for the Password Manager using tkinter.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from password_manager import PasswordManager


class SimplePasswordManagerGUI:
    """Simple GUI for the Password Manager."""
    
    def __init__(self):
        self.pm = PasswordManager()
        self.root = tk.Tk()
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the main GUI window."""
        self.root.title("🔐 Password Manager")
        self.root.geometry("600x400")
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Status
        self.status_var = tk.StringVar(value="🔒 Locked")
        status_label = ttk.Label(main_frame, textvariable=self.status_var)
        status_label.pack(pady=(0, 10))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=(0, 10))
        
        ttk.Button(button_frame, text="🔓 Unlock", command=self.unlock).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🔒 Lock", command=self.lock).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="➕ Add", command=self.add_password).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🔍 Search", command=self.search).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🔑 Generate", command=self.generate).pack(side=tk.LEFT, padx=5)
        
        # Treeview for passwords
        columns = ('Service', 'Username', 'URL')
        self.tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double-click
        self.tree.bind('<Double-1>', self.view_password)
        
        # Action buttons
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(action_frame, text="👁️ View", command=self.view_password).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="✏️ Edit", command=self.edit_password).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="🗑️ Delete", command=self.delete_password).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="📋 Copy", command=self.copy_password).pack(side=tk.LEFT, padx=5)
        
    def unlock(self):
        """Unlock the password manager."""
        if self.pm.is_unlocked:
            messagebox.showinfo("Info", "Already unlocked!")
            return
        
        password = simpledialog.askstring("Unlock", "Enter master password:", show='*')
        if password and self.pm.unlock(password):
            self.status_var.set("🔓 Unlocked")
            self.refresh_passwords()
            messagebox.showinfo("Success", "Unlocked successfully!")
        else:
            messagebox.showerror("Error", "Invalid password!")
    
    def lock(self):
        """Lock the password manager."""
        self.pm.lock()
        self.status_var.set("🔒 Locked")
        self.clear_tree()
        messagebox.showinfo("Success", "Locked successfully!")
    
    def add_password(self):
        """Add a new password."""
        if not self.pm.is_unlocked:
            messagebox.showerror("Error", "Please unlock first!")
            return
        
        service = simpledialog.askstring("Add Password", "Service/Website:")
        if not service:
            return
        
        username = simpledialog.askstring("Add Password", "Username:")
        if not username:
            return
        
        password = simpledialog.askstring("Add Password", "Password:", show='*')
        if not password:
            return
        
        url = simpledialog.askstring("Add Password", "URL (optional):")
        
        if self.pm.add_password(service, username, password, url or ""):
            messagebox.showinfo("Success", "Password added!")
            self.refresh_passwords()
        else:
            messagebox.showerror("Error", "Failed to add password!")
    
    def search(self):
        """Search passwords."""
        if not self.pm.is_unlocked:
            messagebox.showerror("Error", "Please unlock first!")
            return
        
        query = simpledialog.askstring("Search", "Enter search term:")
        if query:
            results = self.pm.search_passwords(query)
            self.display_passwords(results)
    
    def generate(self):
        """Generate a strong password."""
        try:
            password = self.pm.generate_password()
            messagebox.showinfo("Generated Password", f"Password: {password}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate: {e}")
    
    def refresh_passwords(self):
        """Refresh password list."""
        if self.pm.is_unlocked:
            passwords = self.pm.get_all_passwords()
            self.display_passwords(passwords)
    
    def display_passwords(self, passwords):
        """Display passwords in treeview."""
        self.clear_tree()
        for pwd in passwords:
            self.tree.insert('', tk.END, values=(
                pwd['service'],
                pwd['username'],
                pwd['url'] or ''
            ), tags=(pwd['service'], pwd['username']))
    
    def clear_tree(self):
        """Clear treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def view_password(self, event=None):
        """View selected password."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a password!")
            return
        
        item = self.tree.item(selection[0])
        service = item['values'][0]
        username = item['values'][1]
        
        password_data = self.pm.get_password(service, username)
        if password_data:
            messagebox.showinfo("Password", 
                              f"Service: {service}\n"
                              f"Username: {username}\n"
                              f"Password: {password_data['password']}")
    
    def edit_password(self):
        """Edit selected password."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a password!")
            return
        
        item = self.tree.item(selection[0])
        service = item['values'][0]
        username = item['values'][1]
        
        password_data = self.pm.get_password(service, username)
        if password_data:
            new_password = simpledialog.askstring("Edit Password", 
                                                "New password:", show='*')
            if new_password:
                if self.pm.update_password(service, username, new_password):
                    messagebox.showinfo("Success", "Password updated!")
                    self.refresh_passwords()
                else:
                    messagebox.showerror("Error", "Failed to update!")
    
    def delete_password(self):
        """Delete selected password."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a password!")
            return
        
        item = self.tree.item(selection[0])
        service = item['values'][0]
        username = item['values'][1]
        
        if messagebox.askyesno("Confirm", f"Delete password for {service}?"):
            if self.pm.delete_password(service, username):
                messagebox.showinfo("Success", "Password deleted!")
                self.refresh_passwords()
            else:
                messagebox.showerror("Error", "Failed to delete!")
    
    def copy_password(self):
        """Copy password to clipboard."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a password!")
            return
        
        item = self.tree.item(selection[0])
        service = item['values'][0]
        username = item['values'][1]
        
        password_data = self.pm.get_password(service, username)
        if password_data:
            self.root.clipboard_clear()
            self.root.clipboard_append(password_data['password'])
            messagebox.showinfo("Success", "Password copied to clipboard!")
    
    def run(self):
        """Run the GUI."""
        self.root.mainloop()


def main():
    """Main entry point."""
    app = SimplePasswordManagerGUI()
    app.run()


if __name__ == "__main__":
    main() 