from chatterbot import ChatBot
from chatterbot.conversation import Statement

# Create a ChatBot instance
bot = ChatBot('MyBot')

# Function to train the bot based on user feedback
def train_bot(conversation, feedback):
    # Get the user's input statement
    user_input = conversation[-1]

    # Get the bot's response to the user's input
    bot_response = bot.get_response(user_input)

    # Check the feedback provided
    if feedback:
        # If the feedback is positive, mark the bot's response as correct
        bot_response.confidence = 1.0
        print(bot_response.confidence)
        print("Thank you for your positive feedback!")
    else:
        # If the feedback is negative, prompt the user for an alternative response
        new_response = input("Please provide an alternative response: ")

        # Create a new statement with the alternative response
        alternative_response = Statement(text=new_response)

        # Replace the bot's response with the alternative response
        conversation[-1] = alternative_response

        print("Thank you for your feedback. The bot has been trained with an alternative response.")

    # Train the bot with the conversation
    bot.learn_response(user_input, bot_response)

# Example usage
user_input = input("User: ")
conversation = []

while user_input.lower() != 'exit':
    # Append the user's input to the conversation
    conversation.append(Statement(text=user_input))

    # Get the bot's response to the user's input
    bot_response = bot.get_response(user_input)
    print("Bot:", bot_response) 


    # Get user feedback (1 for positive, 0 for negative)
    feedback = int(input("Is the response good? (1 for yes, 0 for no): "))

    # Train the bot based on the conversation and feedback
    train_bot(conversation, feedback)


    user_input = input("User: ")


