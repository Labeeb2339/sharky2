#!/usr/bin/env python3
"""
Quick utility to update NASA JWT token in the framework
"""

import re
import jwt
import json
import datetime

def validate_token(token):
    """Validate NASA JWT token"""
    try:
        # Decode without verification to check structure
        payload = jwt.decode(token, options={'verify_signature': False})
        
        # Check required fields
        required_fields = ['uid', 'exp', 'iat', 'iss']
        for field in required_fields:
            if field not in payload:
                return False, f"Missing required field: {field}"
        
        # Check if token is expired
        exp_time = datetime.datetime.fromtimestamp(payload['exp'])
        if exp_time < datetime.datetime.now():
            return False, f"Token expired on {exp_time}"
        
        # Check issuer
        if 'earthdata.nasa.gov' not in payload.get('iss', ''):
            return False, "Not a NASA Earthdata token"
        
        return True, {
            'uid': payload['uid'],
            'expires': exp_time,
            'issued': datetime.datetime.fromtimestamp(payload['iat']),
            'valid_days': (payload['exp'] - payload['iat']) / (24 * 3600)
        }
        
    except Exception as e:
        return False, f"Invalid token format: {e}"

def update_token_in_framework(new_token):
    """Update token in automatic_nasa_framework.py"""
    
    try:
        # Read current framework file
        with open('automatic_nasa_framework.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and replace token
        token_pattern = r'self\.jwt_token = "[^"]*"'
        new_token_line = f'self.jwt_token = "{new_token}"'
        
        if re.search(token_pattern, content):
            updated_content = re.sub(token_pattern, new_token_line, content)
            
            # Write back to file
            with open('automatic_nasa_framework.py', 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            return True, "Token updated successfully in automatic_nasa_framework.py"
        else:
            return False, "Could not find token line in framework file"
            
    except Exception as e:
        return False, f"Error updating file: {e}"

def main():
    """Main token update utility"""
    
    print("🔑 NASA JWT TOKEN UPDATE UTILITY")
    print("=" * 50)
    
    # Get new token from user
    print("\n📝 Enter your new NASA JWT token:")
    print("(Get it from: https://urs.earthdata.nasa.gov/profile)")
    new_token = input("\nToken: ").strip()
    
    if not new_token:
        print("❌ No token provided")
        return
    
    # Validate token
    print("\n🔍 Validating token...")
    is_valid, result = validate_token(new_token)
    
    if not is_valid:
        print(f"❌ Token validation failed: {result}")
        return
    
    # Display token info
    print("✅ Token is valid!")
    print(f"   Account: {result['uid']}")
    print(f"   Issued: {result['issued']}")
    print(f"   Expires: {result['expires']}")
    print(f"   Valid for: {result['valid_days']:.1f} days")
    
    # Confirm update
    confirm = input(f"\n❓ Update framework with this token? (y/N): ").strip().lower()
    
    if confirm in ['y', 'yes']:
        # Update framework
        print("\n🔄 Updating framework...")
        success, message = update_token_in_framework(new_token)
        
        if success:
            print(f"✅ {message}")
            print("\n🚀 Framework updated! You can now run:")
            print("   python automatic_nasa_framework.py")
            print("   streamlit run app.py")
        else:
            print(f"❌ Update failed: {message}")
    else:
        print("❌ Update cancelled")

if __name__ == "__main__":
    main()
