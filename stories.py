# news-image-20261124 — story slate, Tuesday 24 November 2026.
# 44 stories, 7 regions. Every item verified Tue 24 Nov 2026 ~14:45 WIB
# against a named wire/primary source (see the research note).
# Rules baked into the decks: Nepal uses NPR 24,000 crore (wires split
# $1.62bn vs $1.63bn); Cikande "24 confirmed dead, 28 missing" — body
# bags (26) are NOT deaths; Colombia bomb 12 hurt (later El Tiempo
# report, not the first 5); Gaza 1,675 dead since the ceasefire, as
# attributed by the Gaza Health Ministry; NO toll is decked for the
# El Chapo Isidro arrest shootout (wires split 11 vs 20); Dymer final
# toll 11 dead, 5 in hospital, search over Mon night; the IRGC Patriot
# claim, the Khartoum drone-origin claim, China "Ma" and Putin's
# Article 5 openness are all ATTRIBUTED, never stated as fact;
# Gauteng "agreed in principle; signing pending"; US ports = cyber
# attack ATTEMPTS, not breaches. Items dated 19/20/21/22 Nov carry
# that date inside their deck or in the DATE CHECK box; nothing is
# decked as Tuesday news unless it is. Do-NOT-write: NO "Trump-Japan
# trade deal" / "Trump-Indonesia deal" (July 2025); NO "COP31 deal"
# — COP31 COLLAPSED Sun 22 Nov.

LEADS = [
    # (num, region, field, tag, headline, deck, source, art)
    (1, "Americas", "Markets", "MARKETS",
     "HUANG IS BACK: NVIDIA +31%",
     "Board reinstates CEO 11 days after exit; Trump intervened. "
     "S&P +4.7%, Nasdaq +6.4%. Mon.",
     "Reuters", "chip"),
    (2, "Europe", "Defence", "NATO",
     "NATO SENDS AWACS TO POLAND",
     "Allies agree air cover after 3 Russian missiles fell in "
     "Poland Fri. No Article 4 invoked. Mon.",
     "Reuters", "awacs"),
    (3, "Asia", "Defence", "KOREA",
     "RUSSIAN JETS SPARK SHELTER ALERT",
     "Jets enter Korea air-defence zone off Ulleungdo; alert 07:52, "
     "lifted in 5 min. No airspace breach. Tue.",
     "Korea JoongAng Daily", "jets"),
    (4, "Asia", "Disasters", "DISASTER",
     "CIKANDE FIRE: 24 DEAD, 28 MISSING",
     "24 confirmed dead Mon; 26 body bags found Tue. DNA ID takes weeks.",
     "Reuters", "fire"),
    (5, "Oceania", "Sport", "CRICKET",
     "INDIA TEST ENDS IN DRAW",
     "NZ 239/5 hold on in Wellington; India 720/9 dec. Mitchell 49*.",
     "ESPNcricinfo", "cricket"),
    (6, "Asia", "Politics", "DIPLOMACY",
     "INDIA GIVES NEPAL NPR 24,000-CRORE AID",
     "Modi announces package; 8 MoUs signed in Delhi. Mon.",
     "Hindu BusinessLine", "flags"),
    (7, "Europe", "War", "UKRAINE",
     "ZELENSKYY: FOUR-WAY TALKS 'TOMORROW'",
     "Ready for Ukraine-Europe-US-Russia talks 'tomorrow'.",
     "Europe Says", "talks"),
    (8, "Americas", "War", "COLOMBIA",
     "VILLAVICENCIO CAR BOMB",
     "12 hurt in blast at governor's office; no deaths.",
     "El Tiempo", "blast"),
    (9, "Europe", "Labour", "STRIKES",
     "GERMAN STRIKES SPREAD TO TUESDAY",
     "IG Metall: ~39,000 workers at 22 sites Tue, incl. Airbus. "
     "Pay +5% demanded.",
     "Reuters", "picket"),
    (10, "Americas", "Defence", "CANADA",
     "PENTAGON REBUKES CANADA",
     "Fact sheet: Ottawa 'falling short' on defence; only 41.9% "
     "of air fleet ready.",
     "AP", "jet"),
    (11, "Americas", "Tech", "CHIPS",
     "US BLACKLISTS MEGASPEED",
     "Commerce bars chip sales to Nvidia-linked firm.",
     "Reuters", "ban"),
    (12, "Europe", "War", "UKRAINE",
     "DYMER: FINAL TOLL 11 DEAD",
     "Search ends Mon night; 11 dead incl. girl, 11; 5 in hospital. "
     "Boy, 7, rescued.",
     "Kyiv Post", "flats"),
    (13, "Asia", "Politics", "BANGLADESH",
     "HASINA PLANS DEC 16 RETURN",
     "Ex-PM sets date to fly home from India; Dhaka: only by "
     "extradition. Tue.",
     "Reuters", "plane"),
]

