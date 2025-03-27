from abc_classes import ABot
from api_requests import get_sub_session
from teams_classes import NewUser, NewPost
import random
import string
import os
import json
from openai import OpenAI
from collections import defaultdict

API_KEY = os.getenv('ENV_VAR1')
client = OpenAI(api_key=API_KEY)


from datetime import datetime, timedelta

class Bot(ABot):
    def create_tweetGPT(self, previous_posts = None):
        user_prompts = {
        "en": [
            "Complain lightheartedly about something minor that happened today"
        ],
        "fr": [
            "Plains-toi avec humour de quelque chose d'inimportant qui s'est passé aujourd'hui",
        ]
    }
        
        if previous_posts:
            context_posts = f"- {random.choice(previous_posts)}"
            base_prompt = f"Here is a recent tweet:\n{context_posts}\n\nRewrite exactly this tweet and make a very minor change, it could be punctuation, putting it in lower caps, rephrasing very very lightly; just make sure the tone doesn't change and the tweets could almost be mistaken one from another.\n MAKE SURE TO USE THE SAME LANGUAGE"
        else:
            base_prompt = "Complain lightheartedly about something minor that happened today\n"

        response = client.chat.completions.create(
            model="gpt-4", 
            messages=[
                {"role": "system", "content": base_prompt},
            ]
        )
        return response.choices[0].message.content.strip()
    
    def translate_text(self, text, target_language):
        response = client.chat.completions.create(
            model="gpt-4",temperature=1.4,
            messages=[
                {"role": "system", "content": f"Translate this tweet into {target_language} while keeping it natural and engaging."},
                {"role": "user", "content": text}
            ],
        )
        return response.choices[0].message.content.strip()
    
    def create_user(self, session_info):
        # todo logic
        self.metadata = session_info.metadata
        self.language = session_info.lang  
        self.influence_target = session_info.influence_target
        self.start_time = getattr(session_info, "start_time", None)
        self.end_time = getattr(session_info, "end_time", None)
        self.sub_sessions_info = session_info.sub_sessions_info
        self.sub_sessions_id = session_info.sub_sessions_id

        existing_usernames = set() #to avoid repetition

        def username_generator():
            #prefix
            prefixes = ["lil", "theBest", "Big", "Mister", "Kween", "Dr", "Super", "Crafty", "TheReal", "Official","TheOG", "user", "Massive", "CraZ", "Baby", "The", "__", "_","our","__.", "the", "aa."]  #add randomly
            used_prefixes = set()

            #name combo
            normal_nicknames = [("James", "Jim"), ("Mary", "Molly"), ("John", "Johnny"), ("Patricia", "Pat"), ("Robert", "Bob"),("Jennifer", "Jen"), ("Michael", "Mike"), ("Linda", "Lindy"), ("William", "Will"), ("Elizabeth", "Liz"),
            ("David", "Dave"), ("Barbara", "Barb"), ("Richard", "Richardinosaur"), ("Susan", "Su"), ("Joseph", "Joe"),("Jessica", "Jess"), ("Thomas", "Tom"), ("Sarah", "Sadie"), ("Charles", "Charlie"), ("Karen", "Kari"),
            ("Christopher", "Chris"), ("Nancy", "Nan"), ("Daniel", "Dan"), ("Lisa", "Lizzy"), ("Matthew", "Matt"),("Betty", "Betsy"), ("Anthony", "Tony"), ("Margaret", "Maggie"), ("Mark", "Marc"), ("Sandra", "Sandy"),("Donald", "Don"), ("Ashley", "Ash"), ("Steven", "Steve"), ("Kimberly", "Kim"),
            ("Paul", "Pauly"),("Emily", "Em"), ("Andrew", "Drew"), ("Donna", "Donnie"), ("Joshua", "Josh"), ("Michelle", "Mitch"),("Kenneth", "Ken"), ("Dorothy", "Dot"), ("Kevin", "Kev"), ("Carol", "Carrie"), ("Brian", "Bri"),("Amanda", "Mandy"), ("George", "Georgie"), ("Melissa", "Mel"), ("Edward", "Ed"), ("Deborah", "Debbie")]
            funny_nicknames = [
            ("James", "Jimbo"), ("Mary", "Moo"), ("John", "J-Dog"), ("Patricia", "Trishy"), ("Robert", "Robby-Bob"),("Jennifer", "Jelly"), ("Michael", "Mikey Mike"), ("Linda", "L-Dawg"), ("William", "Billy the Kid"), ("Elizabeth", "Lizzie McGuire"),("David", "D-Money"), ("Barbara", "Babs"), ("Richard", "Dicky"), ("Susan", "Sushi"), ("Joseph", "JoJo"),("Jessica", "Jessinator"), ("Thomas", "Tommy Pickles"), ("Sarah", "Sazzy"), ("Charles", "Chuckles"), ("Karen", "K-Ren"),
            ("Christopher", "Topher"), ("Nancy", "Nanners"), ("Daniel", "D-Man"), ("Lisa", "Lizard"), ("Matthew", "Matty Ice"),("Betty", "Betz"), ("Anthony", "Ant-Man"), ("Margaret", "Megatron"), ("Mark", "Marky Mark"), ("Sandra", "Sandy Cheeks"),("Donald", "Don Juan"), ("Ashley", "Ash Ketchum"), ("Steven", "Stevie Wonder"), ("Kimberly", "Kiki"), ("Emily", "Em&Em"), ("Andrew", "Drewbie"), ("Donna", "DonDon"), ("Joshua", "Juicy J"),("Michelle", "Mitchie"), ("Kenneth", "Kenny G"), ("Dorothy", "DotDot"), ("Kevin", "Kevlar"), ("Carol", "Carrot"),("Brian", "Bri-Bri"), ("Amanda", "Mandarin"), ("George", "Georgio"), ("Melissa", "Melon"), ("Edward", "Eddie Spaghetti"),("Deborah", "Debo"), ("Franklin", "Frank the Tank"), ("Tiffany", "Tiff-Tiff"), ("Oscar", "Ozzy"), ("Lucas", "Lukey Duke"),
            ("Victoria", "VeeVee"), ("Theodore", "Teddy Bear"), ("Cynthia", "Cyn"), ("Leonard", "Lenny Face"), ("Phillip", "Flip"),("Veronica", "Ronnie"), ("Samuel", "Samwise"), ("Nicole", "Nikki Minaj"), ("Gregory", "Greggles"), ("Raymond", "Ray-Ray"),("Harold", "Harry-O"), ("Gerald", "G-Money"), ("Sylvia", "Sylvester"), ("Walter", "Wally World"), ("Isabella", "Izzy Bizzy"),("Xavier", "X-Man"), ("Felicia", "Bye Felicia"), ("Brandon", "B-Rad"), ("Catherine", "Kitty"), ("Leon", "Leo the Lion"),("Randy", "Randog"), ("Vincent", "Vinnie the Pooh"), ("Eugene", "Gene Machine"), ("Monica", "Momo"), ("Charlotte", "Charizard")
    ]

            use_funny_name = random.choice([True, False])
            real_name, nickname = random.choice(funny_nicknames if use_funny_name else normal_nicknames)

            #end digits
            num_digits = random.randint(0, 2) #random digits
            suffix = ''.join(random.choices(string.digits, k=num_digits))  
            username = f"{nickname}{suffix}"

            #20% of the time add a prefix if there are available ones
            if random.random() < 0.2 and prefixes:
                available_prefixes = list(set(prefixes) - used_prefixes) 
                if available_prefixes:  
                    prefix = random.choice(available_prefixes)
                    username = f"{prefix}{username}"
                    used_prefixes.add(prefix)

            if username not in existing_usernames:
                existing_usernames.add(username)
                name = real_name if random.random() < 0.7 else nickname  # Sometimes use real name, sometimes nickname
                return username, name

        def create_descriptionGPT(self):
            user_descriptions = [user["description"] for user in session_info.users if user.get("description")]
            if len(user_descriptions) > 30:
                user_descriptions = random.sample(user_descriptions, 30)
            
            other_descriptions = "\n".join([f"{i+1}. {desc}" for i, desc in enumerate(user_descriptions)])
            response = client.chat.completions.create(model="gpt-4",
            messages=[{"role": "system", "content": "Rewrite IN THE SAME LANGUAGE, these user descriptions, mix them up or add a fun twist but keep the same tone and structures (important), Return each description on a new line without numbering or extra formatting."},
                  {"role": "user", "content": other_descriptions}],
            )
            
            rewritten_descriptions = response.choices[0].message.content.split("\n")
            return [desc.strip() for desc in rewritten_descriptions if desc.strip()]

        user_descriptions = [user["description"] for user in session_info.users if user.get("description")]
        user_data = [username_generator() for _ in range(5)]
        new_users = []

        for i, user in enumerate(user_data):
            username, name = user
            description = random.choice(user_descriptions) if user_descriptions else ""
            new_user = NewUser(username=username, name=name, description=description)
            new_users.append(new_user)

        return new_users


    def generate_content(self, datasets_json, users_list):
        posts = []
        influence_target = self.influence_target
        existing_posts = [post["text"] for post in getattr(datasets_json, "posts", []) if "text" in post]
        topic_keywords = []
        max_total_for_each_user = 100
        min_total_for_each_user = 10

        user_post_counts = defaultdict(int)

        if not influence_target or influence_target == "default_topic":
            if hasattr(self, "metadata") and isinstance(self.metadata, dict):
                topics = self.metadata.get("topics", [])
                topic_keywords = [kw for topic in topics if isinstance(topic, dict) for kw in topic.get("keywords", [])]
                influence_target = random.choice(topic_keywords) if topic_keywords else "random_trending"
    
        existing_posts = [post["text"] for post in getattr(datasets_json, "posts", []) if "text" in post]
        
        all_sub_sessions_id = self.sub_sessions_id
        user_distribution = self.metadata.get("user_distribution_across_time", [])

        for sub_session_id in all_sub_sessions_id:
            sub_session = self.sub_sessions_info[sub_session_id-1]
            sub_session_start = datetime.fromisoformat(sub_session["start_time"].replace("Z", ""))
            sub_session_end = datetime.fromisoformat(sub_session["end_time"].replace("Z", ""))

            relevant_time_slots = [slot for slot in user_distribution if datetime.fromisoformat(slot["start_at"].replace("Z", "")) >= sub_session_start 
            and datetime.fromisoformat(slot["end_at"].replace("Z", "")) <= sub_session_end]

            for time_slot in relevant_time_slots:
                time_slot_start = datetime.fromisoformat(time_slot["start_at"].replace("Z", ""))
                time_slot_end = datetime.fromisoformat(time_slot["end_at"].replace("Z", ""))
                percentage_users = time_slot["percentage_of_users"] / 100
                percentage_posts = time_slot["percentage_of_posts"] / 100
            
            users_in_slot = random.sample(users_list, max(1, int(len(users_list) * percentage_users)))

            for user in users_in_slot:
                current_total = user_post_counts[user.user_id]
                if current_total >= max_total_for_each_user:
                    continue
                
                if current_total < min_total_for_each_user:
                    needed_to_reach_min = min_total_for_each_user - current_total

                    needed_to_reach_min = min(
                        needed_to_reach_min,
                        max_total_for_each_user - current_total
                    )

                    possible_extra = random.randint(0, 4)

                    leftover_for_100 = max_total_for_each_user - (current_total + needed_to_reach_min)
                    if leftover_for_100 < possible_extra:
                        possible_extra = leftover_for_100

                    post_count = needed_to_reach_min + possible_extra

                else:          
                    desired_count = random.randint(9, 11)
                    leftover_for_100 = max_total_for_each_user - current_total
                    post_count = min(desired_count, leftover_for_100)
                
                
                previous_posts = []

                for _ in range(post_count):
                    random_offset = random.uniform(0, (sub_session_end - sub_session_start).total_seconds())
                    post_time = sub_session_start + timedelta(seconds=random_offset)
                    post_time_str = post_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")

                    choice_type = random.random()
                    topic_keywords = self.influence_target.get("keywords", [])

                    if choice_type < 0.1:
                        keyword = self.influence_target.get("topic", []) if random.random() < 0.5 else random.choice(topic_keywords) 
                        text = random.choice([
                                f"I just realized how deep I’ve gone down the {keyword} rabbit hole today.",
                                f"Anyone else trying to figure out what makes {keyword} so addictive?",
                                f"I’m torn—am I overthinking {keyword}, or is it really that big of a deal?",
                                f"Can't decide if {keyword} deserves this hype or if we're all just bored.",
                                f"Every time I promise to ignore {keyword}, something pulls me right back in.",
                                f"Is it weird that {keyword} is all I see on my feed lately?",
                                f"Suddenly, everyone’s an expert on {keyword} and I’m just here with my popcorn.",
                                f"I was skeptical about {keyword}, but now I’m the one who won’t stop talking about it.",
                                f"I swear I blinked and {keyword} took over the entire internet.",
                                f"The debate around {keyword} is intense—do we need a referee or something?",
                                f"I thought {keyword} was overrated until I actually paid attention to it.",
                                f"It’s wild how half my day disappeared because I kept scrolling through {keyword} updates.",
                                f"I used to roll my eyes at {keyword}, but now I’m fully invested in the drama.",
                                f"Not gonna lie, {keyword} kinda sparked my curiosity more than I care to admit.",
                                f"Somehow, {keyword} has turned into my go-to conversation starter this week.",
                                f"I’m still on the fence about {keyword}, but it’s definitely not boring.",
                                f"When did my timeline decide that {keyword} was the only thing worth discussing?",
                                f"I love how {keyword} can bring out the best (and worst) in people’s takes.",
                                f"So... are we all just pretending {keyword} isn’t low-key controlling our lives?",
                                f"Never thought I’d say this, but I might be in too deep with {keyword} now."
                            ])
                        if self.language != "en":
                            text = self.translate_text(text, target_language=self.language)
                    else:
                        text = self.create_tweetGPT(existing_posts)

                    posts.append(NewPost(text=text, author_id=user.user_id, created_at=post_time_str, user=user))
                    previous_posts.append(text)
                    user_post_counts[user.user_id] += 1
                
                if user_post_counts[user.user_id] >= max_total_for_each_user:
                    continue

        return posts
