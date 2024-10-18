from datetime import datetime
import re

formated_time = '26.10.2024'

test = re.fullmatch(r'^\d{1,2}.\d{1,2}.\d{4}$', formated_time)

new_date = datetime.strptime(
                formated_time, '%d.%m.%Y'
            )
print(new_date)