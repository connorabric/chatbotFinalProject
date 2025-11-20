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
# same as the clean trainging data function
def clean_sentence(user):
    userInput = user.lower()
    sentence = re.sub(r"[^\w\s]", "", userInput).strip()
    words = sentence.split()
    keywords = [w for w in words if w not in stop_words]


    return keywords
# cleans the 3000 words we are trainging it on, breaks into sentences and stores in map
def clean_training_data(training_data):
    parts = [p.strip() for p in training_data.split("|") if p.strip()]

    cleaned_data = []

    # Process every group of 3
    for i in range(0, len(parts), 3):
        sentence = parts[i]
        keywords = parts[i+1]
        questions = parts[i+2]

        cleaned_data.append({
            "sentence": sentence,
            "keywords": [k.strip() for k in keywords.split(",")],
            "questions": [q.strip() for q in questions.split(",")]
        })

    for item in cleaned_data:
        print(item)

    print(cleaned_data)
    return cleaned_data





question_words = ['who', 'what', 'when', 'where', 'why', 'how']
# finds the question words 
def locate_questions_words(training_data):
    words = training_data.lower().split()
    word_counts = {}

    for word in words:
        if word in question_words:
            word_counts[word] = word_counts.get(word, 0) + 1

    print(word_counts)

# determines if its a question or not (still needs work)
def is_question(userInput):
    userInput = userInput.lower().split(" ")
    if "?" in userInput:
        return True
    for word in userInput:
        if word in question_words:
            return True
    return False

 #this function will loop through the cleaned data and give a score based on the keywords passed in from the input
def get_relevance(cleaned_data, keywords):
    
    return




userInput = ['Who is the main character in the movie?',
            'What year was this movie release?',
            'How old is Leonardos characer', 
            'This is new info to add']

print(is_question(userInput[0]), clean_sentence(userInput[0]))

print(clean_training_data(training_data))