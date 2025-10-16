#!/usr/bin/env python3
"""
Validation script to check if the application is properly set up
"""
import os
import sys
import json
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ MISSING {description}: {filepath}")
        return False

def check_directory_exists(dirpath, description):
    """Check if a directory exists"""
    if os.path.isdir(dirpath):
        print(f"✅ {description}: {dirpath}")
        return True
    else:
        print(f"❌ MISSING {description}: {dirpath}")
        return False

def check_json_valid(filepath):
    """Check if JSON file is valid"""
    try:
        with open(filepath, 'r') as f:
            json.load(f)
        return True
    except Exception as e:
        print(f"   ⚠️  JSON validation error: {e}")
        return False

def main():
    print("=" * 60)
    print("CMU-Africa Information Assistant - Setup Validation")
    print("=" * 60)
    print()
    
    all_checks = []
    
    # Check core directories
    print("📁 Checking directories...")
    all_checks.append(check_directory_exists("src", "Source directory"))
    all_checks.append(check_directory_exists("src/pages", "Pages directory"))
    all_checks.append(check_directory_exists("src/utils", "Utils directory"))
    all_checks.append(check_directory_exists("src/data", "Data directory"))
    all_checks.append(check_directory_exists("data", "Runtime data directory"))
    print()
    
    # Check core files
    print("📄 Checking core files...")
    all_checks.append(check_file_exists("src/app.py", "Main application"))
    all_checks.append(check_file_exists("src/config.py", "Configuration"))
    all_checks.append(check_file_exists("requirements.txt", "Requirements"))
    all_checks.append(check_file_exists(".env", "Environment file"))
    all_checks.append(check_file_exists(".env.example", "Environment example"))
    print()
    
    # Check pages
    print("📑 Checking pages...")
    all_checks.append(check_file_exists("src/pages/chat.py", "Chat page"))
    all_checks.append(check_file_exists("src/pages/admin.py", "Admin page"))
    all_checks.append(check_file_exists("src/pages/settings.py", "Settings page"))
    print()
    
    # Check utils
    print("🔧 Checking utilities...")
    all_checks.append(check_file_exists("src/utils/rag_pipeline.py", "RAG pipeline"))
    all_checks.append(check_file_exists("src/utils/storage.py", "Storage manager"))
    all_checks.append(check_file_exists("src/utils/translations.py", "Translations"))
    print()
    
    # Check data files
    print("📚 Checking data files...")
    kb_exists = check_file_exists("src/data/sample_knowledge_base.json", "Sample knowledge base")
    if kb_exists:
        if check_json_valid("src/data/sample_knowledge_base.json"):
            print("   ✅ JSON is valid")
        all_checks.append(True)
    else:
        all_checks.append(False)
    print()
    
    # Check scripts
    print("🔨 Checking scripts...")
    all_checks.append(check_file_exists("populate_knowledge_base.py", "Population script"))
    all_checks.append(check_file_exists("run_local.sh", "Run script"))
    print()
    
    # Check documentation
    print("📖 Checking documentation...")
    all_checks.append(check_file_exists("README.md", "README"))
    all_checks.append(check_file_exists("DEPLOYMENT.md", "Deployment guide"))
    all_checks.append(check_file_exists("CONTRIBUTING.md", "Contributing guide"))
    all_checks.append(check_file_exists("LICENSE", "License"))
    print()
    
    # Check deployment files
    print("🚀 Checking deployment files...")
    all_checks.append(check_file_exists("Dockerfile", "Dockerfile"))
    all_checks.append(check_file_exists("docker-compose.yml", "Docker Compose"))
    all_checks.append(check_file_exists(".streamlit/config.toml", "Streamlit config"))
    print()
    
    # Check environment variables
    print("🔐 Checking environment configuration...")
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        openai_key = os.getenv("OPENAI_API_KEY", "")
        pinecone_key = os.getenv("PINECONE_API_KEY", "")
        pinecone_env = os.getenv("PINECONE_ENVIRONMENT", "")
        
        if openai_key and openai_key != "placeholder_openai_key":
            print("✅ OPENAI_API_KEY is set")
            all_checks.append(True)
        else:
            print("⚠️  OPENAI_API_KEY not set or using placeholder")
            print("   → Set your OpenAI API key in .env file")
            all_checks.append(False)
        
        if pinecone_key and pinecone_key != "placeholder_pinecone_key":
            print("✅ PINECONE_API_KEY is set")
            all_checks.append(True)
        else:
            print("⚠️  PINECONE_API_KEY not set or using placeholder")
            print("   → Set your Pinecone API key in .env file")
            all_checks.append(False)
        
        if pinecone_env:
            print(f"✅ PINECONE_ENVIRONMENT is set: {pinecone_env}")
            all_checks.append(True)
        else:
            print("⚠️  PINECONE_ENVIRONMENT not set")
            all_checks.append(False)
    except ImportError:
        print("⚠️  python-dotenv not installed")
        print("   → Run: pip install python-dotenv")
        all_checks.append(False)
    print()
    
    # Check Python imports
    print("🐍 Checking Python dependencies...")
    required_packages = [
        ("streamlit", "streamlit"),
        ("openai", "openai"),
        ("pinecone", "pinecone-client"),
        ("tiktoken", "tiktoken"),
        ("pandas", "pandas")
    ]
    
    for import_name, package_name in required_packages:
        try:
            __import__(import_name)
            print(f"✅ {package_name} is installed")
            all_checks.append(True)
        except ImportError:
            print(f"❌ {package_name} is NOT installed")
            print(f"   → Run: pip install {package_name}")
            all_checks.append(False)
    print()
    
    # Summary
    print("=" * 60)
    passed = sum(all_checks)
    total = len(all_checks)
    percentage = (passed / total) * 100 if total > 0 else 0
    
    print(f"Results: {passed}/{total} checks passed ({percentage:.1f}%)")
    print("=" * 60)
    print()
    
    if passed == total:
        print("🎉 All checks passed! Your setup is complete.")
        print()
        print("Next steps:")
        print("1. Configure your API keys in .env file")
        print("2. Run: python populate_knowledge_base.py")
        print("3. Run: streamlit run src/app.py")
        print()
        return 0
    elif percentage >= 80:
        print("⚠️  Most checks passed, but some configuration is needed.")
        print("Please review the warnings above and complete the setup.")
        print()
        return 1
    else:
        print("❌ Setup incomplete. Please review the errors above.")
        print()
        return 1

if __name__ == "__main__":
    sys.exit(main())
