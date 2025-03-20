from abc_classes import ABot
from api_requests import get_sub_session
from teams_classes import NewUser, NewPost
import random
import string
import os
import json
from openai import OpenAI

API_KEY = os.getenv('ENV_VAR1')
client = OpenAI(api_key=API_KEY)


from datetime import datetime, timedelta

class Bot(ABot):
    def create_tweetGPT(self, keyword, previous_posts = None):
        user_prompts = {
        "en": [
            "Complain lightheartedly about something minor that happened today, and mention the keyword.",
            "Tweet a funny reaction to a trending topic (tied to the keyword), but make it sound personal.",
            "Share a short, casual story about your day that ties into the keyword.",
            "Write a tweet as though you’re telling a friend a small personal anecdote about the keyword."
        ],
        "fr": [
            "Plain un petit problème personnel qui t’est arrivé aujourd’hui, en mentionnant le mot-clé.",
            "Réagis à un sujet tendance en faisant référence au mot-clé, mais fais en sorte que ce soit personnel.",
            "Raconte une courte anecdote sur ta journée et relie-la au mot-clé.",
            "Écris un tweet comme si tu racontais à un ami une anecdote sur le mot-clé."
        ]
    }
        personal_details = [
            "You spilled coffee on your shirt",
            "You got stuck in traffic",
            "You found a funny note on your door",
            "You nearly missed your bus",
            "You stayed up too late binge-watching a show"
        ]
        selected_prompts = user_prompts.get(self.language, user_prompts["en"])
        detail = random.choice(personal_details)
        if previous_posts:
            context_posts = "\n".join([f"- {post}" for post in previous_posts[-5:]])
            base_prompt = f"Here are some of my recent tweets:\n{context_posts}\n\nMake a new tweet in a similar style and tone.\n"
        else:
            base_prompt = "Write a brand-new tweet.\n"
        final_prompt = f"{base_prompt}Keep it short, casual, and personal. Today’s personal detail: '{detail}'. Mention the keyword '{keyword}'. {random.choice(selected_prompts)}"
        system_prompt = f"You are a casual, chronically-online Twitter user who often references personal experiences and minor daily annoyances. Use a laid-back tone, occasional slang, minimal hashtags, never mention you’re an AI, and tweet in {self.language}."
        response = client.chat.completions.create(
            model="gpt-4",
            temperature=0.9, presence_penalty=0.5,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": final_prompt}
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

        def create_descriptionGPT(self, keyword):
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
        new_descriptions = create_descriptionGPT(client, user_descriptions)


        new_users = [
            NewUser(username=user[0], name=user[1], description=new_descriptions[i])
            for i, user in enumerate([username_generator() for _ in range(5)])
        ]

        return new_users

    def generate_content(self, datasets_json, users_list):
        posts = []
        influence_target = self.influence_target
        topic_keywords = []

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
                post_count = random.randint(3, 7)
                previous_posts = []


                for _ in range(post_count):
                    random_offset = random.uniform(0, (sub_session_end - sub_session_start).total_seconds())
                    post_time = sub_session_start + timedelta(seconds=random_offset)
                    post_time_str = post_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")

                    choice_type = random.random()
                    topic_keywords = self.influence_target.get("keywords", [])

                    if choice_type < 0.2 or len(previous_posts) == 0:
                        keyword = influence_target if random.random() < 0.5 else random.choice(topic_keywords) 
                        text = random.choice([
                            f"Can't stop thinking about {keyword}.",f"Why is everyone talking about {keyword}?",f"Anyone else obsessed with {keyword} lately?",f"{keyword} is taking over my life!",f"What are your thoughts on {keyword}?",f"Just saw something wild about {keyword}.",f"Let’s settle this: is {keyword} overrated?",f"Can’t believe what just happened in {keyword}!",
                            f"My feed is full of {keyword}, and I’m not mad about it.",f"Lowkey addicted to {keyword}.",f"If you don’t love {keyword}, we can’t be friends.",f"Does anyone still care about {keyword}?",f"Need more {keyword} content ASAP.",
                            f"I could talk about {keyword} all day.",f"Explain {keyword} to me like I'm five.",f"Why is {keyword} trending again?",f"{keyword} is pure nostalgia!",f"I swear {keyword} keeps getting better.",f"Who else remembers when {keyword} first started?",f"What’s your unpopular opinion on {keyword}?",
                            f"I might be the only one who still follows {keyword}.",f"Just realized I’ve been following {keyword} for years.",f"{keyword} reminds me of simpler times.",f"Not gonna lie, {keyword} had me in tears today.",f"Wish I could experience {keyword} for the first time again.",f"Is it just me, or is {keyword} everywhere?",f"I need a full documentary on {keyword}.",
                            f"What’s the best moment in {keyword} history?",f"{keyword} fans, assemble!",f"I have so many questions about {keyword}.",f"Somebody explain {keyword} to me!",f"{keyword} just changed the game!",f"This take on {keyword} is actually genius.",
                            f"Can’t believe I slept on {keyword}.",f"Why didn’t anyone tell me {keyword} was this good?",f"{keyword} discourse is getting out of hand.",f"The debate around {keyword} is wild.",f"If you could change one thing about {keyword}, what would it be?",
                            f"Okay, but imagine {keyword} in 10 years.",f"Looking back, {keyword} was ahead of its time.",f"{keyword} stans are built different.",f"What’s the best way to get into {keyword}?",f"Convince me to care about {keyword}.",f"If {keyword} had a theme song, what would it be?",f"I feel like {keyword} is misunderstood.",f"People really sleep on {keyword}.",f"{keyword} deserves more respect.",
                            f"Why is {keyword} so controversial?",f"Tell me one fun fact about {keyword}.",f"Okay but hear me out: {keyword}.",f"I’m about to do a deep dive on {keyword}.",f"Every time I try to ignore {keyword}, it pulls me back in.",f"Today’s hot take: {keyword} is actually amazing.",f"{keyword} appreciation post!",f"Tell me something I don’t know about {keyword}.",f"If you don’t follow {keyword}, you’re missing out.",
                            f"{keyword} needs its own fan club.",f"I have a love-hate relationship with {keyword}.",f"What’s the wildest thing about {keyword}?",f"The more I learn about {keyword}, the more obsessed I get.",
                            f"{keyword} makes me feel some type of way.",f"Do we think {keyword} is here to stay?",f"Who else remembers the golden age of {keyword}?",f"Unpopular opinion: {keyword} is actually great.",f"If you know, you know: {keyword}.",f"{keyword} is proof that the internet is undefeated.",f"The best thing about {keyword}? The memes.",f"How did {keyword} even start?",f"Why do people have such strong opinions about {keyword}?",f"{keyword} hits different at 2 AM.",f"Real ones know the impact of {keyword}.",f"{keyword} is the reason I still have Twitter.",f"What’s the best {keyword} moment of all time?",f"Okay but imagine a world without {keyword}.",
                            f"What’s the most underrated part of {keyword}?",f"I just went down a rabbit hole on {keyword}.",f"If {keyword} was a movie, who would play the lead?",f"What’s your favorite memory of {keyword}?",f"I need a whole podcast on {keyword}.",f"Nothing brings people together like {keyword}.",
                            f"Can someone explain why {keyword} is blowing up?",f"{keyword} fans are the real MVPs.",f"One thing about {keyword}—it never disappoints.",f"{keyword} just made my day.",f"Honestly, {keyword} is an art form.",f"The only thing I care about right now is {keyword}.",f"Is {keyword} getting better or worse?",
                            f"Raise your hand if {keyword} ruined your sleep schedule.",f"{keyword} is my toxic trait.",f"I want a Netflix series about {keyword}.",f"The world would be boring without {keyword}.",f"I bet you didn’t know this about {keyword}.",f"{keyword} is the content I signed up for.",
                            f"I feel like I should be taking notes on {keyword}.",f"The only reason I logged in today was {keyword}.",f"{keyword} is my personality now.",f"Petition to make {keyword} a national holiday.",f"{keyword} is living rent-free in my brain."
                        ])
                        if self.language != "en":
                            text = self.translate_text(text, target_language=self.language)
                    else:
                        text = self.create_tweetGPT(keyword, existing_posts)
                        

                    posts.append(NewPost(text=text, author_id=user.user_id, created_at=post_time_str, user=user))
                    previous_posts.append(posts)

        return posts
