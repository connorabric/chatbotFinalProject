#this is the main file

with open("/Users/connorabric/Documents/trainingdata.txt", "r") as file:
    training_data = file.read()
    print(training_data)

question_words = ['who', 'what', 'when', 'where', 'why', 'how']

def locate_questions_words(training_data):
    words = training_data.lower().split()
    word_counts = {}

    for word in words:
        if word in question_words:
            word_counts[word] = word_counts.get(word, 0) + 1

    print(word_counts)


locate_questions_words(training_data)