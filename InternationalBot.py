from googletrans import Translator
from yandex.Translater import Translater

import discord
import translationAPI

template_channel = "general"
bot_token = "bot-token"
yandex_api_token = "api-token"
command_symbol = "!"


class MyClient(discord.Client):

    google_translator = Translator()
    yandex_translator = Translater()
    translators_list = ["google_translator" , "yandex_translator"] # google, yandex
    choosen_translater = 1

    def get_rid_of_mentions(self, text):
        while "<@!" in text and ">" in text and text.find("<@!") < text.find(">"):
            start_index = text.find("<@!")
            end_index = text.find(">")
            author = self.get_user(int(text[start_index+3:end_index]))
            text = text[:start_index] + str(author).split('#')[0] + text[end_index+1:]
        return text

    async def change_translator(self, channel):
        self.choosen_translater = (self.choosen_translater + 1) % len(self.translators_list)
        await channel.send('Switched to **{0}**'.format(self.translators_list[self.choosen_translater]))
        
    async def translator_info(self, channel):
        await channel.send('I am using now **{0}**'.format(self.translators_list[self.choosen_translater]))
        
    async def help(self, channel):
        message_text = "Availables commands: \n"
        for command in self.commands.keys():
            message_text += "*{0}* \n".format(command)
        await channel.send(message_text)
        
    commands = {
        "help" : help,
        "change_translator" : change_translator,
        "translator_info" :  translator_info
    }

    async def on_ready(self):
        self.yandex_translator.set_key(yandex_api_token)
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.content.startswith(command_symbol) and len(message.content) > 2 and message.content.split()[0][1:] in self.commands and message.author.guild_permissions.administrator:
            await self.commands[message.content.split()[0][1:]](self, message.channel)

        channel_name = str(message.channel)
        if message.author == self.user or not channel_name.startswith(template_channel):
            return

        if channel_name == template_channel:
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
                if str(channel) == "{0}-{1}".format(template_channel, dest) or (str(channel) == template_channel and dest == "ru"):
                    channel_to_send = channel
                    break

            if channel_to_send:
                author = str(message.author).split('#')[0]
                date = str(message.created_at).split('.')[0]
                translated_text = ""
                
                if self.choosen_translater == 0:
                    translated_text = self.google_translator.translate(message.content, src=src, dest=dest).text
                elif self.choosen_translater == 1:
                    self.yandex_translator.set_from_lang(src)
                    self.yandex_translator.set_to_lang(dest)
                    self.yandex_translator.set_text(message.content)
                    translated_text = self.yandex_translator.translate()
                
                translated_text = self.get_rid_of_mentions(translated_text)
                await channel_to_send.send('**{0}** *{1}*:\n{2}'.format(author, date, translated_text))                


client = MyClient()
client.run(bot_token)
