#!/usr/bin/env python3
"""Check NASA JWT token expiration"""

import jwt
import datetime
import requests

# Your current token
token = "eyJ0eXAiOiJKV1QiLCJvcmlnaW4iOiJFYXJ0aGRhdGEgTG9naW4iLCJzaWciOiJlZGxqd3RwdWJrZXlfb3BzIiwiYWxnIjoiUlMyNTYifQ.eyJ0eXAiOiJKV1QiLCJvcmlnaW4iOiJFYXJ0aGRhdGEgTG9naW4iLCJzaWciOiJlZGxqd3RwdWJrZXlfb3BzIiwiYWxnIjoiUlMyNTYifQ.eyJ0eXBlIjoiVXNlciIsInVpZCI6ImxhYmVlYjIzMzkiLCJleHAiOjE3NjI3MzI3OTksImlhdCI6MTc1NzUwMTI1MSwiaXNzIjoiaHR0cHM6Ly91cnMuZWFydGhkYXRhLm5hc2EuZ292IiwiaWRlbnRpdHlfcHJvdmlkZXIiOiJlZGxfb3BzIiwiYWNyIjoiZWRsIiwiYXNzdXJhbmNlX2xldmVsIjozfQ.PIg6AGXJRSs4ql-VOnIAQaOE-v-Y18uSwk-OWPBYM7_AiItzkXbdtInGpStAcOhCqa9NooTXVonhC-DbttTzlGAMjTOvrlOx0lGQkUP8aEwnsC3yTlI6QC6fQ7O5AuAvpcjVR1Tgh8frdRl7aUZuVSEjZtrlmJgl-TZXkctmO9izbH0M5rCxCLaTjAbEkvruv7XcRTYxzrMyhLIUeNqDUBJvxhpWFjXkcBW6Rla6rm_aWKk1TXY-S6NrGBTtcYime3IW6cdBlV65gX2Qbg2F6oqDzPUrNfSk2I_I7RB22esLq6-jBJDBAibg2qJtLo3EeXfJNU8FwJubVVQTjIA_8w"

try:
    # Decode token without verification
    payload = jwt.decode(token, options={"verify_signature": False})
    
    print("🔍 NASA JWT TOKEN ANALYSIS")
    print("=" * 50)
    print(f"User ID: {payload.get('uid', 'Unknown')}")
    print(f"Token expires (timestamp): {payload.get('exp', 'Unknown')}")
    
    if 'exp' in payload:
        exp_date = datetime.datetime.fromtimestamp(payload['exp'])
        current_date = datetime.datetime.now()
        
        print(f"Expiration date: {exp_date}")
        print(f"Current time: {current_date}")
        print(f"Token valid: {exp_date > current_date}")
        
        if exp_date > current_date:
            print("✅ Token is still valid!")
            
            # Test the token with a real NASA API call
            print("\n🛰️ TESTING NASA API ACCESS")
            print("=" * 50)
            
            headers = {
                'Authorization': f'Bearer {token}',
                'Accept': 'application/json',
                'User-Agent': 'NASA-Competition-SharkHabitat/1.0'
            }
            
            # Test CMR search
            cmr_url = "https://cmr.earthdata.nasa.gov/search/granules.json"
            params = {
                'collection_concept_id': 'C1996881146-POCLOUD',  # MODIS Aqua SST
                'temporal': '2024-01-01T00:00:00Z,2024-01-02T23:59:59Z',
                'bounding_box': '-125,32,-115,42',
                'page_size': 1
            }
            
            try:
                response = requests.get(cmr_url, params=params, headers=headers, timeout=10)
                print(f"CMR API Status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ NASA API ACCESS WORKING!")
                    print(f"Found {len(data.get('feed', {}).get('entry', []))} granules")
                    
                    if data.get('feed', {}).get('entry'):
                        granule = data['feed']['entry'][0]
                        print(f"Sample granule: {granule.get('title', 'Unknown')}")
                else:
                    print(f"❌ NASA API Error: {response.status_code}")
                    print(f"Response: {response.text[:200]}...")
                    
            except Exception as e:
                print(f"❌ API Test Error: {e}")
        else:
            print("❌ Token has expired!")
            print("\n🔄 TO GET A NEW TOKEN:")
            print("1. Go to https://urs.earthdata.nasa.gov/")
            print("2. Log in with your NASA Earthdata account")
            print("3. Generate a new JWT token")
            print("4. Replace the token in automatic_nasa_framework.py")
            
except Exception as e:
    print(f"❌ Token decode error: {e}")
    print("\n🔄 TO GET A NEW TOKEN:")
    print("1. Go to https://urs.earthdata.nasa.gov/")
    print("2. Log in with your NASA Earthdata account")
    print("3. Generate a new JWT token")
    print("4. Replace the token in automatic_nasa_framework.py")
