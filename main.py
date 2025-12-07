import re
import spacy

nlp = spacy.load("en_core_web_sm")

# ---------------------- STOP WORDS, SYNONYMS, MISSPELLED WORDS, ETC----------------------
stop_words = [
    "a", "an", "the", "and", "or", "but",
    "if", "then", "else",
    "is", "am", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "having",
    "do", "does", "did", "doing", "in", "on", "at", "to", "from", "by", "with",
    "about", "over", "under", "for", "of", "off", "up", "down",
    "he", "she", "it", "they", "them", "his", "her", "their", "its",
    "you", "your", "me", "my", "mine", "we", "our", "us",
    "this", "that", "these", "those",
    "as", "so", "such", "than", "too",
    "can", "could", "shall", "should", "will", "would",
    "may", "might", "must",
    "not", "no", "nor",
    "just", "only", "really", "very",
    "maybe", "probably", "literally", "basically",
    "actually", "simply",
    "things", "stuff", "thing"
]

misspellings = {
    "the": ["teh", "thhe", "tah"],
    "here": ["heer", "her", "hre"],
    "there": ["ther", "thare", "thre"],
    "and": ["adn", "nad", "annd"],
    "for": ["fro", "fr", "foor"],
    "you": ["yuo", "yoou", "u"],
    "with": ["wiht", "wth", "wihth"],
    "that": ["taht", "tht", "thaat"],
    "was": ["wsa", "ws", "waas"],
    "have": ["hav", "hvae", "haev"],
    "play": ["plaay", "paly", "plae", "plai"],
    "actor": ["akctor", "actorr", "acter", "actr"],
    "movie": ["moovie", "movvie", "movi", "movve"],
    "watch": ["wahtch", "wach", "wathc", "wotch"],
    "film": ["flim", "fliim", "filmm", "falm"],
    "role": ["rol", "rolle", "roel", "rolle"],
    "scene": ["sceen", "scnee", "sene", "scen"],
    "director": ["direktor", "dirctor", "directer", "direcor"],
    "performance": ["performence", "perfomance", "performnce", "performnce"],
    "award": ["awrd", "awrad", "aword", "aword"],
}

synonyms = {
    "play": ["plays", "played", "portrays", "acts", "depicts"],
    "role": ["roles", "character", "part", "portrayal", "persona"],
    "catch": ["pursue", "chase", "apprehend", "hunt", "track"],
    "caught": ["captured", "arrested", "apprehended", "capture"],
    "money": ["cash", "dollars", "million", "amount"],
    "steal": ["stole", "stolen", "forged", "fraud"],
    "old": ["age", "aged"],
    "released": ["premiered", "launched"],
}

greetings = {
    "hi": "Hello! Great to see you.",
    "hello": "Hi there! Welcome.",
    "hey": "Hey! Nice to have you here.",
    "good morning": "Good morning! Wishing you a bright day.",
    "good afternoon": "Good afternoon! Hope your day is going well.",
    "good evening": "Good evening! Glad you're here.",
    "hey there": "Hey there! Nice to see you.",
    "what's up": "Not much! Glad you're here.",
    "howdy": "Howdy! Wishing you a good day.",
    "greetings": "Greetings! Happy to have you here.",
    "yo": "Yo! Great to see you.",
    "hiya": "Hiya! Nice to connect.",
    "sup": "Sup! Glad you're here.",
    "hello there": "Hello there! Great to have you here.",
    "morning": "Morning! Wishing you a good day.",
    "afternoon": "Afternoon! Hope your day is going well.",
    "evening": "Evening! Great to have you here.",
}

question_words = ['who', 'what', 'when', 'where', 'why', 'how']

last_question = {
    "question" : None,
    "keywords" : [],
}


# ---------------------- DATA LOADING ----------------------
with open("/Users/Tanner/Documents/trainingdata.txt", "r") as file:
    training_data = file.read()

