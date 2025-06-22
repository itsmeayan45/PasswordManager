# 🔐 Secure Password Manager

A modern, secure password manager built with Python using only the standard library and cryptography. This password manager provides strong encryption, secure password generation, and both command-line and graphical interfaces.

## ✨ Features

### 🔒 Security Features
- **AES-256 Encryption**: All passwords are encrypted using Fernet (AES-128 in CBC mode with PKCS7 padding)
- **PBKDF2 Key Derivation**: Master password is processed using PBKDF2 with 100,000 iterations
- **Secure Salt Storage**: Unique salt for each database, stored securely
- **Memory Protection**: Passwords are only decrypted when needed and cleared from memory
- **No Plain Text Storage**: Passwords are never stored in plain text

### 🛠️ Core Functionality
- **Add/Edit/Delete Passwords**: Full CRUD operations for password entries
- **Strong Password Generation**: Customizable password generator with configurable character sets
- **Search & Filter**: Find passwords by service, username, or notes
- **Master Password Protection**: Single master password unlocks all stored passwords
- **Local Storage**: SQLite database with encrypted password storage
- **Export Functionality**: Export password metadata (without actual passwords) to JSON

### 🖥️ User Interfaces
- **Command-Line Interface**: Full-featured CLI with interactive menus
- **Graphical User Interface**: Simple tkinter-based GUI
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 📋 Requirements

- Python 3.7 or higher
- `cryptography` library

## 🚀 Installation

1. **Clone or download the project**:
   ```bash
   git clone <repository-url>
   cd password_manager
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the password manager**:
   ```bash
   # Command-line interface
   python cli.py
   
   # Graphical interface
   python gui_simple.py
   ```

## 📖 Usage Guide

### First Time Setup

1. **Launch the password manager** (CLI or GUI)
2. **Unlock with your master password** (this will be created on first use)
3. **Start adding your passwords**

### Command-Line Interface

The CLI provides a comprehensive menu-driven interface:

```
🔐 SECURE PASSWORD MANAGER
============================================================

📋 MAIN MENU:
1. 🔓 Unlock Password Manager
2. 🔒 Lock Password Manager
3. ➕ Add New Password
4. 🔍 Search Passwords
5. 📋 List All Passwords
6. 🔧 Update Password
7. 🗑️ Delete Password
8. 🔑 Generate Strong Password
9. 📤 Export Passwords
10. 🔄 Change Master Password
11. 📊 Show Statistics
0. 🚪 Exit
```

### Graphical Interface

The GUI provides a simple, intuitive interface with:
- **Unlock/Lock buttons** for security
- **Add/Edit/Delete** password operations
- **Search functionality** to find passwords
- **Password generation** with one-click generation
- **Copy to clipboard** functionality

### Password Generation

The password generator creates cryptographically secure passwords with:
- **Customizable length** (8-128 characters)
- **Character set selection**:
  - Uppercase letters (A-Z)
  - Lowercase letters (a-z)
  - Digits (0-9)
  - Special symbols (!@#$%^&*()_+-=[]{}|;:,.<>?)
- **Guaranteed inclusion** of at least one character from each selected set

### Security Best Practices

1. **Choose a Strong Master Password**:
   - Use at least 12 characters
   - Include uppercase, lowercase, digits, and symbols
   - Avoid common words or patterns
   - Consider using a passphrase

2. **Regular Backups**:
   - Export your password data regularly
   - Keep backups in a secure location
   - Consider using cloud storage with encryption

3. **Keep Software Updated**:
   - Regularly update the password manager
   - Keep your operating system updated
   - Use the latest Python version

## 🔧 Configuration

### Database Location
By default, the password database is stored as `passwords.db` in the current directory. You can specify a custom location:

```python
from password_manager import PasswordManager

# Custom database location
pm = PasswordManager(db_path="/path/to/your/passwords.db")
```

### Security Settings
The password manager uses industry-standard security settings:
- **PBKDF2 iterations**: 100,000 (configurable in code)
- **Salt length**: 16 bytes
- **Encryption**: AES-256 via Fernet

## 📁 File Structure

```
password_manager/
├── password_manager.py    # Core password manager class
├── cli.py                # Command-line interface
├── gui_simple.py         # Simple graphical interface
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── passwords.db         # Encrypted password database (created on first use)
```

## 🔍 API Reference

### PasswordManager Class

#### Core Methods
- `unlock(master_password: str) -> bool`: Unlock the password manager
- `lock()`: Lock the password manager
- `add_password(service, username, password, url="", notes="") -> bool`: Add a new password
- `get_password(service, username=None) -> dict`: Retrieve a password
- `update_password(service, username, new_password=None, ...) -> bool`: Update a password
- `delete_password(service, username) -> bool`: Delete a password

#### Utility Methods
- `generate_password(length=16, use_uppercase=True, ...) -> str`: Generate a strong password
- `search_passwords(query: str) -> list`: Search passwords
- `get_all_passwords() -> list`: Get all stored passwords
- `export_passwords(filename: str) -> bool`: Export password metadata
- `change_master_password(old_password, new_password) -> bool`: Change master password

## 🛡️ Security Considerations

### What's Encrypted
- ✅ All stored passwords
- ✅ Master password (derived key only)
- ✅ Database salt

### What's NOT Encrypted
- ❌ Service names (for search functionality)
- ❌ Usernames (for identification)
- ❌ URLs and notes (for convenience)
- ❌ Timestamps (for audit trail)

### Threat Model
This password manager protects against:
- **File system access**: Passwords are encrypted at rest
- **Memory dumps**: Passwords are only decrypted when needed
- **Brute force attacks**: PBKDF2 with 100,000 iterations
- **Rainbow table attacks**: Unique salt per database

**Note**: This password manager does NOT protect against:
- Keyloggers (use a secure environment)
- Screen capture malware (use a secure environment)
- Physical access to unlocked session (lock when not in use)

## 🐛 Troubleshooting

### Common Issues

1. **"Invalid master password" error**:
   - Ensure you're using the correct master password
   - Check for caps lock or keyboard layout issues
   - If forgotten, you'll need to reset the database

2. **Database corruption**:
   - Restore from backup if available
   - Delete `passwords.db` to start fresh (⚠️ **WARNING**: This will lose all passwords)

3. **Import/Export issues**:
   - Ensure you have write permissions in the target directory
   - Check that the export file isn't being used by another application

### Performance Tips

- **Large password databases**: The GUI may become slow with 1000+ entries
- **Memory usage**: Consider locking the manager when not in use
- **Search performance**: Use specific search terms for better results

## 🤝 Contributing

Contributions are welcome! Please ensure:
- Code follows PEP 8 style guidelines
- All new features include appropriate tests
- Security-related changes are thoroughly reviewed
- Documentation is updated for new features

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This password manager is provided as-is for educational and personal use. While it implements strong security practices, no software is 100% secure. Use at your own risk and consider your specific security requirements.

For production or enterprise use, consider using established password managers like:
- Bitwarden
- KeePass
- 1Password
- LastPass

## 🔗 Related Projects

- [Bitwarden](https://bitwarden.com/) - Open-source password manager
- [KeePass](https://keepass.info/) - Offline password manager
- [Python Cryptography](https://cryptography.io/) - Cryptography library used in this project

---

**Remember**: The security of your passwords depends on the strength of your master password and the security of your computing environment. Choose a strong master password and keep your system secure! 
