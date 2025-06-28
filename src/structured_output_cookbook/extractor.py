"""Main extractor class for structured output generation."""

import json
from typing import Type, Dict, Any, Optional
from openai import OpenAI
from pydantic import ValidationError

from .config import Config
from .logger import get_logger
from .schemas.base import BaseSchema, ExtractionResult


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
        Extract structured data from text using the provided schema.
        
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
            
            response = self.client.chat.completions.create(
                model=self.config.openai_model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": text}
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": schema.get_schema_name().lower(),
                        "strict": True,
                        "schema": schema.model_json_schema()
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
    
    def extract_with_custom_schema(
        self,
        text: str,
        schema_dict: Dict[str, Any],
        system_prompt: str
    ) -> ExtractionResult:
        """
        Extract data using a custom JSON schema dictionary.
        
        Args:
            text: Input text to extract from
            schema_dict: JSON schema as dictionary
            system_prompt: System prompt for extraction
            
        Returns:
            ExtractionResult with success status and extracted data
        """
        try:
            self.logger.info("Starting extraction with custom schema")
            
            response = self.client.chat.completions.create(
                model=self.config.openai_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text}
                ],
                response_format={
                    "type": "json_schema", 
                    "json_schema": {
                        "name": "custom_extraction",
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
                self.logger.info("Custom extraction completed successfully")
                
                return ExtractionResult.success_result(
                    data=data,
                    model_used=response.model,
                    tokens_used=response.usage.total_tokens if response.usage else None
                )
                
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to parse JSON response: {e}")
                return ExtractionResult.error_result(f"Invalid JSON response: {str(e)}")
                
        except Exception as e:
            self.logger.error(f"Custom extraction failed: {e}")
            return ExtractionResult.error_result(str(e))