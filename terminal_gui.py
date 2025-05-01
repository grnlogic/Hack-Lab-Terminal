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
    
    def show_menu(self):
        """Display the main menu"""
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("#", style="dim", width=3)
        table.add_column("Action", min_width=20)
        table.add_column("Description", min_width=40)
        
        table.add_row("1", "[green]Start Server[/]", "Start the vulnerable Flask application")
        table.add_row("2", "[red]Stop Server[/]", "Stop the Flask application")
        table.add_row("3", "[blue]SQL Injection[/]", "Run SQL Injection test tool")
        table.add_row("4", "[magenta]XSS Test[/]", "Run Cross-Site Scripting test tool")
        table.add_row("5", "[yellow]Upload Bypass[/]", "Run File Upload Bypass test tool")
        table.add_row("6", "[cyan]View Server Status[/]", "Check if the server is running")
        table.add_row("0", "[bold red]Exit[/]", "Exit the program")
        
        console.print(Panel(table, title="[bold]Hack-Lab Terminal[/]", 
                           subtitle="A Penetration Testing Framework"))
    
    def run(self):
        """Main application loop"""
        console.clear()
        console.print("[bold green]Welcome to Hack-Lab Terminal![/]", justify="center")
        
        while True:
            self.show_menu()
            
            choice = Prompt.ask("Enter your choice", choices=["0", "1", "2", "3", "4", "5", "6"], default="1")
            
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
                status = "Running" if self.server_running else "Stopped"
                color = "green" if self.server_running else "red"
                console.print(f"Server status: [{color}]{status}[/]")
            
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
