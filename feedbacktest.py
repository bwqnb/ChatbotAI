from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

# Create a ChatBot instance
bot = ChatBot('MyBot')

# Create a ListTrainer
trainer = ListTrainer(bot)

# Function to get user feedback and weight
def get_user_feedback():
    feedback = int(input("Is the response good? (1 for yes, 0 for no): "))
    if feedback == 0:
        weight = float(input("Enter the weight to influence the response (0.0 - 1.0): "))
    else:
        weight = 1.0
    return feedback, weight

# Conversation loop
while True:
    # Get user input
    user_input = input("User: ")

    # Get bot's response
    bot_response = bot.get_response(user_input)
    print("Bot:", bot_response)

    # Prompt user for feedback and weight on the bot's response
    feedback, weight = get_user_feedback()

    if feedback == 0:
        alternative_response = input("Please provide an alternative response: ")

        # Train the bot with the user input and alternative response
        trainer.train([
            user_input,
            alternative_response
        ])

        # Decrease confidence for wrong answer
        bot_response.confidence *= weight

    else:
        # Increase confidence for correct answer
        bot_response.confidence *= 1.0

    if user_input.lower() == 'bye':
        break
