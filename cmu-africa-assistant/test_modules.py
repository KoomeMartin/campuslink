"""
Basic module validation tests (no API keys required)
"""

import os
import sys
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_knowledge_base_loading():
    """Test loading knowledge base"""
    print("\n🧪 Test 1: Loading Knowledge Base...")
    try:
        kb_path = os.path.join(os.path.dirname(__file__), 'src', 'data', 'knowledge_base.json')
        with open(kb_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert len(data) > 0, "Knowledge base is empty"
        assert all('id' in entry for entry in data), "Some entries missing 'id'"
        assert all('content' in entry for entry in data), "Some entries missing 'content'"
        
        print(f"✅ PASS: Loaded {len(data)} entries")
        return True
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False


def test_module_imports():
    """Test importing all modules"""
    print("\n🧪 Test 2: Module Imports...")
    try:
        from modules import (
            EmbeddingModel, VectorStore, LLMClient,
            RAGPipeline, Translator
        )
        print("✅ PASS: All modules imported successfully")
        return True
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False


def test_translator_basic():
    """Test translator without API calls"""
    print("\n🧪 Test 3: Translator Basic Functionality...")
    try:
        from modules.translation import Translator
        
        translator = Translator()
        
        # Test supported languages
        langs = translator.get_supported_languages()
        assert 'en' in langs, "English not in supported languages"
        assert 'fr' in langs, "French not in supported languages"
        assert 'rw' in langs, "Kinyarwanda not in supported languages"
        
        # Test language support check
        assert translator.is_supported('en'), "English not recognized"
        assert not translator.is_supported('xyz'), "Invalid language recognized"
        
        print("✅ PASS: Translator basic functions work")
        return True
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False


def test_knowledge_base_structure():
    """Validate knowledge base structure"""
    print("\n🧪 Test 4: Knowledge Base Structure...")
    try:
        kb_path = os.path.join(os.path.dirname(__file__), 'src', 'data', 'knowledge_base.json')
        with open(kb_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        required_fields = ['id', 'category', 'title', 'content', 'tags']
        categories = set()
        
        for entry in data:
            # Check required fields
            for field in required_fields:
                assert field in entry, f"Entry {entry.get('id', 'unknown')} missing field: {field}"
            
            # Check data types
            assert isinstance(entry['id'], str), "ID must be string"
            assert isinstance(entry['category'], str), "Category must be string"
            assert isinstance(entry['title'], str), "Title must be string"
            assert isinstance(entry['content'], str), "Content must be string"
            assert isinstance(entry['tags'], list), "Tags must be list"
            
            categories.add(entry['category'])
        
        print(f"✅ PASS: All entries valid. Categories: {len(categories)}")
        return True
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False


def test_file_structure():
    """Test project file structure"""
    print("\n🧪 Test 5: Project File Structure...")
    try:
        base_path = os.path.dirname(__file__)
        
        required_files = [
            'app.py',
            'init_knowledge_base.py',
            'requirements.txt',
            '.env.example',
            '.gitignore',
            'README.md',
            'LICENSE',
            'src/data/knowledge_base.json',
            'src/modules/__init__.py',
            'src/modules/embeddings.py',
            'src/modules/vector_store.py',
            'src/modules/llm.py',
            'src/modules/rag_pipeline.py',
            'src/modules/translation.py',
            'pages/1_Admin_Panel.py'
        ]
        
        missing_files = []
        for file in required_files:
            full_path = os.path.join(base_path, file)
            if not os.path.exists(full_path):
                missing_files.append(file)
        
        if missing_files:
            print(f"❌ FAIL: Missing files: {missing_files}")
            return False
        
        print("✅ PASS: All required files present")
        return True
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("🎓 CMU-Africa Information Assistant - Module Tests")
    print("=" * 60)
    
    tests = [
        test_file_structure,
        test_knowledge_base_loading,
        test_knowledge_base_structure,
        test_module_imports,
        test_translator_basic
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {sum(results)}/{len(results)} passed")
    print("=" * 60)
    
    if all(results):
        print("✅ All tests passed!")
        print("\n📝 Next steps:")
        print("1. Set up your .env file with API keys")
        print("2. Run: python init_knowledge_base.py")
        print("3. Run: streamlit run app.py")
        return True
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
