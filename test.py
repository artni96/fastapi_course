import re

email_pattern = r"^\S+@\S+\.\S+$"

print(re.fullmatch(email_pattern, 'artni@mail.ru'))
