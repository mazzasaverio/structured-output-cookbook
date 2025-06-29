"""Command line interface for structured output extraction."""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import click
from .config import Config
from .extractor import StructuredExtractor
from .utils import setup_logger, get_logger, SchemaLoader
from .templates.job_description import JobDescriptionSchema
from .templates.recipe import RecipeSchema

# Available predefined templates
TEMPLATES = {
    "job": JobDescriptionSchema,
    "recipe": RecipeSchema,
}


def save_extraction_result(
    result_data: dict,
    template_name: str,
    output_path: Optional[str] = None,
    data_dir: str = "data"
) -> str:
    """Save extraction result to file and return the path."""
    if output_path:
        # Use specified path
        save_path = Path(output_path)
    else:
        # Generate automatic path in data directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{template_name}_extraction_{timestamp}.json"
        
        data_path = Path(data_dir)
        data_path.mkdir(exist_ok=True)
        save_path = data_path / filename
    
    # Ensure parent directory exists
    save_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save the file
    save_path.write_text(
        json.dumps(result_data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    
    return str(save_path)


@click.group()
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
def main(ctx: click.Context, debug: bool) -> None:
    """Structured Output Cookbook - Extract structured data from text using LLMs."""
    ctx.ensure_object(dict)
    
    config = Config.from_env()
    if debug:
        config.log_level = "DEBUG"
    
    setup_logger(config)
    ctx.obj["config"] = config
    ctx.obj["logger"] = get_logger(__name__)


@main.command()
def list_templates() -> None:
    """List available predefined templates."""
    click.echo("Available predefined templates:")
    for name, schema in TEMPLATES.items():
        click.echo(f"  {name}: {schema.get_schema_description()}")


@main.command()
@click.option("--config-dir", default="config/schemas", help="Directory containing YAML schema files")
def list_schemas(config_dir: str) -> None:
    """List available custom YAML schemas."""
    loader = SchemaLoader(config_dir)
    schemas = loader.list_schemas_with_descriptions()
    
    if not schemas:
        click.echo(f"No custom schemas found in {config_dir}")
        click.echo("Create .yaml files in the config directory to add custom schemas.")
        return
    
    click.echo("Available custom schemas:")
    for name, description in schemas:
        click.echo(f"  {name}: {description}")


@main.command()
@click.argument("template", type=click.Choice(list(TEMPLATES.keys())))
@click.option("--input-file", "-i", type=click.Path(exists=True), help="Input text file")
@click.option("--text", "-t", help="Input text directly")
@click.option("--output", "-o", type=click.Path(), help="Output JSON file (default: auto-generated in data/)")
@click.option("--data-dir", default="data", help="Directory for auto-generated outputs")
@click.option("--pretty", is_flag=True, help="Pretty print JSON output")
@click.option("--no-save", is_flag=True, help="Don't save to file, only print to stdout")
@click.pass_context
def extract(
    ctx: click.Context,
    template: str,
    input_file: Optional[str],
    text: Optional[str],
    output: Optional[str],
    data_dir: str,
    pretty: bool,
    no_save: bool
) -> None:
    """Extract data using a predefined template."""
    logger = ctx.obj["logger"]
    config = ctx.obj["config"]
    
    # Get input text
    if input_file:
        input_text = Path(input_file).read_text(encoding="utf-8")
    elif text:
        input_text = text
    else:
        click.echo("Error: Must provide either --input-file or --text", err=True)
        sys.exit(1)
    
    # Extract data
    extractor = StructuredExtractor(config)
    schema = TEMPLATES[template]
    
    logger.info(f"Extracting using template: {template}")
    result = extractor.extract(input_text, schema)
    
    if not result.success:
        click.echo(f"Extraction failed: {result.error}", err=True)
        sys.exit(1)
    
    # Ensure we have data
    if result.data is None:
        click.echo("Error: Extraction succeeded but no data returned", err=True)
        sys.exit(1)
    
    # Format output
    indent = 2 if pretty else None
    output_json = json.dumps(result.data, indent=indent, ensure_ascii=False)
    
    # Save to file unless --no-save is specified
    if not no_save:
        save_path = save_extraction_result(result.data, template, output, data_dir)
        click.echo(f"✅ Results saved to {save_path}")
    
    # Always print to stdout if no output file specified or if pretty print requested
    if not output or pretty or no_save:
        click.echo("📄 Extraction Result:")
        click.echo(output_json)
    
    # Show stats
    if result.tokens_used:
        click.echo(f"📊 Tokens used: {result.tokens_used}")
        click.echo(f"💰 Estimated cost: ~${(result.tokens_used * 0.00001):.4f}")  # Rough estimate


@main.command()
@click.argument("schema_name")
@click.option("--input-file", "-i", type=click.Path(exists=True), help="Input text file")
@click.option("--text", "-t", help="Input text directly")
@click.option("--output", "-o", type=click.Path(), help="Output JSON file (default: auto-generated in data/)")
@click.option("--data-dir", default="data", help="Directory for auto-generated outputs")
@click.option("--config-dir", default="config/schemas", help="Directory containing YAML schema files")
@click.option("--pretty", is_flag=True, help="Pretty print JSON output")
@click.option("--no-save", is_flag=True, help="Don't save to file, only print to stdout")
@click.pass_context
def extract_custom(
    ctx: click.Context,
    schema_name: str,
    input_file: Optional[str],
    text: Optional[str],
    output: Optional[str],
    data_dir: str,
    config_dir: str,
    pretty: bool,
    no_save: bool
) -> None:
    """Extract data using a custom YAML schema."""
    logger = ctx.obj["logger"]
    config = ctx.obj["config"]
    
    # Load YAML schema
    loader = SchemaLoader(config_dir)
    try:
        yaml_schema = loader.load_schema(schema_name)
    except FileNotFoundError:
        click.echo(f"Schema '{schema_name}' not found in {config_dir}", err=True)
        click.echo("Use 'list-schemas' command to see available schemas.", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error loading schema '{schema_name}': {e}", err=True)
        sys.exit(1)
    
    # Get input text
    if input_file:
        input_text = Path(input_file).read_text(encoding="utf-8")
    elif text:
        input_text = text
    else:
        click.echo("Error: Must provide either --input-file or --text", err=True)
        sys.exit(1)
    
    # Extract data
    extractor = StructuredExtractor(config)
    
    logger.info(f"Extracting using custom schema: {schema_name}")
    result = extractor.extract_with_yaml_schema(input_text, yaml_schema)
    
    if not result.success:
        click.echo(f"Extraction failed: {result.error}", err=True)
        sys.exit(1)
    
    # Ensure we have data
    if result.data is None:
        click.echo("Error: Extraction succeeded but no data returned", err=True)
        sys.exit(1)
    
    # Format output
    indent = 2 if pretty else None
    output_json = json.dumps(result.data, indent=indent, ensure_ascii=False)
    
    # Save to file unless --no-save is specified
    if not no_save:
        save_path = save_extraction_result(result.data, schema_name, output, data_dir)
        click.echo(f"✅ Results saved to {save_path}")
    
    # Always print to stdout if no output file specified or if pretty print requested
    if not output or pretty or no_save:
        click.echo("📄 Extraction Result:")
        click.echo(output_json)
    
    # Show stats
    if result.tokens_used:
        click.echo(f"📊 Tokens used: {result.tokens_used}")
        click.echo(f"💰 Estimated cost: ~${(result.tokens_used * 0.00001):.4f}")  # Rough estimate


if __name__ == "__main__":
    main()