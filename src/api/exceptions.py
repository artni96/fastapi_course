class ProjectException(BaseException):
    detail: None = 'Базовое исключение проекта'

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class NotFoundException(ProjectException):
    detail = 'Объект не найден'


class NoAvailableRoomsException(ProjectException):
    detail = 'Нет свободных номеров'


class RoomNotFoundException(BaseException):
    detail = 'Номер с указанным id не найден'


class BookingNotFoundException(BaseException):
    detail = 'Бронирование с указанным id не найдено'


class OnlyForAuthorException(BaseException):
    detail = 'Только автор бронирования может изменять данные'


class DateToLaterThanDateFromException(BaseException):
    detail = 'Дата начала бронирования не может быть позже даты конца бронирования'


class DateToLaterThanCurrentTimeException(BaseException):
    detail = 'Дата бронирования не может быть раньше текущего времени'