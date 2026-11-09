# EP34 — Arup $25.6M deepfake video-call fraud (Hong Kong, 2024) — YouTube, new format
SCENES = [
    ("hook", ["An employee sent twenty five million dollars to criminals.", "Because his bosses asked him to. On a video call."]),
    ("who", ["The company was Arup, the British engineering firm that worked on the Sydney Opera House.", "The employee worked in its Hong Kong office."]),
    ("message", ["It started with a message from the company's UK office.", "At first, he suspected a scam."]),
    ("call", ["So he joined a video call. The finance chief was there. Other colleagues too.", "They looked real. They sounded real."]),
    ("rehook", ["But those faces weren't real.", "They were deepfakes."]),
    ("transfers", ["He made fifteen transfers.", "Two hundred million Hong Kong dollars. About twenty five point six million US dollars."]),
    ("confirm", ["Arup later confirmed it: fake voices and images were used.", "Its finances weren't affected, it said, and none of its internal systems were compromised."]),
    ("police", ["Arup reported it to Hong Kong police in January 2024."]),
    ("twist", ["That's the twist. Nobody hacked a computer.", "They hacked trust."]),
    ("quote", ["Arup's tech chief, Rob Greig, called it an industry, business and social issue.", "And he said attacks like this were rising sharply."]),
    ("question", ["Would you still trust your boss on a video call?", "Tell me in the comments."]),
]
REHOOK = ("BUT THOSE FACES", "WEREN'T REAL.", "THEY WERE DEEPFAKES.")
CAPTION_OVERRIDES = {
    "An employee sent twenty five million dollars to criminals.": "An employee sent $25 million to criminals.",
    "Two hundred million Hong Kong dollars. About twenty five point six million US dollars.": "HK$200 million. About US$25.6 million.",
    "Arup's tech chief, Rob Greig, called it an industry, business and social issue.": "Arup's tech chief, Rob Greig, called it \"an industry, business and social issue.\"",
}
