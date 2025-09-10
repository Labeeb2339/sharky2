# 🔑 Get Your Free NASA Satellite Data Access

## 🛰️ Why You Need a NASA Account

SharkTracker Pro uses real NASA satellite data to analyze shark habitats. To access this amazing data, you need a free NASA Earthdata account. Don't worry - it's completely free and takes just 5 minutes!

---

## 🚀 Super Easy Setup (5 Minutes)

### Step 1: Create Your Free NASA Account
1. **Visit NASA Earthdata**: https://urs.earthdata.nasa.gov/users/new
2. **Fill out the form** with your information:
   - Username (choose something memorable)
   - Email address
   - Password
   - Basic profile information
3. **Click "Register"**
4. **Check your email** and click the verification link
5. **You now have access to NASA's satellite data!** 🎉

### Step 2: Get Your Access Token
1. **Login** to NASA Earthdata: https://urs.earthdata.nasa.gov/
2. **Click your username** in the top right corner
3. **Select "Profile"** from the dropdown menu
4. **Go to "Applications"** tab
5. **Click "Generate Token"**
6. **Copy the long token** (starts with `eyJ...`)
   - This is your personal key to NASA's satellite data!

### Step 3: Add Token to SharkTracker Pro
**Option A: Easy Method (Recommended)**
1. Open the file `automatic_nasa_framework.py`
2. Find line 19 (near the top)
3. Replace `"YOUR_NASA_JWT_TOKEN_HERE"` with your token
4. Save the file

**Option B: For Advanced Users**
Set an environment variable:
```bash
export NASA_JWT_TOKEN="your_token_here"
```

### Step 4: Test Your Setup
```bash
# Run SharkTracker Pro
python automatic_nasa_framework.py

# You should see: "✅ Fresh NASA JWT token loaded"
```

---

## ✅ You're All Set!

**Congratulations!** You now have:
- 🛰️ **Free access** to NASA's satellite data
- 🔑 **Personal token** for SharkTracker Pro
- 🦈 **Ready to analyze** shark habitats worldwide

---

## 🔄 When Your Token Expires (Every 2-3 Months)

Don't worry - tokens expire for security. Here's how to get a new one:

### 🚨 How to Know Your Token Expired
You'll see this error message:
```
❌ Token EXPIRED - Need to refresh
❌ HTTP 401 Unauthorized
```

### 🔄 Getting a New Token (2 Minutes)
1. **Go back to NASA Earthdata**: https://urs.earthdata.nasa.gov/
2. **Login** with your existing account
3. **Go to Profile → Applications**
4. **Click "Generate Token"** (this creates a new one)
5. **Copy the new token**
6. **Replace the old token** in `automatic_nasa_framework.py` (line 19)
7. **You're ready to go again!** 🎉

### 📅 Pro Tip: Set a Reminder
- Tokens typically last **60-90 days**
- Set a calendar reminder for **2 months** from now
- Title: "Refresh NASA token for SharkTracker Pro"

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
