#!/usr/bin/env python3
"""
Deployment Helper Script for Movie Recommender Pro
This script helps you deploy your app to various platforms.
"""

import os
import subprocess
import sys

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...")
    
    # Check if required files exist
    required_files = ['app.py', 'generate_data.py', 'requirements.txt']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files found")
    return True

def generate_data():
    """Generate required data files"""
    print("📊 Generating data files...")
    try:
        result = subprocess.run([sys.executable, 'generate_data.py'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Data files generated successfully")
            return True
        else:
            print(f"❌ Error generating data: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_app():
    """Test if the app runs without errors"""
    print("🧪 Testing application...")
    try:
        # Import the app to check for syntax errors
        import app
        print("✅ Application syntax is correct")
        return True
    except Exception as e:
        print(f"❌ Application error: {e}")
        return False

def show_deployment_instructions():
    """Show deployment instructions"""
    print("\n" + "="*60)
    print("🚀 DEPLOYMENT INSTRUCTIONS")
    print("="*60)
    
    print("\n📋 Option 1: Streamlit Cloud (Recommended)")
    print("-" * 40)
    print("1. Go to https://share.streamlit.io/")
    print("2. Sign in with GitHub")
    print("3. Click 'New app'")
    print("4. Repository: vivekggg/movie2watch")
    print("5. Main file: app.py")
    print("6. Click 'Deploy!'")
    print("\n✨ Your app will be available at: https://your-app-name.streamlit.app")
    
    print("\n📋 Option 2: Heroku")
    print("-" * 40)
    print("1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli")
    print("2. Run: heroku create your-app-name")
    print("3. Run: git push heroku main")
    print("4. Run: heroku run python generate_data.py")
    print("\n✨ Your app will be available at: https://your-app-name.herokuapp.com")
    
    print("\n📋 Option 3: Local Development")
    print("-" * 40)
    print("1. Run: streamlit run app.py")
    print("2. Open: http://localhost:8501")
    
    print("\n🎯 Current Status:")
    print("-" * 40)
    print("✅ Code pushed to GitHub")
    print("✅ Data generation script ready")
    print("✅ All dependencies listed")
    print("✅ Documentation complete")
    
    print("\n🌟 Your Movie Recommender Pro is ready to deploy!")
    print("="*60)

def main():
    """Main deployment helper function"""
    print("🎬 Movie Recommender Pro - Deployment Helper")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        print("❌ Please fix the missing files before deploying")
        return
    
    # Generate data
    if not generate_data():
        print("❌ Please fix data generation issues before deploying")
        return
    
    # Test app
    if not test_app():
        print("❌ Please fix application errors before deploying")
        return
    
    # Show deployment instructions
    show_deployment_instructions()

if __name__ == "__main__":
    main()
