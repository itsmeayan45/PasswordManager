#!/usr/bin/env python3
"""
Demo script for the Password Manager.
This script demonstrates the core functionality of the password manager.
"""

import os
import sys
from password_manager import PasswordManager


def print_separator(title):
    """Print a formatted separator with title."""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def demo_password_generation():
    """Demonstrate password generation functionality."""
    print_separator("PASSWORD GENERATION DEMO")
    
    pm = PasswordManager()
    
    print("🔑 Generating different types of passwords:")
    
    # Generate a standard password
    password1 = pm.generate_password()
    print(f"Standard password (16 chars): {password1}")
    
    # Generate a longer password
    password2 = pm.generate_password(length=24)
    print(f"Long password (24 chars): {password2}")
    
    # Generate password with only letters and digits
    password3 = pm.generate_password(length=12, use_symbols=False)
    print(f"Letters + digits only (12 chars): {password3}")
    
    # Generate a simple PIN-style password
    password4 = pm.generate_password(length=8, use_uppercase=False, 
                                   use_lowercase=False, use_symbols=False)
    print(f"Digits only (8 chars): {password4}")
    
    # Generate a complex password
    password5 = pm.generate_password(length=20, use_uppercase=True, 
                                   use_lowercase=True, use_digits=True, 
                                   use_symbols=True)
    print(f"Complex password (20 chars): {password5}")


def demo_password_management():
    """Demonstrate password management functionality."""
    print_separator("PASSWORD MANAGEMENT DEMO")
    
    # Use a temporary database for demo
    demo_db = "demo_passwords.db"
    
    # Clean up any existing demo database
    if os.path.exists(demo_db):
        os.remove(demo_db)
    
    pm = PasswordManager(demo_db)
    
    print("🔓 Unlocking password manager with master password 'demo123'...")
    if pm.unlock("demo123"):
        print("✅ Successfully unlocked!")
    else:
        print("❌ Failed to unlock!")
        return
    
    print("\n➕ Adding sample passwords...")
    
    # Add some sample passwords
    sample_passwords = [
        ("Gmail", "user@gmail.com", "MySecurePass123!", "https://gmail.com", "Personal email"),
        ("GitHub", "developer", "GitHubPass456!", "https://github.com", "Code repository"),
        ("Bank", "john.doe", "BankSecure789!", "https://mybank.com", "Online banking"),
        ("Social Media", "johndoe", "SocialPass321!", "https://social.com", "Social networking")
    ]
    
    for service, username, password, url, notes in sample_passwords:
        if pm.add_password(service, username, password, url, notes):
            print(f"✅ Added: {service} - {username}")
        else:
            print(f"❌ Failed to add: {service}")
    
    print(f"\n📊 Total passwords stored: {pm.get_password_count()}")
    
    print("\n🔍 Searching for passwords...")
    search_results = pm.search_passwords("gmail")
    print(f"Found {len(search_results)} password(s) containing 'gmail'")
    
    print("\n📋 Listing all passwords (without showing actual passwords):")
    all_passwords = pm.get_all_passwords()
    for i, pwd in enumerate(all_passwords, 1):
        print(f"{i}. {pwd['service']} - {pwd['username']}")
        if pwd['url']:
            print(f"   URL: {pwd['url']}")
        if pwd['notes']:
            print(f"   Notes: {pwd['notes']}")
        print(f"   Updated: {pwd['updated_at']}")
        print()
    
    print("🔐 Retrieving a specific password...")
    gmail_password = pm.get_password("Gmail", "user@gmail.com")
    if gmail_password:
        print(f"Service: {gmail_password['service']}")
        print(f"Username: {gmail_password['username']}")
        print(f"Password: {gmail_password['password']}")
        print(f"URL: {gmail_password['url']}")
        print(f"Notes: {gmail_password['notes']}")
    
    print("\n🔧 Updating a password...")
    if pm.update_password("Gmail", "user@gmail.com", "NewSecurePass456!"):
        print("✅ Password updated successfully!")
        
        # Verify the update
        updated_password = pm.get_password("Gmail", "user@gmail.com")
        if updated_password:
            print(f"New password: {updated_password['password']}")
    
    print("\n📤 Exporting passwords...")
    if pm.export_passwords("demo_export.json"):
        print("✅ Passwords exported to demo_export.json")
    
    print("\n🗑️ Deleting a password...")
    if pm.delete_password("Social Media", "johndoe"):
        print("✅ Password deleted successfully!")
        print(f"Remaining passwords: {pm.get_password_count()}")
    
    print("\n🔄 Changing master password...")
    if pm.change_master_password("demo123", "newdemo456"):
        print("✅ Master password changed successfully!")
        
        # Test the new password
        pm.lock()
        if pm.unlock("newdemo456"):
            print("✅ New master password works correctly!")
        else:
            print("❌ New master password failed!")
    
    # Clean up
    pm.lock()
    print(f"\n🔒 Password manager locked. Demo database: {demo_db}")
    print("💡 You can delete demo_passwords.db and demo_export.json to clean up.")


def demo_security_features():
    """Demonstrate security features."""
    print_separator("SECURITY FEATURES DEMO")
    
    print("🔒 Security Features Implemented:")
    print("✅ AES-256 encryption for all passwords")
    print("✅ PBKDF2 key derivation with 100,000 iterations")
    print("✅ Secure salt storage (16 bytes)")
    print("✅ No plain text password storage")
    print("✅ Memory protection (passwords only decrypted when needed)")
    print("✅ SQLite database with encrypted password field")
    
    print("\n🛡️ Threat Protection:")
    print("✅ File system access protection")
    print("✅ Brute force attack resistance")
    print("✅ Rainbow table attack resistance")
    print("✅ Memory dump protection")
    
    print("\n⚠️ Security Limitations:")
    print("❌ Service names are stored in plain text (for search)")
    print("❌ Usernames are stored in plain text (for identification)")
    print("❌ URLs and notes are stored in plain text (for convenience)")
    print("❌ No protection against keyloggers")
    print("❌ No protection against screen capture malware")


def main():
    """Run the demo."""
    print("🔐 PASSWORD MANAGER DEMO")
    print("This demo showcases the core functionality of the secure password manager.")
    print("Note: This demo uses a temporary database and sample data.")
    
    try:
        # Demo password generation
        demo_password_generation()
        
        # Demo password management
        demo_password_management()
        
        # Demo security features
        demo_security_features()
        
        print_separator("DEMO COMPLETE")
        print("🎉 Demo completed successfully!")
        print("\n📚 Next steps:")
        print("1. Run 'python cli.py' for the command-line interface")
        print("2. Run 'python gui_simple.py' for the graphical interface")
        print("3. Read README.md for detailed usage instructions")
        print("4. Check requirements.txt for dependencies")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        print("Make sure you have installed the required dependencies:")
        print("pip install -r requirements.txt")


if __name__ == "__main__":
    main() 