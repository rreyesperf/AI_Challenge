#!/usr/bin/env python3
"""
Installation Test Script for Agentic RAG API
Tests which packages are successfully installed
"""

import sys

def test_package(package_name, import_statement):
    """Test if a package can be imported"""
    try:
        exec(import_statement)
        print(f"✓ {package_name} - installed and working")
        return True
    except ImportError as e:
        print(f"✗ {package_name} - not installed ({e})")
        return False
    except Exception as e:
        print(f"⚠ {package_name} - installed but has issues ({e})")
        return False

def main():
    print("=" * 60)
    print("Agentic RAG API - Installation Test")
    print("=" * 60)
    
    # Core packages
    print("\n🔧 Core Packages:")
    core_packages = [
        ("Flask", "import flask"),
        ("Requests", "import requests"),
        ("BeautifulSoup4", "from bs4 import BeautifulSoup"),
        ("Python-dotenv", "import dotenv"),
    ]
    
    core_working = 0
    for name, import_stmt in core_packages:
        if test_package(name, import_stmt):
            core_working += 1
    
    # LLM packages
    print("\n🤖 LLM Provider Packages:")
    llm_packages = [
        ("OpenAI", "import openai"),
        ("Anthropic", "import anthropic"),
        ("Google Generative AI", "import google.generativeai"),
    ]
    
    llm_working = 0
    for name, import_stmt in llm_packages:
        if test_package(name, import_stmt):
            llm_working += 1
    
    # Document processing packages
    print("\n📄 Document Processing Packages:")
    doc_packages = [
        ("PyPDF2", "import PyPDF2"),
        ("Python-docx", "from docx import Document"),
    ]
    
    doc_working = 0
    for name, import_stmt in doc_packages:
        if test_package(name, import_stmt):
            doc_working += 1
    
    # RAG packages
    print("\n🔍 RAG/Vector Packages:")
    rag_packages = [
        ("NumPy", "import numpy"),
        ("Sentence Transformers", "from sentence_transformers import SentenceTransformer"),
        ("Tiktoken", "import tiktoken"),
        ("ChromaDB", "import chromadb"),
    ]
    
    rag_working = 0
    for name, import_stmt in rag_packages:
        if test_package(name, import_stmt):
            rag_working += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Installation Summary:")
    print("=" * 60)
    
    print(f"Core packages:             {core_working}/{len(core_packages)} working")
    print(f"LLM provider packages:     {llm_working}/{len(llm_packages)} working")
    print(f"Document processing:       {doc_working}/{len(doc_packages)} working")
    print(f"RAG/Vector packages:       {rag_working}/{len(rag_packages)} working")
    
    # Recommendations
    print("\n💡 Recommendations:")
    
    if core_working < len(core_packages):
        print("❌ Core packages missing - install with:")
        print("   pip install Flask requests beautifulsoup4 python-dotenv")
    else:
        print("✅ Core packages ready - basic Flask app will work")
    
    if llm_working == 0:
        print("❌ No LLM providers available - install at least one:")
        print("   pip install openai  # Recommended")
        print("   pip install anthropic")
        print("   pip install google-generativeai")
    else:
        print(f"✅ {llm_working} LLM provider(s) available")
    
    if doc_working == 0:
        print("⚠️  No document processing - to enable RAG document ingestion:")
        print("   pip install PyPDF2 python-docx")
    
    if rag_working < 3:
        print("⚠️  Limited RAG capabilities - for full RAG functionality:")
        print("   pip install numpy sentence-transformers tiktoken chromadb")
    else:
        print("✅ Full RAG capabilities available")
    
    # Overall status
    total_essential = core_working + min(llm_working, 1)  # Need at least 1 LLM
    
    print("\n🎯 Overall Status:")
    if total_essential >= 5:  # 4 core + 1 LLM
        print("✅ Ready to run! The API should work with basic functionality.")
        print("   Run: python app.py")
    elif core_working == len(core_packages):
        print("⚠️  Core is ready but no LLM providers available.")
        print("   Install at least one LLM provider to use the API.")
    else:
        print("❌ Not ready - core packages missing.")
        print("   Install core packages first.")
    
    print("\n📖 See INSTALLATION_GUIDE.md for detailed installation instructions.")

if __name__ == "__main__":
    main()
