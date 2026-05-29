from typing import Any
import re


class DataCleaner:
    """Utility class for cleaning and normalizing user input data."""

    @staticmethod
    def normalize_spacing(text: Any) -> str:
        """Normalize text spacing without changing the content."""
        if text is None:
            return ""

        cleaned_text = str(text).strip()
        cleaned_text = re.sub(r"\s+", " ", cleaned_text)
        return cleaned_text

    @staticmethod
    def remove_noise(text: Any, max_repeated_letters: int = 2) -> str:
        """Remove common noisy repeated characters while keeping Arabic/English text."""
        cleaned_text = DataCleaner.normalize_spacing(text)
        if not cleaned_text:
            return ""

        cleaned_text = re.sub(r"[_ـ\-=\*~]{3,}", " ", cleaned_text)
        cleaned_text = re.sub(r"([!?.،؛,]){3,}", r"\1", cleaned_text)

        result: list[str] = []
        previous_char = ""
        repeated_count = 0

        for char in cleaned_text:
            if char == previous_char and char.isalpha():
                repeated_count += 1
            else:
                previous_char = char
                repeated_count = 1

            if char.isalpha() and repeated_count > max_repeated_letters:
                continue

            result.append(char)

        cleaned_text = "".join(result)
        cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()
        return cleaned_text

    @staticmethod
    def clean_text(text: Any) -> str:
        """Clean general text while preserving Arabic and English content."""
        return DataCleaner.remove_noise(text)

    @staticmethod
    def text_processor(text: Any) -> str:
        """Backward-compatible alias for clean_text."""
        return DataCleaner.clean_text(text)

    @staticmethod
    def clean_name(name: Any) -> str:
        """Clean a person's name without changing its meaning."""
        cleaned_name = DataCleaner.clean_text(name)
        return cleaned_name.title()

    @staticmethod
    def clean_email(email: Any) -> str:
        """Clean and normalize an email address."""
        return DataCleaner.normalize_spacing(email).lower()

    @staticmethod
    def clean_phone(phone: Any) -> str:
        """Clean a phone number while keeping a leading plus sign if it exists."""
        cleaned_phone = DataCleaner.clean_text(phone)
        if not cleaned_phone:
            return ""

        has_plus = cleaned_phone.startswith("+")
        cleaned_phone = re.sub(r"[^\d]", "", cleaned_phone)

        if has_plus and cleaned_phone:
            return f"+{cleaned_phone}"

        return cleaned_phone

    @staticmethod
    def clean_role(role: Any) -> str:
        """Clean a job role/title."""
        return DataCleaner.clean_text(role)

    @staticmethod
    def clean_number(value: Any, default: int = 0) -> int:
        """Convert a value to a non-negative integer."""
        if value is None or value == "":
            return default

        try:
            number = int(float(value))
        except (TypeError, ValueError):
            return default

        return max(number, 0)

    @staticmethod
    def clean_list(items: Any) -> list[str]:
        """Clean a list of strings and remove duplicates while keeping order."""
        if items is None:
            return []

        if isinstance(items, str):
            items = items.split(",")

        if not isinstance(items, list):
            return []

        cleaned_items: list[str] = []
        seen_items: set[str] = set()

        for item in items:
            cleaned_item = DataCleaner.clean_text(item)
            if not cleaned_item:
                continue

            normalized_item = cleaned_item.lower()
            if normalized_item in seen_items:
                continue

            seen_items.add(normalized_item)
            cleaned_items.append(cleaned_item)

        return cleaned_items

    @staticmethod
    def clean_links(links: Any) -> dict[str, str]:
        """Clean social/profile links."""
        if not isinstance(links, dict):
            return {}

        cleaned_links: dict[str, str] = {}

        for key, value in links.items():
            cleaned_key = DataCleaner.clean_text(key).lower()
            cleaned_value = DataCleaner.normalize_spacing(value)

            if not cleaned_key or not cleaned_value:
                continue

            cleaned_links[cleaned_key] = cleaned_value

        return cleaned_links

    @staticmethod
    def clean_user_profile(profile: dict[str, Any]) -> dict[str, Any]:
        """Clean the full user profile payload."""
        return {
            "name": DataCleaner.clean_name(profile.get("name")),
            "role": DataCleaner.clean_role(profile.get("role")),
            "email": DataCleaner.clean_email(profile.get("email")),
            "phone": DataCleaner.clean_phone(profile.get("phone")),
            "education": DataCleaner.clean_text(profile.get("education")),
            "profile": DataCleaner.clean_text(profile.get("profile")),
            "number_of_years_experience": DataCleaner.clean_number(
                profile.get("number_of_years_experience")
            ),
            "languages": DataCleaner.clean_list(
                profile.get("languages", profile.get("Languages"))
            ),
            "skills": DataCleaner.clean_list(profile.get("skills")),
            "social_media_links": DataCleaner.clean_links(
                profile.get("social_media_links")
            ),
        }
