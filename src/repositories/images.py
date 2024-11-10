from src.models.images import ImagesModel
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import ImageMapper


class ImagesRepository(BaseRepository):
    model = ImagesModel
    mapper = ImageMapper
