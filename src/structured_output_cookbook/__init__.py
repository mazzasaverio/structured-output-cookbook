"""Structured Output Cookbook - Extract structured data from text using LLMs with ready-to-use templates."""

__version__ = "0.1.0"
__author__ = "Saverio Mazza"
__email__ = "saverio3107@gmail.com"
__description__ = "Extract structured data from text using LLMs with ready-to-use templates"
__url__ = "https://github.com/mazzasaverio/structured-output-cookbook"

from .extractor import StructuredExtractor
from .schemas.base import BaseSchema, ExtractionResult
from .utils import SchemaLoader, YamlSchema, setup_minimal_logger
from .templates.job_description import JobDescriptionSchema
from .templates.recipe import RecipeSchema
from .templates.product_review import ProductReviewSchema
from .templates.email import EmailSchema
from .templates.event import EventSchema
from .config import Config

__all__ = [
    "StructuredExtractor",
    "BaseSchema",
    "ExtractionResult", 
    "SchemaLoader",
    "YamlSchema",
    "setup_minimal_logger",
    "JobDescriptionSchema",
    "RecipeSchema",
    "ProductReviewSchema",
    "EmailSchema",
    "EventSchema",
    "Config",
    "__version__",
]