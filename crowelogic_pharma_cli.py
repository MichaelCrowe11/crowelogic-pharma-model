#!/usr/bin/env python3
"""
CroweLogic-Pharma Production CLI
Advanced pharmaceutical AI with quantum computing integration
"""

import click
import sys
import os
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint
from rich.markdown import Markdown

console = Console()

# Version
VERSION = "3.0.0"
BANNER = f"""
╔══════════════════════════════════════════════════════════════════╗
║         CroweLogic-Pharma CLI v{VERSION}                             ║
║    AI-Powered Pharmaceutical Research + Quantum Computing        ║
╚══════════════════════════════════════════════════════════════════╝
"""


class Config:
    """Configuration management"""
    def __init__(self):
        self.config_file = Path.home() / '.crowelogic-pharma' / 'config.json'
        self.config_file.parent.mkdir(exist_ok=True)
        self.load()

    def load(self):
        if self.config_file.exists():
            with open(self.config_file) as f:
                self.data = json.load(f)
        else:
            self.data = {
                'default_model': 'CroweLogic-Pharma:mini',
                'ollama_host': 'http://localhost:11434',
                'output_format': 'rich',
                'azure_config': {}
            }
            self.save()

    def save(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save()


config = Config()


@click.group()
@click.version_option(version=VERSION)
@click.pass_context
def cli(ctx):
    """
    🔬 CroweLogic-Pharma CLI - AI-Powered Pharmaceutical Research

    Integrated platform for drug discovery with quantum computing.
    """
    ctx.ensure_object(dict)
    ctx.obj['config'] = config


# ============================================================================
# MODEL COMMANDS
# ============================================================================

@cli.group()
def model():
    """🤖 AI Model management (Ollama)"""
    pass


@model.command('chat')
@click.option('--model', '-m', default=None, help='Model to use')
@click.option('--query', '-q', help='Direct query (non-interactive)')
def model_chat(model, query):
    """Interactive chat with CroweLogic-Pharma AI"""
    model_name = model or config.get('default_model')

    console.print(Panel(f"[bold cyan]CroweLogic-Pharma AI Chat[/bold cyan]\nModel: {model_name}",
                       border_style="cyan"))

    if query:
        # Direct query mode
        import requests

        with console.status("[bold green]Querying model..."):
            try:
                response = requests.post(
                    f"{config.get('ollama_host')}/api/generate",
                    json={'model': model_name, 'prompt': query, 'stream': False}
                )
                result = response.json()
                console.print(f"\n[bold green]Response:[/bold green]\n{result['response']}\n")
            except Exception as e:
                console.print(f"[bold red]Error:[/bold red] {e}")
    else:
        # Interactive mode
        import subprocess
        subprocess.run(['ollama', 'run', model_name])


@model.command('list')
def model_list():
    """List available models"""
    import subprocess

    console.print("[bold cyan]Available Models:[/bold cyan]\n")
    result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
    console.print(result.stdout)


@model.command('create')
@click.argument('variant', type=click.Choice(['mini', 'standard', 'pro']))
@click.option('--name', '-n', help='Custom model name')
def model_create(variant, name):
    """Create a CroweLogic-Pharma model variant"""
    import subprocess

    model_name = name or f'CroweLogic-Pharma:{variant}'
    modelfile = f'models/CroweLogicPharmaModelfile-{variant}'

    console.print(f"[bold cyan]Creating model:[/bold cyan] {model_name}")
    console.print(f"[bold cyan]From:[/bold cyan] {modelfile}\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Building model...", total=None)

        result = subprocess.run(
            ['ollama', 'create', model_name, '-f', modelfile],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            console.print(f"[bold green]✓ Model created successfully:[/bold green] {model_name}")
            config.set('default_model', model_name)
        else:
            console.print(f"[bold red]✗ Error creating model:[/bold red]\n{result.stderr}")


# ============================================================================
# QUANTUM COMMANDS
# ============================================================================

@cli.group()
def quantum():
    """⚛️  Quantum chemistry and molecular simulations"""
    pass


@quantum.command('analyze')
@click.argument('compound', type=click.Choice(['hericenone', 'ganoderic']))
@click.option('--full', is_flag=True, help='Full analysis (quantum + docking + ADME)')
@click.option('--output', '-o', type=click.Path(), help='Save results to file')
def quantum_analyze(compound, full, output):
    """Analyze mushroom bioactive compounds"""
    from synapse_pharma_integration import DrugDiscoveryAI, QuantumChemistryEngine

    console.print(Panel(
        f"[bold cyan]Quantum Analysis: {compound.upper()}[/bold cyan]",
        border_style="cyan"
    ))

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        if full:
            task = progress.add_task("Running full pipeline...", total=None)
            ai = DrugDiscoveryAI()
            results = ai.full_analysis(f'{compound}_A')

            # Display results
            console.print("\n[bold green]Quantum Properties:[/bold green]")
            qp = results['quantum_properties']
            table = Table(show_header=True)
            table.add_column("Property")
            table.add_column("Value")
            table.add_row("HOMO-LUMO Gap", f"{qp['homo_lumo_gap_ev']:.3f} eV")
            table.add_row("UV λmax", f"{qp['uv_lambda_max']:.1f} nm")
            if 'reactivity' in qp:
                table.add_row("Reactivity", qp['reactivity'])
            console.print(table)

            console.print("\n[bold green]Docking Results:[/bold green]")
            dr = results['docking_results']
            table2 = Table(show_header=True)
            table2.add_column("Metric")
            table2.add_column("Value")
            table2.add_row("Target", dr['target'])
            table2.add_row("Docking Score", f"{dr['docking_score']:.2f} kcal/mol")
            table2.add_row("Predicted Ki", f"{dr['predicted_Ki_nM']:.1f} nM")
            table2.add_row("Drug-likeness", dr['adme_properties']['drug_likeness'])
            console.print(table2)

            console.print("\n[bold green]Recommendation:[/bold green]")
            rec = results['therapeutic_recommendation']
            console.print(f"  Development Potential: [cyan]{rec['development_potential']}[/cyan]")
            console.print(f"  Clinical Applications: [cyan]{rec['clinical_applications']}[/cyan]")

        else:
            task = progress.add_task("Running quantum analysis...", total=None)
            engine = QuantumChemistryEngine()

            if compound == 'hericenone':
                results = engine.analyze_hericenone_structure()
            else:
                results = engine.analyze_ganoderic_acid_structure()

            # Display results
            console.print("\n[bold green]Results:[/bold green]")
            table = Table(show_header=True)
            table.add_column("Property")
            table.add_column("Value")
            for key, value in results.items():
                if key not in ['electronic_transitions']:
                    table.add_row(str(key), str(value))
            console.print(table)

    # Save if requested
    if output:
        with open(output, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        console.print(f"\n[bold green]✓ Results saved to:[/bold green] {output}")


@quantum.command('dock')
@click.argument('compound', type=click.Choice(['hericenone', 'ganoderic']))
@click.option('--compare', is_flag=True, help='Compare both compounds')
def quantum_dock(compound, compare):
    """Molecular docking simulation"""
    from synapse_pharma_integration import MolecularSimulator

    simulator = MolecularSimulator()

    console.print(Panel("[bold cyan]Molecular Docking Simulation[/bold cyan]", border_style="cyan"))

    with console.status("[bold green]Running docking simulation..."):
        if compound == 'hericenone' or compare:
            h_results = simulator.simulate_hericenone_docking()

            console.print("\n[bold green]Hericenone A → TrkA (NGF Receptor)[/bold green]")
            table = Table(show_header=True)
            table.add_column("Metric")
            table.add_column("Value")
            table.add_row("Docking Score", f"{h_results['docking_score']:.2f} kcal/mol")
            table.add_row("Predicted Ki", f"{h_results['predicted_Ki_nM']:.1f} nM")
            table.add_row("Predicted IC50", f"{h_results['predicted_IC50_nM']:.1f} nM")
            table.add_row("pKi", f"{h_results['pKi']:.2f}")
            table.add_row("Bioavailability", "✓" if h_results['adme_properties']['oral_bioavailability'] else "✗")
            console.print(table)

        if compound == 'ganoderic' or compare:
            g_results = simulator.simulate_ganoderic_acid_docking()

            console.print("\n[bold green]Ganoderic Acid A → NF-κB[/bold green]")
            table = Table(show_header=True)
            table.add_column("Metric")
            table.add_column("Value")
            table.add_row("Docking Score", f"{g_results['docking_score']:.2f} kcal/mol")
            table.add_row("Predicted Ki", f"{g_results['predicted_Ki_nM']:.1f} nM")
            table.add_row("Predicted IC50", f"{g_results['predicted_IC50_nM']:.1f} nM")
            table.add_row("pKi", f"{g_results['pKi']:.2f}")
            table.add_row("Bioavailability", "✓" if g_results['adme_properties']['oral_bioavailability'] else "✗")
            console.print(table)


# ============================================================================
# DATA COMMANDS
# ============================================================================

@cli.group()
def data():
    """📊 Training data management"""
    pass


@data.command('generate')
@click.option('--source', type=click.Choice(['huggingface', 'chembl', 'all']), default='all')
def data_generate(source):
    """Generate training data from sources"""
    import subprocess

    console.print(Panel("[bold cyan]Training Data Generation[/bold cyan]", border_style="cyan"))

    if source in ['huggingface', 'all']:
        console.print("\n[bold green]Generating Hugging Face data...[/bold green]")
        result = subprocess.run(['python', 'scripts/add_huggingface_data.py'])
        if result.returncode == 0:
            console.print("[bold green]✓ Hugging Face data generated[/bold green]")

    if source in ['chembl', 'all']:
        console.print("\n[bold green]Generating ChEMBL data...[/bold green]")
        console.print("[yellow]Note: Requires ChEMBL data file[/yellow]")

    if source == 'all':
        console.print("\n[bold green]Running consolidation...[/bold green]")
        result = subprocess.run(['python', 'scripts/consolidate_training_data.py'])
        if result.returncode == 0:
            console.print("[bold green]✓ Data consolidated successfully[/bold green]")


@data.command('stats')
def data_stats():
    """Show training data statistics"""
    stats_file = Path('training_data/crowelogic_pharma_expanded_training_stats.json')

    if stats_file.exists():
        with open(stats_file) as f:
            stats = json.load(f)

        console.print(Panel("[bold cyan]Training Data Statistics[/bold cyan]", border_style="cyan"))

        console.print(f"\n[bold]Total Examples:[/bold] {stats['total_examples']}")
        console.print(f"[bold]Avg Prompt Length:[/bold] {stats['avg_prompt_length']:.0f} chars")
        console.print(f"[bold]Avg Response Length:[/bold] {stats['avg_response_length']:.0f} chars")

        console.print("\n[bold green]By Source:[/bold green]")
        table = Table(show_header=True)
        table.add_column("Source")
        table.add_column("Count", justify="right")
        table.add_column("Percentage", justify="right")

        for source, count in sorted(stats['by_source'].items(), key=lambda x: x[1], reverse=True):
            pct = (count / stats['total_examples']) * 100
            table.add_row(source, str(count), f"{pct:.1f}%")
        console.print(table)

        console.print("\n[bold green]By Category:[/bold green]")
        table2 = Table(show_header=True)
        table2.add_column("Category")
        table2.add_column("Count", justify="right")

        for category, count in sorted(stats['by_category'].items(), key=lambda x: x[1], reverse=True)[:10]:
            table2.add_row(category, str(count))
        console.print(table2)
    else:
        console.print("[yellow]No statistics available. Run 'crowelogic data generate' first.[/yellow]")


# ============================================================================
# DEPLOY COMMANDS
# ============================================================================

@cli.group()
def deploy():
    """☁️  Azure deployment management"""
    pass


@deploy.command('config')
def deploy_config():
    """Configure Azure deployment"""
    import subprocess

    console.print(Panel("[bold cyan]Azure Deployment Configuration[/bold cyan]", border_style="cyan"))

    result = subprocess.run(['python', 'azure_deployment/deploy_azure.py', '--config'])

    if result.returncode == 0:
        console.print("\n[bold green]✓ Configuration created[/bold green]")
        console.print("Edit deployment_config.json with your Azure details")


@deploy.command('start')
@click.option('--type', type=click.Choice(['aci', 'azureml']), default='aci')
def deploy_start(type):
    """Deploy to Azure"""
    import subprocess

    console.print(Panel(f"[bold cyan]Deploying to Azure ({type.upper()})[/bold cyan]", border_style="cyan"))

    with console.status("[bold green]Deploying to Azure..."):
        result = subprocess.run(['python', 'azure_deployment/deploy_azure.py', '--type', type])

    if result.returncode == 0:
        console.print("\n[bold green]✓ Deployment successful[/bold green]")
    else:
        console.print("\n[bold red]✗ Deployment failed[/bold red]")


# ============================================================================
# CONFIG COMMANDS
# ============================================================================

@cli.group()
def cfg():
    """⚙️  CLI configuration"""
    pass


@cfg.command('show')
def cfg_show():
    """Show current configuration"""
    console.print(Panel("[bold cyan]Current Configuration[/bold cyan]", border_style="cyan"))

    table = Table(show_header=True)
    table.add_column("Setting")
    table.add_column("Value")

    for key, value in config.data.items():
        if key != 'azure_config':
            table.add_row(key, str(value))

    console.print(table)


@cfg.command('set')
@click.argument('key')
@click.argument('value')
def cfg_set(key, value):
    """Set configuration value"""
    config.set(key, value)
    console.print(f"[bold green]✓ Set {key} = {value}[/bold green]")


@cfg.command('reset')
def cfg_reset():
    """Reset to default configuration"""
    if click.confirm('Reset configuration to defaults?'):
        config.data = {
            'default_model': 'CroweLogic-Pharma:mini',
            'ollama_host': 'http://localhost:11434',
            'output_format': 'rich',
            'azure_config': {}
        }
        config.save()
        console.print("[bold green]✓ Configuration reset[/bold green]")


# ============================================================================
# INFO COMMANDS
# ============================================================================

@cli.command('info')
def info():
    """Show system information"""
    import subprocess
    import platform

    console.print(Panel("[bold cyan]CroweLogic-Pharma System Information[/bold cyan]", border_style="cyan"))

    table = Table(show_header=False)
    table.add_column("Item", style="bold")
    table.add_column("Value")

    table.add_row("Version", VERSION)
    table.add_row("Python", platform.python_version())
    table.add_row("Platform", platform.system())
    table.add_row("Config File", str(config.config_file))
    table.add_row("Default Model", config.get('default_model'))

    # Check Ollama
    try:
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        ollama_version = result.stdout.strip() if result.returncode == 0 else "Not installed"
        table.add_row("Ollama", ollama_version)
    except:
        table.add_row("Ollama", "Not found")

    # Check Synapse-Lang
    try:
        import synapse_lang
        table.add_row("Synapse-Lang", "✓ Installed")
    except:
        table.add_row("Synapse-Lang", "✗ Not installed")

    console.print(table)


@cli.command('demo')
@click.option('--type', type=click.Choice(['quantum', 'docking', 'full']), default='full')
def demo(type):
    """Run demonstration"""
    import subprocess

    console.print(Panel(f"[bold cyan]{type.upper()} Demo[/bold cyan]", border_style="cyan"))

    demos = {
        'quantum': 'synapse_pharma_integration/examples/quantum_demo.py',
        'docking': 'synapse_pharma_integration/examples/docking_demo.py',
        'full': 'synapse_pharma_integration/examples/full_pipeline_demo.py'
    }

    subprocess.run(['python', demos[type]])


if __name__ == '__main__':
    console.print(BANNER)
    cli(obj={})
