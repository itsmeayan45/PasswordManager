#!/usr/bin/env python3
"""
Launcher script for the Password Manager.
Allows users to choose between CLI and GUI interfaces.
"""

import sys
import os


def print_banner():
    """Print the application banner."""
    print("🔐 SECURE PASSWORD MANAGER")
    print("=" * 40)
    print("A modern, secure password manager built with Python")
    print("=" * 40)
    print()


def print_menu():
    """Print the launcher menu."""
    print("Choose an interface:")
    print("1. 🖥️  Command Line Interface (CLI)")
    print("2. 🖱️  Graphical User Interface (GUI)")
    print("3. 🧪 Run Demo")
    print("4. 🧪 Run Tests")
    print("5. 📚 Show Help")
    print("0. 🚪 Exit")
    print()


def run_cli():
    """Run the command-line interface."""
    try:
        from cli import main
        main()
    except ImportError as e:
        print(f"❌ Error importing CLI: {e}")
        print("Make sure cli.py is in the same directory.")
    except Exception as e:
        print(f"❌ Error running CLI: {e}")


def run_gui():
    """Run the graphical user interface."""
    try:
        from gui_simple import main
        main()
    except ImportError as e:
        print(f"❌ Error importing GUI: {e}")
        print("Make sure gui_simple.py is in the same directory.")
    except Exception as e:
        print(f"❌ Error running GUI: {e}")


def run_demo():
    """Run the demo script."""
    try:
        from demo import main
        main()
    except ImportError as e:
        print(f"❌ Error importing demo: {e}")
        print("Make sure demo.py is in the same directory.")
    except Exception as e:
        print(f"❌ Error running demo: {e}")


def run_tests():
    """Run the test suite."""
    try:
        from test_password_manager import run_tests
        success = run_tests()
        if success:
            print("\n🎉 All tests passed!")
        else:
            print("\n❌ Some tests failed!")
    except ImportError as e:
        print(f"❌ Error importing tests: {e}")
        print("Make sure test_password_manager.py is in the same directory.")
    except Exception as e:
        print(f"❌ Error running tests: {e}")


def show_help():
    """Show help information."""
    print("\n📚 PASSWORD MANAGER HELP")
    print("=" * 30)
    
    print("\n🔧 Installation:")
    print("1. Install Python 3.7 or higher")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Run this launcher: python run.py")
    
    print("\n🖥️  Interfaces:")
    print("- CLI: Full-featured command-line interface with menus")
    print("- GUI: Simple graphical interface using tkinter")
    
    print("\n🔑 First Time Setup:")
    print("1. Choose an interface (CLI or GUI)")
    print("2. Unlock with your master password (created on first use)")
    print("3. Start adding your passwords")
    
    print("\n🔒 Security Features:")
    print("- AES-256 encryption for all passwords")
    print("- PBKDF2 key derivation (100,000 iterations)")
    print("- Secure salt storage")
    print("- No plain text password storage")
    
    print("\n📁 Files:")
    print("- password_manager.py: Core password manager class")
    print("- cli.py: Command-line interface")
    print("- gui_simple.py: Simple graphical interface")
    print("- demo.py: Demonstration script")
    print("- test_password_manager.py: Test suite")
    print("- requirements.txt: Python dependencies")
    print("- README.md: Detailed documentation")
    
    print("\n⚠️  Important Notes:")
    print("- Choose a strong master password")
    print("- Keep your master password safe")
    print("- Regular backups are recommended")
    print("- This is for educational/personal use")
    
    print("\n📖 For more information, see README.md")


def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import cryptography
        return True
    except ImportError:
        print("❌ Missing required dependency: cryptography")
        print("Please install it with: pip install cryptography")
        print("Or install all dependencies with: pip install -r requirements.txt")
        return False


def main():
    """Main launcher function."""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        print("\nPress Enter to exit...")
        input()
        return
    
    while True:
        print_menu()
        
        try:
            choice = input("Enter your choice (0-5): ").strip()
            
            if choice == '0':
                print("👋 Goodbye!")
                break
            elif choice == '1':
                print("\n🚀 Starting Command Line Interface...")
                run_cli()
            elif choice == '2':
                print("\n🚀 Starting Graphical User Interface...")
                run_gui()
            elif choice == '3':
                print("\n🚀 Running Demo...")
                run_demo()
            elif choice == '4':
                print("\n🚀 Running Tests...")
                run_tests()
            elif choice == '5':
                show_help()
            else:
                print("❌ Invalid choice! Please enter a number between 0 and 5.")
            
            if choice in ['1', '2', '3', '4']:
                print("\nPress Enter to return to launcher...")
                input()
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            print("Press Enter to continue...")
            input()


if __name__ == "__main__":
    main() 