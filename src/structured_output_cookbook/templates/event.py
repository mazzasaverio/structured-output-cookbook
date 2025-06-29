"""Event extraction schema."""

from typing import List, Union, Optional
from pydantic import BaseModel, Field, ConfigDict
from ..schemas.base import BaseSchema


class EventSchema(BaseSchema):
    """Extract structured information from event descriptions."""

    # Basic event information
    title: str = Field(description="Event title or name")
    description: Union[str, None] = Field(description="Event description or summary")
    event_type: Union[str, None] = Field(
        description="Type of event: conference, workshop, party, meeting, etc."
    )
    category: Union[str, None] = Field(
        description="Category: business, social, educational, cultural, etc."
    )

    # Date and time
    start_date: Union[str, None] = Field(description="Start date of the event")
    end_date: Union[str, None] = Field(description="End date of the event")
    start_time: Union[str, None] = Field(description="Start time")
    end_time: Union[str, None] = Field(description="End time")
    duration: Union[str, None] = Field(description="Duration of the event")
    timezone: Union[str, None] = Field(description="Timezone if specified")

    # Location information
    venue_name: Union[str, None] = Field(description="Name of the venue")
    address: Union[str, None] = Field(description="Full address of the event")
    city: Union[str, None] = Field(description="City where event takes place")
    state_province: Union[str, None] = Field(description="State or province")
    country: Union[str, None] = Field(description="Country")
    is_virtual: Union[bool, None] = Field(
        description="Whether the event is virtual/online"
    )
    virtual_platform: Union[str, None] = Field(
        description="Platform for virtual events"
    )

    # Organizer information
    organizer_name: Union[str, None] = Field(
        description="Name of the organizing person or entity"
    )
    organizer_contact: Union[str, None] = Field(
        description="Contact information for organizer"
    )
    organizing_company: Union[str, None] = Field(
        description="Company organizing the event"
    )

    # Attendance information
    capacity: Union[int, None] = Field(description="Maximum number of attendees")
    expected_attendance: Union[int, None] = Field(
        description="Expected number of attendees"
    )
    target_audience: List[str] = Field(description="Target audience or demographics")

    # Registration and costs
    registration_required: Union[bool, None] = Field(
        description="Whether registration is required"
    )
    registration_deadline: Union[str, None] = Field(description="Registration deadline")
    registration_link: Union[str, None] = Field(description="URL for registration")
    cost: Union[str, None] = Field(description="Cost or price to attend")
    is_free: Union[bool, None] = Field(description="Whether the event is free")

    # Content and speakers
    agenda_topics: List[str] = Field(description="Main topics or agenda items")
    speakers: List[str] = Field(description="Names of speakers or presenters")
    keynote_speakers: List[str] = Field(description="Keynote speakers if specified")

    # Additional details
    dress_code: Union[str, None] = Field(description="Dress code if specified")
    language: Union[str, None] = Field(description="Primary language of the event")
    accessibility_info: Union[str, None] = Field(
        description="Accessibility information"
    )
    parking_info: Union[str, None] = Field(description="Parking information")
    food_provided: Union[bool, None] = Field(
        description="Whether food/refreshments are provided"
    )

    # Contact and links
    website: Union[str, None] = Field(description="Event website")
    social_media: List[str] = Field(description="Social media links or hashtags")
    contact_email: Union[str, None] = Field(description="Contact email for inquiries")
    contact_phone: Union[str, None] = Field(description="Contact phone number")

    # Tags and categorization
    tags: List[str] = Field(description="Tags or keywords associated with the event")
    industries: List[str] = Field(
        description="Industries or sectors relevant to the event"
    )

    @classmethod
    def get_extraction_prompt(cls) -> str:
        return """
        Extract structured information from the following event description or announcement.
        Focus on identifying:
        - Event title, type, and description
        - Date, time, and location details (including virtual platform if applicable)
        - Organizer and contact information
        - Registration requirements and costs
        - Speakers, agenda topics, and target audience
        - Additional logistics like dress code, parking, accessibility
        - Websites, social media, and contact details
        
        If information is not explicitly mentioned, leave the field empty or null.
        For date/time fields, preserve the original format when possible.
        Extract all relevant items for list fields.
        """.strip()
