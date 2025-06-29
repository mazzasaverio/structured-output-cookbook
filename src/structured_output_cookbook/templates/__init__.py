"""Predefined templates for common extraction tasks."""

from .job_description import JobDescriptionSchema
from .recipe import RecipeSchema
from .product_review import ProductReviewSchema
from .email import EmailSchema
from .event import EventSchema

__all__ = [
    "JobDescriptionSchema",
    "RecipeSchema",
    "ProductReviewSchema",
    "EmailSchema",
    "EventSchema",
]
