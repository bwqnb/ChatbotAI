from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

def provide_feedback(user_input, bot_response, is_good):
    bot = ChatBot('MyBot')

    if is_good:
        bot.learn_response(bot_response, user_input)
    else:
        bot.learn_response('I apologize. I will try to improve.', user_input)

# Create ChatBot instance
bot = ChatBot('MyBot')

# Train the bot
trainer = ChatterBotCorpusTrainer(bot)
trainer.train("chatterbot.corpus.english")

# Provide feedback
user_input = "Hello"
bot_response = bot.get_response(user_input)
is_good = False

provide_feedback(user_input, bot_response.text, is_good)
