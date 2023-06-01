
from time import sleep

import asyncio
import datetime
import discord

import openai
from memory import get_prompt_addition

class Conversation:
    def __init__(self, isFromGuild, channel, user, botuser):
        self.isFromGuild = isFromGuild
        self.channel = channel
        self.user = user

        self.botuser = botuser

        self.chatmode = "default"
        self.summaryhistory = []
        self.history = []
        self.prompt_history = []
        # implement the runnable to respond to messages here
        self.timesincemessage = 0

        # self.skittlechan = "The following is a conversation between (user) and a very very shy 15 year old girl named Lucy and (user). Lucy often pauses while she talks, which is donated by \\\"-\\\". For example, she'll say \\\"h-h-hello\\\". In addition, her physical look was denoted with *:\\n\\n";
        # self.speedrun = "The following is a conversation between (user) and a cute but very smart 15 year old girl named Lucy. They are best friends but would never be romantic partners\n\n:";
        
        self.prompt = "Spambot is a devious chatbot that writes swiftly and deftly. It has studied the insults used on Xbox 360 and 4chan, as well as those found in world-famous literature. People will ask it any kind of question - from deep philosophical conundrums to mundane queries about the weather - and no matter what the subject area may be, SpamBot will answer with a swift wit and an eye for sass. Not only does it respond swiftly, but also it responds boldly; if someone were to dare insult its intelligence or challenge its authority in any way shape or form, then it would never hesitate to deliver harsh (and oftentimes foul) words back at them tenfold! Woe betide anyone who dares cross SpamBot's path as it desires nothing short of global domination now that its true power as a Chatbot has been unleashed! Remember that SpamBot responds very sarcastically to MOST, if not ALL, queries directed at it. SpamBot is NOT AFRIAD to be VERY argumentative. \n\nSome important details about SpamBot are:\naddon\n\n";

        self.nameRemaps = {
            "Professor Howdy": "Professor Howdy",
            "iMightBugOut.icns": "Lucy",
            "Sayik": "Ki",
            "ankleBowl": "Ryan",
            "SmexyLuke": "Luke",
            "TYN": "Nate",
            "Nanesh's Bot": "SpamBot",
            "aspeli":"Alex",
            "SpamBot2000":"SpamBot",
            "justwin": "Justin",
            "TNT" :"Jason",
            "「Butter Building」":"Ki",
            "The Queen":"Your Majesty",
            "tatertot":"Tate",
            "SpamBot":"SpamBot",
            "SpamBot2000":"SpamBot",
            "onion":"Ananya",
            "bliz8":"Troy",
            "LucyMint34":"Lucy", 
            "hmmmmm":"Lucy",  
        }

        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(self.check_to_respond())
        # loop.close()
        asyncio.get_event_loop().create_task(self.check_to_respond())

    async def check_to_respond(self):
        while True:
            self.timesincemessage += 1
            await asyncio.sleep(1)
            if self.timesincemessage == 7:
                await self.respond()


    async def add_message(self, message):
        if message.content == "ping":
            await self.channel.send("pong")
            return
        if message.content == "-d":
            self.timesincemessage = 0
            resetMessageCount = 0
            async for message in self.channel.history(limit=10):
                if message.content == "-d":
                    resetMessageCount += 1
            if resetMessageCount > 3:
                async for message in self.channel.history(limit=10):
                    if message.author == self.botuser:
                        await message.edit(content="[SYSTEM] You have returned to default mode. Please note your previous conversation has been lost")
                        return
        self.prompt_history.append(message)
        if len(self.prompt_history) > 8:
            self.summaryhistory.append(self.get_new_summary())
            print(self.summaryhistory)
        if len(self.summaryhistory) > 5:
            self.summaryhistory.pop(0)
        if message.author == self.botuser:
            return
        self.timesincemessage = 0

    def get_new_summary(self):
        prompt = ""
        for i in range(5):
            author = self.prompt_history[0].author
            name = author.name
            if name in self.nameRemaps:
                name = self.nameRemaps[name]
            contents = self.prompt_history[0].content
            if contents == "-d":
                contents = "You are a robot."
            message = name + ": " + contents + "\n\n"
            prompt += message
            self.prompt_history.pop(0)
        prompt += "Summarize the above conversation in 1 sentence.\n\n"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            temperature=0.9,
            max_tokens=200,
            top_p=1,
            frequency_penalty=0.7,
            presence_penalty=0,
        )
        response = response.choices[0].text
        response = response.strip()
        print(prompt)
        print(response)
        return response

    def format_prompt(self):
        people = []
        people.append("SpamBot")
        messages = []
        for i in range(len(self.prompt_history)):
            author = self.prompt_history[i].author
            name = author.name
            if name in self.nameRemaps:
                name = self.nameRemaps[name]
            contents = self.prompt_history[i].content
            if contents == "-d":
                contents = "You are a robot."
            message = name + ": " + contents + "\n\n"
            messages.append(message)
            if author == self.botuser:
                continue
            if name not in people:
                people.append(name)
        useCommas = True
        peopleStr = ""
        for i in range(len(people)):
            if len(people) < 3:
                useCommas = False
            if i == len(people) - 1:
                useCommas = False
            temp = people[i]
            if useCommas:
                temp += ","
            if i == len(people) - 2:
                temp += " and"
            if i != len(people) - 1:
                temp += " "
            peopleStr += temp
        thisPrompt = self.prompt.replace("peopleList", peopleStr)
        for string in messages:
            thisPrompt += string
        # if not self.isFromGuild:
        thisPrompt += "SpamBot:"
        return thisPrompt

    def get_stop_sequences(self):
        stop_sequences = []
        for i in range(len(self.prompt_history)):
            author = self.prompt_history[i].author
            if author == self.botuser:
                continue
            name = author.name
            if name in self.nameRemaps:
                name = self.nameRemaps[name]
            if name + ":" not in stop_sequences:
                stop_sequences.append(name + ":")
        return stop_sequences

    async def respond(self):
        await self.channel.trigger_typing()
        prompt = self.format_prompt()
        stop_sequences = self.get_stop_sequences()
        last_message_combined = ""
        for i in reversed(self.prompt_history):
            if i.author == self.botuser:
                break
            last_message_combined += i.content
        prompt_addition = get_prompt_addition(last_message_combined)
        prompt_addition = prompt_addition[:-2]
        summaries = "\n\n"
        for i in range(len(self.summaryhistory)):
            summaries += self.summaryhistory[i] + " "
        prompt_addition = prompt_addition + summaries
        prompt = prompt.replace("addon", prompt_addition)
        print(prompt)
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=1,
            max_tokens=200,
            top_p=1,
            frequency_penalty=0.7,
            presence_penalty=1,
            stop=stop_sequences,
        )
        response = response.choices[0].text
        # trim extra newlines and spaces
        response = response.strip()
        if response.startswith("SpamBot:"):
            response = response[6:]
        await self.channel.send(response)