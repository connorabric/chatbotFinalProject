import re
import spacy

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
    "becomes" : ['becoms', 'becames', 'becums','becmoes', 'becmes', 'becones','becemose','becimes','becames','becoems'],
    "frank" : ['frnak','fank','frnk','frark','frannk','frnak','fraank','frak','frnka'],
    "emotional" : ['emitional','emotinal','emmotional','emocional','emmotianal','emotionel','emotionnal','emtionel','emoiotnal','emontional'],
    "hanratty" : ['hanraty','hanratti','hanrattey','hanrattty','hanratly','hanarty','hanrattyy','hanrattye','harnatty','hanrarty'],
    "who" : ['woh','wgo','wh','wo','wjo','whp','whi','wuo'],
    "film" : ['flim','filim','filnm','fllm','filn','fliim','filmm','filim','fllim','filsm'],
    "life" : ['lfie','lfe','lif','liife','lifr','lifee','liffe','liife','lifd','lifw'],
    "identity" : ['identity','identitiy','idenety','idnentity','identiy','identiyt','identity','ideeity'],
    "father" : ['fater','fahter','fther','fathar','fathe','fgather','fatherr','faterh','faterj','fathre','fagher'],
    "even" : ['evan','evn','eeven','eevn','evem','efen','eben','evne','evem','eveb'],

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

question_words = ['who', 'what', 'when', 'where', 'why', 'how', 'do', 'does', 'if', "which"]

# ---------------------- DATA LOADING ----------------------
with open("/Users/connorabric/Documents/trainingdata.txt", "r") as file:
    training_data = file.read()
# ---------------------- CLEAN SENTENCE ----------------------
def clean_sentence(user_input):
    doc = nlp(user_input)
    keywords = [token.lemma_.lower() for token in doc 
                if token.is_alpha and token.lemma_ not in stop_words and token.pos_ in ["NOUN","PROPN","ADJ","VERB"]]
    return keywords
# ---------------------- CLEAN TRAINING DATA ----------------------
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

cleaned_data = clean_training_data(training_data)  # Clean once

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

# ---------------------- RELEVANCE ----------------------
def get_relevance(cleaned_data, keywords):
    best_item = None
    best_score = 0
    for item in cleaned_data:
        score = sum(2 for kw in keywords if kw in item["keywords"])
        if score > best_score:
            best_score = score
            best_item = item
    if best_item:
        return best_item["sentence"]
    return None

# ---------------------- QUESTION DETECTION ----------------------
def is_question(msg):
    text = msg.lower().strip()
    print()
    if text.endswith("?") or text.split()[0] in question_words:
        print("made it")
        keywords = clean_sentence(msg)
        print(keywords)
        return get_relevance(cleaned_data, keywords) or "I'm not sure, but I'll learn more soon!"
    return None

# ---------------------- NEW INFO ----------------------
def is_new_info(msg):
    # Placeholder: logic to learn new facts
    if msg.lower() == "testing":
        return "Got it! Added new info."
    return None

# ---------------------- PREPROCESS ----------------------
def preprocess(msg):
    msg = correct_spelling(msg)
    msg = replace_synonyms(msg)
    return msg

# ---------------------- MAIN BOT RESPONSE, THIS IS THE MAIN LOGIC ----------------------
def bot_response(msg):
    tester = False  
    msg = preprocess(msg)

    greeting = check_greeting(msg)
    if greeting:
        tester = True
        return greeting

    answer = is_question(msg)
    if answer:
        tester = True
        return answer

    new_info_response = is_new_info(msg)
    if new_info_response:
        tester = True
        return new_info_response

    if not tester:
        return "Sorry, I am not sure about this. Is there something else you would like to ask?"


# ---------------------- TEST ----------------------
user_inputs = [
    "Who is teh main character in the movvie?",
    "What year was this movie released?",
    "How old is Leonardo's character?",
    "This is new info to add", 
    "how did he get caught", 
    "how much money did he make?"
]


