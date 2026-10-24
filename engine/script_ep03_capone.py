# EP03 — "Al Capone: jailed for taxes"
SCENES = [
    ("hook", [
        "In 1931, the most feared gangster in America went to prison.",
        "Not for murder. For taxes.",
    ]),
    ("rise", [
        "Al Capone ruled Chicago during Prohibition. Illegal beer, speakeasies, and gambling.",
    ]),
    ("money", [
        "By some estimates, his empire made about sixty million dollars a year.",
        "And he paid zero income tax on it.",
    ]),
    ("law", [
        "Then, in 1927, the Supreme Court ruled that even illegal money can be taxed.",
    ]),
    ("boast", [
        "Capone reportedly laughed. They can't collect legal taxes from illegal money.",
    ]),
    ("agent", [
        "Treasury agents started digging. One of them, Frank Wilson, went through about two million documents.",
    ]),
    ("ledger", [
        "And he found it. Old ledgers, tracing payments to Capone that were never reported.",
    ]),
    ("trial", [
        "Capone was charged with tax evasion. He bragged about a deal for just two years.",
        "The judge refused.",
    ]),
    ("verdict", [
        "On October 17th, 1931, he was found guilty.",
        "Eleven years in prison, plus eighty thousand dollars in fines and court costs.",
    ]),
    ("prison", [
        "He was sent to Atlanta, then to Alcatraz.",
    ]),
    ("ending", [
        "He left prison in 1939, sick and weak, and died in 1947.",
        "The man who beat every bullet, was beaten by a bookkeeper.",
    ]),
    ("cta", [
        "Next: eleven men in Halloween masks stole two point seven million dollars.",
        "Follow so you don't miss it.",
    ]),
]

CAPTION_OVERRIDES = {
    "By some estimates, his empire made about sixty million dollars a year.":
        "By some estimates, his empire made about $60 million a year.",
    "Then, in 1927, the Supreme Court ruled that even illegal money can be taxed.":
        "Then, in 1927, the Supreme Court ruled that even illegal money can be taxed.",
    "Capone reportedly laughed. They can't collect legal taxes from illegal money.":
        "Capone reportedly laughed: \"They can't collect legal taxes from illegal money.\"",
    "Treasury agents started digging. One of them, Frank Wilson, went through about two million documents.":
        "Treasury agents started digging. One of them, Frank Wilson, went through about 2 million documents.",
    "He bragged about a deal for just two years.": "",
    "Capone was charged with tax evasion. He bragged about a deal for just two years.":
        "Capone was charged with tax evasion. He bragged about a deal for just 2 years.",
    "On October 17th, 1931, he was found guilty.": "On October 17, 1931, he was found guilty.",
    "Eleven years in prison, plus eighty thousand dollars in fines and court costs.":
        "11 years in prison, plus $80,000 in fines and court costs.",
    "Next: eleven men in Halloween masks stole two point seven million dollars.":
        "Next: 11 men in Halloween masks stole $2.7 million.",
}
CAPTION_OVERRIDES = {k: v for k, v in CAPTION_OVERRIDES.items() if v}
