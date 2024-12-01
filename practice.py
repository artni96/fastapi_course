from datetime import date, timedelta
DATE_FORMAT = '%d.%m.%Y'


print(date.today().strftime('%d.%m.%Y'), date.today()+timedelta(days=3))
print((date.today() + timedelta(days=6)).strftime(DATE_FORMAT))