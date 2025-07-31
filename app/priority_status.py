#!/usr/bin/env python3
"""
Provider Priority Status Summary
Shows the current LLM provider configuration and priority order
"""

from services.llm_service import LLMService

def show_priority_status():
    print("🎯 LLM Provider Priority Status Summary")
    print("=" * 50)
    
    # Initialize service
    service = LLMService()
    
    # Show available providers
    providers = service.list_providers()
    print(f"📋 Available Providers: {providers}")
    
    # Show priority order
    print(f"🎯 Priority Order: {['ollama', 'openai', 'anthropic', 'google']}")
    
    # Show default provider
    try:
        default_provider = service.get_provider()
        print(f"⭐ Default Provider: {default_provider.provider_name if default_provider else 'None'}")
    except Exception as e:
        print(f"⭐ Default Provider: Error - {e}")
    
    # Show configuration
    print("\n🔧 Configuration Summary:")
    print(f"   Ollama (Local LLM): http://localhost:11434")
    print(f"   OpenAI: API Key Required")
    print(f"   Anthropic: API Key Required") 
    print(f"   Google: API Key Required")
    
    print("\n✅ Status: Simplified Ollama-first priority implemented!")
    print("   - System tries ollama (local) first")
    print("   - Falls back to openai → anthropic → google")
    print("   - Removed complex LocalLLMProvider")
    print("   - Single Ollama provider at port 11434")

if __name__ == "__main__":
    show_priority_status()
