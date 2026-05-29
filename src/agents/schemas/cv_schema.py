from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Any


class PersonalInfo(BaseModel):
    model_config = ConfigDict(extra="ignore")

    full_name: str = ""
    email: str = ""
    phone: str = ""
    location: str = ""
    linkedin: str = ""
    github: str = ""


class Skills(BaseModel):
    model_config = ConfigDict(extra="ignore")

    programming_languages: list[str] = Field(default_factory=list)
    frameworks: list[str] = Field(default_factory=list)
    databases: list[str] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)
    ai_ml: list[str] = Field(default_factory=list)

    @field_validator(
        "programming_languages",
        "frameworks",
        "databases",
        "tools",
        "ai_ml",
        mode="before",
    )
    @classmethod
    def ensure_list(cls, value: Any) -> list[str]:
        if value is None:
            return []

        if isinstance(value, str):
            return [value] if value.strip() else []

        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]

        return []


class CVData(BaseModel):
    model_config = ConfigDict(extra="ignore")

    personal_info: PersonalInfo = Field(default_factory=PersonalInfo)
    skills: Skills = Field(default_factory=Skills)
    experience: list[dict[str, Any]] = Field(default_factory=list)
    projects: list[dict[str, Any]] = Field(default_factory=list)
    education: list[dict[str, Any]] = Field(default_factory=list)
    certifications: list[dict[str, Any]] = Field(default_factory=list)
    languages: list[dict[str, Any] | str] = Field(default_factory=list)

    @field_validator(
        "experience",
        "projects",
        "education",
        "certifications",
        "languages",
        mode="before",
    )
    @classmethod
    def ensure_collection(cls, value: Any) -> list[Any]:
        if value is None:
            return []

        if isinstance(value, list):
            return value

        return []


class CVParseResult(BaseModel):
    model_config = ConfigDict(extra="ignore")

    summary: str = ""
    cv_data: CVData = Field(default_factory=CVData)

    @field_validator("summary", mode="before")
    @classmethod
    def ensure_summary(cls, value: Any) -> str:
        if value is None:
            return ""

        return str(value).strip()
