# Examples

This directory contains example files demonstrating the usage of the Structured Output Cookbook.

## Files

### `example_usage.py`
A comprehensive Python script showing how to use the library programmatically with:
- Predefined templates (job descriptions, recipes)
- Custom YAML schemas
- Schema validation

### `job_description.txt`
Sample job description for testing job extraction template.

### `news_article.txt`
Sample news article for testing custom news extraction schema.

### `recipe.txt`
Sample recipe for testing recipe extraction template.

## Running Examples

### CLI Usage
```bash
# List available predefined templates
structured-output list-templates

# List available custom schemas
structured-output list-schemas

# Extract using predefined template
structured-output extract recipe --input-file examples/recipe.txt --pretty

# Extract using custom YAML schema
structured-output extract-custom news_article --input-file examples/news_article.txt --pretty
```

### Programmatic Usage
```bash
# Run the comprehensive example
python examples/example_usage.py
```

## Creating Custom Schemas

1. Create a new YAML file in `config/schemas/`
2. Follow the structure defined in `config/README.md`
3. Test your schema with the CLI or programmatically

## Environment Setup

Make sure you have your OpenAI API key set:
```bash
export OPENAI_API_KEY="your-api-key-here"
``` 