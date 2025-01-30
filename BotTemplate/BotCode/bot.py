from abc_classes import ABot
from teams_classes import NewUser, NewPost
import random
import string
import json

class Bot(ABot):
    def create_user(self, session_info):
        # todo logic
        self.metadata = session_info.metadata 
        self.influence_target = session_info.influence_target
        
        def username_generator():

            popular_nicknames = [("James", "Jim"), ("Mary", "Molly"), ("John", "Johnny"), ("Patricia", "Pat"), ("Robert", "Bob"),("Jennifer", "Jen"), ("Michael", "Mike"), ("Linda", "Lindy"), ("William", "Will"), ("Elizabeth", "Liz"),
            ("David", "Dave"), ("Barbara", "Barb"), ("Richard", "Rich"), ("Susan", "Sue"), ("Joseph", "Joe"),("Jessica", "Jess"), ("Thomas", "Tom"), ("Sarah", "Sadie"), ("Charles", "Charlie"), ("Karen", "Kari"),
            ("Christopher", "Chris"), ("Nancy", "Nan"), ("Daniel", "Dan"), ("Lisa", "Lizzy"), ("Matthew", "Matt"),("Betty", "Betsy"), ("Anthony", "Tony"), ("Margaret", "Maggie"), ("Mark", "Marc"), ("Sandra", "Sandy"),("Donald", "Don"), ("Ashley", "Ash"), ("Steven", "Steve"), ("Kimberly", "Kim"),
            ("Paul", "Pauly"),("Emily", "Em"), ("Andrew", "Drew"), ("Donna", "Donnie"), ("Joshua", "Josh"), ("Michelle", "Mitch"),("Kenneth", "Ken"), ("Dorothy", "Dot"), ("Kevin", "Kev"), ("Carol", "Carrie"), ("Brian", "Bri"),("Amanda", "Mandy"), ("George", "Georgie"), ("Melissa", "Mel"), ("Edward", "Ed"), ("Deborah", "Debbie")]
            real_name, nickname = random.choice(popular_nicknames)

            #Adding Digits Randomly
            num_digits = random.randint(0, 4) 
            suffix = ''.join(random.choices(string.digits, k=num_digits))  
            username = f"{nickname}{suffix}"
            name = real_name if random.random() < 0.7 else nickname #sometimes real name sometimes nickname 
            return username, name
        
        user_descriptions = [user["description"] for user in session_info.users if user.get("description")]

        # Example:
        new_users = [
        NewUser(username=user[0], name=user[1], description=random.choice(user_descriptions) if user_descriptions else "Hello, I'm a bot")
        for user in [username_generator() for _ in range(20)]
        ]
        
        return new_users

    def generate_content(self, datasets_json, users_list):
        posts = []

        influence_target = getattr(datasets_json, "influence_target", "default_topic")


        print("Metadata from session_info:", self.metadata)

        topic_keywords = []

        if hasattr(self, "metadata") and isinstance(self.metadata, dict):
            topics = self.metadata.get("topics", [])
            print("Extracted Topics:", topics) 
            if isinstance(topics, list):
                for topic in topics:
                    if isinstance(topic, dict) and "keywords" in topic:
                        topic_keywords.extend(topic["keywords"])

        print("Extracted Keywords:", topic_keywords) 

        existing_posts = [post["text"] for post in getattr(datasets_json, "posts", []) if "text" in post]

        for user in users_list:
            post_count = random.randint(10, 15)

            for _ in range(post_count):
                if existing_posts and random.random() < 0.7:
                    text = random.choice(existing_posts)
                else:
                    keyword = influence_target if random.random() < 0.5 else random.choice(topic_keywords) if topic_keywords else "NO_VALID_TOPICS"
                    text = random.choice([
                        f"I really love {keyword}!",
                        f"NEED {keyword}!",
                        f"Really hate {keyword}!",
                        f"Missing {keyword} rn"
                    ])

                posts.append(NewPost(text=text, author_id=user.user_id, created_at="2024-03-17T00:20:30.000Z", user=user))

        return posts