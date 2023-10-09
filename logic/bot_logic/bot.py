import json
import random
from faker import Faker
import requests
from logic.models import PostModel


class BotExecutor:
    def __init__(self, json_path):
        self.fake = Faker("it_IT")
        try:
            with open(json_path, "r") as file:
                self.file = json.load(file)        
        except FileNotFoundError as e:
            print(f"File error: {e}")
        except json.JSONDecodeError as e:
            print(f"JSON error: {e}")
            
    def signup_users(self):
        for _ in range(self.file["number_of_users"]):
            data = {
                "username": self.fake.user_name(),
                "email": f"{self.fake.user_name()}@gmail.com",
                "password": self.fake.password(),
            }
            response = requests.post("http://localhost:8000/api/register_model/", json=data)
            if response.status_code == 201:        
                print("Executed")
            else:
                print(response.status_code)
                print(response.text)
    
    def create_content(self):
        for _ in range(self.file["number_of_users"]):
            for _ in range(1, self.file["max_posts_per_user"]):
                data = {
                    "text_field": self.fake.text(),
                    "author_user": random.choice(range(self.file["number_of_users"])),
                }
                files = {
                    "image_field": open("Manhattan.jpg", "rb"),                    
                }
                response = requests.post("http://localhost:8000/api/create_post/", data=data,
                                         files=files)
                if response.status_code == 201:        
                    print("Executed")
                else:
                    print(response.status_code)
                    print(response.text)
    
    def like_action(self):
        for n in range(1, self.file["number_of_users"]):
            total_posts = PostModel.objects.all().count()
            for _ in range(self.file["max_likes_per_user"]):
                random_post = random.randint(1, total_posts)
                response = requests.put(
                    f"http://localhost:8000/api/like_action/{random_post}/?current_user={n}")
                if response.status_code == 200:        
                    print("Executed")
                else:
                    print(response.status_code)
                    print(response.text)
            