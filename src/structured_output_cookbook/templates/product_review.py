"""Product review extraction schema."""

from typing import List, Union, Optional
from pydantic import BaseModel, Field, ConfigDict
from ..schemas.base import BaseSchema


class ProductReviewSchema(BaseSchema):
    """Extract structured information from product reviews."""
    
    product_name: str = Field(description="Name of the product being reviewed")
    brand: Union[str, None] = Field(description="Brand of the product")
    rating: Union[float, None] = Field(description="Rating given (1-5 stars or similar scale)")
    overall_sentiment: str = Field(description="Overall sentiment: positive, negative, or neutral")
    reviewer_name: Union[str, None] = Field(description="Name of the reviewer if mentioned")
    purchase_verified: Union[bool, None] = Field(description="Whether the purchase was verified")
    
    # Review content
    title: Union[str, None] = Field(description="Title of the review")
    summary: Union[str, None] = Field(description="Brief summary of the review")
    
    # Pros and cons
    pros: List[str] = Field(description="Positive aspects mentioned in the review")
    cons: List[str] = Field(description="Negative aspects mentioned in the review")
    
    # Specific aspects
    value_for_money: Union[str, None] = Field(description="Comments about value for money")
    quality: Union[str, None] = Field(description="Comments about product quality")
    ease_of_use: Union[str, None] = Field(description="Comments about ease of use")
    customer_service: Union[str, None] = Field(description="Comments about customer service experience")
    
    # Recommendation
    would_recommend: Union[bool, None] = Field(description="Whether reviewer would recommend the product")
    recommend_for: List[str] = Field(description="Who or what situations this product is recommended for")
    
    # Additional info
    usage_duration: Union[str, None] = Field(description="How long the reviewer has used the product")
    comparison_products: List[str] = Field(description="Other products mentioned for comparison")
    
    @classmethod
    def get_extraction_prompt(cls) -> str:
        return """
        Extract structured information from the following product review.
        Focus on identifying:
        - Product name, brand, and overall rating/sentiment
        - Reviewer information if available
        - Key positive and negative points (pros and cons)
        - Specific aspects like quality, value, ease of use
        - Recommendations and comparisons
        - Duration of use and verification status
        
        If information is not explicitly mentioned, leave the field empty or null.
        For lists, extract all relevant items mentioned.
        """.strip() 