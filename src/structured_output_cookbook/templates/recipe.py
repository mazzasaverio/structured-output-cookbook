"""Recipe extraction schema."""

from typing import List, Optional
from pydantic import BaseModel, Field
from ..schemas.base import BaseSchema


class Ingredient(BaseModel):
    """Single ingredient with quantity and unit."""
    
    name: str = Field(description="Ingredient name")
    quantity: Optional[str] = Field(default=None, description="Amount needed")
    unit: Optional[str] = Field(default=None, description="Unit of measurement")
    notes: Optional[str] = Field(default=None, description="Additional notes")


class RecipeSchema(BaseSchema):
    """Extract structured information from recipes."""
    
    name: str = Field(description="Recipe name or title")
    description: Optional[str] = Field(
        default=None, 
        description="Brief description of the dish"
    )
    cuisine: Optional[str] = Field(
        default=None,
        description="Cuisine type (Italian, Asian, etc.)"
    )
    difficulty: Optional[str] = Field(
        default=None,
        description="Difficulty level (easy, medium, hard)"
    )
    prep_time: Optional[str] = Field(
        default=None,
        description="Preparation time"
    )
    cook_time: Optional[str] = Field(
        default=None,
        description="Cooking time"
    )
    total_time: Optional[str] = Field(
        default=None,
        description="Total time required"
    )
    servings: Optional[int] = Field(
        default=None,
        description="Number of servings"
    )
    ingredients: List[Ingredient] = Field(
        default_factory=list,
        description="List of ingredients with quantities"
    )
    instructions: List[str] = Field(
        default_factory=list,
        description="Step-by-step cooking instructions"
    )
    tags: List[str] = Field(
        default_factory=list,
        description="Recipe tags (vegetarian, gluten-free, etc.)"
    )
    nutrition: Optional[dict] = Field(
        default=None,
        description="Nutritional information if available"
    )
    
    @classmethod
    def get_extraction_prompt(cls) -> str:
        return """
        Extract structured information from the following recipe text.
        Focus on identifying:
        - Recipe name and description
        - Timing information (prep, cook, total time)
        - Complete ingredients list with quantities and units
        - Step-by-step instructions
        - Difficulty level and serving information
        - Any dietary tags or restrictions
        
        For ingredients, try to separate quantity, unit, and ingredient name.
        If information is not available, leave fields empty.
        """.strip()