#this is the main file
import re

stop_words = [
    "a", "an", "the", "and", "or", "but",
    "if", "then", "else",
    "is", "am", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "having",
    "do", "does", "did", "doing","in", "on", "at", "to", "from", "by", "with", "about", "over", 
    "under","for", "of", "off", "up", "down","he", "she", "it", "they", "them", "his", "her", "their",
    "its","you", "your", "me", "my", "mine", "we", "our", "us","this", "that", "these", "those","as",
    "so", "such", "than", "too","can", "could", "shall", "should", "will", "would",
    "may", "might", "must","not", "no", "nor","just","only","really","very","maybe", "probably", "literally", "basically",
    "actually", "simply", "kind", "kindof", "sort", "sortof", "things",
    "stuff", "thing", "anyway", "almost", "mostly", "often", "sometimes",
    "somehow", "somewhat", "slightly", "pretty", "quite", "rather", "even",
    "else", "yet", "already", "around", "back", "away", "together",
    "throughout", "across", "within", "without", "between", "among",
    "toward", "towards", "along", "though", "although", "perhaps",
    "however", "meanwhile", "overall", "further", "furthermore",
    "additionally", "besides", "therefore", "thus"
]





with open("/Users/connorabric/Documents/trainingdata.txt", "r") as file:
    training_data = file.read()

def clean_sentence(user):
    userInput = user.lower()
    sentence = re.sub(r"[^\w\s]", "", userInput).strip()
    words = sentence.split()
    keywords = [w for w in words if w not in stop_words]


    return keywords

def clean_training_data(training_data):
    sentences = training_data.lower().split(".")
    cleaned_data = []

    for s in sentences:
        # Remove punctuation
        sentence = re.sub(r"[^\w\s]", "", s).strip()
        if not sentence:
            continue

        # Extract keywords (non-stopwords)
        words = sentence.split()
        keywords = [w for w in words if w not in stop_words]

        # Store this sentence and its keywords
        cleaned_data.append({
            "sentence": sentence,
            "keywords": keywords
        })

    print(cleaned_data)
    return cleaned_data





question_words = ['who', 'what', 'when', 'where', 'why', 'how']

def locate_questions_words(training_data):
    words = training_data.lower().split()
    word_counts = {}

    for word in words:
        if word in question_words:
            word_counts[word] = word_counts.get(word, 0) + 1

    print(word_counts)

def is_question(userInput):
    userInput = userInput.lower().split(" ")
    if "?" in userInput:
        return True
    for word in userInput:
        if word in question_words:
            return True
    return False





userInput = ['Who is the main character in the movie?',
            'What year was this movie release?',
            'How old is Leonardos characer', 
            'This is new info to add']

print(is_question(userInput[0]), clean_sentence(userInput[0]))

# print(clean_training_data(training_data))