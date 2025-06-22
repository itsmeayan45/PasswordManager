import json
import os
import secrets
import string
import sqlite3
import hashlib
import base64
from typing import Dict, List, Optional, Tuple
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class PasswordManager:
    """
    A secure password manager using Python standard library and cryptography.
    Stores encrypted passwords in SQLite database with master password protection.
    """
    
    def __init__(self, db_path: str = "passwords.db"):
        self.db_path = db_path
        self.fernet = None
        self.is_unlocked = False
        self._init_database()
    
    def _init_database(self):
        """Initialize the SQLite database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create table for encrypted passwords
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service TEXT NOT NULL,
                username TEXT NOT NULL,
                encrypted_password TEXT NOT NULL,
                url TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create table for salt storage
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS salt (
                id INTEGER PRIMARY KEY,
                salt TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _get_or_create_salt(self) -> bytes:
        """Get existing salt or create a new one."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT salt FROM salt WHERE id = 1")
        result = cursor.fetchone()
        
        if result:
            salt = base64.b64decode(result[0])
        else:
            # Generate new salt
            salt = os.urandom(16)
            cursor.execute("INSERT INTO salt (id, salt) VALUES (1, ?)", 
                         (base64.b64encode(salt).decode(),))
            conn.commit()
        
        conn.close()
        return salt
    
    def _derive_key(self, master_password: str) -> bytes:
        """Derive encryption key from master password using PBKDF2."""
        salt = self._get_or_create_salt()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
        return key
    
    def unlock(self, master_password: str) -> bool:
        """Unlock the password manager with master password."""
        try:
            key = self._derive_key(master_password)
            self.fernet = Fernet(key)
            self.is_unlocked = True
            return True
        except Exception:
            return False
    
    def lock(self):
        """Lock the password manager."""
        self.fernet = None
        self.is_unlocked = False
    
    def _check_unlocked(self):
        """Check if password manager is unlocked."""
        if not self.is_unlocked or not self.fernet:
            raise ValueError("Password manager is locked. Call unlock() first.")
    
    def generate_password(self, length: int = 16, 
                         use_uppercase: bool = True,
                         use_lowercase: bool = True,
                         use_digits: bool = True,
                         use_symbols: bool = True) -> str:
        """Generate a strong random password."""
        if length < 8:
            raise ValueError("Password length must be at least 8 characters")
        
        chars = ""
        if use_uppercase:
            chars += string.ascii_uppercase
        if use_lowercase:
            chars += string.ascii_lowercase
        if use_digits:
            chars += string.digits
        if use_symbols:
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        if not chars:
            raise ValueError("At least one character set must be selected")
        
        # Ensure at least one character from each selected set
        password = []
        if use_uppercase:
            password.append(secrets.choice(string.ascii_uppercase))
        if use_lowercase:
            password.append(secrets.choice(string.ascii_lowercase))
        if use_digits:
            password.append(secrets.choice(string.digits))
        if use_symbols:
            password.append(secrets.choice("!@#$%^&*()_+-=[]{}|;:,.<>?"))
        
        # Fill the rest randomly
        while len(password) < length:
            password.append(secrets.choice(chars))
        
        # Shuffle the password
        password_list = list(password)
        secrets.SystemRandom().shuffle(password_list)
        return ''.join(password_list)
    
    def add_password(self, service: str, username: str, password: str, 
                    url: str = "", notes: str = "") -> bool:
        """Add a new password entry."""
        self._check_unlocked()
        
        try:
            encrypted_password = self.fernet.encrypt(password.encode()).decode()
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO passwords (service, username, encrypted_password, url, notes)
                VALUES (?, ?, ?, ?, ?)
            ''', (service, username, encrypted_password, url, notes))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding password: {e}")
            return False
    
    def get_password(self, service: str, username: str = None) -> Optional[Dict]:
        """Retrieve a password entry."""
        self._check_unlocked()
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if username:
                cursor.execute('''
                    SELECT service, username, encrypted_password, url, notes, created_at, updated_at
                    FROM passwords WHERE service = ? AND username = ?
                ''', (service, username))
            else:
                cursor.execute('''
                    SELECT service, username, encrypted_password, url, notes, created_at, updated_at
                    FROM passwords WHERE service = ?
                ''', (service,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                service, username, encrypted_password, url, notes, created_at, updated_at = result
                decrypted_password = self.fernet.decrypt(encrypted_password.encode()).decode()
                
                return {
                    'service': service,
                    'username': username,
                    'password': decrypted_password,
                    'url': url,
                    'notes': notes,
                    'created_at': created_at,
                    'updated_at': updated_at
                }
            return None
        except Exception as e:
            print(f"Error retrieving password: {e}")
            return None
    
    def get_all_passwords(self) -> List[Dict]:
        """Retrieve all password entries."""
        self._check_unlocked()
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT service, username, encrypted_password, url, notes, created_at, updated_at
                FROM passwords ORDER BY service, username
            ''')
            
            results = cursor.fetchall()
            conn.close()
            
            passwords = []
            for result in results:
                service, username, encrypted_password, url, notes, created_at, updated_at = result
                decrypted_password = self.fernet.decrypt(encrypted_password.encode()).decode()
                
                passwords.append({
                    'service': service,
                    'username': username,
                    'password': decrypted_password,
                    'url': url,
                    'notes': notes,
                    'created_at': created_at,
                    'updated_at': updated_at
                })
            
            return passwords
        except Exception as e:
            print(f"Error retrieving passwords: {e}")
            return []
    
    def update_password(self, service: str, username: str, new_password: str = None,
                       new_username: str = None, new_url: str = None, 
                       new_notes: str = None) -> bool:
        """Update an existing password entry."""
        self._check_unlocked()
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get current entry
            cursor.execute('''
                SELECT encrypted_password, url, notes FROM passwords 
                WHERE service = ? AND username = ?
            ''', (service, username))
            
            result = cursor.fetchone()
            if not result:
                conn.close()
                return False
            
            current_encrypted_password, current_url, current_notes = result
            
            # Update fields
            if new_password:
                encrypted_password = self.fernet.encrypt(new_password.encode()).decode()
            else:
                encrypted_password = current_encrypted_password
            
            new_username = new_username or username
            new_url = new_url if new_url is not None else current_url
            new_notes = new_notes if new_notes is not None else current_notes
            
            cursor.execute('''
                UPDATE passwords 
                SET username = ?, encrypted_password = ?, url = ?, notes = ?, 
                    updated_at = CURRENT_TIMESTAMP
                WHERE service = ? AND username = ?
            ''', (new_username, encrypted_password, new_url, new_notes, service, username))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating password: {e}")
            return False
    
    def delete_password(self, service: str, username: str) -> bool:
        """Delete a password entry."""
        self._check_unlocked()
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                DELETE FROM passwords WHERE service = ? AND username = ?
            ''', (service, username))
            
            deleted = cursor.rowcount > 0
            conn.commit()
            conn.close()
            return deleted
        except Exception as e:
            print(f"Error deleting password: {e}")
            return False
    
    def search_passwords(self, query: str) -> List[Dict]:
        """Search passwords by service, username, or notes."""
        self._check_unlocked()
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT service, username, encrypted_password, url, notes, created_at, updated_at
                FROM passwords 
                WHERE service LIKE ? OR username LIKE ? OR notes LIKE ?
                ORDER BY service, username
            ''', (f'%{query}%', f'%{query}%', f'%{query}%'))
            
            results = cursor.fetchall()
            conn.close()
            
            passwords = []
            for result in results:
                service, username, encrypted_password, url, notes, created_at, updated_at = result
                decrypted_password = self.fernet.decrypt(encrypted_password.encode()).decode()
                
                passwords.append({
                    'service': service,
                    'username': username,
                    'password': decrypted_password,
                    'url': url,
                    'notes': notes,
                    'created_at': created_at,
                    'updated_at': updated_at
                })
            
            return passwords
        except Exception as e:
            print(f"Error searching passwords: {e}")
            return []
    
    def get_password_count(self) -> int:
        """Get the total number of stored passwords."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM passwords")
            count = cursor.fetchone()[0]
            
            conn.close()
            return count
        except Exception as e:
            print(f"Error getting password count: {e}")
            return 0
    
    def export_passwords(self, filename: str) -> bool:
        """Export all passwords to a JSON file (encrypted)."""
        self._check_unlocked()
        
        try:
            passwords = self.get_all_passwords()
            
            # Remove sensitive data for export
            export_data = []
            for pwd in passwords:
                export_data.append({
                    'service': pwd['service'],
                    'username': pwd['username'],
                    'url': pwd['url'],
                    'notes': pwd['notes'],
                    'created_at': pwd['created_at'],
                    'updated_at': pwd['updated_at']
                })
            
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error exporting passwords: {e}")
            return False
    
    def change_master_password(self, old_password: str, new_password: str) -> bool:
        """Change the master password by re-encrypting all passwords."""
        if not self.unlock(old_password):
            return False
        
        try:
            # Get all passwords
            passwords = self.get_all_passwords()
            
            # Create new key
            new_key = self._derive_key(new_password)
            new_fernet = Fernet(new_key)
            
            # Re-encrypt all passwords
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for pwd in passwords:
                new_encrypted_password = new_fernet.encrypt(pwd['password'].encode()).decode()
                cursor.execute('''
                    UPDATE passwords 
                    SET encrypted_password = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE service = ? AND username = ?
                ''', (new_encrypted_password, pwd['service'], pwd['username']))
            
            conn.commit()
            conn.close()
            
            # Update current fernet instance
            self.fernet = new_fernet
            return True
        except Exception as e:
            print(f"Error changing master password: {e}")
            return False 