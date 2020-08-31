from googletrans import Translator

import os
import discord
import translationAPI
import MasterOfCeremony

bot_token = os.environ["BOT_TOKEN"]
admin_command_symbol = "!"
user_command_symbol = "/"


class MyClient(discord.Client):

    is_enabled = True
    google_translator = Translator()
    translators_list = ["google_translator"] # google, yandex
    choosen_translater = 0
    
    master_of_ceremony = MasterOfCeremony.MasterOfCeremony()

    def get_rid_of_mentions(self, text):
        while "<@!" in text and ">" in text and text.find("<@!") < text.find(">"):
            start_index = text.find("<@!")
            end_index = text.find(">")
            author = self.get_user(int(text[start_index+3:end_index]))
            text = text[:start_index] + str(author).split('#')[0] + text[end_index+1:]
        return text

###=============================================
###     ADMIN COMMANDS
###=============================================

    async def handle_admin_commands(self, message):
        if message.content.startswith(admin_command_symbol) and len(message.content) > 2 and message.content.split()[0][1:] in self.admin_commands and message.author.guild_permissions.administrator:
            await self.admin_commands[message.content.split()[0][1:]](self, message.channel)
    
    async def change_translator(self, channel):
        self.choosen_translater = (self.choosen_translater + 1) % len(self.translators_list)
        await channel.send('Switched to **{0}**'.format(self.translators_list[self.choosen_translater]))
        
    async def translator_info(self, channel):
        await channel.send('I am using now **{0}**'.format(self.translators_list[self.choosen_translater]))
        
    async def admin_help(self, channel):
        message_text = "Available admin commands: \n"
        for command in self.admin_commands.keys():
            message_text += "*{0}{1}* \n".format(admin_command_symbol, command)
        await channel.send(message_text)
        
    async def enable_bot(self, channel):
        self.is_enabled = True
        await channel.send("YAY!!!!")
        
    async def disable_bot(self, channel):
        self.is_enabled = False
        await channel.send("OK =(")
        
    admin_commands = {
        "help" : admin_help,
        "change_translator" : change_translator,
        "translator_info" :  translator_info,
        "disable_bot" : disable_bot,
        "enable_bot" : enable_bot
    }

###=============================================
###     USER COMMANDS
###=============================================

    async def handle_user_commands(self, message):
        if message.content.startswith(user_command_symbol) and len(message.content) > 2 and message.content.split()[0][1:] in self.user_commands:
            await self.user_commands[message.content.split()[0][1:]](self, message)
        
    async def user_help(self, message):
        message_text = "Available user commands: \n"
        for command in self.user_commands.keys():
            message_text += "*{0}{1}* \n".format(user_command_symbol, command)
        await message.channel.send(message_text)
        
    user_commands = {
        "help" : user_help,
    }
    
###=============================================
###     OTHER CLASSES HANDLERS
###=============================================
    
    async def handle_classes_callbacks(self, message):
        for callback in self.classes_callbacks_list:
            await callback(self, message)
    
    async def master_of_ceremony_callback(self, message):
        await self.master_of_ceremony.execute(message)
        
    classes_callbacks_list = [
        master_of_ceremony_callback,
    ]
###=============================================
###     API CALLBACKS
###=============================================

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        channel_id = message.channel.id
        if message.author == self.user or not channel_id in translationAPI.channel_id_to_language.keys():
            return

        if not self.is_enabled:
            return
            
        await self.handle_admin_commands(message)
        await self.handle_user_commands(message)
        await self.handle_classes_callbacks(message)
            
        src = translationAPI.channel_id_to_language[channel_id]

        for dest in translationAPI.allowed_languages:
            if src == dest or dest == translationAPI.DEFAULT:
                continue
                
            channel_to_send = None

            for channel in self.get_all_channels():
                if channel.id == translationAPI.language_to_channel_id[dest]:
                    channel_to_send = channel
                    break

            if channel_to_send:
                author = str(message.author).split('#')[0]
                date = str(message.created_at).split('.')[0]
                translated_text = ""
                
                if self.choosen_translater == 0:
                        translated_text = self.google_translator.translate(message.content, dest=dest).text
                
                translated_text = self.get_rid_of_mentions(translated_text)
                await channel_to_send.send('**{0}** *{1}*:\n{2}'.format(author, date, translated_text))                


client = MyClient()
client.run(bot_token)
