from B4Bot import B4Bot

chatbot = B4Bot(
    'Ron Obvious',
    trainer='trainer.trainers.UbuntuCorpusTrainer'
)

while True:
    fraze=input("You:")
    response = chatbot.get_response(fraze)

    print(response)