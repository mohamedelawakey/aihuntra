from typing import Any, TypedDict


class AgentState(TypedDict):
    """Represents the state of an agent."""

    # user_profile
    name: str
    role: str
    email: str
    phone: str
    education: str
    profile: str
    number_of_years_experience: int
    languages: list[str]
    skills: list[str]
    social_media_links: dict[str, str]

    # cv
    cv_path: str
    cv_name: str
    cv_metadata: dict[str, Any]
    cv_content: list[dict[str, str]]
    cv_raw_text: str
    cv_number_of_pages: int
    cv_characters_count: int
    cv_summary: str
    cv_data: dict[str, Any]
    cv_errors: list[str]
