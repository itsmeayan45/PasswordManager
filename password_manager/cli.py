#!/usr/bin/env python3
"""
Command-line interface for the Password Manager.
Provides an interactive menu-driven interface for managing passwords.
"""

import getpass
import sys
import os
from typing import Optional
from password_manager import PasswordManager


class PasswordManagerCLI:
    """Command-line interface for the Password Manager."""
    
    def __init__(self):
        self.pm = PasswordManager()
        self.current_user = None
    
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Print the application header."""
        print("=" * 60)
        print("🔐 SECURE PASSWORD MANAGER")
        print("=" * 60)
        print()
    
    def print_menu(self):
        """Print the main menu options."""
        print("📋 MAIN MENU:")
        print("1. 🔓 Unlock Password Manager")
        print("2. 🔒 Lock Password Manager")
        print("3. ➕ Add New Password")
        print("4. 🔍 Search Passwords")
        print("5. 📋 List All Passwords")
        print("6. 🔧 Update Password")
        print("7. 🗑️  Delete Password")
        print("8. 🔑 Generate Strong Password")
        print("9. 📤 Export Passwords")
        print("10. 🔄 Change Master Password")
        print("11. 📊 Show Statistics")
        print("0. 🚪 Exit")
        print()
    
    def get_secure_input(self, prompt: str, hide: bool = False) -> str:
        """Get secure user input, optionally hiding the input."""
        if hide:
            return getpass.getpass(prompt)
        else:
            return input(prompt)
    
    def unlock_manager(self):
        """Unlock the password manager."""
        print("🔓 UNLOCK PASSWORD MANAGER")
        print("-" * 30)
        
        if self.pm.is_unlocked:
            print("✅ Password manager is already unlocked!")
            return
        
        master_password = self.get_secure_input("Enter master password: ", hide=True)
        
        if self.pm.unlock(master_password):
            print("✅ Password manager unlocked successfully!")
            self.current_user = "User"
        else:
            print("❌ Invalid master password!")
    
    def lock_manager(self):
        """Lock the password manager."""
        if not self.pm.is_unlocked:
            print("❌ Password manager is already locked!")
            return
        
        self.pm.lock()
        self.current_user = None
        print("🔒 Password manager locked successfully!")
    
    def add_password(self):
        """Add a new password entry."""
        if not self.pm.is_unlocked:
            print("❌ Please unlock the password manager first!")
            return
        
        print("➕ ADD NEW PASSWORD")
        print("-" * 20)
        
        service = input("Service/Website: ").strip()
        username = input("Username: ").strip()
        
        if not service or not username:
            print("❌ Service and username are required!")
            return
        
        # Check if password already exists
        existing = self.pm.get_password(service, username)
        if existing:
            print(f"⚠️  Password for {service} with username {username} already exists!")
            overwrite = input("Do you want to overwrite it? (y/N): ").lower()
            if overwrite != 'y':
                return
        
        # Ask for password or generate one
        password_choice = input("Enter password manually or generate one? (m/g): ").lower()
        
        if password_choice == 'g':
            try:
                length = int(input("Password length (default 16): ") or "16")
                use_uppercase = input("Include uppercase letters? (Y/n): ").lower() != 'n'
                use_lowercase = input("Include lowercase letters? (Y/n): ").lower() != 'n'
                use_digits = input("Include digits? (Y/n): ").lower() != 'n'
                use_symbols = input("Include symbols? (Y/n): ").lower() != 'n'
                
                password = self.pm.generate_password(
                    length=length,
                    use_uppercase=use_uppercase,
                    use_lowercase=use_lowercase,
                    use_digits=use_digits,
                    use_symbols=use_symbols
                )
                print(f"Generated password: {password}")
            except ValueError as e:
                print(f"❌ Error generating password: {e}")
                return
        else:
            password = self.get_secure_input("Password: ", hide=True)
        
        url = input("URL (optional): ").strip()
        notes = input("Notes (optional): ").strip()
        
        if self.pm.add_password(service, username, password, url, notes):
            print("✅ Password added successfully!")
        else:
            print("❌ Failed to add password!")
    
    def search_passwords(self):
        """Search for passwords."""
        if not self.pm.is_unlocked:
            print("❌ Please unlock the password manager first!")
            return
        
        print("🔍 SEARCH PASSWORDS")
        print("-" * 20)
        
        query = input("Enter search term: ").strip()
        if not query:
            print("❌ Search term is required!")
            return
        
        results = self.pm.search_passwords(query)
        
        if not results:
            print("❌ No passwords found matching your search.")
            return
        
        print(f"\n📋 Found {len(results)} password(s):")
        print("-" * 80)
        
        for i, pwd in enumerate(results, 1):
            print(f"{i}. Service: {pwd['service']}")
            print(f"   Username: {pwd['username']}")
            print(f"   Password: {'*' * len(pwd['password'])}")
            if pwd['url']:
                print(f"   URL: {pwd['url']}")
            if pwd['notes']:
                print(f"   Notes: {pwd['notes']}")
            print(f"   Updated: {pwd['updated_at']}")
            print()
        
        # Option to view password
        while True:
            choice = input("Enter number to view password (or press Enter to continue): ").strip()
            if not choice:
                break
            
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(results):
                    pwd = results[idx]
                    print(f"\n🔐 Password for {pwd['service']} ({pwd['username']}):")
                    print(f"Password: {pwd['password']}")
                    break
                else:
                    print("❌ Invalid selection!")
            except ValueError:
                print("❌ Please enter a valid number!")
    
    def list_all_passwords(self):
        """List all stored passwords."""
        if not self.pm.is_unlocked:
            print("❌ Please unlock the password manager first!")
            return
        
        print("📋 ALL PASSWORDS")
        print("-" * 15)
        
        passwords = self.pm.get_all_passwords()
        
        if not passwords:
            print("📭 No passwords stored yet.")
            return
        
        print(f"Total passwords: {len(passwords)}")
        print("-" * 80)
        
        for i, pwd in enumerate(passwords, 1):
            print(f"{i}. {pwd['service']} - {pwd['username']}")
            if pwd['url']:
                print(f"   URL: {pwd['url']}")
            if pwd['notes']:
                print(f"   Notes: {pwd['notes']}")
            print(f"   Updated: {pwd['updated_at']}")
            print()
    
    def update_password(self):
        """Update an existing password entry."""
        if not self.pm.is_unlocked:
            print("❌ Please unlock the password manager first!")
            return
        
        print("🔧 UPDATE PASSWORD")
        print("-" * 20)
        
        service = input("Service/Website: ").strip()
        username = input("Username: ").strip()
        
        if not service or not username:
            print("❌ Service and username are required!")
            return
        
        # Check if password exists
        existing = self.pm.get_password(service, username)
        if not existing:
            print("❌ Password not found!")
            return
        
        print(f"Current entry: {service} - {username}")
        
        # Ask what to update
        print("\nWhat would you like to update?")
        print("1. Password")
        print("2. Username")
        print("3. URL")
        print("4. Notes")
        print("5. All fields")
        
        choice = input("Enter choice (1-5): ").strip()
        
        new_password = None
        new_username = None
        new_url = None
        new_notes = None
        
        if choice in ['1', '5']:
            password_choice = input("Enter new password manually or generate one? (m/g): ").lower()
            if password_choice == 'g':
                try:
                    length = int(input("Password length (default 16): ") or "16")
                    password = self.pm.generate_password(length=length)
                    new_password = password
                    print(f"Generated password: {password}")
                except ValueError as e:
                    print(f"❌ Error generating password: {e}")
                    return
            else:
                new_password = self.get_secure_input("New password: ", hide=True)
        
        if choice in ['2', '5']:
            new_username = input("New username: ").strip()
        
        if choice in ['3', '5']:
            new_url = input("New URL: ").strip()
        
        if choice in ['4', '5']:
            new_notes = input("New notes: ").strip()
        
        if self.pm.update_password(service, username, new_password, new_username, new_url, new_notes):
            print("✅ Password updated successfully!")
        else:
            print("❌ Failed to update password!")
    
    def delete_password(self):
        """Delete a password entry."""
        if not self.pm.is_unlocked:
            print("❌ Please unlock the password manager first!")
            return
        
        print("🗑️  DELETE PASSWORD")
        print("-" * 20)
        
        service = input("Service/Website: ").strip()
        username = input("Username: ").strip()
        
        if not service or not username:
            print("❌ Service and username are required!")
            return
        
        # Confirm deletion
        confirm = input(f"Are you sure you want to delete the password for {service} ({username})? (y/N): ").lower()
        if confirm != 'y':
            print("❌ Deletion cancelled.")
            return
        
        if self.pm.delete_password(service, username):
            print("✅ Password deleted successfully!")
        else:
            print("❌ Password not found or failed to delete!")
    
    def generate_password(self):
        """Generate a strong password."""
        print("🔑 GENERATE STRONG PASSWORD")
        print("-" * 30)
        
        try:
            length = int(input("Password length (default 16): ") or "16")
            use_uppercase = input("Include uppercase letters? (Y/n): ").lower() != 'n'
            use_lowercase = input("Include lowercase letters? (Y/n): ").lower() != 'n'
            use_digits = input("Include digits? (Y/n): ").lower() != 'n'
            use_symbols = input("Include symbols? (Y/n): ").lower() != 'n'
            
            password = self.pm.generate_password(
                length=length,
                use_uppercase=use_uppercase,
                use_lowercase=use_lowercase,
                use_digits=use_digits,
                use_symbols=use_symbols
            )
            
            print(f"\n🔐 Generated Password: {password}")
            print(f"Length: {len(password)} characters")
            
            # Calculate strength
            strength = 0
            if use_uppercase:
                strength += 26
            if use_lowercase:
                strength += 26
            if use_digits:
                strength += 10
            if use_symbols:
                strength += 32
            
            possible_combinations = strength ** length
            print(f"Possible combinations: {possible_combinations:,}")
            
        except ValueError as e:
            print(f"❌ Error generating password: {e}")
    
    def export_passwords(self):
        """Export passwords to a file."""
        if not self.pm.is_unlocked:
            print("❌ Please unlock the password manager first!")
            return
        
        print("📤 EXPORT PASSWORDS")
        print("-" * 20)
        
        filename = input("Export filename (default: passwords_export.json): ").strip()
        if not filename:
            filename = "passwords_export.json"
        
        if not filename.endswith('.json'):
            filename += '.json'
        
        if self.pm.export_passwords(filename):
            print(f"✅ Passwords exported to {filename}")
        else:
            print("❌ Failed to export passwords!")
    
    def change_master_password(self):
        """Change the master password."""
        if not self.pm.is_unlocked:
            print("❌ Please unlock the password manager first!")
            return
        
        print("🔄 CHANGE MASTER PASSWORD")
        print("-" * 30)
        
        old_password = self.get_secure_input("Current master password: ", hide=True)
        new_password = self.get_secure_input("New master password: ", hide=True)
        confirm_password = self.get_secure_input("Confirm new master password: ", hide=True)
        
        if new_password != confirm_password:
            print("❌ New passwords don't match!")
            return
        
        if len(new_password) < 8:
            print("❌ New password must be at least 8 characters long!")
            return
        
        if self.pm.change_master_password(old_password, new_password):
            print("✅ Master password changed successfully!")
        else:
            print("❌ Failed to change master password!")
    
    def show_statistics(self):
        """Show password manager statistics."""
        print("📊 PASSWORD MANAGER STATISTICS")
        print("-" * 35)
        
        total_passwords = self.pm.get_password_count()
        print(f"Total passwords stored: {total_passwords}")
        print(f"Database file: {self.pm.db_path}")
        print(f"Status: {'🔓 Unlocked' if self.pm.is_unlocked else '🔒 Locked'}")
        
        if self.pm.is_unlocked and total_passwords > 0:
            passwords = self.pm.get_all_passwords()
            
            # Count by service
            services = {}
            for pwd in passwords:
                service = pwd['service']
                services[service] = services.get(service, 0) + 1
            
            print(f"\n📋 Passwords by service:")
            for service, count in sorted(services.items()):
                print(f"   {service}: {count}")
    
    def run(self):
        """Run the main CLI loop."""
        while True:
            self.clear_screen()
            self.print_header()
            
            if self.pm.is_unlocked:
                print(f"👤 Logged in as: {self.current_user}")
                print()
            
            self.print_menu()
            
            choice = input("Enter your choice (0-11): ").strip()
            print()
            
            if choice == '0':
                print("👋 Goodbye!")
                break
            elif choice == '1':
                self.unlock_manager()
            elif choice == '2':
                self.lock_manager()
            elif choice == '3':
                self.add_password()
            elif choice == '4':
                self.search_passwords()
            elif choice == '5':
                self.list_all_passwords()
            elif choice == '6':
                self.update_password()
            elif choice == '7':
                self.delete_password()
            elif choice == '8':
                self.generate_password()
            elif choice == '9':
                self.export_passwords()
            elif choice == '10':
                self.change_master_password()
            elif choice == '11':
                self.show_statistics()
            else:
                print("❌ Invalid choice! Please enter a number between 0 and 11.")
            
            if choice != '0':
                input("\nPress Enter to continue...")


def main():
    """Main entry point."""
    try:
        cli = PasswordManagerCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 