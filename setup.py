#!/usr/bin/env python3
"""
Quick setup script for Customer Segmentation ML Application
"""

import os
import sys
import subprocess
import platform

def print_banner():
    banner = """
    ╔════════════════════════════════════════════════════════╗
    ║   🎯 Customer Segmentation ML Application              ║
    ║   Quick Setup & Run Script                            ║
    ╚════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ required. Your version:", sys.version)
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detected")

def install_dependencies():
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        sys.exit(1)

def create_virtual_env():
    """Create virtual environment if it doesn't exist"""
    venv_path = "venv"
    if not os.path.exists(venv_path):
        print(f"\n🔧 Creating virtual environment at '{venv_path}'...")
        subprocess.check_call([sys.executable, "-m", "venv", venv_path])
        print("✅ Virtual environment created")
        
        # Provide activation instructions
        if platform.system() == "Windows":
            print(f"\n💡 To activate the virtual environment, run:")
            print(f"   .\\{venv_path}\\Scripts\\activate")
        else:
            print(f"\n💡 To activate the virtual environment, run:")
            print(f"   source {venv_path}/bin/activate")
    else:
        print(f"✅ Virtual environment already exists at '{venv_path}'")

def start_backend():
    print("\n🚀 Starting backend server...")
    print("   API will be available at http://localhost:10000")
    print("   Press Ctrl+C to stop the server\n")
    
    try:
        os.chdir("backend")
        subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\n✅ Server stopped")
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        sys.exit(1)

def show_menu():
    print("\n" + "="*55)
    print("🎯 Customer Segmentation Application")
    print("="*55)
    print("1. Create Virtual Environment")
    print("2. Install Dependencies")
    print("3. Start Backend Server")
    print("4. Run All Setup Steps")
    print("5. View Project Structure")
    print("6. View Documentation")
    print("0. Exit")
    print("="*55)

def show_project_structure():
    structure = """
    📁 Project Structure:
    
    customer-segmentation-app/
    ├── backend/
    │   ├── main.py (FastAPI application)
    │   ├── model.py (ML algorithms)
    │   ├── preprocessing.py (Data processing)
    │   └── utils.py (Helper functions)
    ├── frontend/
    │   ├── index.html (Dashboard)
    │   ├── style.css (Styling)
    │   └── script.js (Frontend logic)
    ├── data/
    │   └── sample_customers.csv (Sample data)
    ├── requirements.txt (Dependencies)
    ├── render.yaml (Deployment config)
    └── README.md (Documentation)
    """
    print(structure)

def main():
    print_banner()
    check_python_version()
    
    while True:
        show_menu()
        choice = input("\n👉 Select option (0-6): ").strip()
        
        if choice == "1":
            create_virtual_env()
        elif choice == "2":
            install_dependencies()
        elif choice == "3":
            start_backend()
        elif choice == "4":
            create_virtual_env()
            install_dependencies()
            print("\n✅ Setup complete!")
            print("\n📝 Next steps:")
            print("   1. Activate virtual environment")
            print("   2. Start backend: python -m backend.main")
            print("   3. Open frontend/index.html in browser")
        elif choice == "5":
            show_project_structure()
        elif choice == "6":
            print("\n📚 Documentation available in README.md")
            print("   Key sections:")
            print("   • Installation & Setup")
            print("   • Usage Guide")
            print("   • API Documentation")
            print("   • Deployment Instructions")
            print("   • Troubleshooting")
        elif choice == "0":
            print("\n👋 Goodbye! Happy segmenting!")
            break
        else:
            print("❌ Invalid option. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled")
        sys.exit(0)
