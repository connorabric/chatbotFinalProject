import re
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# ---------------------- STOP WORDS ----------------------
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
    "Who is the main character in the movie?",
    "What year was this movie released?",
    "How old is Leonardo's character?",
    "This is new info to add", 
    "how did he get caught", 
    "how much money did he make? "
]

cleaned = clean_training_data(training_data)

for u in user_inputs:
    print("\nUSER:", u)
    print("Question?", is_question(u))
    keywords = clean_sentence(u)
    print("Keywords:", keywords)

    match, score = get_relevance(cleaned, keywords)

    if match:
        print("Best Match:", match["sentence"])
        print("Score:", score)
    else:
        print("I'm sorry, I do not know about this topic.")
