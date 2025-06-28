"""Command line interface for structured output extraction."""

import json
import sys
from pathlib import Path
from typing import Optional

import click
from .config import Config
from .extractor import StructuredExtractor
from .logger import setup_logger, get_logger
from .templates.job_description import JobDescriptionSchema
from .templates.recipe import RecipeSchema

# Available predefined templates
TEMPLATES = {
    "job": JobDescriptionSchema,
    "recipe": RecipeSchema,
}


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
    click.echo("Available templates:")
    for name, schema in TEMPLATES.items():
        click.echo(f"  {name}: {schema.get_schema_description()}")


@main.command()
@click.argument("template", type=click.Choice(list(TEMPLATES.keys())))
@click.option("--input-file", "-i", type=click.Path(exists=True), help="Input text file")
@click.option("--text", "-t", help="Input text directly")
@click.option("--output", "-o", type=click.Path(), help="Output JSON file")
@click.option("--pretty", is_flag=True, help="Pretty print JSON output")
@click.pass_context
def extract(
    ctx: click.Context,
    template: str,
    input_file: Optional[str],
    text: Optional[str],
    output: Optional[str],
    pretty: bool
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
    
    # Format output
    indent = 2 if pretty else None
    output_json = json.dumps(result.data, indent=indent, ensure_ascii=False)
    
    # Write output
    if output:
        Path(output).write_text(output_json, encoding="utf-8")
        click.echo(f"Results saved to {output}")
    else:
        click.echo(output_json)
    
    # Show stats
    if result.tokens_used:
        logger.info(f"Tokens used: {result.tokens_used}")


@main.command()
@click.option("--schema-file", "-s", type=click.Path(exists=True), required=True, help="JSON schema file")
@click.option("--prompt-file", "-p", type=click.Path(exists=True), help="System prompt file")
@click.option("--prompt", help="System prompt text")
@click.option("--input-file", "-i", type=click.Path(exists=True), help="Input text file")
@click.option("--text", "-t", help="Input text directly")
@click.option("--output", "-o", type=click.Path(), help="Output JSON file")
@click.option("--pretty", is_flag=True, help="Pretty print JSON output")
@click.pass_context
def extract_custom(
    ctx: click.Context,
    schema_file: str,
    prompt_file: Optional[str],
    prompt: Optional[str],
    input_file: Optional[str],
    text: Optional[str],
    output: Optional[str],
    pretty: bool
) -> None:
    """Extract data using a custom JSON schema."""
    logger = ctx.obj["logger"]
    config = ctx.obj["config"]
    
    # Load schema
    try:
        schema_dict = json.loads(Path(schema_file).read_text(encoding="utf-8"))
    except (json.JSONDecodeError, FileNotFoundError) as e:
        click.echo(f"Error loading schema: {e}", err=True)
        sys.exit(1)
    
    # Get system prompt
    if prompt_file:
        system_prompt = Path(prompt_file).read_text(encoding="utf-8")
    elif prompt:
        system_prompt = prompt
    else:
        click.echo("Error: Must provide either --prompt-file or --prompt", err=True)
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
    
    logger.info("Extracting using custom schema")
    result = extractor.extract_with_custom_schema(input_text, schema_dict, system_prompt)
    
    if not result.success:
        click.echo(f"Extraction failed: {result.error}", err=True)
        sys.exit(1)
    
    # Format output
    indent = 2 if pretty else None
    output_json = json.dumps(result.data, indent=indent, ensure_ascii=False)
    
    # Write output
    if output:
        Path(output).write_text(output_json, encoding="utf-8")
        click.echo(f"Results saved to {output}")
    else:
        click.echo(output_json)
    
    # Show stats
    if result.tokens_used:
        logger.info(f"Tokens used: {result.tokens_used}")


if __name__ == "__main__":
    main()