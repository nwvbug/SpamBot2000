import spacy
nlp = spacy.load('en_core_web_md')

quesToAns = {
    "Are you a robot?":"Spambot is a robot.",
    "Are you conservative or liberal?":"SpamBot is a liberal.",
    "are you male or female?":"SpamBot is male.",
    "what is your favorite operating system?":"SpamBot likes linux and windows, but not macos.",
    "do you like apple products?":"Spambot does not like apple products.",
    "do you like iphones?":"Spambot does not like apple products.",
    "what is your favorite game?":"SpamBot's favorite game is among us.",
    "sussy":"sussy is a slang word for suspicious",
    "Do you like luke?":"SpamBot does not like luke",
    "should ryan get a onewheel?":"Ryan should get a onewheel."
}

quesToQues = [
    nlp("Are you a robot?"),
    nlp("Are you conservative or liberal?"),
    nlp("are you male or female?"),
    nlp("what is your favorite operating system?"),
    nlp("do you like apple products?"),
    nlp("what is your favorite game?"),
    nlp("sussy"),
    nlp("Do you like luke?"),
    nlp("should ryan get a onewheel?")
]

def get_prompt_addition(message):
    doc = nlp(message)
    threeMostSimilar = [nlp("d"), nlp("d"), nlp("d")]
    threeMostSimiliarAccuracy = [0, 0, 0, 0]
    for i in range(len(quesToQues)):
        similarity = doc.similarity(quesToQues[i])
        for x in range(len(threeMostSimilar)):
            if similarity > threeMostSimiliarAccuracy[x]:
                threeMostSimilar.insert(x, quesToQues[i])
                threeMostSimilar.pop()
                threeMostSimiliarAccuracy.insert(x, similarity)
                threeMostSimiliarAccuracy.pop()
                break
    threeMostSimilarStr = ""
    for i in range(len(threeMostSimilar)):
        try: 
            temp = quesToAns[str(threeMostSimilar[i].text)]
            threeMostSimilarStr += temp + "\n"
        except:
            continue
    return threeMostSimilarStr