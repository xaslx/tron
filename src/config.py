from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict



class Config(BaseSettings):

    db_host: str = Field(alias='POSTGRES_HOST')
    db_port: int = Field(alias='POSTGRES_PORT')
    db_user: str = Field(alias='POSTGRES_USER')
    db_password: str = Field(alias='POSTGRES_PASSWORD')
    db_name: str = Field(alias='POSTGRES_DB')
    
    trongrid_api: str = Field(alias='TRONGRID_API')
    trongrid_url: str = Field(alias='TRONGRID_URL')

    @property
    def DATABASE_URL(self) -> str:
        return f'postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}'


    model_config = SettingsConfigDict(env_file='.env')