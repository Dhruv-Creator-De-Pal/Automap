
import ollama
import subprocess
import os
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

try:
    from fpdf import FPDF
except ImportError:
    print("⚠️  fpdf2 not installed. Installing...")
    subprocess.run(["pip", "install", "fpdf2"], check=True)
    from fpdf import FPDF

#check if ollama is installed 

def check_ollama(llm_link=None):
    global ochk
    try:
        requests.get(llm_link+"/api/tags", timeout=5)
        
        return True
    except:
        return False
        
def llm_model(llm_link):
    try :
        list_llm=requests.get(llm_link+"/api/tags", timeout=5).json()
        return list_llm
    except:
        return False


# ========== PARSE XML ==========
def parse_xml(xml_file):
    """Parse nmap XML and extract device info"""
    devices = []
    
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Loop through each host
        for host in root.findall('host'):
            device = {}
            
            # Get IP address
            ip_elem = host.find(".//address[@addrtype='ipv4']")
            device['ip'] = ip_elem.get('addr') if ip_elem is not None else 'N/A'
            
            # Get MAC address
            mac_elem = host.find(".//address[@addrtype='mac']")
            device['mac'] = mac_elem.get('addr') if mac_elem is not None else 'N/A'
            device['vendor'] = mac_elem.get('vendor') if mac_elem is not None else 'N/A'
            
            # Get hostname
            hostname_elem = host.find('.//hostname')
            device['hostname'] = hostname_elem.get('name') if hostname_elem is not None else 'N/A'
            
            # Get open ports and services
            device['ports'] = []
            device['services'] = []
            
            for port in host.findall('.//port'):
                state_elem = port.find('state')
                if state_elem is not None and state_elem.get('state') == 'open':
                    port_num = port.get('portid')
                    service_elem = port.find('service')
                    service_name = service_elem.get('name') if service_elem is not None else 'unknown'
                    
                    device['ports'].append(int(port_num))
                    device['services'].append(service_name)
            
            # Get OS guess
            os_elem = host.find(".//osmatch")
            device['os'] = os_elem.get('name') if os_elem is not None else 'N/A'
            
            devices.append(device)
        
        print(f" Parsed {len(devices)} devices")
        return devices
    
    except Exception as e:
        print(f" Error parsing XML: {e}")
        return None


# ========== ANALYZE DATA ==========
def analyze_data(devices):
    """Extract statistics from devices"""
    from collections import Counter
    
    stats = {}
    stats['total_hosts'] = len(devices)
    stats['total_ports'] = sum(len(d['ports']) for d in devices)
    
    # Get all ports and find top 3
    all_ports = []
    for device in devices:
        all_ports.extend(device['ports'])
    
    port_counts = Counter(all_ports)
    stats['top_ports'] = port_counts.most_common(3)
    
    # Count services
    stats['ssh_count'] = sum(1 for d in devices if 22 in d['ports'])
    stats['http_count'] = sum(1 for d in devices if 80 in d['ports'])
    stats['https_count'] = sum(1 for d in devices if 443 in d['ports'])
    
    # Find devices with many ports
    stats['multi_port_devices'] = [d for d in devices if len(d['ports']) > 5]
    
    return stats


