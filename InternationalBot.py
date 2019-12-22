from googletrans import Translator

import discord
import translAPI

bot_token = "token-here"


class MyClient(discord.Client):

    def get_rid_of_mentions(self, text):
        while text.find("<@!") != -1 and text.find(">") != -1 and text.find("<@!") < text.find(">"):
            author = self.get_user(int(text[text.find("<@!")+3:text.find(">")]))
            text = text[:text.find("<@!")] + str(author).split('#')[0] + text[text.find(">")+1:]
        return text

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        translator = Translator()

        if message.author == self.user or not str(message.channel).startswith("general"):
            return

        if str(message.channel) == "general":
            src = "ru"
        else:
            src = str(message.channel).split('-')[-1]

        for dest in translAPI.allowed_languages:
            if dest == "":
                dest = "ru"
				
            if src == dest:
                continue
            channel_to_send = None

            for channel in self.get_all_channels():
                if str(channel) == "general-{0}".format(dest) or (str(channel) == "general" and dest == "ru"):
                    channel_to_send = channel
                    break

            if channel_to_send:
                author = str(message.author).split('#')[0]
                date = str(message.created_at).split('.')[0]
                translated_text = translator.translate(message.content, src=src, dest=dest).text
                translated_text = self.get_rid_of_mentions(translated_text)
                await channel_to_send.send('**{0}** *{1}*:\n{2}'.format(author, date, translated_text))


client = MyClient()
client.run(bot-token)
