from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import NoResultFound

from src.constants import IMAGE_PATH
from src.models.hotels import HotelsModel
from src.models.images import ImagesModel
from src.models.rooms import RoomsModel
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import HotelDataMapper
from src.repositories.utils.images import ImageManager
from src.repositories.utils.rooms import rooms_ids_for_booking
from src.schemas.hotels import HotelAddRequest, HotelPatch
from src.schemas.images import ImageCreate
from src.tasks.tasks import resize_image


class HotelsRepository(BaseRepository):
    model = HotelsModel
    mapper = HotelDataMapper

    def filtered_query(self, query, location=None, title=None, id=None):
        if id is not None:
            query = query.filter_by(id=id)
        if title is not None:
            query = query.filter(self.model.title.icontains(title))
        if location is not None:
            query = query.filter(self.model.location.icontains(
                location))
        return query

    async def get_filtered_hotels(
            self,
            date_from: date,
            date_to: date,
            location: str,
            title: str,
            offset: int,
            limit: int
    ):
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=date_from, date_to=date_to
        )
        hotels_ids_to_get = (
            select(RoomsModel.hotel_id)
            .select_from(RoomsModel)
            .filter(RoomsModel.id.in_(rooms_ids_to_get))
        )
        query = select(self.model).filter(self.model.id.in_(hotels_ids_to_get))
        filtered_query_by_params = self.filtered_query(
            query=query,
            location=location,
            title=title
        )
        filtered_query_by_params = filtered_query_by_params.limit(
            limit).offset(offset)
        result = await self.session.execute(filtered_query_by_params)
        return [self.mapper.map_to_domain_entity(hotel)
                for hotel in result.scalars().all()]

    async def add(self, data: HotelAddRequest, db):
        if data.image:
            new_random_name = ImageManager().create_random_name()
            image_name = ImageManager().base64_to_file(
                base64_string=data.image,
                image_name=new_random_name
            )
            image_data = ImageCreate(
                name=image_name,
            )
            image_id = await db.images.add(image_data)
            data.image = image_id.id
            resize_image.delay(f'{IMAGE_PATH}{image_name}')
        new_data_stmt = (
            insert(self.model).values(**data.model_dump()).returning(
                self.model
            )
        )
        result = await self.session.execute(new_data_stmt)
        new_model_obj = result.unique().scalars().one()
        return self.mapper.map_to_domain_entity(new_model_obj)

    async def remove(self, **filtered_by) -> dict:
        try:
            hotel_to_delete_stmt = (
                delete(self.model)
                .filter_by(**filtered_by)
                .returning(self.model)
            )
            removed_hotel = await self.session.execute(hotel_to_delete_stmt)
            removed_hotel = removed_hotel.scalars().one()
            if removed_hotel.image:
                image_to_delete_stmt = (
                    delete(ImagesModel)
                    .filter_by(id=removed_hotel.image)
                    .returning(ImagesModel.name)
                )
                image_name = await self.session.execute(image_to_delete_stmt)
                image_name = image_name.scalars().one()
                ImageManager().delete_file(file_name_with_ext=image_name)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Не удалось удалить отель'
            )
        if removed_hotel:
            return {'status': 'OK'}
        return {'status': 'Отель не существует'}

    async def change(
            self,
            db,
            data: HotelPatch,
            exclude_unset: bool = False,
            **filtered_by
    ):
        if data.image:
            image_id_subquery = (
                select(self.model.image)
                .filter_by(**filtered_by)
                .subquery('image_id_subquery')
            )
            image_to_delete_stmt = (
                delete(ImagesModel)
                .filter_by(id=image_id_subquery)
                .returning(ImagesModel.name)
            )
            image_name = await self.session.execute(image_to_delete_stmt)
            image_name = image_name.scalars().one_or_none()
            if image_name:
                ImageManager().delete_file(file_name_with_ext=image_name)
            new_random_name = ImageManager().create_random_name()
            image_name = ImageManager().base64_to_file(
                base64_string=data.image,
                image_name=new_random_name
            )
            image_data = ImageCreate(
                name=image_name,
            )
            image_id = await db.images.add(image_data)
            data.image = image_id.id
        query = (
            update(self.model)
            .filter_by(**filtered_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            .returning(self.model)
        )
        result = await self.session.execute(query)
        try:
            model_obj = result.scalars().one()
            return self.mapper.map_to_domain_entity(model_obj)
        except NoResultFound:
            return {'status': 'NOT FOUND'}
