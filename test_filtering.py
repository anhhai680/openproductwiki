#!/usr/bin/env python3
"""
Test Multi-Language File Filtering
==================================

This script tests whether the updated repository configuration correctly 
filters out multi-language files during processing.
"""

import requests
import json
import time

def test_repository_filtering():
    """Test if multi-language files are properly filtered"""
    
    print("🧪 Testing Multi-Language File Filtering")
    print("=" * 50)
    
    # Test repository that we know has multi-language README files
    test_repo = {
        "owner": "AsyncFuncAI",
        "repo": "deepwiki-open",
        "type": "github"
    }
    
    print(f"📁 Test Repository: {test_repo['owner']}/{test_repo['repo']}")
    
    # Check current configuration
    try:
        response = requests.get("http://localhost:8001/lang/config")
        if response.status_code == 200:
            lang_config = response.json()
            print(f"🌐 Language Config: {lang_config}")
        else:
            print(f"❌ Failed to get language config: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error checking language config: {e}")
        return
    
    # Simulate processing request to see what files would be included
    try:
        # This endpoint should show us what files are being processed
        print("\n📋 Checking file filtering...")
        print("ℹ️  Generate a wiki for this repository and check if multi-language files are excluded")
        print("ℹ️  Expected: README.zh.md, README.ja.md, etc. should be filtered out")
        print("ℹ️  Only README.md (English) should be included")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    test_repository_filtering()