#!/usr/bin/env python3

import os
import re
import json
import time
import sqlite3
import requests
from urllib.parse import urlparse
import socket
import sys

# Check for required packages
required_packages = {
    'dns': 'dnspython',
    'whois': 'python-whois',
    'bs4': 'beautifulsoup4'
}

for module, package in required_packages.items():
    try:
        __import__(module)
    except ImportError:
        print(f"Missing required package: {package}")
        print(f"Please install it using: pip install {package}")
        print("Or install all dependencies with: pip install -r requirements.txt")
        sys.exit(1)

# Only import after checking
import dns.resolver
import whois
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

class OSINTFramework:
    def __init__(self, workspace='default'):
        self.workspace_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'workspaces', workspace)
        os.makedirs(self.workspace_dir, exist_ok=True)
        self.db_path = os.path.join(self.workspace_dir, 'data.db')
        self.init_db()
        self.options = {
            'USER_AGENT': 'Hack-Lab OSINT Tool',
            'TIMEOUT': 10,
            'THREADS': 5,
            'TARGET': '',
            'DEPTH': 2,
        }
        
    def init_db(self):
        """Initialize the database with necessary tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS domains (
            domain TEXT PRIMARY KEY,
            registrar TEXT,
            creation_date TEXT,
            expiration_date TEXT,
            last_updated TEXT,
            notes TEXT
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS hosts (
            host TEXT PRIMARY KEY,
            ip_address TEXT,
            country TEXT,
            city TEXT,
            org TEXT,
            notes TEXT
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ports (
            host TEXT,
            port INTEGER,
            protocol TEXT,
            service TEXT,
            banner TEXT,
            notes TEXT,
            PRIMARY KEY (host, port, protocol)
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            url TEXT PRIMARY KEY,
            title TEXT,
            status_code INTEGER,
            content_type TEXT,
            notes TEXT
        )
        ''')
        
        conn.commit()
        conn.close()
        
    def insert_domain(self, domain, registrar=None, creation_date=None, expiration_date=None, last_updated=None, notes=None):
        """Insert domain record into database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT OR REPLACE INTO domains 
        (domain, registrar, creation_date, expiration_date, last_updated, notes) 
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (domain, registrar, creation_date, expiration_date, last_updated, notes))
        
        conn.commit()
        conn.close()
        
    def insert_host(self, host, ip_address=None, country=None, city=None, org=None, notes=None):
        """Insert host record into database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT OR REPLACE INTO hosts 
        (host, ip_address, country, city, org, notes) 
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (host, ip_address, country, city, org, notes))
        
        conn.commit()
        conn.close()
        
    def insert_port(self, host, port, protocol=None, service=None, banner=None, notes=None):
        """Insert port record into database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT OR REPLACE INTO ports 
        (host, port, protocol, service, banner, notes) 
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (host, port, protocol, service, banner, notes))
        
        conn.commit()
        conn.close()
        
    def insert_url(self, url, title=None, status_code=None, content_type=None, notes=None):
        """Insert URL record into database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT OR REPLACE INTO urls 
        (url, title, status_code, content_type, notes) 
        VALUES (?, ?, ?, ?, ?)
        ''', (url, title, status_code, content_type, notes))
        
        conn.commit()
        conn.close()
    
    def query(self, sql, params=()):
        """Run a query against the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(sql, params)
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_domains(self):
        """Retrieve all domains"""
        return self.query("SELECT * FROM domains")
    
    def get_hosts(self):
        """Retrieve all hosts"""
        return self.query("SELECT * FROM hosts")
    
    def get_ports(self):
        """Retrieve all ports"""
        return self.query("SELECT * FROM ports")
    
    def get_urls(self):
        """Retrieve all URLs"""
        return self.query("SELECT * FROM urls")
    
    def dns_lookup(self, domain):
        """Perform DNS lookup for a domain"""
        print(f"[*] Performing DNS lookup for {domain}")
        try:
            ip_address = socket.gethostbyname(domain)
            self.insert_host(domain, ip_address=ip_address)
            print(f"[+] Found IP: {ip_address} for {domain}")
            return ip_address
        except socket.gaierror:
            print(f"[-] Could not resolve {domain}")
            return None
    
    def whois_lookup(self, domain):
        """Perform WHOIS lookup for a domain"""
        print(f"[*] Performing WHOIS lookup for {domain}")
        try:
            whois_data = whois.whois(domain)
            
            # Extract relevant information
            registrar = whois_data.registrar if hasattr(whois_data, 'registrar') else None
            creation_date = str(whois_data.creation_date) if hasattr(whois_data, 'creation_date') else None
            expiration_date = str(whois_data.expiration_date) if hasattr(whois_data, 'expiration_date') else None
            last_updated = str(whois_data.updated_date) if hasattr(whois_data, 'updated_date') else None
            
            # Store information in database
            self.insert_domain(domain, registrar, creation_date, expiration_date, last_updated)
            
            print(f"[+] WHOIS information gathered for {domain}")
            return whois_data
        except Exception as e:
            print(f"[-] WHOIS lookup failed for {domain}: {str(e)}")
            return None
    
    def scan_url(self, url):
        """Scan a URL and gather information"""
        print(f"[*] Scanning URL: {url}")
        try:
            headers = {'User-Agent': self.options['USER_AGENT']}
            response = requests.get(url, headers=headers, timeout=self.options['TIMEOUT'])
            
            status_code = response.status_code
            content_type = response.headers.get('Content-Type', '').split(';')[0]
            
            # Parse title if HTML
            title = None
            if 'text/html' in content_type:
                soup = BeautifulSoup(response.text, 'html.parser')
                title_tag = soup.find('title')
                if title_tag:
                    title = title_tag.text.strip()
            
            # Store information in database
            self.insert_url(url, title, status_code, content_type)
            
            print(f"[+] URL scanned: {url} (Status: {status_code})")
            
            # Extract links for crawling if HTML
            links = []
            if 'text/html' in content_type:
                soup = BeautifulSoup(response.text, 'html.parser')
                for a_tag in soup.find_all('a', href=True):
                    href = a_tag['href']
                    # Convert relative URLs to absolute
                    if href.startswith('/'):
                        parsed_url = urlparse(url)
                        href = f"{parsed_url.scheme}://{parsed_url.netloc}{href}"
                    links.append(href)
            
            return {
                'url': url,
                'status_code': status_code,
                'content_type': content_type,
                'title': title,
                'links': links
            }
        except requests.RequestException as e:
            print(f"[-] Failed to scan URL {url}: {str(e)}")
            return None
    
    def port_scan(self, host, ports=None):
        """Scan common ports on a host"""
        if ports is None:
            ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 5432, 8080, 8443]
        
        print(f"[*] Scanning ports on {host}")
        results = []
        
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((host, port))
                if result == 0:
                    service = socket.getservbyport(port) if port < 1024 else 'unknown'
                    self.insert_port(host, port, 'tcp', service)
                    results.append(port)
                    print(f"[+] Port {port} ({service}) is open on {host}")
                sock.close()
            except:
                pass
        
        return results
    
    def crawl(self, starting_url, max_depth=1):
        """Crawl a website to discover URLs"""
        print(f"[*] Starting crawl from {starting_url} with max depth {max_depth}")
        
        visited = set()
        to_visit = [(starting_url, 0)]  # (url, depth)
        
        while to_visit:
            current_url, depth = to_visit.pop(0)
            
            if current_url in visited or depth > max_depth:
                continue
            
            visited.add(current_url)
            result = self.scan_url(current_url)
            
            if result and depth < max_depth:
                domain = urlparse(current_url).netloc
                for link in result.get('links', []):
                    try:
                        parsed = urlparse(link)
                        if parsed.netloc == domain or not parsed.netloc:
                            if link not in visited:
                                to_visit.append((link, depth + 1))
                    except:
                        pass
        
        print(f"[+] Crawl completed. Visited {len(visited)} URLs")
        return list(visited)
    
    def analyze_domain(self, domain):
        """Perform comprehensive intelligence gathering on a domain"""
        print(f"[*] Starting analysis for {domain}")
        
        # Normalize domain - handling all TLDs
        domain = domain.lower().strip()
        if domain.startswith(('http://', 'https://')):
            parsed = urlparse(domain)
            domain = parsed.netloc
        
        # Remove trailing slash and www if present
        domain = domain.rstrip('/')
        if domain.startswith('www.'):
            domain = domain[4:]
        
        # Set the target
        self.options['TARGET'] = domain
        
        # Run WHOIS lookup
        whois_data = self.whois_lookup(domain)
        
        # Run DNS lookup
        ip = self.dns_lookup(domain)
        
        # Run port scan if we have an IP
        open_ports = []
        if ip:
            open_ports = self.port_scan(ip)
        
        # Run web crawl - try HTTPS first, then HTTP
        urls = []
        starting_url = f"https://{domain}"
        try:
            response = requests.head(starting_url, timeout=self.options['TIMEOUT'])
            # If HTTPS works, use it
            if response.status_code < 400:  # Any successful or redirect status
                urls = self.crawl(starting_url, max_depth=int(self.options['DEPTH']))
            else:
                # Try HTTP instead
                starting_url = f"http://{domain}"
                urls = self.crawl(starting_url, max_depth=int(self.options['DEPTH']))
        except requests.RequestException:
            # Try HTTP if HTTPS fails
            try:
                starting_url = f"http://{domain}"
                urls = self.crawl(starting_url, max_depth=int(self.options['DEPTH']))
            except requests.RequestException as e:
                print(f"[-] Could not access website at {domain}: {str(e)}")
                urls = []
        
        print(f"[+] Analysis completed for {domain}")
        return {
            'domain': domain,
            'whois': whois_data,
            'ip': ip,
            'urls': urls
        }

def run_osint_scan(domain):
    """Function to run an OSINT scan from command line"""
    osint = OSINTFramework()
    results = osint.analyze_domain(domain)
    
    print("\n== SCAN RESULTS ==")
    print(f"Domain: {results['domain']}")
    print(f"IP Address: {results['ip']}")
    print(f"URLs Discovered: {len(results['urls'])}")
    
    # Show DB contents
    print("\n== DATABASE CONTENTS ==")
    print("\nDomains:")
    for domain in osint.get_domains():
        print(domain)
    
    print("\nHosts:")
    for host in osint.get_hosts():
        print(host)
    
    print("\nPorts:")
    for port in osint.get_ports():
        print(port)
    
    print("\nURLs:")
    for url in osint.get_urls()[:10]:  # Show first 10 URLs
        print(url)
    
    return osint

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python tool_osint.py <domain>")
        sys.exit(1)
    
    run_osint_scan(sys.argv[1])
