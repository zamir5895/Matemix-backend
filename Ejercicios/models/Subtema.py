from pydantic import BaseModel, Field

class CreateSubtema(BaseModel):
    titulo: str
    descripcion: str | None = None
    video_url: list[str] = Field(default_factory=list)
    preguntas: dict[str, list[str]] = Field(default_factory=dict)
    tema_id:str

class ListYoutubeTemasCreation(BaseModel):
    urls: list[str] = Field(default_factory=list)
    