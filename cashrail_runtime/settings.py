from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CASHRAIL_", env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./cashrail.db"
    controller_token: SecretStr = Field(min_length=32)
    enable_live_execution: bool = False
    stripe_webhook_secret: SecretStr = Field(min_length=8)
    environment: str = "development"
    auto_create_schema: bool = True
    controller_policy_version: str = "cashrail-v1"
    controller_allowed_actions: str = (
        "PUBLIC_RESEARCH,INTERNAL_SCORING,DRAFT_OUTREACH,DRAFT_PROPOSAL"
    )

    @property
    def allowed_controller_actions(self) -> frozenset[str]:
        return frozenset(
            action.strip()
            for action in self.controller_allowed_actions.split(",")
            if action.strip()
        )

    @model_validator(mode="after")
    def production_safety(self) -> "Settings":
        if self.environment == "production" and self.database_url.startswith("sqlite:"):
            raise ValueError("production requires a transactional external database")
        if self.environment == "production" and self.auto_create_schema:
            raise ValueError(
                "production requires migrations; auto schema creation must be disabled"
            )
        return self
