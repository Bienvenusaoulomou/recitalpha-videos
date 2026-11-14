# EP46 — Colonial Pipeline: $4.4M ransom (75 BTC), FBI recovered 63.7 BTC (~$2.3M), 2021
SCENES = [
    ("hook", ["A company paid hackers four point four million dollars in bitcoin.", "A month later, the FBI took most of it back."]),
    ("shutdown", ["On May seventh, twenty twenty-one, Colonial Pipeline shut down its operations.", "A ransomware gang called DarkSide had broken into its computers."]),
    ("fuel", ["Colonial carries a huge share of the fuel used on America's East Coast.", "And now the pipeline was stopped."]),
    ("paid", ["So the company paid seventy-five bitcoins.", "Then worth about four point four million dollars."]),
    ("rehook", ["But then the FBI followed the money.", "All the way to one wallet."]),
    ("wallet", ["Investigators tracked the bitcoin through multiple transfers.", "To a wallet the hackers used to collect the payment."]),
    ("seized", ["In June, the Justice Department seized sixty-three point seven bitcoins.", "About eighty-five percent of the ransom.", "Deputy Attorney General Lisa Monaco said: today we turned the tables on DarkSide."]),
    ("twist", ["But by then, bitcoin's price had fallen.", "So it was worth only about two point three million dollars."]),
    ("quote", ["A federal prosecutor said: the extortionists will never see this money.", "And the FBI said cutting off access to revenue is one of the most impactful consequences we can impose."]),
    ("question", ["Should companies be allowed to pay ransoms at all?", "Tell me in the comments."]),
]
REHOOK = ("BUT THEN THE FBI", "FOLLOWED THE MONEY.", "ALL THE WAY TO ONE WALLET.")
CAPTION_OVERRIDES = {
    "Deputy Attorney General Lisa Monaco said: today we turned the tables on DarkSide.": "Deputy Attorney General Lisa Monaco said: \"Today we turned the tables on DarkSide.\"",
    "And the FBI said cutting off access to revenue is one of the most impactful consequences we can impose.": "And the FBI said: \"Cutting off access to revenue is one of the most impactful consequences we can impose.\"",
    "A company paid hackers four point four million dollars in bitcoin.": "A company paid hackers $4.4 million in bitcoin.",
    "On May seventh, twenty twenty-one, Colonial Pipeline shut down its operations.": "On May 7, 2021, Colonial Pipeline shut down its operations.",
    "So the company paid seventy-five bitcoins.": "So the company paid 75 bitcoins.",
    "Then worth about four point four million dollars.": "Then worth about $4.4 million.",
    "In June, the Justice Department seized sixty-three point seven bitcoins.": "In June, the Justice Department seized 63.7 bitcoins.",
    "About eighty-five percent of the ransom.": "About 85% of the ransom.",
    "So it was worth only about two point three million dollars.": "So it was worth only about $2.3 million.",
    "A federal prosecutor said: the extortionists will never see this money.": "A federal prosecutor said: \"The extortionists will never see this money.\"",
}
