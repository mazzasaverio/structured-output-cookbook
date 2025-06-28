"""Job description extraction schema."""

from typing import List, Optional
from pydantic import Field
from ..schemas.base import BaseSchema


class JobDescriptionSchema(BaseSchema):
    """Extract structured information from job descriptions."""
    
    title: str = Field(description="Job title or position name")
    company: str = Field(description="Company name")
    location: Optional[str] = Field(default=None, description="Job location")
    employment_type: Optional[str] = Field(
        default=None, 
        description="Employment type (full-time, part-time, contract, etc.)"
    )
    experience_level: Optional[str] = Field(
        default=None,
        description="Required experience level (entry, mid, senior, etc.)"
    )
    salary_range: Optional[str] = Field(
        default=None,
        description="Salary range or compensation information"
    )
    required_skills: List[str] = Field(
        default_factory=list,
        description="Required technical skills and technologies"
    )
    preferred_skills: List[str] = Field(
        default_factory=list,
        description="Preferred or nice-to-have skills"
    )
    responsibilities: List[str] = Field(
        default_factory=list,
        description="Key job responsibilities and duties"
    )
    requirements: List[str] = Field(
        default_factory=list,
        description="Job requirements and qualifications"
    )
    benefits: List[str] = Field(
        default_factory=list,
        description="Benefits and perks offered"
    )
    remote_work: Optional[bool] = Field(
        default=None,
        description="Whether remote work is available"
    )
    
    @classmethod
    def get_extraction_prompt(cls) -> str:
        return """
        Extract structured information from the following job description. 
        Focus on identifying:
        - Job title and company information
        - Location and employment details
        - Required and preferred skills
        - Responsibilities and requirements
        - Compensation and benefits
        
        If information is not explicitly mentioned, leave the field empty or null.
        """.strip()