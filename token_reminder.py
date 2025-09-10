#!/usr/bin/env python3
"""
NASA Token Reminder System
Simple system to remind you when to refresh your NASA token
"""

import json
import os
from datetime import datetime, timedelta

class TokenReminder:
    """Simple token expiration reminder system"""
    
    def __init__(self):
        self.reminder_file = "token_reminder.json"
        self.load_reminder_data()
    
    def load_reminder_data(self):
        """Load token reminder data"""
        if os.path.exists(self.reminder_file):
            try:
                with open(self.reminder_file, 'r') as f:
                    data = json.load(f)
                    self.last_refresh = datetime.fromisoformat(data.get('last_refresh', '2024-01-01'))
                    self.refresh_interval = data.get('refresh_interval_days', 30)
            except:
                self.set_defaults()
        else:
            self.set_defaults()
    
    def set_defaults(self):
        """Set default values"""
        self.last_refresh = datetime.now()
        self.refresh_interval = 30  # 30 days
    
    def save_reminder_data(self):
        """Save reminder data"""
        data = {
            'last_refresh': self.last_refresh.isoformat(),
            'refresh_interval_days': self.refresh_interval,
            'next_refresh': (self.last_refresh + timedelta(days=self.refresh_interval)).isoformat()
        }
        
        with open(self.reminder_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def mark_token_refreshed(self):
        """Mark that token was refreshed today"""
        self.last_refresh = datetime.now()
        self.save_reminder_data()
        print("✅ Token refresh recorded")
    
    def check_token_status(self):
        """Check if token needs refreshing"""
        days_since_refresh = (datetime.now() - self.last_refresh).days
        days_until_refresh = self.refresh_interval - days_since_refresh
        
        print("🔑 NASA TOKEN STATUS")
        print("=" * 30)
        print(f"Last refresh: {self.last_refresh.strftime('%Y-%m-%d')}")
        print(f"Days since refresh: {days_since_refresh}")
        print(f"Days until next refresh: {days_until_refresh}")
        
        if days_until_refresh <= 0:
            print("🚨 TOKEN REFRESH NEEDED!")
            print("\n📋 TO REFRESH YOUR TOKEN:")
            print("1. Go to: https://urs.earthdata.nasa.gov/")
            print("2. Log in with your account")
            print("3. Generate new JWT token")
            print("4. Update automatic_nasa_framework.py line 19")
            print("5. Run: python token_reminder.py --refreshed")
            return False
        elif days_until_refresh <= 5:
            print("⚠️ TOKEN REFRESH NEEDED SOON!")
            print(f"   Refresh in {days_until_refresh} days")
            return True
        else:
            print("✅ Token is current")
            return True
    
    def show_refresh_instructions(self):
        """Show detailed refresh instructions"""
        print("\n🔄 NASA TOKEN REFRESH INSTRUCTIONS")
        print("=" * 50)
        print()
        print("STEP 1: Get New Token")
        print("   • Go to: https://urs.earthdata.nasa.gov/")
        print("   • Log in with your NASA Earthdata account")
        print("   • Navigate to 'Applications' → 'Authorized Apps'")
        print("   • Generate new token or refresh existing")
        print("   • Copy the entire JWT token")
        print()
        print("STEP 2: Update Framework")
        print("   • Open: automatic_nasa_framework.py")
        print("   • Find line 19: self.jwt_token = \"...\"")
        print("   • Replace with your new token")
        print("   • Save the file")
        print()
        print("STEP 3: Test and Record")
        print("   • Test: python automatic_nasa_framework.py")
        print("   • Record: python token_reminder.py --refreshed")
        print()
        print("🏆 Your framework will then use real NASA data for 30+ days!")

def main():
    import sys
    
    reminder = TokenReminder()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--refreshed':
        # Mark token as refreshed
        reminder.mark_token_refreshed()
        print("\n🎉 Token refresh recorded! Your framework is ready for 30+ days of real NASA data.")
    elif len(sys.argv) > 1 and sys.argv[1] == '--instructions':
        # Show detailed instructions
        reminder.show_refresh_instructions()
    else:
        # Check token status
        is_current = reminder.check_token_status()
        
        if not is_current:
            reminder.show_refresh_instructions()
        
        print(f"\n💡 TIP: Run 'python token_reminder.py --instructions' for detailed refresh steps")

if __name__ == "__main__":
    main()
