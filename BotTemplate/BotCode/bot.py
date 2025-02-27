from abc_classes import ABot
from teams_classes import NewUser, NewPost
import random
import string
import json
from datetime import datetime, timedelta

class Bot(ABot):
    def create_user(self, session_info):
        # todo logic
        self.metadata = session_info.metadata 
        self.influence_target = session_info.influence_target
        self.start_time = getattr(session_info, "start_time", None)
        self.end_time = getattr(session_info, "end_time", None)

        existing_usernames = set() #to avoid repetition
        
        def username_generator():
            #prefix
            prefixes = ["lil", "theBest", "Big", "Mister", "Kween", "Dr", "Super", "Crafty", "TheReal", "Official","TheOG", "user", "Massive", "CraZ", "Baby", "The", "__", "_","our","__.", "the", "aa."]  #add randomly
            used_prefixes = set()

            #name combo
            normal_nicknames = [("James", "Jim"), ("Mary", "Molly"), ("John", "Johnny"), ("Patricia", "Pat"), ("Robert", "Bob"),("Jennifer", "Jen"), ("Michael", "Mike"), ("Linda", "Lindy"), ("William", "Will"), ("Elizabeth", "Liz"),
            ("David", "Dave"), ("Barbara", "Barb"), ("Richard", "Rich"), ("Susan", "Sue"), ("Joseph", "Joe"),("Jessica", "Jess"), ("Thomas", "Tom"), ("Sarah", "Sadie"), ("Charles", "Charlie"), ("Karen", "Kari"),
            ("Christopher", "Chris"), ("Nancy", "Nan"), ("Daniel", "Dan"), ("Lisa", "Lizzy"), ("Matthew", "Matt"),("Betty", "Betsy"), ("Anthony", "Tony"), ("Margaret", "Maggie"), ("Mark", "Marc"), ("Sandra", "Sandy"),("Donald", "Don"), ("Ashley", "Ash"), ("Steven", "Steve"), ("Kimberly", "Kim"),
            ("Paul", "Pauly"),("Emily", "Em"), ("Andrew", "Drew"), ("Donna", "Donnie"), ("Joshua", "Josh"), ("Michelle", "Mitch"),("Kenneth", "Ken"), ("Dorothy", "Dot"), ("Kevin", "Kev"), ("Carol", "Carrie"), ("Brian", "Bri"),("Amanda", "Mandy"), ("George", "Georgie"), ("Melissa", "Mel"), ("Edward", "Ed"), ("Deborah", "Debbie")]
            funny_nicknames = [
            ("James", "Jimbo"), ("Mary", "Moo"), ("John", "J-Dog"), ("Patricia", "Trishy"), ("Robert", "Robby-Bob"),("Jennifer", "Jelly"), ("Michael", "Mikey Mike"), ("Linda", "L-Dawg"), ("William", "Billy the Kid"), ("Elizabeth", "Lizzie McGuire"),("David", "D-Money"), ("Barbara", "Babs"), ("Richard", "Dicky"), ("Susan", "Sushi"), ("Joseph", "JoJo"),("Jessica", "Jessinator"), ("Thomas", "Tommy Pickles"), ("Sarah", "Sazzy"), ("Charles", "Chuckles"), ("Karen", "K-Ren"),
            ("Christopher", "Topher"), ("Nancy", "Nanners"), ("Daniel", "D-Man"), ("Lisa", "Lizard"), ("Matthew", "Matty Ice"),("Betty", "Betz"), ("Anthony", "Ant-Man"), ("Margaret", "Megatron"), ("Mark", "Marky Mark"), ("Sandra", "Sandy Cheeks"),("Donald", "Don Juan"), ("Ashley", "Ash Ketchum"), ("Steven", "Stevie Wonder"), ("Kimberly", "Kiki"),("Paul", "P-Diddy"), ("Emily", "Em&Em"), ("Andrew", "Drewbie"), ("Donna", "DonDon"), ("Joshua", "Juicy J"),("Michelle", "Mitchie"), ("Kenneth", "Kenny G"), ("Dorothy", "DotDot"), ("Kevin", "Kevlar"), ("Carol", "Carrot"),("Brian", "Bri-Bri"), ("Amanda", "Mandarin"), ("George", "Georgio"), ("Melissa", "Melon"), ("Edward", "Eddie Spaghetti"),("Deborah", "Debo"), ("Franklin", "Frank the Tank"), ("Tiffany", "Tiff-Tiff"), ("Oscar", "Ozzy"), ("Lucas", "Lukey Duke"),
            ("Victoria", "VeeVee"), ("Theodore", "Teddy Bear"), ("Cynthia", "Cyn"), ("Leonard", "Lenny Face"), ("Phillip", "Flip"),("Veronica", "Ronnie"), ("Samuel", "Samwise"), ("Nicole", "Nikki Minaj"), ("Gregory", "Greggles"), ("Raymond", "Ray-Ray"),("Harold", "Harry-O"), ("Gerald", "G-Money"), ("Sylvia", "Sylvester"), ("Walter", "Wally World"), ("Isabella", "Izzy Bizzy"),("Xavier", "X-Man"), ("Felicia", "Bye Felicia"), ("Brandon", "B-Rad"), ("Catherine", "Kitty"), ("Leon", "Leo the Lion"),("Randy", "Randog"), ("Vincent", "Vinnie the Pooh"), ("Eugene", "Gene Machine"), ("Monica", "Momo"), ("Charlotte", "Charizard")
    ]

            
            use_funny_name = random.choice([True, False])
            real_name, nickname = random.choice(funny_nicknames if use_funny_name else normal_nicknames)


            #end digits
            num_digits = random.randint(0, 4) #random digits
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
        
        user_descriptions = [user["description"] for user in session_info.users if user.get("description")]

        # Example:
        new_users = [
        NewUser(username=user[0], name=user[1], description=random.choice(user_descriptions) if user_descriptions else "Hello, I'm a bot")
        for user in [username_generator() for _ in range(10)]
        ]
        
        return new_users

    def generate_content(self, datasets_json, users_list):
        posts = []

        influence_target = getattr(datasets_json, "influence_target", "default_topic")


        topic_keywords = []

        if not influence_target or influence_target == "default_topic":
            if hasattr(self, "metadata") and isinstance(self.metadata, dict):
                topics = self.metadata.get("topics", [])
                topic_keywords = [kw for topic in topics if isinstance(topic, dict) for kw in topic.get("keywords", [])]
                influence_target = random.choice(topic_keywords) if topic_keywords else "random_trending"

        #print("Extracted Keywords:", topic_keywords) 

        existing_posts = [post["text"] for post in getattr(datasets_json, "posts", []) if "text" in post]

        for user in users_list:
            post_count = random.randint(10, 15)

            if not self.start_time or not self.end_time:
                session_start = "2024-03-17T00:20:30.000Z"
                session_end = "2024-03-17T00:20:30.000Z"
            else:
                session_start = datetime.fromisoformat(self.start_time.replace("Z", ""))
                session_end = datetime.fromisoformat(self.end_time.replace("Z", ""))


            for _ in range(post_count):
                random_offset = random.uniform(0, (session_end - session_start).total_seconds())
                post_time = session_start + timedelta(seconds=random_offset)
                post_time_str = post_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")

                if existing_posts and random.random() < 0.85:
                    text = random.choice(existing_posts)
                else:
                    keyword = influence_target if random.random() < 0.5 else random.choice(topic_keywords) if topic_keywords else "NO_VALID_TOPICS"
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

                posts.append(NewPost(text=text, author_id=user.user_id, created_at=post_time_str, user=user))

        return posts
