from pydantic import BaseModel, Field

class CreateSUbtema(BaseModel):
    titulo: str
    descripcion: str | None = None
    video_id: list[str] = Field(default_factory=list)
    preguntas: dict[str, list[str]] = Field(default_factory=dict)

class ListYoutubeTemasCreation(BaseModel):
    urls: list[str] = Field(default_factory=list)

