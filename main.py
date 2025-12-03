import re
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# ---------------------- STOP WORDS, SYNONYMS, MISSPELLED WORDS----------------------
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

# Common misspellings including everyday and movie-related words
misspellings = {
    # everyday words
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
    "catch": ["pursue", "chase", "apprehend", "hunt", "track down"],
    "fool": ["deceive", "trick", "outsmart", "beguile", "mislead"],
    "forgery": ["counterfeit", "fake", "falsification", "fraud", "replica"],
    "flight": ["plane ride", "aviation", "air travel", "airline", "pilot journey"],
    "investigate": ["investigates", "investigated", "investigating", "look into", "probe"],
    "lawyer": ["attorney", "counsel", "legal advisor", "advocate", "solicitor"],
    "detective": ["agent", "investigator", "officer", "FBI agent", "sleuth"],
    "escape": ["escapes", "evades", "flee", "run away", "get away"],
}

# Basic greetings dictionary with shorter statements
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
    "hiya friend": "Hiya friend! Always nice to see you.",
    "hey buddy": "Hey buddy! Glad you're around.",
    "hi everyone": "Hi everyone! Wonderful to see you all.",
    "morning": "Morning! Wishing you a good day.",
    "afternoon": "Afternoon! Hope your day is going well.",
    "evening": "Evening! Great to have you here.",
}



question_words = ['who', 'what', 'when', 'where', 'why', 'how']

# ---------------------- DATA LOADING ----------------------
with open("/Users/connorabric/Documents/trainingdata.txt", "r") as file:
    training_data = file.read()

# ---------------------- CLEAN SENTENCE W/ SPACY ----------------------
def clean_sentence(user_input):
    doc = nlp(user_input)

    keywords = []
    for token in doc:
        if token.is_alpha and token.lemma_ not in stop_words:
            if token.pos_ in ["NOUN", "PROPN", "VERB"]:  
                keywords.append(token.lemma_.lower())

    return keywords
# ------------------------- CHECK SPELLING -------------------------
def check_spelling(user_input):
    words = user_input.split(" ")
    for word in words:
        for k,v in misspellings.items():
            for w in v:
                if word == w:
                    words.remove(word)
                    print(word)
                    word = k
                    words.append(word)
                    print("New", word)
    print(words)

    return

# ---------------------- FORMAT TRAINING DATA ----------------------
def clean_training_data(training_data):
    parts = [p.strip() for p in training_data.split("|") if p.strip()]
    cleaned_data = []

    for i in range(0, len(parts), 3):
        sentence = parts[i]
        keywords = parts[i+1]
        questions = parts[i+2]

        keyword_list = []
        for k in keywords.split(","):
            k = k.strip()
            cleaned = clean_sentence(k)
            keyword_list.extend(cleaned)

        cleaned_data.append({
            "sentence": sentence,
            "keywords": keyword_list,
            "questions": [q.strip() for q in questions.split(",")]
        })

    return cleaned_data

# ---------------------- QUESTION DETECTION ----------------------
def is_question(user_input):
    lower = user_input.lower().strip()
    if lower.endswith("?"):
        return True
    if lower.split()[0] in question_words:
        return True
    return False

# ---------------------- RELEVANCE SYSTEM ----------------------
def get_relevance(cleaned_data, keywords):

    best_item = None
    best_score = 0

    for item in cleaned_data:
        score = 0

        for kw in keywords:
            if kw in item["keywords"]:
                score += 2      

        # for kw in keywords:
        #     if kw in item["sentence"].lower():
        #         score += 1

        if score > best_score:
            best_score = score
            best_item = item

    return best_item, best_score

# ---------------------- MAIN TEST ----------------------
user_inputs = [
    "Who is teh main character in the movvie",
    "What year was this movie released?",
    "How old is Leonardo's character?",
    "This is new info to add", 
    "how did he get caught", 
    "how much money did he make? "
]

# cleaned = clean_training_data(training_data)

# for u in user_inputs:
#     print("\nUSER:", u)
#     print("Question?", is_question(u))
#     keywords = clean_sentence(u)
#     print("Keywords:", keywords)

#     match, score = get_relevance(cleaned, keywords)

#     if match:
#         print("Best Match:", match["sentence"])
#         print("Score:", score)
#     else:
#         print("I'm sorry, I do not know about this topic.")


print(check_spelling(user_inputs[0]))