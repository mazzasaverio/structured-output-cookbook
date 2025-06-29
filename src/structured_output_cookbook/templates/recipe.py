"""Recipe extraction schema."""

from typing import List, Union, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from ..schemas.base import BaseSchema


class Ingredient(BaseModel):
    """Single ingredient with quantity and unit."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(description="Ingredient name")
    quantity: Union[str, None] = Field(description="Amount needed")
    unit: Union[str, None] = Field(description="Unit of measurement")
    notes: Union[str, None] = Field(description="Additional notes")


class RecipeSchema(BaseSchema):
    """Extract structured information from recipes."""

    name: str = Field(description="Recipe name or title")
    description: Union[str, None] = Field(description="Brief description of the dish")
    cuisine: Union[str, None] = Field(description="Cuisine type (Italian, Asian, etc.)")
    difficulty: Union[str, None] = Field(
        description="Difficulty level (easy, medium, hard)"
    )
    prep_time: Union[str, None] = Field(description="Preparation time")
    cook_time: Union[str, None] = Field(description="Cooking time")
    total_time: Union[str, None] = Field(description="Total time required")
    servings: Union[int, None] = Field(description="Number of servings")
    ingredients: List[Ingredient] = Field(
        description="List of ingredients with quantities"
    )
    instructions: List[str] = Field(description="Step-by-step cooking instructions")
    tags: List[str] = Field(description="Recipe tags (vegetarian, gluten-free, etc.)")
    nutrition: Union[Dict[str, Any], None] = Field(
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