# ---------------------- CLEAN TRAINING DATA ----------------------
def clean_training_data(training_data):
    lines = training_data.strip().split("\n")
    cleaned_data = []
    
    for line in lines:
        parts = [p.strip() for p in line.split("|") if p.strip()]
        if len(parts) >= 3:
            sentence = parts[0]
            keywords_raw = parts[1]
            questions_raw = parts[2]
            
            # Keep keywords as-is (lowercase and split)
            keyword_list = [k.strip().lower() for k in keywords_raw.split(",")]
            
            cleaned_data.append({
                "sentence": sentence,
                "sentence_lower": sentence.lower(),
                "keywords": keyword_list,
                "questions": [q.strip().lower() for q in questions_raw.split(",")]
            })
    
    return cleaned_data

cleaned_data = clean_training_data(training_data)

# ---------------------- CLEAN SENTENCE ----------------------
def clean_sentence(user_input):
    """Extract meaningful keywords from user input"""
    doc = nlp(user_input)
    keywords = []
    
    # Get lemmatized keywords
    for token in doc:
        if token.is_alpha and token.lemma_ not in stop_words:
            if token.pos_ in ["NOUN", "PROPN", "ADJ", "VERB", "NUM"]:
                # Keep original form for "caught" to preserve meaning
                if token.text.lower() in ["caught", "arrested", "captured"]:
                    keywords.append(token.text.lower())
                else:
                    keywords.append(token.lemma_.lower())
    
    # Add multi-word phrases for better matching
    text_lower = user_input.lower()
    if "get caught" in text_lower or "got caught" in text_lower:
        keywords.append("get-caught")
    if "where" in text_lower and "caught" in text_lower:
        keywords.append("where-caught")
    
    return keywords

# ---------------------- CHECK GREETING ----------------------
def check_greeting(msg):
    msg = msg.strip().lower()
    msg = re.sub(r'[^a-zA-Z ]', '', msg)
    return greetings.get(msg)

# ---------------------- SPELLING ----------------------
def correct_spelling(msg):
    words = msg.split()
    corrected = []
    for w in words:
        found = False
        for key, variants in misspellings.items():
            if w.lower() in variants:
                corrected.append(key)
                found = True
                break
        if not found:
            corrected.append(w)
    return " ".join(corrected)

# ---------------------- SYNONYMS ----------------------
def replace_synonyms(msg):
    words = msg.split()
    replaced = []
    for w in words:
        replaced_word = w
        for key, syn_list in synonyms.items():
            if w.lower() in syn_list or w.lower() == key:
                replaced_word = key
                break
        replaced.append(replaced_word)
    return " ".join(replaced)

# ---------------------- EQUIVALENT WORDS ----------------------
def equivalent_words(word):
    """Get all equivalent forms of a word"""
    out = {word}
    for key, syn_list in synonyms.items():
        if word == key or word in syn_list:
            out.add(key)
            out.update(syn_list)
    return out

# ---------------------- SIMPLIFIED RELEVANCE MATCHING ----------------------
def get_relevance(cleaned_data, keywords, question_type=None, original_text=""):
    """Simple matching based on keyword overlap - no hardcoded logic!"""
    best_item = None
    best_score = 0

    for item in cleaned_data:
        score = 0
        
        # 1. Question type match
        if question_type and question_type in item["questions"]:
            score += 15
        
        # 2. Check if any user keywords match item keywords
        for user_kw in keywords:
            # Get all equivalent forms of the user's keyword
            equiv = equivalent_words(user_kw)
            
            # Check against all item keywords
            for item_kw in item["keywords"]:
                for e in equiv:
                    # Match if keyword contains or is contained
                    if e in item_kw or item_kw in e:
                        score += 10
                        break
        
        # 3. Check if keywords appear in the actual sentence
        for user_kw in keywords:
            equiv = equivalent_words(user_kw)
            for e in equiv:
                if e in item["sentence_lower"]:
                    score += 5
                    break

        if score > best_score:
            best_score = score
            best_item = item

    # Return answer if score is high enough
    # Increased threshold to avoid matching unrelated questions
    return best_item["sentence"] if best_score > 25 else None

# ---------------------- IS SAME QUESTION ----------------------
times_repeated = 0

