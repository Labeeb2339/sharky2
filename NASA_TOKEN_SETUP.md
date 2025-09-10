# 🔑 NASA Token Setup Guide

## 🎯 Overview
Complete guide for setting up and managing NASA Earthdata JWT tokens for the shark habitat prediction framework.

---

## 🚀 Quick Setup (5 Minutes)

### Step 1: Create NASA Earthdata Account
1. Go to: https://urs.earthdata.nasa.gov/users/new
2. Fill out the registration form
3. Verify your email address
4. Login to your new account

### Step 2: Generate JWT Token
1. Login to NASA Earthdata: https://urs.earthdata.nasa.gov/
2. Go to "Applications" → "Authorized Apps"
3. Click "Generate Token"
4. Copy the JWT token (starts with `eyJ...`)

### Step 3: Update Framework
```python
# In automatic_nasa_framework.py, line 19:
self.jwt_token = "eyJ0eXAiOiJKV1QiLCJvcmlnaW4iOiJFYXJ0aGRhdGEgTG9naW4i..."
```

### Step 4: Test Setup
```bash
python automatic_nasa_framework.py
```

---

## 🔍 Token Management

### Check Token Status
```python
import jwt
import datetime

token = "YOUR_JWT_TOKEN_HERE"

# Decode token (no signature verification needed for info)
payload = jwt.decode(token, options={'verify_signature': False})

print(f"User: {payload.get('uid')}")
print(f"Issued: {datetime.datetime.fromtimestamp(payload.get('iat'))}")
print(f"Expires: {datetime.datetime.fromtimestamp(payload.get('exp'))}")

# Check if expired
now = datetime.datetime.now().timestamp()
if payload.get('exp') < now:
    print("❌ Token EXPIRED - Need to refresh")
else:
    days_left = (payload.get('exp') - now) / (24 * 3600)
    print(f"✅ Token valid for {days_left:.1f} more days")
```

### Quick Token Check Script
```bash
python -c "
import jwt
import datetime
token = 'YOUR_TOKEN_HERE'
payload = jwt.decode(token, options={'verify_signature': False})
exp = datetime.datetime.fromtimestamp(payload['exp'])
now = datetime.datetime.now()
print(f'Token expires: {exp}')
print(f'Status: {'EXPIRED' if exp < now else 'VALID'}')
"
```

---

## 🔄 Token Refresh (When Expired)

### Method 1: Manual Refresh (Recommended)
1. **Login to NASA Earthdata**: https://urs.earthdata.nasa.gov/
2. **Go to Profile** → "Applications" → "Authorized Apps"
3. **Revoke old token** (if exists)
4. **Generate new token**
5. **Copy new JWT token**
6. **Update framework**:
   ```python
   # In automatic_nasa_framework.py, line 19:
   self.jwt_token = "NEW_JWT_TOKEN_HERE"
   ```

### Method 2: Using Update Script
```bash
python update_nasa_token.py
# Follow prompts to enter new token
```

### Method 3: Environment Variable (Advanced)
```bash
# Set environment variable
export NASA_JWT_TOKEN="YOUR_NEW_TOKEN"

# Update framework to read from environment
# In automatic_nasa_framework.py:
import os
self.jwt_token = os.getenv('NASA_JWT_TOKEN', 'fallback_token_here')
```

---

## ⚠️ Token Security & Best Practices

### Security Guidelines
- ✅ **Keep tokens private** - Never share or commit to version control
- ✅ **Use environment variables** for production deployments
- ✅ **Refresh regularly** - Don't wait for expiration
- ✅ **Monitor usage** - NASA tracks API usage per token
- ❌ **Don't share tokens** between users/accounts
- ❌ **Don't hardcode in public repositories**

### Token Sharing Policy
**Q: Can I use tokens from other accounts?**

**Technical Answer**: Yes, JWT tokens are transferable and will work.

**Legal/Ethical Answer**: No, NASA Terms of Service specify tokens are for account holder only.

**Recommendation**: Create your own free NASA Earthdata account (takes 5 minutes).

