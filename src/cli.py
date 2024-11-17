import click
import asyncio
from enum import Enum
from typing import Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from datetime import datetime
import uuid
import os
from src.chains.requirements_chain import create_requirements_chain, ModelProvider
from src.chains.code_generation_chain import create_code_generation_chain
from src.utils.file_utils import process_code_structure
from src.config.settings import settings

console = Console()

class ProcessingMode(str, Enum):
    REQUIREMENTS = "requirements"
    CODE = "code"
    FULL = "full"

class CodeGenerator:
    def __init__(self, model_provider: ModelProvider = ModelProvider.OPENAI):
        self.requirements_chain = create_requirements_chain(model_provider)
        self.code_gen_chain = create_code_generation_chain(model_provider)
        self.project_dir = None

    def create_project_directory(self) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        project_name = f"project_{timestamp}_{unique_id}"
        
        project_dir = os.path.join(settings.project_output_dir, project_name)
        os.makedirs(project_dir, exist_ok=True)
        
        docs_dir = os.path.join(project_dir, "docs")
        os.makedirs(docs_dir, exist_ok=True)
        
        return project_dir

    async def process_input(self, user_input: str, mode: ProcessingMode):
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                # Create project directory for full mode
                if mode == ProcessingMode.FULL:
                    self.project_dir = self.create_project_directory()
                    progress.add_task("Created project directory", total=None)

                # Generate Functional Requirements
                task = progress.add_task("Generating functional requirements...", total=None)
                functional_chain = self.requirements_chain.chains[0]
                func_result = functional_chain.run(user_input=user_input)
                progress.update(task, completed=True)
                console.print("\n[green]✓[/green] Functional Requirements Generated")
                console.print(func_result)

                # Generate Technical Requirements
                task = progress.add_task("Generating technical requirements...", total=None)
                technical_chain = self.requirements_chain.chains[1]
                tech_result = technical_chain.run(functional_requirements=func_result)
                progress.update(task, completed=True)
                console.print("\n[green]✓[/green] Technical Requirements Generated")
                console.print(tech_result)

                if mode in [ProcessingMode.CODE, ProcessingMode.FULL]:
                    # Generate Code for each phase
                    phases = ["Phase 1", "Phase 2", "Phase 3"]
                    
                    for phase in phases:
                        task = progress.add_task(f"Generating code for {phase}...", total=None)
                        code_result = self.code_gen_chain.invoke({
                            "functional_requirements": func_result,
                            "technical_requirements": tech_result,
                            "phase": phase
                        })
                        progress.update(task, completed=True)
                        console.print(f"\n[green]✓[/green] {phase} Code Generated")
                        
                        if mode == ProcessingMode.FULL:
                            task = progress.add_task(f"Processing {phase} code files...", total=None)
                            process_code_structure(code_result["code_structure"], base_path=self.project_dir)
                            progress.update(task, completed=True)

                if mode == ProcessingMode.FULL:
                    console.print(f"\n[green]✓[/green] Project created at: {self.project_dir}")

        except Exception as e:
            console.print(f"\n[red]Error:[/red] {str(e)}")
            raise

@click.command()
@click.argument('user_input', type=str)
@click.option('--mode', 
    type=click.Choice(['requirements', 'code', 'full']), 
    default='requirements',
    help='Processing mode: requirements, code, or full project generation'
)
@click.option('--model', 
    type=click.Choice(['openai', 'anthropic']), 
    default='openai',
    help='Choose the AI model provider'
)
def main(user_input: str, mode: str, model: str):
    """Generate code from natural language description."""
    model_provider = ModelProvider.OPENAI if model == 'openai' else ModelProvider.ANTHROPIC
    processing_mode = ProcessingMode(mode)
    
    console.print(f"[bold blue]Starting AI Code Generator[/bold blue]")
    console.print(f"Mode: {mode}")
    console.print(f"Model: {model}\n")

    generator = CodeGenerator(model_provider)
    asyncio.run(generator.process_input(user_input, processing_mode))

if __name__ == '__main__':
    main() 