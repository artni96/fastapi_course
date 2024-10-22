from datetime import datetime
import re

formated_time = '26.10.2024'

test = re.fullmatch(r'^\d{1,2}.\d{1,2}.\d{4}$', formated_time)

new_date = datetime.strptime(
                formated_time, '%d.%m.%Y'
            )

input_dict = {
    'title': None,
    'id': 3
}

output_data = {k: v for k, v in input_dict.items() if v is not None}
print(output_data)
