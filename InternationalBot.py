from googletrans import Translator

import discord
import translationAPI

bot_token = "token-here"


class MyClient(discord.Client):

    translator = Translator()

    def get_rid_of_mentions(self, text):
        while "<@!" in text and ">" in text and text.find("<@!") < text.find(">"):
            start_index = text.find("<@!")
            end_index = text.find(">")
            author = self.get_user(int(text[start_index+3:end_index]))
            text = text[:start_index] + str(author).split('#')[0] + text[end_index+1:]
        return text

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        channel_name = str(message.channel)
        if message.author == self.user or not channel_name.startswith("general"):
            return

        if channel_name == "general":
            src = "ru"
        else:
            src = channel_name.split('-')[-1]

        for dest in translationAPI.allowed_languages:
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
                translated_text = self.translator.translate(message.content, src=src, dest=dest).text
                translated_text = self.get_rid_of_mentions(translated_text)
                await channel_to_send.send('**{0}** *{1}*:\n{2}'.format(author, date, translated_text))


client = MyClient()
client.run(bot-token)
