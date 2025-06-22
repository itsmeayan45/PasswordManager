#!/usr/bin/env python3
"""
Simple test script for the Password Manager.
Tests core functionality to ensure everything works correctly.
"""

import os
import tempfile
import unittest
from password_manager import PasswordManager


class TestPasswordManager(unittest.TestCase):
    """Test cases for the Password Manager."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a temporary database for testing
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.pm = PasswordManager(self.temp_db.name)
    
    def tearDown(self):
        """Clean up test environment."""
        self.pm.lock()
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_password_generation(self):
        """Test password generation functionality."""
        # Test basic password generation
        password = self.pm.generate_password()
        self.assertIsInstance(password, str)
        self.assertGreaterEqual(len(password), 8)
        
        # Test custom length
        password = self.pm.generate_password(length=20)
        self.assertEqual(len(password), 20)
        
        # Test character set options
        password = self.pm.generate_password(length=10, use_symbols=False)
        self.assertIsInstance(password, str)
        self.assertEqual(len(password), 10)
        
        # Test minimum length validation
        with self.assertRaises(ValueError):
            self.pm.generate_password(length=5)
    
    def test_unlock_lock(self):
        """Test unlock and lock functionality."""
        # Test initial state
        self.assertFalse(self.pm.is_unlocked)
        
        # Test unlock with master password
        self.assertTrue(self.pm.unlock("testpassword123"))
        self.assertTrue(self.pm.is_unlocked)
        
        # Test lock
        self.pm.lock()
        self.assertFalse(self.pm.is_unlocked)
    
    def test_add_get_password(self):
        """Test adding and retrieving passwords."""
        # Unlock first
        self.pm.unlock("testpassword123")
        
        # Add a password
        self.assertTrue(self.pm.add_password("TestService", "testuser", "testpass123"))
        
        # Retrieve the password
        password_data = self.pm.get_password("TestService", "testuser")
        self.assertIsNotNone(password_data)
        self.assertEqual(password_data['service'], "TestService")
        self.assertEqual(password_data['username'], "testuser")
        self.assertEqual(password_data['password'], "testpass123")
    
    def test_update_password(self):
        """Test password update functionality."""
        # Unlock and add a password
        self.pm.unlock("testpassword123")
        self.pm.add_password("TestService", "testuser", "oldpass123")
        
        # Update the password
        self.assertTrue(self.pm.update_password("TestService", "testuser", "newpass456"))
        
        # Verify the update
        password_data = self.pm.get_password("TestService", "testuser")
        self.assertEqual(password_data['password'], "newpass456")
    
    def test_delete_password(self):
        """Test password deletion."""
        # Unlock and add a password
        self.pm.unlock("testpassword123")
        self.pm.add_password("TestService", "testuser", "testpass123")
        
        # Verify password exists
        self.assertIsNotNone(self.pm.get_password("TestService", "testuser"))
        
        # Delete the password
        self.assertTrue(self.pm.delete_password("TestService", "testuser"))
        
        # Verify password is deleted
        self.assertIsNone(self.pm.get_password("TestService", "testuser"))
    
    def test_search_passwords(self):
        """Test password search functionality."""
        # Unlock and add multiple passwords
        self.pm.unlock("testpassword123")
        self.pm.add_password("Gmail", "user@gmail.com", "pass1")
        self.pm.add_password("GitHub", "developer", "pass2")
        self.pm.add_password("Gmail", "admin@gmail.com", "pass3")
        
        # Search for Gmail passwords
        results = self.pm.search_passwords("gmail")
        self.assertEqual(len(results), 2)
        
        # Search for GitHub
        results = self.pm.search_passwords("github")
        self.assertEqual(len(results), 1)
        
        # Search for non-existent
        results = self.pm.search_passwords("nonexistent")
        self.assertEqual(len(results), 0)
    
    def test_get_all_passwords(self):
        """Test retrieving all passwords."""
        # Unlock and add passwords
        self.pm.unlock("testpassword123")
        self.pm.add_password("Service1", "user1", "pass1")
        self.pm.add_password("Service2", "user2", "pass2")
        
        # Get all passwords
        all_passwords = self.pm.get_all_passwords()
        self.assertEqual(len(all_passwords), 2)
        
        # Verify content
        services = [pwd['service'] for pwd in all_passwords]
        self.assertIn("Service1", services)
        self.assertIn("Service2", services)
    
    def test_password_count(self):
        """Test password counting."""
        # Unlock and add passwords
        self.pm.unlock("testpassword123")
        self.assertEqual(self.pm.get_password_count(), 0)
        
        self.pm.add_password("Service1", "user1", "pass1")
        self.assertEqual(self.pm.get_password_count(), 1)
        
        self.pm.add_password("Service2", "user2", "pass2")
        self.assertEqual(self.pm.get_password_count(), 2)
        
        self.pm.delete_password("Service1", "user1")
        self.assertEqual(self.pm.get_password_count(), 1)
    
    def test_change_master_password(self):
        """Test master password change."""
        # Unlock with initial password
        self.pm.unlock("oldpassword123")
        self.pm.add_password("TestService", "testuser", "testpass123")
        
        # Change master password
        self.assertTrue(self.pm.change_master_password("oldpassword123", "newpassword456"))
        
        # Lock and unlock with new password
        self.pm.lock()
        self.assertTrue(self.pm.unlock("newpassword456"))
        
        # Verify password still accessible
        password_data = self.pm.get_password("TestService", "testuser")
        self.assertIsNotNone(password_data)
        self.assertEqual(password_data['password'], "testpass123")
    
    def test_export_passwords(self):
        """Test password export functionality."""
        # Unlock and add passwords
        self.pm.unlock("testpassword123")
        self.pm.add_password("Service1", "user1", "pass1", "http://service1.com", "Test note")
        
        # Export passwords
        export_file = "test_export.json"
        self.assertTrue(self.pm.export_passwords(export_file))
        
        # Verify file exists
        self.assertTrue(os.path.exists(export_file))
        
        # Clean up
        os.unlink(export_file)
    
    def test_locked_operations(self):
        """Test that operations fail when locked."""
        # Try operations without unlocking
        with self.assertRaises(ValueError):
            self.pm.add_password("Service", "user", "pass")
        
        with self.assertRaises(ValueError):
            self.pm.get_password("Service", "user")
        
        with self.assertRaises(ValueError):
            self.pm.update_password("Service", "user", "newpass")
        
        with self.assertRaises(ValueError):
            self.pm.delete_password("Service", "user")
        
        with self.assertRaises(ValueError):
            self.pm.search_passwords("query")
        
        with self.assertRaises(ValueError):
            self.pm.get_all_passwords()
        
        with self.assertRaises(ValueError):
            self.pm.export_passwords("test.json")


def run_tests():
    """Run all tests."""
    print("🧪 Running Password Manager Tests...")
    print("=" * 50)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPasswordManager)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("✅ All tests passed!")
        print(f"Tests run: {result.testsRun}")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
    else:
        print("❌ Some tests failed!")
        print(f"Tests run: {result.testsRun}")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        
        if result.failures:
            print("\nFailures:")
            for test, traceback in result.failures:
                print(f"  - {test}: {traceback}")
        
        if result.errors:
            print("\nErrors:")
            for test, traceback in result.errors:
                print(f"  - {test}: {traceback}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1) 