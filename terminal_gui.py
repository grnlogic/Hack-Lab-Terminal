import os
import subprocess
import sys
import threading
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.live import Live
from rich.progress import Progress
from rich.prompt import Confirm
from concurrent.futures import ThreadPoolExecutor
import importlib

console = Console()

class HackLabTerminal:
    def __init__(self):
        self.server_process = None
        self.server_running = False
        
    def start_server(self):
        """Start the Flask server in a separate thread"""
        if not self.server_running:
            console.print("[bold green]Starting Flask server...[/]")
            # Start server as a subprocess
            self.server_process = subprocess.Popen(
                [sys.executable, "app.py"], 
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.server_running = True
            
            # Start a thread to read and display server output
            threading.Thread(target=self._monitor_server_output, daemon=True).start()
            
            # Give the server time to start
            time.sleep(2)
            console.print("[bold green]✓[/] Server running at [link=http://localhost:5000]http://localhost:5000[/link]")
        else:
            console.print("[yellow]Server is already running[/]")
    
    def _monitor_server_output(self):
        """Monitor and print server output"""
        for line in iter(self.server_process.stderr.readline, b''):
            console.print(f"[dim]{line.decode().strip()}[/]")
    
    def stop_server(self):
        """Stop the Flask server"""
        if self.server_running and self.server_process:
            console.print("[bold red]Stopping server...[/]")
            self.server_process.terminate()
            self.server_process = None
            self.server_running = False
            console.print("[bold red]✓[/] Server stopped")
        else:
            console.print("[yellow]No server is running[/]")
    
    def run_sqli_tool(self):
        """Run the SQL Injection tool"""
        console.print("[bold blue]Running SQL Injection Tool...[/]")
        result = subprocess.run([sys.executable, "tool_sqli.py"], capture_output=True, text=True)
        console.print(Panel(result.stdout, title="SQL Injection Results", border_style="blue"))
    
    def run_xss_tool(self):
        """Run the XSS tool"""
        console.print("[bold magenta]Running XSS Tool...[/]")
        result = subprocess.run([sys.executable, "tool_xss.py"], capture_output=True, text=True)
        console.print(Panel(result.stdout, title="XSS Test Results", border_style="magenta"))
    
    def run_upload_tool(self):
        """Run the Upload Bypass tool"""
        console.print("[bold yellow]Running Upload Bypass Tool...[/]")
        result = subprocess.run([sys.executable, "tool_upload.py"], capture_output=True, text=True)
        console.print(Panel(result.stdout, title="Upload Bypass Results", border_style="yellow"))
    
    def run_command_tool(self):
        """Run the Command Injection tool"""
        console.print("[bold cyan]Running Command Injection Tool...[/]")
        result = subprocess.run([sys.executable, "tool_command.py"], capture_output=True, text=True)
        console.print(Panel(result.stdout, title="Command Injection Results", border_style="cyan"))

    def run_traversal_tool(self):
        """Run the Path Traversal tool"""
        console.print("[bold green]Running Path Traversal Tool...[/]")
        result = subprocess.run([sys.executable, "tool_traversal.py"], capture_output=True, text=True)
        console.print(Panel(result.stdout, title="Path Traversal Results", border_style="green"))

    def run_csrf_tool(self):
        """Run the CSRF tool"""
        console.print("[bold purple]Running CSRF Tool...[/]")
        result = subprocess.run([sys.executable, "tool_csrf.py"], capture_output=True, text=True)
        console.print(Panel(result.stdout, title="CSRF Attack Results", border_style="purple"))

    def run_password_tool(self):
        """Run the Password Strength Testing tool with mountain theme"""
        console.clear()
        console.print("[bold yellow]      /\\        /\\        /\\      [/]")
        console.print("[bold yellow]     /  \\      /  \\      /  \\     [/]")
        console.print("[bold orange3]    /    \\    /    \\    /    \\    [/]")
        console.print("[bold orange3]   /      \\  /      \\  /      \\   [/]")
        console.print("[bold orange3] /        \\/        \\/        \\  [/]")
        console.print("[bold white]╭──────────── PASSWORD STRENGTH FORTRESS ────────────╮[/]")
        console.print()
        
        # Get input type
        console.print("[bold]Choose your path:[/]")
        console.print("  [yellow]⛰️  1.[/] Test a single password (Interactive)")
        console.print("  [orange3]⛰️  2.[/] Test multiple passwords from a file")
        
        choice = Prompt.ask("[bold]Select your journey[/]", choices=["1", "2"], default="1")
        
        if choice == "1":
            console.print("\n[bold yellow]🔒 Testing a single password - The direct climb[/]")
            # For single password testing, run in interactive mode
            result = subprocess.run([sys.executable, "tool_password.py"], text=True)
        else:
            # For file testing, ask for file path
            console.print("\n[bold orange3]🔒 Testing multiple passwords - The mountain range[/]")
            password_file = Prompt.ask("[bold]Enter path to password file[/]")
            console.print(f"[bold]Testing passwords from {password_file}[/]")
            result = subprocess.run(
                [sys.executable, "tool_password.py", password_file], 
                capture_output=True, 
                text=True
            )
            # Display results with mountain-themed formatting
            output_lines = result.stdout.splitlines()
            console.print("\n[bold orange3]🏔️  PASSWORD STRENGTH RESULTS  🏔️[/]")
            console.print("[bold yellow]    ⛰️     ⛰️     ⛰️     ⛰️     ⛰️     ⛰️    [/]")
            
            for line in output_lines:
                if "Password Score:" in line:
                    score = line.split(":")[1].strip()
                    if score.startswith("0") or score.startswith("1"):
                        console.print(f"  ⚠️  [red]{line}[/] - Weak! Like a crumbling hill")
                    elif score.startswith("2") or score.startswith("3"):
                        console.print(f"  ⚠️  [yellow]{line}[/] - Moderate, like a small mountain")
                    else:
                        console.print(f"  ✅  [green]{line}[/] - Strong! A mighty peak")
                else:
                    console.print(f"      {line}")
            
            console.print("[bold yellow]    ⛰️     ⛰️     ⛰️     ⛰️     ⛰️     ⛰️    [/]")

    def run_recon_tool(self):
        """Run the Reconnaissance tool"""
        console.print("[bold green]Running Reconnaissance Tool...[/]")
        
        # Get target domain
        domain = Prompt.ask("[bold]Enter domain to scan[/]", default="example.com")
        
        # Show options
        options = Table()
        options.add_column("Option")
        options.add_column("Value")
        
        recon = importlib.import_module('tool_recon').ReconFramework()
        
        for key, value in recon.options.items():
            options.add_row(key, str(value))
        
        console.print(Panel(options, title="Recon Options"))
        
        # Confirm
        if Confirm.ask("[bold]Start reconnaissance scan?[/]"):
            with Progress() as progress:
                task = progress.add_task("[green]Running reconnaissance...", total=100)
                
                # Run in a separate thread to keep the UI responsive
                def run_scan():
                    try:
                        return recon.recon_domain(domain)
                    except Exception as e:
                        return {"error": str(e)}
                
                with ThreadPoolExecutor() as executor:
                    future = executor.submit(run_scan)
                    
                    # Show progress while waiting
                    while not future.done():
                        progress.update(task, advance=0.5)
                        time.sleep(0.1)
                    
                    # Get results
                    results = future.result()
                    progress.update(task, completed=100)
                
                if "error" in results:
                    console.print(f"[bold red]Error during scan:[/] {results['error']}")
                else:
                    # Display results
                    console.print(Panel(f"[bold]Domain:[/] {results['domain']}\n[bold]IP:[/] {results['ip']}", 
                                       title="Basic Information"))
                    
                    # Show discovered URLs
                    if results.get('urls'):
                        urls_table = Table(show_header=True)
                        urls_table.add_column("URL")
                        for url in results['urls'][:10]:  # Show first 10
                            urls_table.add_row(url)
                        
                        if len(results['urls']) > 10:
                            urls_table.add_row(f"... and {len(results['urls']) - 10} more")
                        
                        console.print(Panel(urls_table, title=f"Discovered URLs ({len(results['urls'])} total)"))
                    
                    # Show open ports
                    ports = recon.get_ports()
                    if ports:
                        ports_table = Table(show_header=True)
                        ports_table.add_column("Host")
                        ports_table.add_column("Port")
                        ports_table.add_column("Service")
                        
                        for port_info in ports:
                            ports_table.add_row(port_info[0], str(port_info[1]), port_info[3] or "")
                        
                        console.print(Panel(ports_table, title="Open Ports"))
                    
                    console.print("[green]Reconnaissance completed![/]")

    def run_osint_tool(self):
        """Run the OSINT tool with more visually interesting UI"""
        console.clear()
        # Mountain range header
        console.print("[bold blue]      /\\        /\\        /\\      [/]")
        console.print("[bold cyan]     /  \\      /  \\      /  \\     [/]")
        console.print("[bold green]    /    \\    /    \\    /    \\    [/]")
        console.print("[bold yellow]   /      \\  /      \\  /      \\   [/]")
        console.print("[bold magenta] /        \\/        \\/        \\  [/]")
        console.print("[bold white]╭──────────── OSINT INTELLIGENCE GATHERING ────────────╮[/]")
        console.print()
        console.print("[dim]This tool gathers public information about a domain including WHOIS data,[/]")
        console.print("[dim]DNS records, open ports, and web content.[/]")
        
        # Try to import the OSINT module with error handling
        try:
            osint_module = importlib.import_module('tool_osint')
        except ImportError as e:
            missing_module = str(e).split("'")[1] if "'" in str(e) else str(e)
            console.print(f"[bold red]⚠ Error:[/] Missing module: {missing_module}")
            if missing_module == 'dns':
                console.print("[yellow]Please install required packages:[/] pip install dnspython python-whois beautifulsoup4")
            elif missing_module == 'whois':
                console.print("[yellow]Please install required package:[/] pip install python-whois")
            elif missing_module == 'bs4':
                console.print("[yellow]Please install required package:[/] pip install beautifulsoup4")
            else:
                console.print("[yellow]Please install all requirements:[/] pip install -r requirements.txt")
            return
        
        # Step 1: Get target domain
        console.print("\n[bold cyan]⛰️  STEP 1:[/] [bold]Enter the domain you want to analyze[/]")
        console.print("[dim]Example: google.com, microsoft.com, or any domain you want to gather information about.[/]")
        domain = Prompt.ask("[bold]Enter domain[/]", default="example.com")
        
        try:
            # Step 2: Initialize OSINT framework
            console.print("\n[bold cyan]⛰️  STEP 2:[/] [bold]Initializing OSINT framework...[/]")
            osint = osint_module.OSINTFramework()
            
            # Display the current configuration with mountain-like border
            console.print("\n[bold]Current Configuration:[/]")
            console.print("[bold cyan]   ▲    ▲    ▲    ▲    ▲    ▲    ▲    ▲  [/]")
            for key, value in osint.options.items():
                console.print(f"  [cyan]⛰[/]  [bold]{key}:[/] [green]{value}[/]")
            console.print("[bold cyan]   ▼    ▼    ▼    ▼    ▼    ▼    ▼    ▼  [/]")
            console.print("[dim]These are the default settings that will be used for the analysis.[/]")
            
            # Step 3: Confirm and start analysis
            console.print("\n[bold cyan]⛰️  STEP 3:[/] [bold]Ready to begin analysis[/]")
            console.print(f"[dim]The tool will now gather intelligence about [bold]{domain}[/bold] if you proceed.[/dim]")
            
            if Confirm.ask("[bold]Start OSINT analysis now?[/]"):
                console.print("\n[bold green]⚡ Analysis started! This may take a few minutes...[/]")
                
                with Progress() as progress:
                    task = progress.add_task("[green]Gathering intelligence...", total=100)
                    
                    # Run in a separate thread to keep the UI responsive
                    def run_scan():
                        try:
                            return osint.analyze_domain(domain)
                        except Exception as e:
                            return {"error": str(e)}
                    
                    with ThreadPoolExecutor() as executor:
                        future = executor.submit(run_scan)
                        
                        # Show progress with mountain climbing theme
                        messages = [
                            "Starting the climb...",
                            "Ascending to base camp (WHOIS)...",
                            "Climbing higher (DNS)...",
                            "Traversing ridge (Ports)...",
                            "Reaching the summit (Web Content)...",
                            "Surveying the landscape..."
                        ]
                        msg_index = 0
                        
                        while not future.done():
                            # Update progress message periodically
                            if msg_index < len(messages) and progress.tasks[0].completed > (msg_index * 16):
                                progress.update(task, description=f"[green]⛰️ {messages[msg_index]}")
                                msg_index += 1
                            
                            progress.update(task, advance=0.5)
                            time.sleep(0.1)
                        
                        # Get results
                        results = future.result()
                        progress.update(task, completed=100, description="[bold green]🏔️ Summit reached! Analysis complete!")
                
                # Display results with mountain-themed formatting
                console.print("\n[bold cyan]🏔️  INTELLIGENCE SUMMIT  🏔️[/]")
                
                if "error" in results:
                    console.print(f"[bold red]❌ Error during analysis:[/] {results['error']}")
                else:
                    # Domain info as a mountain peak
                    console.print("\n[bold white]            ▲            [/]")
                    console.print("[bold white]           /|\\           [/]")
                    console.print("[bold white]          / | \\          [/]")
                    console.print("[bold cyan]         /  |  \\         [/]")
                    console.print(f"[bold cyan]      🏔️ {results['domain']} 🏔️      [/]")
                    console.print(f"[bold green]      IP: {results['ip'] or 'Not resolved'}      [/]")
                    
                    # Show discovered URLs
                    if results.get('urls'):
                        console.print("\n[bold cyan]🌲 Website Content (Forest of URLs):[/]")
                        console.print("[bold green]    ⛰️     ⛰️     ⛰️     ⛰️     ⛰️     ⛰️    [/]")
                        
                        for i, url in enumerate(results['urls'][:8]):  # Show first 8
                            tree = "🌲" if i % 2 == 0 else "🌳"
                            console.print(f"  {tree}  [green]{url}[/]")
                        
                        if len(results['urls']) > 8:
                            console.print(f"  🌲  [dim]... and {len(results['urls']) - 8} more URLs found[/]")
                        
                        console.print("[bold green]    ⛰️     ⛰️     ⛰️     ⛰️     ⛰️     ⛰️    [/]")
                    
                    # Show open ports as mountain caves
                    ports = osint.get_ports()
                    if ports:
                        console.print("\n[bold red]🔌 Network Access Points (Mountain Caves):[/]")
                        console.print("[bold red]    🏔️     🏔️     🏔️     🏔️     🏔️     🏔️    [/]")
                        
                        for port_info in ports:
                            console.print(f"  🚪  [red]Port {port_info[1]}[/] ([cyan]{port_info[3] or 'unknown'}[/]) on [dim]{port_info[0]}[/]")
                        
                        console.print("[bold red]    🏔️     🏔️     🏔️     🏔️     🏔️     🏔️    [/]")
                    
                    console.print("\n[bold green]✅ OSINT expedition completed successfully![/]")
                    console.print("[dim]The gathered intelligence has been mapped and saved to the database.[/]")
            else:
                console.print("[yellow]Expedition cancelled. The mountains will wait for another day.[/]")
                
        except Exception as e:
            console.print(f"[bold red]❌ Error occurred:[/] {str(e)}")
            console.print("[yellow]Please ensure all climbing gear (dependencies) is installed with:[/] pip install -r requirements.txt")

    def show_menu(self):
        """Display the main menu with a mountain-like interface"""
        # Mountain-like header
        console.print("\n[bold cyan]    /\\      /\\      /\\      /\\      /\\      /\\[/]")
        console.print("[bold blue]   /  \\    /  \\    /  \\    /  \\    /  \\    /  \\[/]")
        console.print("[bold green]  /    \\__/    \\__/    \\__/    \\__/    \\__/    \\[/]")
        console.print("[bold magenta]╭─────────────────────── HACK-LAB TERMINAL ───────────────────────╮[/]")
        console.print("[dim cyan]        Penetration Testing & Security Analysis Tools[/]")
        console.print()
        
        # Create gradient menu items instead of a table
        menu_items = [
            ("1", "[green]Start Server[/]", "Start the vulnerable Flask application"),
            ("2", "[red]Stop Server[/]", "Stop the Flask application"),
            ("3", "[blue]SQL Injection[/]", "Run SQL Injection test tool"),
            ("4", "[magenta]XSS Test[/]", "Run Cross-Site Scripting test tool"),
            ("5", "[yellow]Upload Bypass[/]", "Run File Upload Bypass test tool"),
            ("6", "[cyan]Command Injection[/]", "Run Command Injection test tool"),
            ("7", "[green]Path Traversal[/]", "Run Path Traversal test tool"),
            ("8", "[purple]CSRF Attack[/]", "Run Cross-Site Request Forgery test tool"),
            ("9", "[orange3]Password Strength[/]", "Test password strength against cracking attempts"),
            ("10", "[green]OSINT[/]", "Run Open Source Intelligence tools"),
            ("0", "[bold red]Exit[/]", "Exit the program")
        ]
        
        # Display menu items with decorative elements
        for num, action, desc in menu_items:
            left_decor = "  ▲  " if num in ["3", "6", "9"] else "  ◆  " if num in ["1", "4", "7", "10"] else "  ■  "
            console.print(f"{left_decor}[bold white]{num}.[/] {action} [dim]- {desc}[/]")
        
        # Mountain-like footer
        console.print()
        console.print("[bold green]  /\\    /\\    /\\    /\\    /\\    /\\    /\\    /\\    /\\  [/]")
        console.print("[bold blue] /  \\__/  \\__/  \\__/  \\__/  \\__/  \\__/  \\__/  \\__/  \\ [/]")
        console.print("[bold magenta]╰────────────────────────────────────────────────────────────────╯[/]")
        
        # Watermark
        console.print("[dim]Made with [red]❤[/] by [bold cyan]grnlogic[/][/]", justify="right")
    
    def run(self):
        """Main application loop"""
        console.clear()
        
        # Show a startup watermark with ASCII art
        console.print("[bold green]Welcome to Hack-Lab Terminal![/]", justify="center")
        console.print("""
[bold cyan]       /\\          __  __                       __        __   [/]
[bold cyan]      /  \\        / / / /____ _ _____ ____    / /   ____ _/ /__ [/]
[bold blue]     /    \\      / /_/ // __ `// ___// __ \\  / /   / __ `/ //_/ [/]
[bold blue]    /      \\    / __  // /_/ // /__ / /_/ / / /___/ /_/ // ,<   [/]
[bold green]   /   /\\   \\  /_/ /_/ \\__,_/ \\___/ \\____//_____/ \\__,_//_/|_| [/]
[bold green]  /   /  \\   \\                                               [/]
[bold yellow] /___/    \\___\\                                              [/]
        """, justify="center")
        
        # Add watermark
        console.print("[dim italic]Made with [red]❤[/] by [bold cyan]grnlogic[/][/]", justify="center")
        console.print()
        console.print("[dim]Press Enter to continue...[/]", end="")
        input()
        console.clear()
        
        while True:
            self.show_menu()
            
            choice = Prompt.ask("Enter your choice", choices=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], default="1")
            
            if choice == "0":
                if self.server_running:
                    self.stop_server()
                console.print("[bold]Thank you for using Hack-Lab Terminal![/]", justify="center")
                break
            elif choice == "1":
                self.start_server()
            elif choice == "2":
                self.stop_server()
            elif choice == "3":
                self.run_sqli_tool()
            elif choice == "4":
                self.run_xss_tool()
            elif choice == "5":
                self.run_upload_tool()
            elif choice == "6":
                self.run_command_tool()
            elif choice == "7":
                self.run_traversal_tool()
            elif choice == "8":
                self.run_csrf_tool()
            elif choice == "9":
                self.run_password_tool()
            elif choice == "10":
                self.run_osint_tool()
            
            console.print("\nPress Enter to continue...", end="")
            input()
            console.clear()

if __name__ == "__main__":
    # Check if rich is installed
    try:
        import rich
    except ImportError:
        print("This program requires the 'rich' library.")
        print("Please install it using: pip install rich")
        sys.exit(1)
        
    terminal = HackLabTerminal()
    terminal.run()