def is_same_question(msg, keywords):
    """Track repeated questions and provide varied responses"""
    # global last_question
    global times_repeated

    # Determines if the question is the same as the last_question
    if msg == last_question["question"]:
        times_repeated += 1
    else:
        last_question["question"] = msg
        last_question["keywords"] = keywords
        times_repeated = 0
        return None
    
    # Determines the number of times asked and answers differently based on how many times asked
    if times_repeated == 1:
        return "I have already responded to this question, but to satisfy your curiosity, "
    elif times_repeated > 1:
        return f"I have answered this {times_repeated} times already, but to satisfy your curiosity, "
    
    return None

# ---------------------- IS FOLLOW-UP QUESTION ----------------------
def is_follow_up(msg):
    # Uses list instead of Spacy for more strict searching
    pronouns = ["he", "him", "his", "she", "her", "hers", "they", "them", "their", "theirs", "it", "its", "that", "this","these","those"]
    context_words = ["also", "too", "additionally", "furthermore"]
    context_phrases = ["what about", "how about", "tell me more"]

    msg = msg.lower().replace("?", "")
    if any(phrase in msg for phrase in context_phrases):
        return True

    doc = nlp(msg)
    
    # Check if message has:
    # 1. Pronouns w/o any proper nouns OR
    # 2. Pronouns before any proper nouns OR
    # 3. Any context words
    has_proper_noun = False
    for token in doc:
        if token.text.lower() in pronouns and has_proper_noun is False:
            return True
        elif token.pos_ == "PROPN":
            has_proper_noun = True
        elif token.text.lower() in context_words:
            return True

    return False

# ---------------------- QUESTION DETECTION ----------------------
def is_question(msg):
    text = msg.lower().strip()
    
    if text.endswith("?") or (len(text.split()) > 0 and text.split()[0] in question_words):
        # Extract question type
        question_type = None
        words = text.replace("?", "").split()
        if words and words[0] in question_words:
            question_type = words[0]
        
        # Get keywords from the question
        keywords = clean_sentence(msg)

        # Check if this is a follow-up question
        if is_follow_up(msg) and last_question["keywords"]:
            search_keywords = keywords + last_question["keywords"]
        else:
            search_keywords = keywords
        
        # Check if this is a repeated question
        same_question_prefix = is_same_question(msg, search_keywords)
        
        # Get the answer
        answer = get_relevance(cleaned_data, search_keywords, question_type, msg)

        
        # If it's a repeated question and we have an answer, add the prefix
        if same_question_prefix and answer:
            return same_question_prefix + answer
        
        return answer or "I'm not sure, but I'll learn more soon!"
    
    return None

# ---------------------- NEW INFO DETECTION ----------------------
def is_new_info(msg):
    text = msg.lower().strip()
    if len(text.split()) < 5:
        return None
    
    doc = nlp(text)
    
    has_subject = False
    has_verb = False
    has_object_or_complement = False
    
    for token in doc:
        if token.dep_ in ["nsubj", "nsubjpass"]:  # Subject
            has_subject = True
        if token.pos_ == "VERB":  # Verb
            has_verb = True
        if token.dep_ in ["dobj", "attr", "prep", "acomp"]:  # Object/complement
            has_object_or_complement = True
    
    is_declarative = has_subject and has_verb and has_object_or_complement
    
    if not is_declarative:
        return None
    
    has_entities = len(doc.ents) > 0
    has_proper_nouns = any(token.pos_ == "PROPN" for token in doc)
    
    if has_entities or has_proper_nouns:
        return add_new_info(msg)
    
    return None


