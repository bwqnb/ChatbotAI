# ⢿⣿⣿⣿⣭⠹⠛⠛⠛⢿⣿⣿⣿⣿⡿⣿⠷⠶⠿⢻⣿⣛⣦⣙⠻⣿
# ⣿⣿⢿⣿⠏⠀⠀⡀⠀⠈⣿⢛⣽⣜⠯⣽⠀⠀⠀⠀⠙⢿⣷⣻⡀⢿
# ⠐⠛⢿⣾⣖⣤⡀⠀⢀⡰⠿⢷⣶⣿⡇⠻⣖⣒⣒⣶⣿⣿⡟⢙⣶⣮
# ⣤⠀⠀⠛⠻⠗⠿⠿⣯⡆⣿⣛⣿⡿⠿⠮⡶⠼⠟⠙⠊⠁⠀⠸⢣⣿
# ⣿⣷⡀⠀⠀⠀⠀⠠⠭⣍⡉⢩⣥⡤⠥⣤⡶⣒⠀⠀⠀⠀⠀⢰⣿⣿
# ⣿⣿⡽⡄⠀⠀⠀⢿⣿⣆⣿⣧⢡⣾⣿⡇⣾⣿⡇⠀⠀⠀⠀⣿⡇⠃
# ⣿⣿⣷⣻⣆⢄⠀⠈⠉⠉⠛⠛⠘⠛⠛⠛⠙⠛⠁⠀⠀⠀⠀⣿⡇⢸
# ⢞⣿⣿⣷⣝⣷⣝⠦⡀⠀⠀⠀⠀⠀⠀⠀⡀⢀⠀⠀⠀⠀⠀⠛⣿⠈
# ⣦⡑⠛⣟⢿⡿⣿⣷⣝⢧⡀⠀⠀⣶⣸⡇⣿⢸⣧⠀⠀⠀⠀⢸⡿⡆
# ⣿⣿⣷⣮⣭⣍⡛⠻⢿⣷⠿⣶⣶⣬⣬⣁⣉⣀⣀⣁⡤⢴⣺⣾⣽⡇
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
from chatterbot.logic import BestMatch
from chatterbot.response_selection import get_most_frequent_response
from chatterbot.response_selection import get_random_response


def get_user_feedback():
    feedback = int(input("Is the response good? (1 for yes, 0 for no): "))
    if feedback == 0:
        weight = float(input("Enter the weight to influence the response (0.0 - 1.0): "))
    else:
        weight = 1.0
    return feedback, weight


chatbot = ChatBot(
    'My Chatbot',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand.', 
            'maximum_similarity_threshold': 0.90, # accounts for some typos
            # 'response_selection_method': 'get_random_response'

        }
    ]
     
)

trainer = ListTrainer(chatbot)


trainer.train([
    'Hi',
    'Hello',
    'Greetings',
    'Salutations',
    'Aloha',
    'Bonjour'
])
trainer.train([
    'What is the ship date of my order?',
    '06/30/2002'
    # most likely will have to create a function that calls the most recent update of a database/data then finds the ID # and fetches the ship date of the order
])
trainer.train([ 
    'What is the tracking number of my order?',
    '312319785'
    # most likely will have to create a function that calls the most recent update of a database/data then finds the ID # and fetches the tracking number of the order
])
trainer.train([
    'Do you have this item in stock?',
    'Yes, we currently have that available'
    # most likely will have to fetch this from supply data
])
trainer.train([
    'Do you have this item in stock?',
    'No, it is not available'
    # most likely will have to fetch this from supply data
])
trainer.train([
    'What is the estimate freight for my order?',
    '3 lb'
    # most likely will have to fetch this from supply data
])
trainer.train([
    'I need a copy of invoice.',
    'Here is a copy of the invoice.'
    # ?
])
trainer.train([
    'Okay Thanks',
    'No Problem! Have a Good Day!'
])
trainer.train([
    'Thank you',
    'No Problem! Have a Good Day!'
])
trainer.train([
    'What is the price of the product?',
    '$3'
    # most likely will have to fetch this from supply data
])
trainer.train([
    'Did you receive my order?',
    'Yes, we received the order'
    # most likely will have to fetch this from supply data
])
trainer.train([
    'Did you receive my order?',
    'No, we did not receive the order'
    # most likely will have to fetch this from supply data
])
trainer.train([
    'Please send me product samples.',
    'Okay, retrieving product samples'
    # ?
])
trainer.train([
    'What is your production lead time?',
    '9-5:30'
    # ?
])
trainer.train([
    'Can you meet my in hand date?',
    'Yes, we have time'
    # ?
])
trainer.train([
    'Can you meet my in hand date?',
    'No, we do not have time'
    # ?
])

exit_conditions = (":q", "quit", "exit", "Bye", "bye", "gnight", "good night", "byebye", "ciao")
name = input("Enter Your Name: ")
print("You are now connected with the AI ChatBot.")
while True:
    request = input("> ")
    # query = input(name + ": ")
    if request in exit_conditions:
        print('> Bye')                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
        break
    else:
        bot_response = chatbot.get_response(request)
        print(f"> {bot_response}")
        feedback, weight = get_user_feedback()

        if feedback == 0:
            alternative_response = input("Please provide an alternative response: ")

            # Train the bot with the user input and alternative response
            trainer.train([
                request,
                alternative_response
            ])

            # Decrease confidence for wrong answer
            bot_response.confidence *= weight

        else:
            # Increase confidence for correct answer
            bot_response.confidence *= 1.0 
            # chatbot.get_response("Hello, how are you today?")