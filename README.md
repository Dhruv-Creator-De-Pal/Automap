# 🔍 Automap - AI-Powered Network Security Scanner

> **Intelligent Network Intelligence** — Scan networks with Nmap, analyze with AI, generate professional security reports in seconds.

---

## 🚀 What is Automap?

Automap is a **next-generation network security scanner** that combines the power of Nmap with AI-driven analysis. Instead of raw data dumps, you get:

- ✅ Automated network scanning
- ✅ Intelligent device discovery (IPs, MACs, hostnames, OS detection)
- ✅ Real-time AI security analysis via Ollama
- ✅ **Professional PDF reports** with visual hierarchy
- ✅ Automatic highlights of security risks
- ✅ Service detection and port analysis

**In 30 seconds, go from:** Network → Scan → Analysis → Professional Report

---

## 📊 Features at a Glance

| Feature | Description |
|---------|------------|
| 🔎 **Network Scanning** | Aggressive nmap scans with -A -T4 flags |
| 🤖 **AI Analysis** | Ollama integration for real-time security insights |
| 📄 **Smart Reports** | Beautiful PDFs with visual hierarchy & symbols |
| ⚠️ **Risk Highlighting** | Auto-detects SSH, HTTP, multi-port devices |
| 🖥️ **Device Inventory** | Complete host enumeration with details |
| 🎯 **Security Summary** | Top ports, exposures, and recommendations |

---

## 💻 Installation

### Requirements
- Python 3.8+
- Nmap installed
- Ollama server (local or remote)
- Linux/Unix (tested on Ubuntu, RHEL)

### Quick Start

```bash
# Clone repository
git clone https://github.com/yourusername/automap.git
cd automap

# Install dependencies
pip install -r requirements.txt

# Run Automap
sudo python main.py
```

### requirements.txt
```
requests==2.31.0
fpdf2==2.7.0
apscheduler==3.10.4
```

---

## 🚀 Usage

### Basic Scan

```bash
$ sudo python main.py
---

## 🔐 Security Notes

- Always run with `sudo` for root-level network access
- Ollama should be on a trusted network
- Report files contain sensitive network data — keep secure
- Consider running in isolated environment for production

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `nmap: command not found` | Install: `sudo apt install nmap` |
| `Ollama connection failed` | Check Ollama is running: `curl http://ollama:9090/api/tags` |
| `Permission denied` | Run with `sudo`: `sudo python main.py` |
| `Old cached reports` | Reports auto-cleanup runs weekly |

---

## 🤝 Upcomeing update:

- [ ] Real-time scanning updates
- [ ] Slack/Discord notifications
- [ ] Database integration

---

## 📝 License

MIT License — See LICENSE file

---

## ⭐ Show Your Support

If Automap helped you, consider:
- ⭐ **Star this repo** on GitHub
- 🔄 **Share** with your network
- 📧 **Send feedback** or suggestions
- 🐛 **Report issues** you find

---

## 📞 Contact & Support

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions

---

## 🎯 Roadmap

- [ ] v2.1: Scheduled automated scans
- [ ] v2.2: Multi-target comparison
- [ ] v2.3: Custom alert system

---

**Made with ❤️ for network security professionals**

```
   _         _                         
  / \   _   _| |_ ___  _ __ ___   __ _ _ __
 / _ \ | | | | __/ _ \| '_ ` _ \ / _` | '_ \
/ ___ \| |_| | || (_) | | | | | | (_| | |_) |
/_/   \_\\__,_|\__\___/|_| |_| |_|\__,_| .__/
                                       |_|

Your Network. Secured. Analyzed. Reported.
```
