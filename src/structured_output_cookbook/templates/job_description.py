"""Job description extraction schema."""

from typing import List, Union
from pydantic import Field
from ..schemas.base import BaseSchema


class JobDescriptionSchema(BaseSchema):
    """Extract structured information from job descriptions."""

    title: str = Field(description="Job title or position name")
    company: str = Field(description="Company name")
    location: Union[str, None] = Field(description="Job location")
    employment_type: Union[str, None] = Field(
        description="Employment type (full-time, part-time, contract, etc.)"
    )
    experience_level: Union[str, None] = Field(
        description="Required experience level (entry, mid, senior, etc.)"
    )
    salary_range: Union[str, None] = Field(
        description="Salary range or compensation information"
    )
    required_skills: List[str] = Field(
        description="Required technical skills and technologies"
    )
    preferred_skills: List[str] = Field(description="Preferred or nice-to-have skills")
    responsibilities: List[str] = Field(
        description="Key job responsibilities and duties"
    )
    requirements: List[str] = Field(description="Job requirements and qualifications")
    benefits: List[str] = Field(description="Benefits and perks offered")
    remote_work: Union[bool, None] = Field(
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
