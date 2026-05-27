def build_initial_story_prompt(choice, age, personality, interests, reason):
    prompt = (
        f"You are a future-oriented news writer for a cinematic alternate universe. "
        f"A user asks: '{choice}' and provides age {age}, personality traits '{personality}', "
        f"interests '{interests}', and reason '{reason}'. "
        "Write a believable future news headline and a 20-line article that reads like a human newspaper feature. "
        "Include how life changed, struggles, successes, relationships, career progression, and emotional moments. "
        "Make the tone immersive, emotional, futuristic, and grounded in cause-and-effect storytelling. "
        "Do not write fantasy. Keep the world plausible and reflective of the user's alternate choice. "
        "Return the answer in this exact JSON structure with no extra explanation:\n"
        "{\n  \"headline\": \"...\",\n  \"article\": \"...\"\n}\n"
    )
    return prompt


def build_continuity_story_prompt(previous_story, next_age):
    prompt = (
        f"Continue the same alternate universe 10 years after this news entry. "
        f"Previous headline: '{previous_story['headline']}'. Previous article summary: '{previous_story['article'][:320]}'. "
        f"Current age was {previous_story['age']}, now age {next_age}. "
        "Keep the same core career path, emotional themes, and relationships. "
        "Produce a new future headline and a new 20-line article that shows growth, aging, achievements, obstacles, "
        "and continuity of personality. Mention how the earlier choice shaped this next stage. "
        "Return only a JSON object with keys 'headline' and 'article'."
    )
    return prompt


def build_image_prompt(choice, current_age, personality, interests, future_age=None, continuity=False):
    age_description = f"now {future_age}" if future_age else f"around {current_age}"
    timeline_note = "Continuing the same universe with deeper emotional maturity." if continuity else "A first glimpse into a new alternate future."
    prompt = (
        f"Cinematic, realistic portrait of a person in a futuristic setting. "
        f"This image represents the alternate future of someone who chose: '{choice}'. "
        f"They are {age_description} years old, with '{personality}' energy and interests in '{interests}'. "
        f"Use emotional lighting, futuristic city reflections, and a grounded, cinematic mood. "
        f"The image should feel like a glossy future newspaper cover photo with depth, human warmth, and a strong sense of possibility. "
        f"{timeline_note}"
    )
    return prompt
