#!/usr/bin/env python3
"""
Test NASA API access and token limitations
"""

import requests
import json
import datetime

def test_nasa_token_access():
    """Test NASA API access with current token"""
    
    token = 'eyJ0eXAiOiJKV1QiLCJvcmlnaW4iOiJFYXJ0aGRhdGEgTG9naW4iLCJzaWciOiJlZGxqd3RwdWJrZXlfb3BzIiwiYWxnIjoiUlMyNTYifQ.eyJ0eXBlIjoiVXNlciIsInVpZCI6ImxhYmVlYjIzMzkiLCJleHAiOjE3NjI3MzI3OTksImlhdCI6MTc1NzUxMTI2OSwiaXNzIjoiaHR0cHM6Ly91cnMuZWFydGhkYXRhLm5hc2EuZ292IiwiaWRlbnRpdHlfcHJvdmlkZXIiOiJlZGxfb3BzIiwiYWNyIjoiZWRsIiwiYXNzdXJhbmNlX2xldmVsIjozfQ.Sh5Iq9_16xMVE4ZU3Pbrqm1v1lGpxJIQEy_JpaAAwPKz7bN-tZy5v6OWaUabiQSrn0PFvNI08gJ3iI7NEvm47IjWWmzVwYc8cuIuM0a7kYxpLoVy8zwAlgwwefbY-YsJ0rsLfakvcvpEId_Qi5tAr24T5tSh3VkZsZzbW9HUBQI5jZvP-dr_tUuD_BIZkLgLmrDGRBfykSN4a9fKwacclNYCeRvhPsgbl4MtszR1As33rzwZziegEWjDcl6a64Z---X2BCSvUSnVekFQwQAwc9sHF12qJ4IiT1NKowXqAagp2uVMZhi_h5Mw9A7UrkumIH11-7kGNihQTFm1tsW4Hg'
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json',
        'User-Agent': 'NASA-Competition-SharkHabitat/1.0'
    }
    
    print("🔍 TESTING NASA API ACCESS & TOKEN LIMITATIONS")
    print("=" * 60)
    
    # Test 1: CMR API access
    print('\n🛰️ Testing NASA CMR API access...')
    try:
        response = requests.get(
            'https://cmr.earthdata.nasa.gov/search/collections.json?keyword=MODIS&page_size=5', 
            headers=headers, 
            timeout=15
        )
        print(f'   CMR API: HTTP {response.status_code}')
        if response.status_code == 200:
            data = response.json()
            collections = data.get('feed', {}).get('entry', [])
            print(f'   Collections found: {len(collections)}')
            print('   ✅ CMR API access working')
        else:
            print(f'   ❌ CMR API failed: {response.text[:100]}')
    except Exception as e:
        print(f'   ❌ CMR Error: {e}')
    
    # Test 2: Granule search
    print('\n📡 Testing NASA Granule Search...')
    try:
        params = {
            'collection_concept_id': 'C1996881146-POCLOUD',  # MODIS Aqua L3 SST
            'temporal': '2024-01-01T00:00:00Z,2024-01-31T23:59:59Z',
            'bounding_box': '-125,32,-117,42',  # California coast
            'page_size': 5
        }
        
        response = requests.get(
            'https://cmr.earthdata.nasa.gov/search/granules.json',
            params=params,
            headers=headers,
            timeout=15
        )
        
        print(f'   Granule Search: HTTP {response.status_code}')
        if response.status_code == 200:
            data = response.json()
            granules = data.get('feed', {}).get('entry', [])
            print(f'   Granules found: {len(granules)}')
            if granules:
                print('   ✅ Granule search working')
                print(f'   Sample granule: {granules[0].get("title", "Unknown")[:50]}...')
            else:
                print('   ⚠️ No granules found for this time/location')
        else:
            print(f'   ❌ Granule search failed: {response.text[:100]}')
    except Exception as e:
        print(f'   ❌ Granule Error: {e}')
    
    # Test 3: ERDDAP access (public, no auth needed)
    print('\n🌊 Testing NOAA ERDDAP access...')
    try:
        response = requests.get(
            'https://coastwatch.pfeg.noaa.gov/erddap/info/index.json',
            timeout=15
        )
        print(f'   ERDDAP API: HTTP {response.status_code}')
        if response.status_code == 200:
            print('   ✅ ERDDAP access working (public data)')
        else:
            print(f'   ❌ ERDDAP failed: {response.status_code}')
    except Exception as e:
        print(f'   ❌ ERDDAP Error: {e}')
    
    # Test 4: Token validation
    print('\n🔑 Testing Token Validation...')
    try:
        response = requests.get(
            'https://urs.earthdata.nasa.gov/api/users/tokens',
            headers=headers,
            timeout=15
        )
        print(f'   Token Validation: HTTP {response.status_code}')
        if response.status_code == 200:
            print('   ✅ Token is valid and authenticated')
        else:
            print(f'   ❌ Token validation failed: {response.status_code}')
    except Exception as e:
        print(f'   ❌ Token validation error: {e}')

if __name__ == "__main__":
    test_nasa_token_access()
