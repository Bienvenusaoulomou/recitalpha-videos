# EP45 — Kenya State House website hacked, 5 BTC ransom (Jul 18 2026)
SCENES = [
    ("hook", ["Hackers took over the website of Kenya's president.", "Then they asked for five bitcoins."]),
    ("price", ["That's about forty-one million shillings.", "Roughly three hundred and twenty thousand dollars."]),
    ("message", ["It happened on July eighteenth, twenty twenty-six.", "The homepage was replaced with a message to President Ruto, and a bitcoin wallet."]),
    ("deadline", ["The hackers wanted the money before six o'clock that evening.", "Or they would leak everything about him.", "And they called it their third warning."]),
    ("rehook", ["But this wasn't the first time.", "Not even close."]),
    ("before", ["In November twenty twenty-five, attackers hit several Kenyan government websites at once.", "Including the presidency's."]),
    ("confirm", ["State House confirmed the breach.", "The site went offline, while cyber teams worked to contain the attack."]),
    ("minister", ["Kenya's ICT minister, William Kabogo, said: our cyber team is on top of the situation.", "He said there was no evidence of data theft or loss.", "The site soon came back online."]),
    ("nobody", ["No group has publicly claimed the attack.", "And there's no public report that anyone paid."]),
    ("billions", ["Kenya's cyber agency says government systems face billions of attempted attacks."]),
    ("question", ["Should a government ever pay hackers?", "Tell me in the comments."]),
]
REHOOK = ("BUT THIS WASN'T", "THE FIRST TIME.", "NOT EVEN CLOSE.")
CAPTION_OVERRIDES = {
    "Kenya's ICT minister, William Kabogo, said: our cyber team is on top of the situation.": "Kenya's ICT minister, William Kabogo, said: \"Our cyber team is on top of the situation.\"",
    "Then they asked for five bitcoins.": "Then they asked for 5 bitcoins.",
    "That's about forty-one million shillings.": "That's about 41 million shillings.",
    "Roughly three hundred and twenty thousand dollars.": "Roughly $320,000.",
    "It happened on July eighteenth, twenty twenty-six.": "It happened on July 18, 2026.",
    "The hackers wanted the money before six o'clock that evening.": "The hackers wanted the money before 6 o'clock that evening.",
    "In November twenty twenty-five, attackers hit several Kenyan government websites at once.": "In November 2025, attackers hit several Kenyan government websites at once.",
}
