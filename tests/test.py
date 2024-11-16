import  json

with open('mock_hotels.json', 'r') as f:
    response = json.load(f)
    for obj in response:
        print(obj)