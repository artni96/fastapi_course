from datetime import date, timedelta, datetime

current_time = date.today().strftime('%d.%m.%Y')
print(current_time)
print(type(current_time))
formated_time = '16.10.2024'
new_time = datetime.strptime(formated_time, '%d.%m.%Y')
print(new_time.date())
print(type(new_time.date()))
