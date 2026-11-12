# EP42 — Pegasus spyware price list (NYT 2016) + WhatsApp v. NSO ($167M verdict May 2025 -> ~$4M, Oct 2025)
SCENES = [
    ("hook", ["Spying on ten iPhones cost six hundred and fifty thousand dollars.", "That was the price list of the world's most famous spyware."]),
    ("pricelist", ["In 2016, The New York Times reported the prices of Pegasus, made by Israel's NSO Group.", "Five hundred thousand dollars to install it. Then six hundred and fifty thousand for ten iPhone users.", "Plus seventeen percent of the total, every year."]),
    ("attack", ["In 2019, WhatsApp said Pegasus was used through its app against about fourteen hundred users.", "So WhatsApp sued NSO."]),
    ("rehook", ["In May 2025, a jury put a price on that attack.", "And it was huge."]),
    ("verdict", ["One hundred and sixty-seven million dollars in punitive damages.", "Plus about four hundred and forty-four thousand in compensatory damages."]),
    ("cut", ["But in October 2025, the judge cut the punitive damages to about four million dollars.", "And she banned NSO from targeting WhatsApp."]),
    ("customers", ["Governments pay a lot for this.", "Mexico's government said past administrations spent about sixty-one million dollars on Pegasus."]),
    ("appeal", ["NSO says it sells only to governments, and it has appealed the ruling."]),
    ("question", ["Should spyware companies be allowed to sell to governments?", "Tell me in the comments."]),
]
REHOOK = ("A JURY PUT A PRICE", "ON THAT ATTACK.", "IT WAS HUGE.")
CAPTION_OVERRIDES = {
    "Spying on ten iPhones cost six hundred and fifty thousand dollars.": "Spying on 10 iPhones cost $650,000.",
    "Five hundred thousand dollars to install it. Then six hundred and fifty thousand for ten iPhone users.": "$500,000 to install it. Then $650,000 for 10 iPhone users.",
    "Plus seventeen percent of the total, every year.": "Plus 17% of the total, every year.",
    "In 2019, WhatsApp said Pegasus was used through its app against about fourteen hundred users.": "In 2019, WhatsApp said Pegasus was used through its app against about 1,400 users.",
    "One hundred and sixty-seven million dollars in punitive damages.": "$167 million in punitive damages.",
    "Plus about four hundred and forty-four thousand in compensatory damages.": "Plus about $444,000 in compensatory damages.",
    "But in October 2025, the judge cut the punitive damages to about four million dollars.": "But in October 2025, the judge cut the punitive damages to about $4 million.",
    "Mexico's government said past administrations spent about sixty-one million dollars on Pegasus.": "Mexico's government said past administrations spent about $61 million on Pegasus.",
}
