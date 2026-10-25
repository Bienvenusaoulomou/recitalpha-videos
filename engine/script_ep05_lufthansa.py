# EP05 v2 — "The Lufthansa heist" (JFK airport, 1978) — tightened + re-hook (retention rules 2026-10-25)
SCENES = [
    ("hook", [
        "Six masked men walked out of New York's biggest airport with five million dollars in cash.",
        "Not one dollar was ever found.",
    ]),
    ("place", [
        "December 11th, 1978. JFK airport. The Lufthansa cargo terminal.",
    ]),
    ("cash", [
        "Inside the vault: American cash, flown home from West Germany.",
        "Used bills. Almost impossible to trace.",
    ]),
    ("insider", [
        "The tip came from the inside.",
        "A cargo supervisor, Louis Werner, owed about twenty thousand dollars in gambling debts.",
    ]),
    ("rehook", [
        "But stealing it was the easy part.",
        "Keeping it was deadly.",
    ]),
    ("night", [
        "Around three a.m., a black van rolled up to the terminal.",
        "Six men, masks, guns.",
    ]),
    ("loot", [
        "Cash and jewels. About five point eight million dollars, in sixty-four minutes.",
        "At the time, the biggest cash robbery in American history.",
    ]),
    ("van", [
        "One man had one job: get rid of the van.",
        "He didn't. Police found it days later.",
    ]),
    ("fallout", [
        "Then, one by one, people linked to the heist started to disappear.",
        "The money never came back.",
    ]),
    ("verdict", [
        "Only one man was ever convicted for the robbery: the inside man. Fifteen years.",
        "Twelve years later, the story ended up in the movie Goodfellas.",
    ]),
    ("cta", [
        "Next: a man sold land in a country that did not exist. And hundreds of people sailed there.",
        "Follow so you don't miss it.",
    ]),
]

REHOOK = ("STEALING IT WAS", "THE EASY PART.", "KEEPING IT WAS DEADLY.")

CAPTION_OVERRIDES = {
    "Six masked men walked out of New York's biggest airport with five million dollars in cash.":
        "Six masked men walked out of New York's biggest airport with $5 million in cash.",
    "December 11th, 1978. JFK airport. The Lufthansa cargo terminal.":
        "December 11, 1978. JFK airport. The Lufthansa cargo terminal.",
    "A cargo supervisor, Louis Werner, owed about twenty thousand dollars in gambling debts.":
        "A cargo supervisor, Louis Werner, owed about $20,000 in gambling debts.",
    "Around three a.m., a black van rolled up to the terminal.":
        "Around 3 a.m., a black van rolled up to the terminal.",
    "Cash and jewels. About five point eight million dollars, in sixty-four minutes.":
        "Cash and jewels. About $5.8 million, in 64 minutes.",
    "Only one man was ever convicted for the robbery: the inside man. Fifteen years.":
        "Only one man was ever convicted for the robbery: the inside man. 15 years.",
    "Twelve years later, the story ended up in the movie Goodfellas.":
        "12 years later, the story ended up in the movie Goodfellas.",
}
