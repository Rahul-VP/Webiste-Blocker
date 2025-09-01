# 🌐 Website Blocker (Mini Firewall)

A beginner-friendly Python tool that allows you to block and unblock websites by modifying your system's hosts file. This creates a simple firewall effect that prevents blocked websites from loading in your browser.

## ✨ Features

- **Block websites** - Redirect blocked sites to localhost (127.0.0.1)
- **Unblock websites** - Remove blocks and restore access
- **View blocked list** - See all currently blocked websites
- **Cross-platform** - Works on Windows, Linux, and macOS
- **Automatic logging** - All actions are logged to `blocker_log.txt`
- **User-friendly interface** - Simple menu system with clear messages
- **No external dependencies** - Uses only standard Python libraries

## 🚀 How It Works

The Website Blocker works by modifying your system's hosts file:

- **Windows**: `C:\Windows\System32\drivers\etc\hosts`
- **Linux/macOS**: `/etc/hosts`

When you block a website, it adds a line like:
```
127.0.0.1 facebook.com
```

This redirects all requests to `facebook.com` to your local machine (localhost), effectively blocking access to the website.

## 📋 Requirements

- **Python 3.6+** (comes pre-installed on most systems)
- **Administrator/root privileges** (required to modify hosts file)
- **No additional packages** - uses only standard Python libraries

## 🛠️ Installation

### Option 1: Direct Download
1. Download `website_blocker.py` to your computer
2. Open terminal/command prompt as Administrator
3. Navigate to the file's directory
4. Run the script

## 🚀 Usage

### Windows
1. **Right-click** on Command Prompt or PowerShell
2. Select **"Run as Administrator"**
3. Navigate to the script directory:
   ```cmd
   cd /d "D:\Python\FirewallBlock"
   ```
4. Run the script:
   ```cmd
   python website_blocker.py
   ```

### Linux/macOS
1. Open terminal
2. Navigate to the script directory:
   ```bash
   cd /path/to/FirewallBlock
   ```
3. Run with sudo:
   ```bash
   sudo python3 website_blocker.py
   ```

## 📖 How to Use

Once the script is running, you'll see a menu with these options:

```
📋 Menu Options:
1. Block a website
2. Unblock a website
3. Show blocked websites
4. Refresh blocked list
5. Exit
```

### Blocking a Website
1. Choose option **1**
2. Enter the website name (e.g., `facebook.com`)
3. The script will add it to your hosts file
4. You'll see: "✅ facebook.com is blocked successfully 🚫"

### Unblocking a Website
1. Choose option **2**
2. Enter the website name to unblock
3. The script will remove it from your hosts file
4. You'll see: "✅ facebook.com is unblocked successfully ✅"

### Viewing Blocked Websites
- Choose option **3** to see all currently blocked websites
- Choose option **4** to refresh the list if you've made manual changes

## 🧪 Testing

After blocking a website:

1. **Clear your browser cache** (important!)
2. Try to visit the blocked website
3. You should see an error or "This site can't be reached"
4. Unblock the website to restore access

**Note**: Some browsers cache DNS lookups, so you may need to:
- Clear browser cache and cookies
- Restart your browser
- Flush DNS cache (`ipconfig /flushdns` on Windows)

## 📝 Logging

All actions are automatically logged to `blocker_log.txt` in the same directory:

```
[2024-01-15 14:30:25] BLOCKED: facebook.com
[2024-01-15 14:35:10] UNBLOCKED: facebook.com
[2024-01-15 15:00:00] BLOCKED: youtube.com
```

## ⚠️ Important Notes

### Administrator Privileges Required
- **Windows**: Must run CMD/PowerShell as Administrator
- **Linux/macOS**: Must use `sudo` command
- This is required because the hosts file is a system file

### Hosts File Location
- **Windows**: `C:\Windows\System32\drivers\etc\hosts`
- **Linux/macOS**: `/etc/hosts`

### Browser Cache
- Clear browser cache after blocking/unblocking
- Some browsers may need to be restarted
- DNS cache may need to be flushedy

The executable will be created in the `dist/` folder and can be run directly without Python installed.

## 🏗️ Project Structure

```
FirewallBlock/
├── website_blocker.py      # Main Python script
├── README.md              # This file
├── blocker_log.txt        # Action log (created automatically)
└── requirements.txt       # Dependencies (none required)
```

## 🔒 Security Considerations

- **Administrator privileges**: The script requires admin access to modify system files
- **Hosts file modification**: Changes affect your entire system
- **Backup**: Consider backing up your hosts file before use
- **Trust**: Only run scripts from trusted sources

## 🤝 Contributing

Feel free to contribute improvements:
- Bug fixes
- New features
- Better error handling
- Cross-platform compatibility
- Documentation improvements
---

**Happy Blocking! 🚫🌐✅**
