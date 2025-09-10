#!/usr/bin/env python3
"""
NASA Authentication Setup
Easy setup for automatic NASA token generation and refresh
"""

import getpass
import json
import os
from nasa_auto_auth import setup_nasa_credentials, get_nasa_token

def main():
    print("🛰️ NASA AUTOMATIC AUTHENTICATION SETUP")
    print("=" * 60)
    print()
    
    print("This will set up automatic NASA token generation for your framework.")
    print("Your credentials will be stored securely and tokens will auto-refresh.")
    print()
    
    # Check if already set up
    if os.path.exists("nasa_credentials.json"):
        print("🔍 Found existing NASA credentials")
        choice = input("Do you want to update them? (y/n): ").lower()
        if choice != 'y':
            print("✅ Using existing credentials")
            test_existing_setup()
            return
    
    print("🔐 ENTER YOUR NASA EARTHDATA CREDENTIALS")
    print("=" * 50)
    print("If you don't have an account, create one at: https://urs.earthdata.nasa.gov/")
    print()
    
    # Get credentials
    username = input("NASA Earthdata Username [labeeb2339]: ").strip() or "labeeb2339"
    password = getpass.getpass("NASA Earthdata Password: ")
    
    if not password:
        print("❌ Password is required")
        return
    
    print(f"\n🔄 Setting up automatic authentication for user: {username}")
    
    # Set up credentials
    if setup_nasa_credentials(username, password):
        print("\n✅ SUCCESS! Automatic NASA authentication is now configured")
        print()
        
        # Test the setup
        print("🧪 TESTING AUTOMATIC TOKEN GENERATION...")
        token = get_nasa_token()
        
        if token:
            print("✅ SUCCESS! Your framework now has automatic real NASA data access")
            print()
            print("🚀 NEXT STEPS:")
            print("1. Run your framework: python automatic_nasa_framework.py")
            print("2. Your framework will automatically:")
            print("   • Generate fresh NASA tokens when needed")
            print("   • Refresh expired tokens automatically")
            print("   • Always use real NASA satellite data")
            print("   • Never require manual token management")
            print()
            print("🏆 Your framework is now FULLY AUTOMATED with real NASA data!")
        else:
            print("⚠️ Token generation failed - check your credentials")
            
    else:
        print("❌ Setup failed - please check your credentials")
        print()
        print("📋 TROUBLESHOOTING:")
        print("1. Verify your NASA Earthdata account at: https://urs.earthdata.nasa.gov/")
        print("2. Make sure your username and password are correct")
        print("3. Check if your account is active and verified")

def test_existing_setup():
    """Test existing NASA authentication setup"""
    print("\n🧪 TESTING EXISTING SETUP...")
    
    try:
        token = get_nasa_token()
        
        if token:
            print("✅ SUCCESS! Existing setup works perfectly")
            print("   Your framework has automatic real NASA data access")
        else:
            print("⚠️ Existing setup needs updating")
            print("   Run this script again to update credentials")
            
    except Exception as e:
        print(f"❌ Error testing setup: {e}")
        print("   Run this script again to reconfigure")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🔄 Setup cancelled")
    except Exception as e:
        print(f"\n❌ Setup error: {e}")
        print("\n📞 If you need help:")
        print("1. Check your NASA Earthdata account")
        print("2. Verify your internet connection")
        print("3. Try running the setup again")
