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

question_words = ['who', 'what', 'when', 'where', 'why', 'how', 'do', 'does', 'if', "which"]

# ---------------------- DATA LOADING ----------------------
# with open("/Users/connorabric/Documents/trainingdata.txt", "r") as file:
#     training_data = file.read()

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
                keywords.append(token.lemma_.lower())
    
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
    return best_item["sentence"] if best_score > 10 else None

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
        
        
        #Determines if question is the same
        same = is_same_question(msg)
        if same:
            answer = same + get_relevance(cleaned_data, keywords, question_type, msg) # Use simplified relevance matching
            return answer
        
        answer = get_relevance(cleaned_data, keywords, question_type, msg) # Use simplified relevance matching
        return answer or "I'm not sure, but I'll learn more soon!"
    
    return None

# ---------------------- NEW INFO ----------------------
def is_new_info(msg):
    if msg.lower() == "testing":
        return "Got it! Added new info."
    return None

# ---------------------- PREPROCESS ----------------------
def preprocess(msg):
    msg = correct_spelling(msg)
    msg = replace_synonyms(msg)
    return msg

# ---------------------- IS SAME QUESTION ----------------------
last_question = None
times_repeated = 0

def is_same_question(msg):
    global last_question
    global times_repeated

    # Determines if the question is the same as the last_question
    if msg == last_question:
        times_repeated += 1
    else:
        last_question = msg
        times_repeated = 0
        return
    
    # Determines the number of times asked and answers differently based on how many times asked
    if times_repeated == 1:
        return "I have already responded to this question, but to satisfy your curiosity, "
    elif times_repeated > 1:
        return f"I have answered this {times_repeated} times already, but to satisfy your curiosity, "

# ---------------------- MAIN BOT RESPONSE ----------------------
def bot_response(msg):
    if not msg or not msg.strip():
        return "Please type a question or message."
    
    msg = preprocess(msg)

    greeting = check_greeting(msg)
    if greeting:
        return greeting

    answer = is_question(msg)
    if answer:
        return answer

    new_info_response = is_new_info(msg)
    if new_info_response:
        return new_info_response

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

if __name__ == "__main__":
    answer = bot_response("how old is leonardo?")
    print(answer)
    answer = bot_response("how old is leonardo?")
    print(answer)  
    answer = bot_response("how old is leonardo?")
    print(answer)
    answer = bot_response("how old is leonardo?")
    print(answer)