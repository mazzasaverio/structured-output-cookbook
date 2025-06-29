"""Main extractor class for structured output generation."""

import json
from typing import Type, Dict, Any, Optional
from openai import OpenAI
from pydantic import ValidationError

from .config import Config
from .utils import get_logger
from .schemas.base import BaseSchema, ExtractionResult
from .utils import YamlSchema


class StructuredExtractor:
    """Main extractor class using OpenAI's structured outputs."""
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize the extractor with configuration."""
        self.config = config or Config.from_env()
        self.client = OpenAI(api_key=self.config.openai_api_key)
        self.logger = get_logger(__name__)
        
    def extract(
        self, 
        text: str, 
        schema: Type[BaseSchema],
        system_prompt: Optional[str] = None
    ) -> ExtractionResult:
        """
        Extract structured data from text using a predefined Pydantic schema.
        
        Args:
            text: Input text to extract from
            schema: Pydantic schema class to use for extraction
            system_prompt: Optional custom system prompt
            
        Returns:
            ExtractionResult with success status and extracted data
        """
        try:
            self.logger.info(
                f"Starting extraction with schema: {schema.get_schema_name()}"
            )
            
            # Use custom prompt or schema default
            prompt = system_prompt or schema.get_extraction_prompt()
            
            # Generate schema and ensure additionalProperties is false
            schema_dict = schema.model_json_schema()
            self._ensure_additional_properties_false(schema_dict)
            
            response = self.client.chat.completions.create(
                model=self.config.openai_model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": text}
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": schema.get_schema_name().lower().replace(" ", "_"),
                        "strict": True,
                        "schema": schema_dict
                    }
                },
                timeout=self.config.timeout_seconds
            )
            
            # Parse the response
            content = response.choices[0].message.content
            if not content:
                return ExtractionResult.error_result("Empty response from LLM")
            
            # Parse JSON and validate with schema
            try:
                raw_data = json.loads(content)
                validated_data = schema(**raw_data)
                
                self.logger.info("Extraction completed successfully")
                
                return ExtractionResult.success_result(
                    data=validated_data.model_dump(),
                    model_used=response.model,
                    tokens_used=response.usage.total_tokens if response.usage else None
                )
                
            except (json.JSONDecodeError, ValidationError) as e:
                self.logger.error(f"Failed to parse/validate response: {e}")
                return ExtractionResult.error_result(f"Invalid response format: {str(e)}")
                
        except Exception as e:
            self.logger.error(f"Extraction failed: {e}")
            return ExtractionResult.error_result(str(e))
    
    def extract_with_yaml_schema(
        self,
        text: str,
        yaml_schema: YamlSchema
    ) -> ExtractionResult:
        """
        Extract structured data from text using a YAML schema configuration.
        
        Args:
            text: Input text to extract from
            yaml_schema: YamlSchema object containing schema and prompt
            
        Returns:
            ExtractionResult with success status and extracted data
        """
        try:
            self.logger.info(f"Starting extraction with YAML schema: {yaml_schema.name}")
            
            # Ensure schema has additionalProperties: false
            schema_dict = yaml_schema.schema.copy()
            self._ensure_additional_properties_false(schema_dict)
            
            response = self.client.chat.completions.create(
                model=self.config.openai_model,
                messages=[
                    {"role": "system", "content": yaml_schema.system_prompt},
                    {"role": "user", "content": text}
                ],
                response_format={
                    "type": "json_schema", 
                    "json_schema": {
                        "name": yaml_schema.name.lower().replace(" ", "_"),
                        "strict": True,
                        "schema": schema_dict
                    }
                },
                timeout=self.config.timeout_seconds
            )
            
            content = response.choices[0].message.content
            if not content:
                return ExtractionResult.error_result("Empty response from LLM")
            
            try:
                data = json.loads(content)
                self.logger.info("YAML schema extraction completed successfully")
                
                return ExtractionResult.success_result(
                    data=data,
                    model_used=response.model,
                    tokens_used=response.usage.total_tokens if response.usage else None
                )
                
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to parse JSON response: {e}")
                return ExtractionResult.error_result(f"Invalid JSON response: {str(e)}")
                
        except Exception as e:
            self.logger.error(f"YAML schema extraction failed: {e}")
            return ExtractionResult.error_result(str(e))
    
    def _ensure_additional_properties_false(self, schema_dict: Dict[str, Any]) -> None:
        """Recursively ensure all objects have additionalProperties: false."""
        if isinstance(schema_dict, dict):
            if schema_dict.get("type") == "object":
                schema_dict["additionalProperties"] = False
            
            # Recursively process nested schemas
            for key, value in schema_dict.items():
                if key in ["properties", "items", "anyOf", "allOf", "oneOf"]:
                    if isinstance(value, dict):
                        self._ensure_additional_properties_false(value)
                    elif isinstance(value, list):
                        for item in value:
                            if isinstance(item, dict):
                                self._ensure_additional_properties_false(item)
                elif isinstance(value, dict):
                    self._ensure_additional_properties_false(value)