def add_new_info(msg):
    doc = nlp(msg) 
    basic_keywords = clean_sentence(msg) 
    entities = [ent.text.lower() for ent in doc.ents] 
    noun_chunks = [chunk.text.lower() for chunk in doc.noun_chunks]
    compound_keywords = []
    
    subjects = [token.text.lower() for token in doc if token.dep_ in ["nsubj", "nsubjpass"]]
    verbs = [token.lemma_.lower() for token in doc if token.pos_ == "VERB"]
    objects = [token.text.lower() for token in doc if token.dep_ in ["dobj", "pobj", "attr"]]
    locations = [token.text.lower() for token in doc if token.dep_ == "prep" and token.head.pos_ == "VERB"]
    
    for subj in subjects:
        for verb in verbs:
            compound_keywords.append(f"{subj}-{verb}")
            for obj in objects:
                compound_keywords.append(f"{subj}-{verb}-{obj}")
        for obj in objects:
            compound_keywords.append(f"{subj}-{obj}")
        for loc in locations:
            compound_keywords.append(f"{subj}-{loc}")
    
    all_keywords = list(set(basic_keywords + entities + noun_chunks + compound_keywords))
    
    question_types = ["what"]  # Default
    
    if any(token.lemma_ in ["play", "act", "perform", "portray"] for token in doc):
        question_types.append("who")
    if any(ent.label_ in ["DATE", "TIME"] for ent in doc.ents):
        question_types.append("when")
    if any(ent.label_ in ["GPE", "LOC", "FAC"] for ent in doc.ents) or any(token.dep_ == "prep" for token in doc):
        question_types.append("where")
    if any(token.lemma_ in ["because", "cause", "reason", "since"] for token in doc):
        question_types.append("why")
    if any(token.lemma_ in ["by", "use", "method", "way", "through"] for token in doc):
        question_types.append("how")
    
    new_entry = {
        "sentence": msg,
        "sentence_lower": msg.lower(),
        "keywords": all_keywords,
        "questions": question_types
    }
    
    cleaned_data.append(new_entry)
    
    try:
        with open("/Users/connorabric/Documents/trainingdata.txt", "a") as f:
            keyword_str = ", ".join(all_keywords)
            question_str = ", ".join(question_types)
            f.write(f"\n{msg} | {keyword_str} | {question_str} |")
        return f"Thanks! I learned: '{msg}'. I'll remember that!"
    except Exception as e:
        return f"Got it! I learned: '{msg}' (stored in memory for this session)"

# ---------------------- PREPROCESS ----------------------
def preprocess(msg):
    msg = correct_spelling(msg)
    msg = replace_synonyms(msg)
    return msg

# ---------------------- MAIN BOT RESPONSE ----------------------
def bot_response(msg):
    if not msg or not msg.strip():
        return "Please type a question or message."
    
    msg = preprocess(msg)

    # 1. Check for greetings
    greeting = check_greeting(msg)
    if greeting:
        return greeting

    # 2. Check for questions
    answer = is_question(msg)
    if answer:
        return answer

    # 3. Check for new information (before fallback)
    new_info_response = is_new_info(msg)
    if new_info_response:
        return new_info_response

    # 4. Default fallback
    return "Sorry, I am not sure about this. Is there something else you would like to ask?"

# ---------------------- TEST ----------------------
# if __name__ == "__main__":
#     user_inputs = [
#         "how old is leonardo?",
#         "how old is frank?",
#         "when was the movie released?",
#         "who is carl?",
#         "how much money was stolen?",
#         "how did frank get caught?",
#         "how did carl find him?",
#         "why did frank run away?",
#         "who plays the main character?"
#     ]
    
#     print("Testing simplified chatbot:\n")
#     for test_input in user_inputs:
#         response = bot_response(test_input)
#         print(f"Q: {test_input}")
#         print(f"A: {response}\n")

test_questions_1 = [
    "Who plays Frank in Catch Me If You Can?",
    "How old is Frank?",
    "Who does Tom Hanks play?"
    "What did Tom Hanks base his accent on?"
]

test_questions_2 = [
    "Who plays Frank in Catch Me If You Can?",
    "How old is he?",  # Follow-up: "he" = Leonardo
    "Who does Tom Hanks play?",
    "What did he base his accent on?"
]

print("Testing simplified chatbot:\n")
for test_input in test_questions_1:
    response = bot_response(test_input)
    print(f"Q: {test_input}")
    print(f"A: {response}\n")

print("-------------------------------------------------------")

for test_input in test_questions_2:
    response = bot_response(test_input)
    print(f"Q: {test_input}")
    print(f"A: {response}\n")
