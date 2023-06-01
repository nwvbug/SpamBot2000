from conversation import Conversation
import discord

from threading import Thread

class MyClient(discord.Client):
    async def on_ready(self):
        self.conversations = {}
        print('Logged on as', self.user)

    async def on_message(self, message):
        channel = message.channel
        if channel not in self.conversations:
            is_private = False
            if isinstance(channel, discord.DMChannel):
                is_private = True
            self.conversations[channel] = Conversation(not is_private, channel, message.author, self.user)
        conversation = self.conversations[channel]
        await conversation.add_message(message)
        # thread = Thread(target=conversation.add_message, args = (message, ))
        # thread.start()