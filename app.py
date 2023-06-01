import discord

import openai
from discordpy import MyClient
openai.api_key = ""

class App:
    def __init__(self):
        self.id = ""
        self.lastInteract = 0
        self.name = "SpamBot2000"
        self.discordpy = MyClient()
        self.discordpy.run('')


app = App()