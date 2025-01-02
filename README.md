<div align="center">
  <h2 align="center">Pastebin Autoposter</h2>
  <p align="center">
    A tool designed to automate posting content to Pastebin with proxy support, Cloudflare bypass, and efficient batch processing.
    <br />
    <br />
    <a href="https://discord.cyberious.xyz">💬 Discord</a>
    ·
    <a href="https://github.com/sexfrance/Pastebin-Autoposter#-changelog">📜 ChangeLog</a>
    ·
    <a href="https://github.com/sexfrance/Pastebin-Autoposter/issues">⚠️ Report Bug</a>
    ·
    <a href="https://github.com/sexfrance/Pastebin-Autoposter/issues">💡 Request Feature</a>
  </p>
</div>

---

### ⚙️ Installation

- Requires: `Python 3.7+`
- Make a python virtual environment: `python3 -m venv venv`
- Source the environment: `venv\Scripts\activate` (Windows) / `source venv/bin/activate` (macOS, Linux)
- Install the requirements: `pip install -r requirements.txt`

---

### 🔥 Features

- Automated content posting to Pastebin
- Cloudflare challenge bypass
- Proxy support for avoiding rate limits
- Multi-threaded posting capabilities
- Flexible content management (single file or directory-based)
- Custom post titles support
- Automatic saving of paste URLs
- Smart rate limit handling

---

### 📝 Usage

1. **Content Setup**:

   - Option 1: Place your content in `input/content.txt`
   - Option 2: Add multiple files in `input/Content/` directory (filename becomes post title)

2. **Proxy Setup** (Optional):

   - Add proxies to `input/proxies.txt` (one per line)
   - Format: `ip:port` or `user:pass@ip:port`

3. **Configuration**:

   - Adjust settings in `input/config.toml`:
     ```toml
     [dev]
     Debug = false
     Proxyless = false
     Threads = 1
     ```

4. **Running the script**:

   ```bash
   python main.py
   ```

5. **Output**:
   - Generated Pastebin URLs are saved in `output/links.txt`

---

### 📹 Preview

![Preview](https://i.imgur.com/PEzFMpH.gif)

---

### ❗ Disclaimers

- This project is for educational purposes only
- The author is not responsible for any misuse of this tool
- Respect Pastebin's terms of service and rate limits
- When using proxies, ensure they are properly configured and reliable

---

### 📜 ChangeLog

```diff
v0.0.1 ⋮ 12/26/2024
! Initial release.
```

<p align="center">
  <img src="https://img.shields.io/github/license/sexfrance/Pastebin-Autoposter.svg?style=for-the-badge&labelColor=black&color=f429ff&logo=IOTA"/>
  <img src="https://img.shields.io/github/stars/sexfrance/Pastebin-Autoposter.svg?style=for-the-badge&labelColor=black&color=f429ff&logo=IOTA"/>
  <img src="https://img.shields.io/github/languages/top/sexfrance/Pastebin-Autoposter.svg?style=for-the-badge&labelColor=black&color=f429ff&logo=python"/>
</p>
