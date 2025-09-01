"""
Website Blocker (Mini Firewall)
A simple Python tool to block and unblock websites by modifying the hosts file.
Requires administrator privileges to run.
"""

import os
import sys
import time
import platform
from datetime import datetime

class WebsiteBlocker:
    def __init__(self):
        self.system = platform.system().lower()
        self.hosts_file = self._get_hosts_file_path()
        self.log_file = "blocker_log.txt"
        self.blocked_websites = set()
        self._load_blocked_websites()
    
    def _get_hosts_file_path(self):
        """Get the hosts file path based on the operating system."""
        if self.system == "windows":
            return r"C:\Windows\System32\drivers\etc\hosts"
        elif self.system in ["linux", "darwin"]:  # Linux or macOS
            return "/etc/hosts"
        else:
            print(f"Unsupported operating system: {self.system}")
            sys.exit(1)
    
    def _load_blocked_websites(self):
        """Load currently blocked websites from the hosts file."""
        try:
            if os.path.exists(self.hosts_file):
                with open(self.hosts_file, 'r', encoding='utf-8') as file:
                    for line in file:
                        line = line.strip()
                        if line.startswith('127.0.0.1') and not line.startswith('#'):
                            parts = line.split()
                            if len(parts) >= 2:
                                website = parts[1]
                                self.blocked_websites.add(website)
                print(f"📋 Loaded {len(self.blocked_websites)} blocked websites from hosts file")
            else:
                print(f"⚠️ Hosts file not found at: {self.hosts_file}")
        except PermissionError:
            print("❌ Permission denied! Please run as administrator/root.")
            print(f"On Windows: Run CMD/PowerShell as Administrator")
            print(f"On Linux/Mac: Use 'sudo python3 {sys.argv[0]}'")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error loading hosts file: {e}")
            sys.exit(1)
    
    def _log_action(self, action, website):
        """Log actions to the log file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {action}: {website}\n"
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as file:
                file.write(log_entry)
        except Exception as e:
            print(f"⚠️ Warning: Could not write to log file: {e}")
    
    def _is_website_blocked(self, website):
        """Check if a website is currently blocked."""
        return website in self.blocked_websites
    
    def _get_blocking_entries(self, website):
        """Get all the blocking entries needed for a website."""
        entries = []
        
        # Main domain
        entries.append(f"127.0.0.1 {website}")
        
        # www subdomain
        if not website.startswith('www.'):
            entries.append(f"127.0.0.1 www.{website}")
        
        # Common subdomains for popular sites
        if website in ['youtube.com', 'youtu.be']:
            entries.extend([
                "127.0.0.1 m.youtube.com",
                "127.0.0.1 music.youtube.com",
                "127.0.0.1 kids.youtube.com",
                "127.0.0.1 studio.youtube.com",
                "127.0.0.1 tv.youtube.com",
                "127.0.0.1 youtube-nocookie.com"
            ])
        elif website in ['facebook.com', 'fb.com']:
            entries.extend([
                "127.0.0.1 m.facebook.com",
                "127.0.0.1 mobile.facebook.com",
                "127.0.0.1 touch.facebook.com",
                "127.0.0.1 business.facebook.com"
            ])
        elif website in ['twitter.com', 'x.com']:
            entries.extend([
                "127.0.0.1 mobile.twitter.com",
                "127.0.0.1 m.twitter.com",
                "127.0.0.1 t.co"
            ])
        elif website in ['instagram.com']:
            entries.extend([
                "127.0.0.1 m.instagram.com",
                "127.0.0.1 www.instagram.com"
            ])
        elif website in ['reddit.com']:
            entries.extend([
                "127.0.0.1 m.reddit.com",
                "127.0.0.1 old.reddit.com",
                "127.0.0.1 new.reddit.com"
            ])
        elif website in ['tiktok.com']:
            entries.extend([
                "127.0.0.1 m.tiktok.com",
                "127.0.0.1 www.tiktok.com"
            ])
        
        return entries
    
    def _add_website_to_hosts(self, website):
        """Add a website to the hosts file to block it."""
        try:
            # Read current hosts file
            with open(self.hosts_file, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            # Get all blocking entries needed
            blocking_entries = self._get_blocking_entries(website)
            added_entries = []
            
            # Check which entries don't already exist
            for entry in blocking_entries:
                entry_line = entry + "\n"
                if entry_line not in lines:
                    # Add new blocking entry
                    with open(self.hosts_file, 'a', encoding='utf-8') as file:
                        file.write(entry_line)
                    added_entries.append(entry)
                    print(f"📝 Added entry: {entry}")
                else:
                    print(f"ℹ️ Entry already exists: {entry}")
            
            return len(added_entries) > 0
        except Exception as e:
            print(f"❌ Error adding website to hosts file: {e}")
            return False
    
    def _remove_website_from_hosts(self, website):
        """Remove a website from the hosts file to unblock it."""
        try:
            # Read current hosts file
            with open(self.hosts_file, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            # Get all blocking entries for this website
            blocking_entries = self._get_blocking_entries(website)
            new_lines = []
            removed_count = 0
            
            for line in lines:
                line_stripped = line.strip()
                should_keep = True
                
                for entry in blocking_entries:
                    if line_stripped == entry:
                        should_keep = False
                        removed_count += 1
                        print(f"📝 Removed entry: {entry}")
                        break
                
                if should_keep:
                    new_lines.append(line)
            
            # Write back the modified content
            with open(self.hosts_file, 'w', encoding='utf-8') as file:
                file.writelines(new_lines)
            
            return removed_count > 0
        except Exception as e:
            print(f"❌ Error removing website from hosts file: {e}")
            return False
    
    def block_website(self, website):
        """Block a website by adding it to the hosts file."""
        # Clean the website input
        website = website.strip().lower()
        
        # Remove protocol if present
        if website.startswith(('http://', 'https://')):
            website = website.replace('http://', '').replace('https://', '')
        
        # Remove www. prefix for consistency
        if website.startswith('www.'):
            website = website.replace('www.', '')
        
        if not website:
            print("❌ Please enter a valid website name.")
            return
        
        if self._is_website_blocked(website):
            print(f"ℹ️ {website} is already blocked 🚫")
            return
        
        print(f"🔄 Blocking {website} and related domains...")
        
        if self._add_website_to_hosts(website):
            self.blocked_websites.add(website)
            print(f"✅ {website} is blocked successfully 🚫")
            print(f"💡 Tip: Clear your browser cache and try visiting {website}")
            print(f"💡 Tip: Also try www.{website} and other subdomains")
            self._log_action("BLOCKED", website)
        else:
            print(f"❌ Failed to block {website}")
    
    def unblock_website(self, website):
        """Unblock a website by removing it from the hosts file."""
        # Clean the website input
        website = website.strip().lower()
        
        # Remove protocol if present
        if website.startswith(('http://', 'https://')):
            website = website.replace('http://', '').replace('https://', '')
        
        # Remove www. prefix for consistency
        if website.startswith('www.'):
            website = website.replace('www.', '')
        
        if not website:
            print("❌ Please enter a valid website name.")
            return
        
        if not self._is_website_blocked(website):
            print(f"ℹ️ {website} is not currently blocked.")
            return
        
        print(f"🔄 Unblocking {website} and related domains...")
        
        if self._remove_website_from_hosts(website):
            self.blocked_websites.remove(website)
            print(f"✅ {website} is unblocked successfully ✅")
            print(f"💡 Tip: Clear your browser cache to restore access to {website}")
            self._log_action("UNBLOCKED", website)
        else:
            print(f"❌ Failed to unblock {website}")
    
    def show_blocked_websites(self):
        """Display all currently blocked websites."""
        if not self.blocked_websites:
            print("📋 No websites are currently blocked.")
            return
        
        print("📋 Currently blocked websites:")
        print("-" * 40)
        for i, website in enumerate(sorted(self.blocked_websites), 1):
            print(f"{i:2d}. {website} 🚫")
        print("-" * 40)
        print(f"Total blocked: {len(self.blocked_websites)}")
    
    def refresh_blocked_list(self):
        """Refresh the list of blocked websites from the hosts file."""
        self.blocked_websites.clear()
        self._load_blocked_websites()
        print("🔄 Blocked websites list refreshed.")
    
    def show_hosts_file_info(self):
        """Show information about the hosts file."""
        print(f"📁 Hosts file location: {self.hosts_file}")
        print(f"📁 Hosts file exists: {'Yes' if os.path.exists(self.hosts_file) else 'No'}")
        
        if os.path.exists(self.hosts_file):
            try:
                with open(self.hosts_file, 'r', encoding='utf-8') as file:
                    content = file.read()
                    lines = content.split('\n')
                    print(f"📁 Total lines in hosts file: {len(lines)}")
                    
                    # Count blocking entries
                    blocking_entries = [line for line in lines if line.strip().startswith('127.0.0.1') and not line.strip().startswith('#')]
                    print(f"📁 Blocking entries found: {len(blocking_entries)}")
                    
                    if blocking_entries:
                        print("📁 Current blocking entries:")
                        for entry in blocking_entries:
                            print(f"   {entry.strip()}")
            except Exception as e:
                print(f"❌ Error reading hosts file: {e}")
    
    def run(self):
        """Main program loop with menu system."""
        print("🌐 Website Blocker (Mini Firewall)")
        print("=" * 40)
        print(f"Hosts file: {self.hosts_file}")
        print(f"Log file: {self.log_file}")
        print("=" * 40)
        
        while True:
            print("\n📋 Menu Options:")
            print("1. Block a website")
            print("2. Unblock a website")
            print("3. Show blocked websites")
            print("4. Refresh blocked list")
            print("5. Show hosts file info")
            print("6. Exit")
            
            try:
                choice = input("\n🔢 Enter your choice (1-6): ").strip()
                
                if choice == "1":
                    website = input("🌐 Enter website to block (e.g., youtube.com): ")
                    self.block_website(website)
                
                elif choice == "2":
                    website = input("🌐 Enter website to unblock (e.g., youtube.com): ")
                    self.unblock_website(website)
                
                elif choice == "3":
                    self.show_blocked_websites()
                
                elif choice == "4":
                    self.refresh_blocked_list()
                
                elif choice == "5":
                    self.show_hosts_file_info()
                
                elif choice == "6":
                    print("👋 Goodbye! Thanks for using Website Blocker.")
                    break
                
                else:
                    print("❌ Invalid choice. Please enter a number between 1-6.")
                
                # Small delay for better user experience
                time.sleep(1)
                
            except KeyboardInterrupt:
                print("\n\n👋 Program interrupted by user. Goodbye!")
                break
            except Exception as e:
                print(f"❌ An error occurred: {e}")
                time.sleep(2)

def check_privileges():
    """Check if the script is running with administrator privileges."""
    try:
        if platform.system().lower() == "windows":
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        else:
            # On Unix-like systems, check if we can write to /etc
            return os.access("/etc", os.W_OK)
    except:
        return False

def main():
    """Main function to run the Website Blocker."""
    print("🔒 Website Blocker (Mini Firewall)")
    print("=" * 50)
    
    # Check if running with admin privileges
    if not check_privileges():
        print("❌ This script requires administrator privileges!")
        print("\n📋 How to run with admin privileges:")
        if platform.system().lower() == "windows":
            print("1. Right-click on CMD or PowerShell")
            print("2. Select 'Run as Administrator'")
            print("3. Navigate to this directory")
            print("4. Run: python website_blocker.py")
        else:
            print("1. Open terminal")
            print("2. Navigate to this directory")
            print("3. Run: sudo python3 website_blocker.py")
        print("\n⚠️ Note: Modifying the hosts file requires admin access.")
        input("\nPress Enter to exit...")
        return
    
    print("✅ Running with administrator privileges")
    print("🚀 Starting Website Blocker...")
    time.sleep(1)
    
    try:
        blocker = WebsiteBlocker()
        blocker.run()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()

