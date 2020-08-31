class Rhyme:
    
    rhyme = ""
    word = ""
    
    def __init__(self, word, rhyme):
        self.word = word
        self.rhyme = rhyme

        
class MasterOfCeremony:

    rhymes = [
        Rhyme("да", "пизда"),
        Rhyme("нет", "пидора ответ"),
    ]
    
    async def execute(self, message):
        for rhyme in self.rhymes:
            if message.content.lower().endswith(rhyme.word):
                await message.channel.send(rhyme.rhyme)