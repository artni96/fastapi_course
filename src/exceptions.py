class ProjectException(BaseException):
    detail: None = 'Базовое исключение проекта'

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class NotFoundException(ProjectException):
    detail = 'Объект не найден'


class NoAvailableRoomsException(ProjectException):
    detail = 'Нет свободных номеров'


class HotelNotFoundException(BaseException):
    @staticmethod
    def detail(hotel_id):
        return f'Отель с id {hotel_id} не найден'

class RoomForHotelNotFoundException(BaseException):

    @staticmethod
    def detail(hotel_id, room_id):
        detail = f'Номер {room_id} в отеле {hotel_id} не найден'
        return detail


class RoomNotFoundException(BaseException):

    @staticmethod
    def detail(room_id):
        return f'Номер {room_id} не найден'


class BookingNotFoundException(BaseException):
    detail = 'Бронирование с указанным id не найдено'


class OnlyForAuthorException(BaseException):
    detail = 'Только автор бронирования может изменять данные'


class DateToLaterThanDateFromException(BaseException):
    detail = 'Дата date_to не может быть позже даты date_from'


class DateToLaterThanCurrentTimeException(BaseException):
    detail = 'Дата date_from не может быть раньше текущего времени'