# ========== GET AI INSIGHTS ==========
def get_ai_insights(devices, stats, usr_model, llm_link):
    """Send scan summary to AI and get insights"""
    try:
        # Build prompt
        prompt = f"""Analyze this network scan:
- Total hosts: {stats['total_hosts']}
- Total open ports: {stats['total_ports']}
- Top ports: {', '.join([f"{p[0]}" for p in stats['top_ports']])}
- SSH exposed: {stats['ssh_count']} devices
- HTTP exposed: {stats['http_count']} devices
- HTTPS exposed: {stats['https_count']} devices

Provide brief insights on:
1. What services are exposed
2. Security concerns
3. Recommendations

Keep it short and useful (5-7 lines)"""

        # Send to Ollama
        response = requests.post(
            f"{llm_link}/api/generate",
            json={
                "model": usr_model,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )
        
        if response.status_code == 200:
            return response.json()['response']
        else:
            return "Could not generate AI insights"
    
    except Exception as e:
        print(f" Error getting AI insights: {e}")
        return "Error generating insights"


# ========== GENERATE REPORT ==========
def generate_report_markdown(devices, stats, ai_insights, target):
    """Generate beautiful markdown report"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"""#  Automap Network Report

**Target:** {target}  
**Scan Time:** {timestamp}  
**Scan Mode:** Aggressive (-A -T4)

---

# Network Summary

- Total Hosts: {stats['total_hosts']}
- Total Open Ports: {stats['total_ports']}

### Top Exposed Ports
"""
    
    for port, count in stats['top_ports']:
        report += f"- {port} (found on {count} devices)\n"
    
    report += f"""
---

# Key Highlights

- SSH exposed: {stats['ssh_count']} devices
- HTTP exposed: {stats['http_count']} devices
- HTTPS exposed: {stats['https_count']} devices
- Multi-port devices: {len(stats['multi_port_devices'])}

---

#  Device Inventory

"""
    
    for device in devices:
        report += f"""### {device['ip']}
- Hostname: {device['hostname']}
- MAC: {device['mac']}
- Vendor: {device['vendor']}
- OS: {device['os']}

#### Open Ports
"""
        for port, service in zip(device['ports'], device['services']):
            report += f"- {port}/tcp → {service}\n"
        
        report += "\n"
    
    report += f"""---

# AI Insights

{ai_insights}

---

# Report Info

Generated by Automap  
Saved at: reports/report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md
"""
    
    return report


# ========== SAVE REPORT AS PDF ==========
def save_report(devices, stats, ai_insights, target):
    """Generate and save PROFESSIONAL PDF report"""
    os.makedirs('reports', exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reports/report_{timestamp}.pdf"
    
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_margins(10, 10, 10)
        
        # ===== HEADER =====
        pdf.set_font("Arial", "B", 20)
        pdf.cell(0, 10, "AUTOMAP NETWORK REPORT", 0, 1, "C")
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 8, f"Security Scan Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1, "C")
        pdf.ln(3)
        
        # Target info
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 8, f"Target Network: {target}", 0, 1)
        pdf.ln(5)
        
        # ===== SUMMARY SECTION =====
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 10, "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", 0, 1)
        pdf.cell(0, 10, "📊 NETWORK SUMMARY", 0, 1)
        pdf.cell(0, 10, "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", 0, 1)
        pdf.ln(2)
        
        # Compact summary line
        pdf.set_font("Arial", "", 10)
        summary_text = f"Hosts: {stats['total_hosts']}  |  Ports: {stats['total_ports']}  |  SSH: {stats['ssh_count']}  |  HTTP: {stats['http_count']}  |  HTTPS: {stats['https_count']}"
        pdf.cell(0, 8, summary_text, 0, 1)
        pdf.ln(3)
        
        # Top ports
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 8, "Top Exposed Ports:", 0, 1)
        pdf.set_font("Arial", "", 9)
        for port, count in stats['top_ports']:
            pdf.cell(0, 6, f"  🔌 Port {port} — Found on {count} device(s)", 0, 1)
        pdf.ln(4)
        
        # ===== HIGHLIGHTS SECTION =====
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 10, "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", 0, 1)
        pdf.cell(0, 10, "⚠️  KEY HIGHLIGHTS", 0, 1)
        pdf.cell(0, 10, "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", 0, 1)
        pdf.ln(2)
        
        pdf.set_font("Arial", "", 9)
        if stats['ssh_count'] > 0:
            pdf.cell(0, 6, f"  ⚠️  SSH exposed on {stats['ssh_count']} device(s) — Review access control", 0, 1)
        if stats['http_count'] > 0:
            pdf.cell(0, 6, f"  🌐 HTTP service on {stats['http_count']} device(s) — Ensure HTTPS enforced", 0, 1)
        if len(stats['multi_port_devices']) > 0:
            pdf.cell(0, 6, f"  🖥  {len(stats['multi_port_devices'])} device(s) with 5+ open ports — High exposure", 0, 1)
        pdf.ln(4)
        
        # ===== DEVICE INVENTORY =====
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 10, "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", 0, 1)
        pdf.cell(0, 10, "🖥  DEVICE INVENTORY", 0, 1)
        pdf.cell(0, 10, "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", 0, 1)
        pdf.ln(3)
        
        for device in devices:
            # Device header
            pdf.set_font("Arial", "B", 10)
            device_name = device['hostname'] if device['hostname'] != 'N/A' else device['ip']
            pdf.cell(0, 8, f"[{device['ip']}]  ({device_name})", 0, 1)
            
            # Device details
            pdf.set_font("Arial", "", 9)
            pdf.cell(0, 6, f"  OS: {device['os']}", 0, 1)
            pdf.cell(0, 6, f"  MAC: {device['mac']} ({device['vendor']})", 0, 1)
            
            # Ports with symbols
            ports_str = ", ".join(map(str, device['ports']))
            pdf.cell(0, 6, f"  Ports: {ports_str}", 0, 1)
            pdf.ln(2)
        
        # ===== AI INSIGHTS =====
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 10, "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", 0, 1)
        pdf.cell(0, 10, "🧠 AI SECURITY INSIGHTS", 0, 1)
        pdf.cell(0, 10, "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", 0, 1)
        pdf.ln(2)
        
        pdf.set_font("Arial", "", 9)
        # Convert insights to bullet points
        insights_lines = ai_insights.split('\n')
        for line in insights_lines[:10]:  # First 10 lines
            if line.strip():
                pdf.multi_cell(0, 5, f"• {line.strip()}")
        
        pdf.ln(3)
        
        # ===== FOOTER =====
        pdf.set_font("Arial", "I", 8)
        pdf.cell(0, 8, "Generated by Automap — Network Security Scanner", 0, 1, "C")
        pdf.cell(0, 8, f"Report saved: {filename}", 0, 1, "C")
        
        pdf.output(filename)
        print(f"📄 Professional report saved: {filename}")
        return filename
    
    except Exception as e:
        print(f"❌ Error saving PDF: {e}")
        return None