### Rate Limiting
- NASA limits requests per token per hour
- Framework automatically handles rate limiting
- Multiple users sharing one token will hit limits faster

---

## 🛠️ Troubleshooting

### Common Token Issues

#### 1. Token Expired
```
Error: HTTP 401 Unauthorized
```
**Solution**: Generate new token following refresh steps above.

#### 2. Invalid Token Format
```
Error: Invalid JWT token format
```
**Solution**: Ensure token starts with `eyJ` and has no extra spaces/characters.

#### 3. Network/API Issues
```
Error: Connection timeout
```
**Solution**: Check internet connection and NASA API status.

#### 4. Rate Limiting
```
Error: HTTP 429 Too Many Requests
```
**Solution**: Wait a few minutes, framework will automatically retry.

### Testing Token Validity
```python
import requests

token = "YOUR_TOKEN_HERE"
headers = {'Authorization': f'Bearer {token}'}

# Test NASA CMR API
response = requests.get(
    'https://cmr.earthdata.nasa.gov/search/collections.json',
    headers=headers,
    params={'page_size': 1}
)

if response.status_code == 200:
    print("✅ Token is valid and working")
else:
    print(f"❌ Token issue: HTTP {response.status_code}")
```

---

## 🔧 Advanced Token Management

### Automatic Token Refresh (Advanced Users)
The framework includes automatic token refresh attempts, but manual refresh is more reliable:

```python
# In nasa_auto_auth.py - automatic refresh system
from nasa_auto_auth import NASAAutoAuth

auth = NASAAutoAuth()
auth.set_credentials("your_username", "your_password")
new_token = auth.get_fresh_token()
```

**Note**: Automatic refresh is complex due to NASA's authentication system changes. Manual refresh every 30-60 days is recommended.

### Token Monitoring Script
```python
# token_monitor.py
import jwt
import datetime
import schedule
import time

def check_token_expiry():
    token = "YOUR_TOKEN_HERE"
    payload = jwt.decode(token, options={'verify_signature': False})
    exp_time = datetime.datetime.fromtimestamp(payload['exp'])
    days_left = (exp_time - datetime.datetime.now()).days
    
    if days_left <= 7:
        print(f"⚠️ Token expires in {days_left} days - Time to refresh!")
    else:
        print(f"✅ Token valid for {days_left} more days")

# Check daily
schedule.every().day.at("09:00").do(check_token_expiry)

while True:
    schedule.run_pending()
    time.sleep(3600)  # Check every hour
```

---

## 📊 Token Information

### Current Token Details
Your current token (from framework):
```
User ID: labeeb2339
Issued: 2025-01-10 (example)
Expires: 2025-03-15 (example)
Valid for: ~60 days
```

### Token Lifecycle
- **Issue Date**: When token was created
- **Expiration**: Typically 60-90 days from issue
- **Refresh Window**: Refresh 7-14 days before expiration
- **Grace Period**: Tokens may work briefly after expiration

---

## 🎯 Quick Reference

### Essential Commands
```bash
# Check token expiry
python -c "import jwt; print(jwt.decode('TOKEN', options={'verify_signature': False})['exp'])"

# Test framework with current token
python automatic_nasa_framework.py

# Update token in framework
# Edit line 19 in automatic_nasa_framework.py

# Launch web app
streamlit run app.py
```

### Important URLs
- **NASA Earthdata Registration**: https://urs.earthdata.nasa.gov/users/new
- **NASA Earthdata Login**: https://urs.earthdata.nasa.gov/
- **Token Management**: https://urs.earthdata.nasa.gov/profile
- **NASA API Status**: https://status.earthdata.nasa.gov/

---

## 🏆 Success Checklist

- [ ] NASA Earthdata account created
- [ ] JWT token generated
- [ ] Token updated in framework (line 19)
- [ ] Framework tested successfully
- [ ] Token expiry date noted
- [ ] Refresh reminder set (7 days before expiry)

**Your NASA token setup is complete! The framework is ready for competition-grade satellite data processing.** 🛰️🦈🏆
