import os
import json
import subprocess
import logging
from typing import Dict, List
from rich.console import Console

console = Console()
logger = logging.getLogger(__name__)

def create_folder_structure(folders: List[str], base_path: str = ".") -> None:
    """Create the folder structure based on the provided list."""
    for folder in folders:
        folder_path = os.path.join(base_path, folder)
        try:
            os.makedirs(folder_path, exist_ok=True)
            console.print(f"[green]Created folder:[/green] {folder_path}")
        except Exception as e:
            console.print(f"[red]Error creating folder {folder_path}:[/red] {str(e)}")
            raise

def write_files(files: Dict[str, str], base_path: str = ".") -> None:
    """Write the provided files with their content."""
    for file_path, content in files.items():
        full_path = os.path.join(base_path, file_path)
        try:
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            console.print(f"[green]Created file:[/green] {full_path}")
            
        except Exception as e:
            console.print(f"[red]Error creating file {full_path}:[/red] {str(e)}")
            raise

def run_commands(commands: List[str], working_dir: str = ".") -> None:
    """Run the provided shell commands."""
    for command in commands:
        try:
            console.print(f"[yellow]Running command:[/yellow] {command}")
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                cwd=working_dir,
                text=True,
                capture_output=True
            )
            console.print(f"[green]Command completed successfully[/green]")
            
        except subprocess.CalledProcessError as e:
            console.print(f"[red]Error running command {command}[/red]")
            console.print(f"Error output: {e.stderr}")
            raise
        except Exception as e:
            console.print(f"[red]Unexpected error running command {command}:[/red] {str(e)}")
            raise

def clean_json_string(json_str: str) -> str:
    """Clean and format JSON string to ensure proper quotes and formatting."""
    try:
        # Try parsing as-is first
        try:
            json.loads(json_str)
            return json_str
        except json.JSONDecodeError:
            pass

        # Remove any leading/trailing whitespace
        json_str = json_str.strip()
        
        # Handle common formatting issues
        cleaned_lines = []
        in_string = False
        
        for line in json_str.split('\n'):
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('//'):
                continue
                
            if ':' in line and not in_string:
                key, value = line.split(':', 1)
                key = key.strip()
                if not (key.startswith('"') and key.endswith('"')):
                    key = f'"{key.strip()}"'
                cleaned_lines.append(f"{key}:{value}")
            else:
                cleaned_lines.append(line)
                
            quotes = line.count('"') - line.count('\\"')
            if quotes % 2 == 1:
                in_string = not in_string
        
        cleaned_json = '\n'.join(cleaned_lines)
        
        # Validate the cleaned JSON
        json.loads(cleaned_json)
        return cleaned_json
                
    except Exception as e:
        console.print(f"[red]Error cleaning JSON string:[/red] {str(e)}")
        raise

def process_code_structure(code_structure: str, base_path: str = ".") -> None:
    """Process the code structure JSON and create files/folders."""
    try:
        # Extract and parse JSON
        json_str = ""
        if "```json" in code_structure:
            start_idx = code_structure.find("```json") + 7
            end_idx = code_structure.find("```", start_idx)
            json_str = code_structure[start_idx:end_idx].strip()
        else:
            start_idx = code_structure.find("{")
            end_idx = code_structure.rfind("}") + 1
            if start_idx != -1 and end_idx != 0:
                json_str = code_structure[start_idx:end_idx]
        
        if not json_str:
            raise ValueError("No valid JSON structure found in the response")
            
        # Parse the JSON
        try:
            structure = json.loads(json_str)
        except json.JSONDecodeError:
            cleaned_json = clean_json_string(json_str)
            structure = json.loads(cleaned_json)
        
        # Process the structure
        commands = structure.get("commands", [])
        if commands:
            run_commands(commands, base_path)
        
        folders = structure.get("folders", [])
        if folders:
            create_folder_structure(folders, base_path)
        
        files = structure.get("files", {})
        if files:
            write_files(files, base_path)
        
    except Exception as e:
        console.print(f"[red]Error processing code structure:[/red] {str(e)}")
        raise 