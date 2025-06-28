"""Structured Output Cookbook - LLM-powered structured data extraction."""

__version__ = "0.1.0"
__author__ = "Your Name"

from .extractor import StructuredExtractor
from .schemas.base import BaseSchema, ExtractionResult
from .templates.job_description import JobDescriptionSchema
from .templates.recipe import RecipeSchema
from .config import Config

__all__ = [
    "StructuredExtractor",
    "BaseSchema",
    "ExtractionResult", 
    "JobDescriptionSchema",
    "RecipeSchema",
    "Config",
]