# (num, region, field, one-line text).
# One line at 8px in a ~232px column holds ~50 chars; the renderer fails
# loudly if any brief exceeds it, so these are kept short on purpose.
BRIEFS = [
    (14, "Middle East", "War", "Gaza: 3 killed incl. UNRWA worker (Mon)"),
    (15, "Europe", "Politics", "Denmark top court backs 'ghetto law' (Mon)"),
    (16, "Americas", "Health", "Pennsylvania measles: 9th death; 1,638 cases"),
    (17, "Asia", "Politics", "China: official gets death for spying (Beijing)"),
    (18, "World/Global", "Tech", "UN chief: agree AI rules within a year"),
    (19, "Americas", "Politics", "Mexico to try 'El Chapo Isidro' at home"),
    (20, "Asia", "Disasters", "8 trekkers missing in Uttarakhand snow (Tue)"),
    (21, "World/Global", "Climate", "COP31 collapses with no deal in Antalya (Sun)"),
    (22, "Americas", "Health", "WHO chief tours darkened Cuba hospital"),
    (23, "Asia", "Economy", "India 3rd in Asia Power Index, score 40.5"),
    (24, "Asia", "Culture", "Shuri Castle main hall reopens in Okinawa"),
    (25, "Asia", "Health", "Bisleri water ruled unsafe; FSSAI to sue (Sun)"),
    (26, "Europe", "Politics", "Putin 'open' to Article 5 guarantees (reported)"),
    (27, "Middle East", "War", "IRGC claims 2 more tankers hit mines (Thu)"),
    (28, "Americas", "Politics", "Schumer: Democrats will probe Huang return"),
    (29, "Americas", "Tech", "US ports face surge in cyberattack attempts"),
    (30, "Americas", "Society", "Miley Cyrus weds Maxx Morando Sat (People)"),
    (31, "Asia", "Politics", "S Korea education minister quits (Sun)"),
    (32, "Asia", "Disasters", "Kota crash: 9 pilgrims killed in Rajasthan"),
    (33, "Europe", "Sport", "Alcaraz wins first ATP Finals title (Sun)"),
    (34, "Europe", "Sport", "Verstappen wins Las Vegas GP (Sat)"),
    (35, "Europe", "Sport", "Liverpool 4-0 Man Utd in Pochettino debut"),
    (36, "Africa", "War", "24 civilians killed in South Sudan attack"),
    (37, "Africa", "Disasters", "Nigeria funeral boat: at least 24 dead (Fri)"),
    (38, "Africa", "Politics", "Gauteng coalition agreed; signing pending"),
    (39, "Africa", "Politics", "Somalia-UAE row: rallies as deadline runs out"),
    (40, "Africa", "War", "Khartoum drone strikes kill 4, hit UN building"),
    (41, "Africa", "Health", "DR Congo Ebola: 11,376 cases, 5,568 deaths"),
    (42, "Middle East", "War", "Syria landmine kills 4-5 children in Idlib"),
    (43, "Middle East", "War", "IRGC claims 2 Patriot radars hit (unverified)"),
    (44, "World/Global", "Tech", "UN lethal-AI talks end with no binding rules"),
]

REGION_ORDER = ["Americas", "Asia", "Europe", "Africa", "Middle East",
                "World/Global", "Oceania"]

# Short label used inside the region bar (the full name is in the footer).
REGION_SHORT = {"World/Global": "World"}

DATE_CHECK = [
    ("COP31 collapse, Antalya", "Sun 22 Nov"),
    ("Bisleri water ruled unsafe", "Sun 22 Nov"),
    ("Putin 'open' to Article 5-style guarantees", "22-23 Nov"),
    ("Hormuz: tankers hit mines (IRGC claim)", "Thu 19 Nov"),
    ("PIF Tower, Riyadh, hit", "Thu 19 Nov"),
    ("ICJ Rohingya genocide verdict", "Thu 19 Nov"),
    ("BepiColombo Mercury orbit arrival", "Sat 21 Nov"),
]

SOURCES_LINE = ("Sources: Reuters, AP, Al Jazeera, AFP, ANI, PTI, "
                "ESPNcricinfo, formula1.com, Hindu BusinessLine, Korea "
                "JoongAng Daily, AJU Press, People, FT, QNC, MEM, ESA, "
                "IANS, Kyiv Post, El Tiempo.")
