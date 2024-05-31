import requests
import json
import uuid
from faker import Faker
import random

fake = Faker()

profiles = []


def generate_hobbies():
    hobbies = [
        "reading", "travelling", "cooking", "sports", "hiking",
        "dancing", "painting", "gardening", "photography", "music"
    ]
    return random.sample(hobbies, 3)


def generate_bio():
    templates = [
        "Hi, I'm {name}. My passions include {hobby1}, {hobby2}, and {hobby3}. In my spare time, you'll find me {activity}. I'm searching for someone who loves {passion} too.",
        "Hello there! I'm {name}, and I enjoy {hobby1}, {hobby2}, and {hobby3}. I love spending weekends {activity}. Looking for someone who shares my interest in {passion}.",
        "Hey! My name is {name}. I'm passionate about {hobby1}, {hobby2}, and {hobby3}. When I'm free, I like to {activity}. Seeking someone who enjoys {passion} as much as I do.",
        "Hi, I'm {name}. I enjoy {hobby1}, {hobby2}, and {hobby3}. I spend my free time {activity}. I'd love to meet someone who shares my enthusiasm for {passion}.",
        "Hello! My name is {name}. My favorite hobbies are {hobby1}, {hobby2}, and {hobby3}. I enjoy {activity} when I'm not working. I'm looking for someone who loves {passion}.",
        "Hey! I'm {name}, a fan of {hobby1}, {hobby2}, and {hobby3}. My weekends are often spent {activity}. I'm seeking a partner who is into {passion}.",
        "Hello! I'm {name}. My interests include {hobby1}, {hobby2}, and {hobby3}. I enjoy {activity} during my free time. I'd love to meet someone who is passionate about {passion}.",
    ]
    template = random.choice(templates)
    hobbies = generate_hobbies()
    bio = template.format(
        name=fake.first_name(),
        hobby1=hobbies[0],
        hobby2=hobbies[1],
        hobby3=hobbies[2],
        activity=fake.sentence(nb_words=5),
        passion=fake.word()
    )
    return bio


def scrape_page(url):
    for _ in range(1, 100):
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            for user in results:
                profile = {
                    'bot_id': str(uuid.uuid4()),
                    'bot_foto': user['picture']['large'],
                    'bot_naam': f"{user['name']['first']} {user['name']['last']}",
                    'bot_land': user['location']['country'],
                    'bot_geslacht': user['gender'],
                    'bot_oud': user['dob']['age'],
                    'bot_beschrijving': generate_bio()
                }
                profiles.append(profile)


starting_url = 'https://randomuser.me/api/'
scrape_page(starting_url)
print(profiles)
with open('profiles.json', 'w') as f:
    json.dump(profiles, f)
