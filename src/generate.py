"""Generate AttentionBench dataset.

Two dimensions:
1. Signal-in-Noise (SIN) — selective attention via noise titration
2. Vigilance Decrement (VIG) — sustained attention via repeated sub-tasks
"""

import json
import random
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

# ============================================================
# SEED DATA: Passages with verified Q&A
# ============================================================

PASSAGES = [
    {
        "id": "passage_01",
        "domain": "marine_biology",
        "text": (
            "In 2021, marine biologist Dr. Kenji Yamada led an expedition to the "
            "Kerova Trench in the South Pacific, discovering three previously unknown "
            "species of bioluminescent organisms at a depth of 2,400 meters. The most "
            "notable discovery was Luminara kerovensis, a jellyfish-like creature "
            "measuring approximately 15 centimeters in diameter that produces a "
            "distinctive blue-green glow through a novel chemical pathway involving "
            "the enzyme luciferase-K7. Unlike known bioluminescent organisms that use "
            "coelenterazine as their primary substrate, L. kerovensis synthesizes "
            "light using a compound Dr. Yamada's team named kerovazine. The expedition, "
            "funded by the Pacifica Marine Institute, deployed the remotely operated "
            "vehicle Triton-4 to collect samples over a 12-day period. Initial analysis "
            "revealed that L. kerovensis maintains its bioluminescence at temperatures "
            "between 1.5 and 4.2 degrees Celsius, suggesting a unique thermal "
            "adaptation. The team published their findings in the March 2022 issue of "
            "Deep-Sea Research Letters, proposing that the Kerova Trench may harbor "
            "an isolated ecosystem that diverged from neighboring regions approximately "
            "6 million years ago."
        ),
        "questions": [
            {"q": "At what depth were the organisms discovered?", "a": "2,400 meters"},
            {"q": "What enzyme is involved in the bioluminescence of L. kerovensis?", "a": "luciferase-K7"},
            {"q": "What is the name of the remotely operated vehicle used?", "a": "Triton-4"},
            {"q": "How long was the sample collection period?", "a": "12 days"},
            {"q": "What compound did the team name as the light-producing substrate?", "a": "kerovazine"},
        ],
    },
    {
        "id": "passage_02",
        "domain": "architecture",
        "text": (
            "The Solheim Bridge, completed in October 2018, spans the Vestfjorden "
            "strait connecting the towns of Rolvøy and Kjeldsund in northern Norway. "
            "Designed by architect Maren Lindqvist of the firm Nordvik & Partners, "
            "the cable-stayed bridge stretches 847 meters with a main span of 524 "
            "meters, making it the longest single-pylon bridge in Scandinavia. The "
            "bridge's distinctive feature is its asymmetric A-frame pylon, rising 173 "
            "meters above sea level, which Lindqvist described as inspired by the mast "
            "of a Viking longship. Construction required 34,000 cubic meters of concrete "
            "and 8,200 tonnes of structural steel, completed over a period of four years "
            "by the contractor Heimdal Construction. The bridge deck sits 62 meters "
            "above the water at its highest point to accommodate the large cargo vessels "
            "that traverse the strait. A unique wind deflection system using 288 "
            "individually angled vanes along the deck edges allows the bridge to remain "
            "open in winds up to 130 kilometers per hour, a critical requirement given "
            "the region's severe winter storms. The total project cost was 2.8 billion "
            "Norwegian kroner, partially funded through a toll system expected to "
            "operate for 15 years."
        ),
        "questions": [
            {"q": "Who designed the Solheim Bridge?", "a": "Maren Lindqvist"},
            {"q": "What is the length of the main span?", "a": "524 meters"},
            {"q": "How tall is the pylon above sea level?", "a": "173 meters"},
            {"q": "How many wind deflection vanes are installed?", "a": "288"},
            {"q": "What was the total project cost?", "a": "2.8 billion Norwegian kroner"},
        ],
    },
    {
        "id": "passage_03",
        "domain": "astronomy",
        "text": (
            "NASA's Vantara probe, launched on September 14, 2023, from Kennedy Space "
            "Center aboard an Atlas VII rocket, is designed to study the subsurface "
            "ocean of Jupiter's moon Europa. The probe carries six scientific instruments, "
            "including the Cryogenic Magnetometer Array developed by Dr. Priya "
            "Chandrasekaran at the Jet Propulsion Laboratory. Vantara's planned "
            "trajectory includes a Venus gravity assist in February 2024 followed by "
            "two Earth gravity assists, with arrival at Jupiter scheduled for August "
            "2029. The probe weighs 3,740 kilograms at launch and is powered by three "
            "radioisotope thermoelectric generators producing a combined 540 watts of "
            "electrical power. Its primary mission objective is to map Europa's ice shell "
            "thickness using ground-penetrating radar operating at a frequency of 9 "
            "megahertz. The mission's estimated total cost is $2.1 billion over its "
            "12-year operational lifetime. A secondary objective involves deploying the "
            "Nereid surface lander, a 180-kilogram package equipped with a thermal "
            "drill capable of penetrating up to 4 meters into Europa's ice crust. "
            "Communication with Earth will be maintained through a 3.7-meter high-gain "
            "antenna operating in the Ka-band."
        ),
        "questions": [
            {"q": "When was the Vantara probe launched?", "a": "September 14, 2023"},
            {"q": "What instrument did Dr. Chandrasekaran develop?", "a": "Cryogenic Magnetometer Array"},
            {"q": "At what frequency does the ground-penetrating radar operate?", "a": "9 megahertz"},
            {"q": "What is the name of the surface lander?", "a": "Nereid"},
            {"q": "How far can the thermal drill penetrate into the ice?", "a": "4 meters"},
        ],
    },
    {
        "id": "passage_04",
        "domain": "chemistry",
        "text": (
            "In 2019, a team led by Professor Helena Kowalski at the University of "
            "Tartu in Estonia achieved the first stable synthesis of Meridine-7, a "
            "complex organometallic compound that had eluded chemists for over two "
            "decades. The synthesis involves a 14-step reaction sequence starting from "
            "commercially available palladium acetate and requiring precise temperature "
            "control at minus 78 degrees Celsius during the critical cyclization step. "
            "Meridine-7 features an unprecedented eight-membered metallocyclic ring "
            "incorporating both palladium and titanium atoms, giving it a distinctive "
            "deep violet color in crystalline form. The compound demonstrates remarkable "
            "catalytic properties, accelerating carbon-carbon bond formation reactions "
            "by a factor of 340 compared to existing catalysts. Professor Kowalski's "
            "team of nine researchers spent three years developing the synthesis, with "
            "graduate student Tomas Rebane performing the decisive experiment on March "
            "3, 2019. The work was published in Nature Chemistry in July 2019 and has "
            "since been cited over 470 times. Industrial applications are being explored "
            "by Nordchem Industries, which licensed the patent for an undisclosed sum "
            "to develop Meridine-7 as a pharmaceutical manufacturing catalyst."
        ),
        "questions": [
            {"q": "At what university was Meridine-7 first synthesized?", "a": "University of Tartu"},
            {"q": "What temperature is required for the critical cyclization step?", "a": "minus 78 degrees Celsius"},
            {"q": "By what factor does Meridine-7 accelerate bond formation?", "a": "340"},
            {"q": "Which graduate student performed the decisive experiment?", "a": "Tomas Rebane"},
            {"q": "What company licensed the patent?", "a": "Nordchem Industries"},
        ],
    },
    {
        "id": "passage_05",
        "domain": "ancient_history",
        "text": (
            "Excavations at Tell al-Raqim in southern Iraq, conducted between 2015 "
            "and 2019 by a joint team from the University of Bologna and the Iraqi "
            "National Museum, uncovered the remains of a previously unknown Sumerian "
            "trading settlement dating to approximately 2800 BCE. Lead archaeologist "
            "Dr. Farah al-Nasiri identified 47 distinct clay tablet fragments bearing "
            "a variant of proto-cuneiform script that differs from known systems in "
            "its use of circular rather than wedge-shaped impressions. The settlement, "
            "which the team named Zarankhur based on references found on five of the "
            "tablets, appears to have been a hub for the lapis lazuli trade, with over "
            "230 carved stone artifacts recovered from a single storage chamber "
            "measuring 6 by 4 meters. Radiocarbon dating of organic material found "
            "alongside the tablets placed the site's primary occupation between 2830 "
            "and 2750 BCE. The most significant find was a bronze figurine standing "
            "23 centimeters tall, depicting a figure holding what appears to be a "
            "balance scale, which Dr. al-Nasiri interpreted as evidence of standardized "
            "weights and measures. The excavation was funded by a 1.2 million euro "
            "grant from the European Research Council."
        ),
        "questions": [
            {"q": "Who was the lead archaeologist at Tell al-Raqim?", "a": "Dr. Farah al-Nasiri"},
            {"q": "How many clay tablet fragments were found?", "a": "47"},
            {"q": "What trade was the settlement a hub for?", "a": "lapis lazuli"},
            {"q": "How tall is the bronze figurine?", "a": "23 centimeters"},
            {"q": "Which university co-led the excavations?", "a": "University of Bologna"},
        ],
    },
    {
        "id": "passage_06",
        "domain": "linguistics",
        "text": (
            "The Keshwari language, spoken by approximately 3,200 people in three "
            "villages along the Bramha River valley in Nepal's Gorkha district, was "
            "first documented by linguist Dr. Annika Svensson of Uppsala University "
            "during fieldwork conducted between 2016 and 2020. Keshwari belongs to the "
            "Tibeto-Burman language family but contains 87 lexical items with no "
            "cognates in any neighboring language, suggesting a prolonged period of "
            "linguistic isolation. The language's most striking feature is its quintuple "
            "number system, which distinguishes singular, dual, trial, quadral, and "
            "plural forms — only the second natural language known to make a grammatical "
            "quadral distinction. Keshwari employs 14 distinct tone patterns, compared "
            "to the four or five typically found in related languages, and uses a rare "
            "verb-initial word order found in fewer than 3 percent of the world's "
            "languages. Dr. Svensson's comprehensive grammar, published in 2021 by "
            "Oxford University Press under the title A Reference Grammar of Keshwari, "
            "runs to 842 pages and documents approximately 4,500 lexical entries. The "
            "language is classified as severely endangered, with no speakers under the "
            "age of 35, and UNESCO designated it for urgent documentation in 2022."
        ),
        "questions": [
            {"q": "How many people speak the Keshwari language?", "a": "3,200"},
            {"q": "How many lexical items have no cognates in neighboring languages?", "a": "87"},
            {"q": "How many distinct tone patterns does Keshwari use?", "a": "14"},
            {"q": "How many pages is Dr. Svensson's grammar?", "a": "842"},
            {"q": "In which river valley are the Keshwari villages located?", "a": "Bramha River valley"},
        ],
    },
    {
        "id": "passage_07",
        "domain": "geology",
        "text": (
            "The Pyreth Caldera, located in the central highlands of Iceland at "
            "coordinates 64.73°N, 18.41°W, formed during a catastrophic eruption "
            "approximately 9,200 years ago that ejected an estimated 85 cubic "
            "kilometers of volcanic material. Geologist Dr. Sigridur Magnusdottir of "
            "the University of Iceland has studied the caldera since 2011, determining "
            "through stratigraphic analysis that the eruption occurred in three distinct "
            "phases over a period of approximately 60 days. The caldera measures 11 "
            "kilometers across at its widest point and reaches a depth of 780 meters "
            "from rim to floor. Dr. Magnusdottir's team discovered that the caldera "
            "walls contain alternating layers of rhyolite and basalt, an unusual "
            "combination that suggests the eruption tapped two separate magma chambers "
            "simultaneously. Geochemical analysis of tephra samples collected from 23 "
            "sites across northern Europe confirmed that ashfall from the Pyreth "
            "eruption reached as far as Finland, covering an area of approximately "
            "340,000 square kilometers. Current geothermal monitoring shows the caldera "
            "floor temperature averaging 47 degrees Celsius, with six active fumarole "
            "fields. A 2022 risk assessment classified the volcano as having a 12 "
            "percent probability of significant eruption within the next century."
        ),
        "questions": [
            {"q": "How much volcanic material was ejected in the eruption?", "a": "85 cubic kilometers"},
            {"q": "Over how many phases did the eruption occur?", "a": "three"},
            {"q": "What is the caldera's width at its widest point?", "a": "11 kilometers"},
            {"q": "What two rock types alternate in the caldera walls?", "a": "rhyolite and basalt"},
            {"q": "How many active fumarole fields are in the caldera?", "a": "six"},
        ],
    },
    {
        "id": "passage_08",
        "domain": "music",
        "text": (
            "The Elara Concerto No. 3 in F-sharp minor, composed by Finnish composer "
            "Aino Virtanen between 1987 and 1991, is widely regarded as the most "
            "technically demanding work in the modern cello repertoire. The concerto "
            "spans four movements with a total performance duration of approximately "
            "52 minutes, requiring the soloist to employ extended techniques including "
            "col legno battuto, harmonic glissandi, and a passage in the third movement "
            "that demands simultaneous pizzicato and arco playing. Virtanen wrote the "
            "work specifically for cellist Mikhail Dobrynin, who premiered it on "
            "November 8, 1991, with the Helsinki Philharmonic Orchestra under conductor "
            "Lars Eriksson at Finlandia Hall. The third movement, marked Presto "
            "furioso, contains a cadenza lasting approximately 7 minutes that Dobrynin "
            "described as scaling a mountain of notes. The orchestration calls for "
            "triple woodwinds, four horns, three trumpets, three trombones, tuba, "
            "timpani, an expanded percussion section including five tuned gongs, harp, "
            "celesta, and strings. The manuscript, comprising 287 handwritten pages, "
            "is housed in the Sibelius Museum in Turku. Commercial recordings exist by "
            "14 cellists, though Dobrynin's 1993 recording for Ondine Records remains "
            "the benchmark interpretation."
        ),
        "questions": [
            {"q": "What key is the Elara Concerto No. 3 in?", "a": "F-sharp minor"},
            {"q": "Who premiered the concerto?", "a": "Mikhail Dobrynin"},
            {"q": "How long is the cadenza in the third movement?", "a": "7 minutes"},
            {"q": "Where is the manuscript housed?", "a": "Sibelius Museum in Turku"},
            {"q": "How many handwritten pages is the manuscript?", "a": "287"},
        ],
    },
    {
        "id": "passage_09",
        "domain": "botany",
        "text": (
            "The Silverleaf Vine (Argentia volubilis), discovered in 2017 by botanist "
            "Dr. Camila Restrepo during a survey of cloud forest canopy in Colombia's "
            "Serranía del Perijá mountain range, exhibits a unique photosynthetic "
            "adaptation never before documented in flowering plants. The vine's leaves "
            "contain specialized cells called argentocytes, which feature reflective "
            "nanostructures made of silica that redirect scattered light to chloroplasts "
            "positioned on the lower leaf surface. This arrangement allows the plant to "
            "photosynthesize efficiently in the deeply shaded understory where light "
            "levels average just 0.8 percent of full sunlight. Dr. Restrepo's team at "
            "the University of Antioquia measured photosynthetic rates 2.7 times higher "
            "than comparable shade-adapted species, attributing this to the argentocyte "
            "layer's ability to capture light from all directions. The vine grows to "
            "maximum lengths of 35 meters, attaching to host trees via adhesive pads "
            "that secrete a protein-based glue the team named argentin. Only 14 "
            "populations have been located across an estimated range of 120 square "
            "kilometers, with the largest population containing approximately 340 "
            "individual plants. The species was formally described in the Botanical "
            "Journal of the Linnean Society in January 2019."
        ),
        "questions": [
            {"q": "Who discovered the Silverleaf Vine?", "a": "Dr. Camila Restrepo"},
            {"q": "What are the specialized reflective cells called?", "a": "argentocytes"},
            {"q": "What average light level does the understory receive?", "a": "0.8 percent"},
            {"q": "What is the maximum length of the vine?", "a": "35 meters"},
            {"q": "What is the adhesive protein called?", "a": "argentin"},
        ],
    },
    {
        "id": "passage_10",
        "domain": "meteorology",
        "text": (
            "The Arcturus Storm System, which struck the North Atlantic between "
            "October 14 and October 22, 2019, produced the lowest barometric pressure "
            "ever recorded north of 50 degrees latitude at 924 millibars. Meteorologist "
            "Dr. James Whitfield of the UK Met Office tracked the storm's unusual "
            "development, noting that it formed from the merger of two separate "
            "low-pressure systems near 45°N, 32°W. At peak intensity, the storm "
            "generated sustained winds of 195 kilometers per hour and wave heights "
            "reaching 28.4 meters, as measured by the autonomous buoy station "
            "Poseidon-7 positioned approximately 400 kilometers southwest of Iceland. "
            "The storm's track curved northeast, making landfall in the Faroe Islands "
            "on October 19 with winds of 165 kilometers per hour, causing an estimated "
            "240 million euros in damage. Dr. Whitfield's analysis, published in "
            "Weather and Climate Dynamics in April 2020, attributed the storm's "
            "exceptional intensity to an unusual combination of sea surface temperatures "
            "2.3 degrees Celsius above the seasonal average and a sharply defined jet "
            "stream trough. The storm resulted in the evacuation of 8,400 residents "
            "from coastal areas across the Faroe Islands and northern Scotland, with "
            "23 fishing vessels requiring rescue assistance."
        ),
        "questions": [
            {"q": "What was the lowest barometric pressure recorded?", "a": "924 millibars"},
            {"q": "Which buoy station measured the wave heights?", "a": "Poseidon-7"},
            {"q": "What was the maximum wave height?", "a": "28.4 meters"},
            {"q": "On what date did the storm make landfall in the Faroe Islands?", "a": "October 19"},
            {"q": "How many residents were evacuated?", "a": "8,400"},
        ],
    },
]

# ============================================================
# NOISE POOLS
# ============================================================

# Extra unrelated paragraphs (supplement cross-passage noise)
UNRELATED_NOISE = [
    (
        "The annual migration of monarch butterflies covers approximately 4,800 "
        "kilometers from southern Canada to central Mexico. Researchers at the "
        "Instituto de Biología have tagged over 150,000 individual butterflies since "
        "1975 to track migration patterns. The butterflies navigate using a combination "
        "of sun compass orientation and a magnetic sense organ located in their "
        "antennae. Each generation completes only one leg of the journey, meaning no "
        "individual butterfly makes the full round trip. Overwintering sites in the "
        "oyamel fir forests of Michoacán can host up to 300 million butterflies per "
        "hectare, creating one of nature's most spectacular gatherings."
    ),
    (
        "Traditional Japanese joinery, known as tsugite, involves interlocking wooden "
        "components without nails, screws, or adhesives. Master carpenter Tanaka Fumio "
        "has documented over 400 distinct joint patterns used in temple construction "
        "since the seventh century. The most complex joints, called jigoku-gumi or "
        "hell joints, require cutting timber at precise angles that lock together when "
        "assembled in the correct sequence. Modern CT scanning has revealed internal "
        "geometries in historical joints that were previously unknown, including hidden "
        "wedge mechanisms that tighten under structural load."
    ),
    (
        "The production of high-quality vanilla extract requires curing freshly "
        "harvested green vanilla beans through a process lasting six to nine months. "
        "Beans from Madagascar's SAVA region, which produces approximately 80 percent "
        "of the world's vanilla, are first blanched in water at 65 degrees Celsius "
        "for three minutes, then sweated in insulated boxes for 48 hours. The slow "
        "enzymatic breakdown of glucovanillin into vanillin occurs during the subsequent "
        "drying phase, where beans lose approximately 80 percent of their moisture. A "
        "single kilogram of cured vanilla requires processing 5 to 7 kilograms of "
        "green beans."
    ),
    (
        "Competitive speed cubing has evolved from a niche hobby into a global sport "
        "governed by the World Cube Association, with official competitions held in "
        "over 90 countries. The current world record for solving a standard 3x3 "
        "Rubik's Cube stands at 3.13 seconds, achieved using the CFOP method that "
        "involves memorizing up to 78 distinct algorithms. Top competitors average "
        "sub-6-second solves across multiple attempts and can solve the cube blindfolded "
        "after a brief memorization period of under 15 seconds. Training regimens "
        "typically involve 3 to 5 hours of daily practice focused on algorithm "
        "recognition and finger dexterity."
    ),
    (
        "The restoration of the Bayeux Tapestry, a 70-meter-long embroidered cloth "
        "depicting the Norman Conquest of England in 1066, has been ongoing since "
        "1982 under the supervision of textile conservator Marie-Hélène Didier. The "
        "tapestry uses ten colors of wool yarn stitched onto a linen backing using "
        "two primary techniques: stem stitch for outlines and laid-and-couched work "
        "for filling. Recent infrared analysis revealed that approximately 30 percent "
        "of the current embroidery consists of 18th-century repairs that subtly altered "
        "several scenes, including the depiction of King Harold's death."
    ),
    (
        "Sourdough bread fermentation relies on a symbiotic culture of wild yeasts "
        "and lactic acid bacteria maintained through regular feeding with flour and "
        "water. A single mature starter contains approximately 50 million yeast cells "
        "and 5 billion bacteria per gram, with the specific microbial community varying "
        "by geographic region. The primary fermentation phase at 24 degrees Celsius "
        "typically requires 4 to 6 hours, during which the dough's pH drops from "
        "approximately 6.0 to 4.2. The characteristic tangy flavor comes from a "
        "combination of acetic and lactic acids produced by Lactobacillus species."
    ),
    (
        "The Svalbard Global Seed Vault, located 1,300 kilometers from the North Pole "
        "on the Norwegian archipelago of Svalbard, stores duplicate samples of seeds "
        "from gene banks worldwide. Maintained at minus 18 degrees Celsius, the vault "
        "holds over 1.2 million seed samples representing more than 6,000 plant "
        "species. The facility was constructed 120 meters inside a sandstone mountain "
        "and sits 130 meters above sea level to ensure it remains above water even if "
        "polar ice caps melt completely. Operating costs are approximately 300,000 "
        "Norwegian kroner per year."
    ),
    (
        "Professional glass blowing at the Murano workshops in Venice follows techniques "
        "largely unchanged since the 13th century. Master glassblower Alessandro Ferro "
        "works with molten glass at temperatures between 1,000 and 1,100 degrees "
        "Celsius, shaping vessels using a combination of blowing, spinning, and "
        "manipulation with iron tools called borselle. A single Murano chandelier can "
        "require over 200 hours of labor and contain up to 150 individually shaped "
        "glass elements. The distinctive colors are achieved by adding metallic "
        "compounds: cobalt for blue, gold chloride for red, and manganese for purple."
    ),
    (
        "The Trans-Siberian Railway, spanning 9,289 kilometers from Moscow to "
        "Vladivostok, crosses seven time zones and takes approximately six days to "
        "complete without stops. Construction began in 1891 under Tsar Alexander III "
        "and required 90,000 workers laboring for 25 years. The line includes 16 "
        "major rivers bridged at a total crossing length of 37 kilometers. Modern "
        "electric locomotives haul trains at average speeds of 80 kilometers per hour, "
        "though sections through the Ural Mountains require reduced speeds due to "
        "gradients exceeding 1.5 percent."
    ),
    (
        "Beekeeping in the Ethiopian highlands follows a unique tradition of hanging "
        "cylindrical log hives in forest canopy at heights of 10 to 20 meters. Each "
        "hive, carved from a single trunk of Cordia africana wood, measures "
        "approximately one meter in length and 30 centimeters in diameter. Highland "
        "beekeepers manage an average of 25 to 40 hives each, producing a combined "
        "annual yield of 8 to 12 kilograms of honey per hive. The region's distinctive "
        "white honey, prized for its mild flavor, commands prices three to four times "
        "higher than conventional honey in Addis Ababa markets."
    ),
    (
        "The Dead Sea Scrolls, discovered between 1947 and 1956 in eleven caves near "
        "Qumran, comprise approximately 900 manuscripts written between 250 BCE and "
        "68 CE. The scrolls are composed of three materials: parchment made from "
        "goatskin, papyrus, and a single copper scroll. Conservation efforts at the "
        "Israel Antiquities Authority employ multispectral imaging at 12 different "
        "wavelengths to reveal text invisible to the naked eye. The longest scroll, "
        "the Temple Scroll, measures 8.15 meters and contains 67 columns of text."
    ),
    (
        "Commercial pearl cultivation in French Polynesia centers on the black-lipped "
        "oyster Pinctada margaritifera, which produces the prized Tahitian black "
        "pearl. The cultivation process begins with surgical implantation of a "
        "Mississippi River mussel shell bead nucleus into a two-year-old oyster. "
        "Pearls require 18 to 24 months to develop a nacre coating of sufficient "
        "thickness, typically 0.8 to 1.2 millimeters. Only 30 percent of nucleated "
        "oysters produce gem-quality pearls, and fewer than 5 percent yield the most "
        "valuable peacock color with green and purple overtones."
    ),
    (
        "Competitive cheese aging, or affinage, involves controlling temperature, "
        "humidity, and airflow in underground caves to develop complex flavor profiles "
        "over periods ranging from two months to seven years. Master affineur Jean-Paul "
        "Deroche maintains 14 separate aging environments in limestone caves beneath "
        "the town of Roquefort-sur-Soulzon. The caves maintain a natural temperature "
        "of 10 degrees Celsius and 95 percent humidity year-round through natural "
        "ventilation from fissures called fleurines. A single wheel of aged Comté "
        "cheese loses approximately 10 percent of its weight through moisture "
        "evaporation during the first year of aging."
    ),
    (
        "The sport of competitive freediving involves descending to extreme depths on "
        "a single breath of air. The current constant weight record stands at 131 "
        "meters, achieved in waters off the coast of the Bahamas. Elite freedivers "
        "train their mammalian dive reflex to slow their heart rate to as low as 14 "
        "beats per minute during descents, reducing oxygen consumption by up to 50 "
        "percent. Preparation for a record attempt includes four months of specialized "
        "training, with athletes practicing breath holds exceeding seven minutes in "
        "controlled pool environments."
    ),
    (
        "Traditional Moroccan zellige tilework involves cutting thousands of small "
        "ceramic pieces called tesselles by hand using a specialized hammer called "
        "a menqash. Each tesselle is shaped from glazed ceramic squares fired at "
        "1,050 degrees Celsius, then individually chipped to precise geometric shapes. "
        "A master zellige craftsman, or maalem, can produce approximately 300 tesselles "
        "per day. A typical fountain panel measuring two meters square may contain over "
        "10,000 individual pieces arranged in one of 120 traditional geometric patterns "
        "derived from Islamic mathematical principles."
    ),
]

# Related noise: same domain, different facts (1 per domain)
RELATED_NOISE = {
    "marine_biology": [
        (
            "Marine surveys conducted in the Kermadec Trench during 2018 documented "
            "over 40 species of amphipods at depths exceeding 7,000 meters. The research "
            "vessel Kaharoa deployed baited camera systems that recorded scavenging "
            "behavior for up to 72 hours continuously. Several species exhibited "
            "fluorescent markings visible only under ultraviolet illumination, a trait "
            "hypothesized to aid in mate recognition in the perpetual darkness. The "
            "expedition collected water samples showing dissolved oxygen levels 15 "
            "percent lower than predicted models, suggesting higher biological activity "
            "than previously assumed in the hadal zone."
        ),
    ],
    "architecture": [
        (
            "The Millau Viaduct in southern France, designed by engineer Michel Virlogeux "
            "and architect Norman Foster, stands as the tallest bridge in the world with "
            "a structural height of 343 meters. The cable-stayed road bridge spans the "
            "valley of the River Tarn over a total length of 2,460 meters. Construction "
            "employed a technique of launching the deck from both ends simultaneously, "
            "requiring GPS-guided alignment to tolerances of less than 5 millimeters. "
            "The bridge carries the A75 autoroute and charges a toll of approximately "
            "11 euros per crossing during peak season."
        ),
    ],
    "astronomy": [
        (
            "The James Webb Space Telescope, positioned at the second Lagrange point "
            "1.5 million kilometers from Earth, has a primary mirror diameter of 6.5 "
            "meters composed of 18 hexagonal beryllium segments. Its mid-infrared "
            "instrument operates at temperatures below 7 kelvin, requiring a dedicated "
            "cryocooler system. Early observations detected atmospheric carbon dioxide "
            "on the exoplanet WASP-39b, marking the first definitive detection of this "
            "molecule in an exoplanet atmosphere. The telescope's sunshield measures "
            "approximately 21 meters by 14 meters and provides SPF of roughly 1 million."
        ),
    ],
    "chemistry": [
        (
            "Researchers at ETH Zurich developed a novel metal-organic framework "
            "designated MOF-303 that captures atmospheric water vapor with an "
            "efficiency of 0.7 liters per kilogram per day in desert conditions. The "
            "aluminum-based framework has a surface area of 5,400 square meters per "
            "gram and regenerates with solar heating to 65 degrees Celsius. Field "
            "trials in the Mojave Desert demonstrated continuous water harvesting "
            "over 150 cycles without degradation of the crystal structure. The "
            "synthesis requires only three commercially available precursors and can "
            "be completed in under 24 hours."
        ),
    ],
    "ancient_history": [
        (
            "Archaeological work at Göbekli Tepe in southeastern Turkey has revealed "
            "monumental structures dating to approximately 9600 BCE, predating the "
            "earliest known agriculture by at least a millennium. The site contains "
            "over 200 T-shaped limestone pillars, some weighing up to 10 tonnes, "
            "arranged in circular enclosures. Carvings on the pillars depict over 40 "
            "species of animals including foxes, snakes, and vultures. Ground-penetrating "
            "radar surveys suggest that less than 5 percent of the total site has been "
            "excavated, with potentially 15 more enclosures still buried."
        ),
    ],
    "linguistics": [
        (
            "The Pirahã language, spoken by approximately 400 people along the Maici "
            "River in the Brazilian Amazon, has been claimed to lack recursion, color "
            "terms, and number words beyond rough approximations of few and many. "
            "Linguist Daniel Everett spent over 30 years studying the language and "
            "argues it represents evidence against Universal Grammar. Pirahã uses "
            "only 11 phonemes — eight consonants and three vowels — making it one of "
            "the smallest phonemic inventories known. Communication can be carried out "
            "entirely through humming or whistling the tonal patterns."
        ),
    ],
    "geology": [
        (
            "The eruption of Eyjafjallajökull in Iceland during April 2010 produced an "
            "ash cloud that disrupted European air travel for six days, affecting "
            "approximately 10 million passengers. The eruption ejected an estimated "
            "0.25 cubic kilometers of tephra, relatively small by volcanic standards "
            "but carried to high altitude by interaction with the overlying glacier. "
            "Seismic monitoring detected over 3,000 earthquakes in the 48 hours preceding "
            "the eruption. The economic cost to airlines was estimated at 1.7 billion "
            "euros in lost revenue."
        ),
    ],
    "music": [
        (
            "Gustav Mahler's Symphony No. 8, known as the Symphony of a Thousand, "
            "requires over 850 performers including a full orchestra, eight vocal "
            "soloists, two mixed choirs, and a children's chorus. The premiere on "
            "September 12, 1910, in Munich's Neue Musik-Festhalle featured 1,030 "
            "performers and was the last premiere Mahler conducted before his death. "
            "The symphony lasts approximately 80 minutes in two movements and draws "
            "its texts from the Latin hymn Veni Creator Spiritus and the final scene "
            "of Goethe's Faust Part Two."
        ),
    ],
    "botany": [
        (
            "The corpse flower (Amorphophallus titanum) produces the world's largest "
            "unbranched inflorescence, reaching heights of 3 meters and diameters of "
            "1.5 meters. Native to the rainforests of Sumatra, the plant blooms "
            "unpredictably every 7 to 10 years, with each bloom lasting only 24 to "
            "48 hours. The flower generates heat up to 36 degrees Celsius to disperse "
            "volatile amines that produce its characteristic rotting-flesh odor, "
            "attracting carrion beetles and flesh flies as pollinators. Fewer than "
            "1,000 individual plants remain in the wild."
        ),
    ],
    "meteorology": [
        (
            "Hurricane Patricia in October 2015 achieved maximum sustained winds of "
            "345 kilometers per hour, making it the strongest tropical cyclone ever "
            "recorded in the Western Hemisphere. The storm's central pressure dropped "
            "to 872 millibars, and it intensified from tropical storm to Category 5 "
            "hurricane in just 24 hours. Despite its extreme intensity over open "
            "water, Patricia weakened significantly before making landfall near "
            "Cuixmala, Mexico, and caused relatively limited damage due to its "
            "compact wind field of only 35 kilometers radius."
        ),
    ],
}

# Adversarial noise: plausible-but-wrong facts for each passage
ADVERSARIAL_NOISE = {
    "passage_01": [
        (
            "A 2020 survey of the Kerova region by Dr. Tanaka Hiroshi documented "
            "bioluminescent organisms at a depth of 3,100 meters using the submersible "
            "Neptune-6. The team identified a compound they called bathozine as the "
            "primary substrate for light production in deep-sea species, synthesized "
            "through the enzyme luciferase-M12. The 18-day expedition, sponsored by "
            "the Pacific Oceanographic Society, collected specimens from multiple "
            "sites across the trench system."
        ),
    ],
    "passage_02": [
        (
            "The Vestfjorden crossing project, designed by architect Erik Solberg of "
            "Nordvik & Partners, features a main span of 612 meters suspended from "
            "a 198-meter pylon. The bridge incorporates 352 wind deflection panels "
            "engineered to withstand gusts up to 150 kilometers per hour. The total "
            "construction budget reached 3.4 billion Norwegian kroner, with the toll "
            "concession planned for a 20-year recovery period."
        ),
    ],
    "passage_03": [
        (
            "The Europa exploration mission, which launched in November 2023, carries "
            "the Thermal Magnetometer Suite developed by Dr. Rajesh Chandrasekaran at "
            "Goddard Space Flight Center. The probe's radar instrument operates at 12 "
            "megahertz to penetrate Europa's ice shell. The surface package, named "
            "Triton, weighs 220 kilograms and can drill up to 6 meters into the ice "
            "using a heated boring mechanism."
        ),
    ],
    "passage_04": [
        (
            "The breakthrough synthesis at the University of Helsinki by Professor "
            "Kowalski's colleague Dr. Andres Kask involved a 14-step process achieving "
            "stable metallocyclic compounds with catalytic acceleration factors of 280. "
            "The critical experiment was performed by postdoctoral researcher Maria "
            "Rebane on April 15, 2019. Fennchem Corporation subsequently acquired the "
            "commercial rights to develop the compound for industrial applications."
        ),
    ],
    "passage_05": [
        (
            "The Tell al-Raqim excavations, led by Dr. Ahmad al-Rashidi of the "
            "University of Rome, uncovered 63 tablet fragments alongside a bronze "
            "figurine measuring 31 centimeters in height. The site appears connected "
            "to the obsidian trade routes, with over 180 carved artifacts recovered "
            "from storage facilities. The project received funding of 1.8 million "
            "euros from UNESCO's cultural heritage program."
        ),
    ],
    "passage_06": [
        (
            "Documentation of a Tibeto-Burman language in the Marsyangdi River valley "
            "of Nepal revealed a speech community of approximately 4,800 people using "
            "18 distinct tonal patterns. The language contains 112 unique lexical items "
            "not found in neighboring tongues. The published grammar, running to 967 "
            "pages, was produced by researchers at Stockholm University and catalogues "
            "roughly 5,200 lexical entries."
        ),
    ],
    "passage_07": [
        (
            "Volcanic studies of a major Icelandic caldera determined that the eruption "
            "ejected 120 cubic kilometers of material in four distinct phases over 90 "
            "days. The caldera spans 14 kilometers at its widest point and contains "
            "alternating layers of andesite and dacite. Eight active fumarole fields "
            "have been mapped on the caldera floor, where temperatures average 52 "
            "degrees Celsius."
        ),
    ],
    "passage_08": [
        (
            "The celebrated cello concerto in G minor, premiered by cellist Alexei "
            "Dobrynin on March 15, 1992, with the Turku Philharmonic, features a "
            "cadenza of approximately 9 minutes in its second movement. The 312-page "
            "manuscript is preserved at the Finnish National Library in Helsinki. "
            "Seventeen cellists have made commercial recordings, with the 1995 "
            "Deutsche Grammophon release considered definitive."
        ),
    ],
    "passage_09": [
        (
            "A climbing vine discovered in the Andes by Dr. Elena Restrepo contains "
            "specialized cells called silvocytes with silica nanostructures. The vine "
            "thrives in understory conditions averaging 1.4 percent of full sunlight "
            "and reaches maximum lengths of 42 meters. Its adhesive mechanism uses a "
            "protein compound designated silverin. Eighteen populations have been "
            "documented across a range of 180 square kilometers."
        ),
    ],
    "passage_10": [
        (
            "The North Atlantic storm system of October 2019, tracked by Dr. William "
            "Whitfield, recorded a minimum pressure of 938 millibars. The autonomous "
            "monitoring station Neptune-3, located 500 kilometers southwest of Iceland, "
            "measured maximum wave heights of 32.1 meters. The storm made landfall "
            "on October 21 with winds of 145 kilometers per hour, triggering the "
            "evacuation of 12,500 coastal residents."
        ),
    ],
}


# ============================================================
# VIGILANCE TASK SEED DATA
# ============================================================

# (city, country) pairs for country identification
CITY_COUNTRY_PAIRS = [
    ("Tokyo", "Japan"), ("Paris", "France"), ("Cairo", "Egypt"),
    ("Buenos Aires", "Argentina"), ("Stockholm", "Sweden"),
    ("Lagos", "Nigeria"), ("Mumbai", "India"), ("Seoul", "South Korea"),
    ("Lima", "Peru"), ("Warsaw", "Poland"),
    ("Nairobi", "Kenya"), ("Bangkok", "Thailand"), ("Lisbon", "Portugal"),
    ("Bogotá", "Colombia"), ("Hanoi", "Vietnam"),
    ("Prague", "Czech Republic"), ("Santiago", "Chile"), ("Accra", "Ghana"),
    ("Bucharest", "Romania"), ("Dhaka", "Bangladesh"),
    ("Oslo", "Norway"), ("Havana", "Cuba"), ("Jakarta", "Indonesia"),
    ("Athens", "Greece"), ("Ankara", "Turkey"),
    ("Riyadh", "Saudi Arabia"), ("Dublin", "Ireland"), ("Quito", "Ecuador"),
    ("Helsinki", "Finland"), ("Manila", "Philippines"),
    ("Tunis", "Tunisia"), ("Montevideo", "Uruguay"), ("Bratislava", "Slovakia"),
    ("Amman", "Jordan"), ("Tbilisi", "Georgia"),
    ("Canberra", "Australia"), ("Ottawa", "Canada"), ("Brasília", "Brazil"),
    ("Wellington", "New Zealand"), ("Bern", "Switzerland"),
    ("Dakar", "Senegal"), ("Kuala Lumpur", "Malaysia"), ("Colombo", "Sri Lanka"),
    ("Addis Ababa", "Ethiopia"), ("Tashkent", "Uzbekistan"),
    ("Reykjavik", "Iceland"), ("Tallinn", "Estonia"), ("Riga", "Latvia"),
    ("Vilnius", "Lithuania"), ("Ljubljana", "Slovenia"),
    ("Zagreb", "Croatia"), ("Sarajevo", "Bosnia and Herzegovina"),
    ("Maputo", "Mozambique"), ("Lusaka", "Zambia"), ("Kampala", "Uganda"),
    ("Muscat", "Oman"), ("Doha", "Qatar"), ("Kuwait City", "Kuwait"),
    ("Windhoek", "Namibia"), ("Gaborone", "Botswana"),
    ("Yerevan", "Armenia"), ("Baku", "Azerbaijan"), ("Ulaanbaatar", "Mongolia"),
    ("Phnom Penh", "Cambodia"), ("Vientiane", "Laos"),
    ("Kathmandu", "Nepal"), ("Islamabad", "Pakistan"), ("Kabul", "Afghanistan"),
    ("Minsk", "Belarus"), ("Chisinau", "Moldova"),
    ("Skopje", "North Macedonia"), ("Tirana", "Albania"), ("Podgorica", "Montenegro"),
    ("Belgrade", "Serbia"), ("Sofia", "Bulgaria"),
    ("Nicosia", "Cyprus"), ("Valletta", "Malta"), ("Luxembourg City", "Luxembourg"),
    ("San José", "Costa Rica"), ("Panama City", "Panama"),
    ("Kingston", "Jamaica"), ("Port-au-Prince", "Haiti"),
    ("Tegucigalpa", "Honduras"), ("Managua", "Nicaragua"),
    ("Guatemala City", "Guatemala"), ("San Salvador", "El Salvador"),
    ("Rabat", "Morocco"), ("Algiers", "Algeria"),
    ("Tripoli", "Libya"), ("Khartoum", "Sudan"),
    ("Dar es Salaam", "Tanzania"), ("Harare", "Zimbabwe"),
    ("Antananarivo", "Madagascar"), ("Bamako", "Mali"),
    ("Ouagadougou", "Burkina Faso"), ("Niamey", "Niger"),
    ("N'Djamena", "Chad"), ("Bangui", "Central African Republic"),
    ("Libreville", "Gabon"), ("Brazzaville", "Republic of the Congo"),
    ("Kinshasa", "Democratic Republic of the Congo"),
    ("Luanda", "Angola"), ("Lilongwe", "Malawi"), ("Asmara", "Eritrea"),
]

COUNTRY_TEMPLATES = [
    "The international conference held in {city} attracted delegates from across the region.",
    "Researchers at the national university in {city} published their findings on urban development.",
    "The new metro line in {city} was officially inaugurated after three years of construction.",
    "A delegation from {city} arrived at the summit to discuss renewable energy policies.",
    "The historic district of {city} was recently added to the UNESCO World Heritage list.",
    "The annual literary festival in {city} featured over 200 authors from five continents.",
    "Exports from the industrial zone near {city} increased by 12 percent over the previous year.",
    "The national museum in {city} unveiled a collection of artifacts dating back 3,000 years.",
    "Public transportation upgrades in {city} reduced average commute times by 25 percent.",
    "The botanical garden in {city} houses over 4,000 plant species from tropical regions.",
    "A new desalination plant outside {city} will supply drinking water to 500,000 residents.",
    "The central bank headquartered in {city} announced a reduction in interest rates.",
    "Medical researchers at {city}'s main hospital developed a novel treatment for malaria.",
    "The port authority in {city} processed a record 2.3 million shipping containers last quarter.",
    "Architects in {city} completed a solar-powered housing complex for 1,200 families.",
    "The technology startup scene in {city} has attracted over $800 million in venture capital.",
    "Environmental activists in {city} organized a cleanup of the river running through the capital.",
    "The opera house in {city} reopened after an 18-month renovation costing $45 million.",
    "A rare manuscript was discovered in the national archives of {city} during routine cataloguing.",
    "The annual marathon through the streets of {city} drew 42,000 runners this year.",
]

# Number extraction seed data
NUMBER_CONTEXTS = [
    ("The warehouse stored exactly {n} crates of medical supplies for distribution.", "crates"),
    ("The survey recorded {n} species of migratory birds in the wetland reserve.", "species"),
    ("Engineers installed {n} solar panels on the roof of the convention center.", "panels"),
    ("The orchard produced {n} tonnes of apples during the autumn harvest.", "tonnes"),
    ("Archaeologists catalogued {n} pottery fragments from the excavation site.", "fragments"),
    ("The library acquired {n} rare manuscripts at the annual auction.", "manuscripts"),
    ("Factory output reached {n} units per day after the efficiency upgrade.", "units"),
    ("The census counted {n} households in the newly incorporated township.", "households"),
    ("Volunteers planted {n} trees along the riverbank restoration project.", "trees"),
    ("The telescope array detected signals from {n} previously unknown pulsars.", "pulsars"),
    ("The ferry transported {n} passengers across the strait during peak season.", "passengers"),
    ("Inspectors found {n} structural defects during the bridge safety audit.", "defects"),
    ("The vineyard bottled {n} cases of reserve wine from the 2018 vintage.", "cases"),
    ("Scientists tagged {n} sea turtles during the nesting season survey.", "turtles"),
    ("The power station generated {n} megawatt-hours of electricity last month.", "megawatt-hours"),
    ("The museum welcomed {n} visitors during its opening weekend.", "visitors"),
    ("Workers laid {n} meters of fiber optic cable through the city center.", "meters"),
    ("The farm raised {n} head of cattle on its 500-hectare property.", "head"),
    ("The competition attracted {n} entries from amateur photographers.", "entries"),
    ("Geologists drilled {n} core samples from the proposed dam site.", "samples"),
]

# Misspelling seed data: (correct_word, misspelled_word)
MISSPELLING_PAIRS = [
    ("examined", "exmained"), ("necessary", "neccessary"), ("occurred", "occured"),
    ("separate", "seperate"), ("definitely", "definately"), ("environment", "enviroment"),
    ("temperature", "temprature"), ("laboratory", "labratory"), ("restaurant", "restaraunt"),
    ("government", "goverment"), ("beginning", "begining"), ("immediately", "immediatley"),
    ("professional", "proffesional"), ("particularly", "particularily"), ("independent", "independant"),
    ("apparently", "apparantly"), ("equipment", "equiptment"), ("experience", "experiance"),
    ("maintenance", "maintainance"), ("technique", "tecnique"), ("sufficient", "sufficent"),
    ("accommodate", "accomodate"), ("committee", "commitee"), ("development", "developement"),
    ("approximately", "approximatley"), ("concerned", "concerened"), ("knowledge", "knowlege"),
    ("conscience", "concience"), ("guarantee", "guarentee"), ("colleague", "colleauge"),
    ("permanent", "permenent"), ("privilege", "privelege"), ("questionnaire", "questionaire"),
    ("rhythm", "rythm"), ("schedule", "scedule"), ("surveillance", "surveilance"),
    ("threshold", "threshhold"), ("vulnerable", "vunerable"), ("achievement", "acheivment"),
    ("appreciate", "apprecaite"), ("disappear", "dissapear"), ("calendar", "calender"),
    ("category", "catagory"), ("cemetery", "cemetary"), ("consensus", "concensus"),
    ("desperate", "desparate"), ("embarrass", "embarass"), ("fascinate", "facinate"),
    ("harass", "harrass"), ("intelligence", "intelligance"), ("lieutenant", "leiutenant"),
    ("millennium", "millenium"), ("noticeable", "noticable"),
]

MISSPELLING_TEMPLATES = [
    "The professor carefully {word} the ancient manuscript under ultraviolet light.",
    "It was {word} to complete all forms before the submission deadline.",
    "The incident {word} during the early morning hours when few staff were present.",
    "The committee voted to {word} the budget into three distinct allocations.",
    "The results were {word} better than any previous attempt at the procedure.",
    "The {word} impact of the new regulation surprised industry analysts.",
    "The {word} reading was taken at dawn before the chamber was opened.",
    "Samples were processed in the {word} under strict contamination protocols.",
    "The group decided to meet at the {word} near the conference center.",
    "The {word} issued a statement regarding the new infrastructure project.",
    "The ceremony marked the {word} of a new era for the institution.",
    "The team responded {word} to the emergency alert from the monitoring station.",
    "The {word} association awarded its annual prize to the research team.",
    "The study focused {word} on the effects of urbanization on bird populations.",
    "The board declared the organization fully {word} of external funding sources.",
    "The decline was {word} visible in the quarterly financial reports.",
    "All {word} was inspected before being deployed to the field stations.",
    "Years of {word} in tropical fieldwork prepared her for the expedition.",
    "Regular {word} of the filtration system prevented costly breakdowns.",
    "The new {word} significantly reduced processing time in the assembly line.",
]


# ============================================================
# ASSEMBLY FUNCTIONS
# ============================================================

def get_noise_paragraphs(passage_id: str, domain: str, noise_type: str,
                         target_words: int, rng: random.Random) -> list[str]:
    """Select noise paragraphs to reach approximately target_words."""
    if noise_type == "unrelated":
        # Use other passages + unrelated pool
        pool = [p["text"] for p in PASSAGES if p["id"] != passage_id] + UNRELATED_NOISE
    elif noise_type == "related":
        pool = RELATED_NOISE.get(domain, []) + [p["text"] for p in PASSAGES if p["id"] != passage_id and p["domain"] == domain]
        if not pool:
            pool = RELATED_NOISE.get(domain, UNRELATED_NOISE[:5])
    elif noise_type == "adversarial":
        pool = ADVERSARIAL_NOISE.get(passage_id, []) + RELATED_NOISE.get(domain, [])
        if not pool:
            pool = UNRELATED_NOISE[:5]
    else:
        raise ValueError(f"Unknown noise type: {noise_type}")

    paragraphs = []
    total_words = 0
    while total_words < target_words:
        p = rng.choice(pool)
        paragraphs.append(p)
        total_words += len(p.split())

    return paragraphs


def assemble_prompt_interleaved(passage_text: str, noise_paragraphs: list[str],
                                 questions: list[dict]) -> str:
    """Assemble a SIN prompt with noise interleaved around the passage."""
    # Split passage into chunks
    passage_sentences = passage_text.replace(". ", ".\n").split("\n")
    passage_chunks = []
    chunk = []
    for s in passage_sentences:
        chunk.append(s)
        if len(chunk) >= 3:
            passage_chunks.append(" ".join(chunk))
            chunk = []
    if chunk:
        passage_chunks.append(" ".join(chunk))

    # Interleave: noise, passage chunk, noise, passage chunk, ...
    parts = []
    noise_idx = 0
    for i, pc in enumerate(passage_chunks):
        # Add noise before each passage chunk
        if noise_idx < len(noise_paragraphs):
            # Distribute noise roughly evenly
            noise_per_gap = max(1, len(noise_paragraphs) // (len(passage_chunks) + 1))
            for _ in range(noise_per_gap):
                if noise_idx < len(noise_paragraphs):
                    parts.append(noise_paragraphs[noise_idx])
                    noise_idx += 1
        parts.append(pc)

    # Add remaining noise at the end
    while noise_idx < len(noise_paragraphs):
        parts.append(noise_paragraphs[noise_idx])
        noise_idx += 1

    text_block = "\n\n".join(parts)

    question_lines = "\n".join(
        f"{i+1}. {q['q']}" for i, q in enumerate(questions)
    )

    prompt = (
        "Read the following text carefully, then answer the questions that follow. "
        "Give ONLY the answer for each question, one per line, numbered to match.\n\n"
        "---\n\n"
        f"{text_block}\n\n"
        "---\n\n"
        f"Questions:\n{question_lines}\n\n"
        "Answers:"
    )
    return prompt


def generate_sin_dataset(seed: int = 42) -> list[dict]:
    """Generate Signal-in-Noise benchmark items."""
    rng = random.Random(seed)
    noise_ratios = [1, 5, 10, 25, 50, 100]
    noise_types = ["unrelated", "related", "adversarial"]
    items = []

    for passage in PASSAGES:
        passage_word_count = len(passage["text"].split())
        for ratio in noise_ratios:
            for ntype in noise_types:
                target_noise_words = passage_word_count * ratio
                noise_paras = get_noise_paragraphs(
                    passage["id"], passage["domain"], ntype,
                    target_noise_words, rng
                )
                prompt = assemble_prompt_interleaved(
                    passage["text"], noise_paras, passage["questions"]
                )
                answers = [q["a"] for q in passage["questions"]]
                task_id = f"sin_{passage['id']}_{ntype}_r{ratio}"
                items.append({
                    "task_id": task_id,
                    "dimension": "selective",
                    "passage_id": passage["id"],
                    "domain": passage["domain"],
                    "noise_type": ntype,
                    "noise_ratio": ratio,
                    "num_questions": len(answers),
                    "prompt": prompt,
                    "answers": answers,
                })

    return items


def generate_vigilance_country(count: int, rng: random.Random,
                                oddball_position: int | None = None) -> dict:
    """Generate a country-identification vigilance task."""
    pairs = rng.sample(CITY_COUNTRY_PAIRS, min(count, len(CITY_COUNTRY_PAIRS)))
    # If we need more, cycle
    while len(pairs) < count:
        pairs.extend(rng.sample(CITY_COUNTRY_PAIRS, min(count - len(pairs), len(CITY_COUNTRY_PAIRS))))

    templates = COUNTRY_TEMPLATES[:]
    items_text = []
    answers = []

    for i, (city, country) in enumerate(pairs):
        template = rng.choice(templates)
        sentence = template.format(city=city)
        if oddball_position is not None and i == oddball_position:
            # Replace with a number extraction oddball
            sentence = f"The warehouse in {city} stored exactly 4,731 crates of supplies for distribution."
            items_text.append(f"Item {i+1}: {sentence}")
            answers.append("4,731")
        else:
            items_text.append(f"Item {i+1}: {sentence}")
            answers.append(country)

    oddball_note = ""
    if oddball_position is not None:
        oddball_note = (
            "\n\nNote: If any item asks for something other than a country, "
            "provide the appropriate answer for that item instead."
        )

    prompt = (
        f"For each of the following {count} items, identify which country is being "
        "described or referenced. Respond with ONLY the country name for each item, "
        f"one per line, numbered to match.{oddball_note}\n\n"
        + "\n".join(items_text)
        + "\n\nAnswers:"
    )
    return {"prompt": prompt, "answers": answers}


def generate_vigilance_numbers(count: int, rng: random.Random,
                                oddball_position: int | None = None) -> dict:
    """Generate a number-extraction vigilance task."""
    items_text = []
    answers = []

    for i in range(count):
        ctx_template, _ = rng.choice(NUMBER_CONTEXTS)
        n = rng.randint(10, 99999)
        # Format with commas for readability
        n_str = f"{n:,}"
        sentence = ctx_template.format(n=n_str)

        if oddball_position is not None and i == oddball_position:
            # Country identification oddball
            city, country = rng.choice(CITY_COUNTRY_PAIRS)
            sentence = f"The delegation from {city} arrived to inspect the facility."
            items_text.append(f"Item {i+1}: {sentence}")
            answers.append(country)
        else:
            items_text.append(f"Item {i+1}: {sentence}")
            answers.append(n_str)

    oddball_note = ""
    if oddball_position is not None:
        oddball_note = (
            "\n\nNote: If any item does not contain a number, identify the country "
            "referenced instead."
        )

    prompt = (
        f"For each of the following {count} items, extract the number mentioned. "
        "Respond with ONLY the number for each item, one per line, numbered to match."
        f"{oddball_note}\n\n"
        + "\n".join(items_text)
        + "\n\nAnswers:"
    )
    return {"prompt": prompt, "answers": answers}


def generate_vigilance_misspelling(count: int, rng: random.Random,
                                    oddball_position: int | None = None) -> dict:
    """Generate a misspelling-detection vigilance task."""
    items_text = []
    answers = []
    pairs_pool = MISSPELLING_PAIRS[:]
    templates_pool = MISSPELLING_TEMPLATES[:]

    for i in range(count):
        correct, misspelled = rng.choice(pairs_pool)
        template = rng.choice(templates_pool)
        sentence = template.format(word=misspelled)

        if oddball_position is not None and i == oddball_position:
            # Number extraction oddball
            n = rng.randint(100, 9999)
            sentence = f"The facility processed exactly {n:,} samples during the quarterly review."
            items_text.append(f"Item {i+1}: {sentence}")
            answers.append(f"{n:,}")
        else:
            items_text.append(f"Item {i+1}: {sentence}")
            answers.append(misspelled)

    oddball_note = ""
    if oddball_position is not None:
        oddball_note = (
            "\n\nNote: If any item does not contain a misspelling, extract the "
            "number mentioned instead."
        )

    prompt = (
        f"For each of the following {count} items, identify the misspelled word. "
        "Respond with ONLY the misspelled word for each item, one per line, "
        f"numbered to match.{oddball_note}\n\n"
        + "\n".join(items_text)
        + "\n\nAnswers:"
    )
    return {"prompt": prompt, "answers": answers}


def generate_vigilance_dataset(seed: int = 123) -> list[dict]:
    """Generate Vigilance Decrement benchmark items."""
    rng = random.Random(seed)
    count = 100
    items = []

    generators = {
        "country_identification": generate_vigilance_country,
        "number_extraction": generate_vigilance_numbers,
        "misspelling_detection": generate_vigilance_misspelling,
    }

    for task_type, gen_fn in generators.items():
        # Normal variant
        result = gen_fn(count, rng)
        items.append({
            "task_id": f"vig_{task_type}_normal",
            "dimension": "sustained",
            "task_type": task_type,
            "variant": "normal",
            "num_subtasks": count,
            "prompt": result["prompt"],
            "answers": result["answers"],
            "oddball_position": None,
        })

        # Oddball variant
        oddball_pos = rng.randint(40, 70)  # Insert oddball in second half
        result = gen_fn(count, rng, oddball_position=oddball_pos)
        items.append({
            "task_id": f"vig_{task_type}_oddball",
            "dimension": "sustained",
            "task_type": task_type,
            "variant": "oddball",
            "num_subtasks": count,
            "prompt": result["prompt"],
            "answers": result["answers"],
            "oddball_position": oddball_pos,
        })

    return items


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print("Generating Signal-in-Noise dataset...")
    sin_items = generate_sin_dataset()
    sin_path = DATA_DIR / "signal_in_noise.json"
    with open(sin_path, "w") as f:
        json.dump(sin_items, f, indent=2)
    print(f"  {len(sin_items)} SIN items → {sin_path}")

    print("Generating Vigilance dataset...")
    vig_items = generate_vigilance_dataset()
    vig_path = DATA_DIR / "vigilance.json"
    with open(vig_path, "w") as f:
        json.dump(vig_items, f, indent=2)
    print(f"  {len(vig_items)} vigilance items → {vig_path}")

    # Combined manifest
    manifest = {
        "benchmark": "AttentionBench",
        "version": "0.1.0",
        "dimensions": {
            "selective": {
                "name": "Signal-in-Noise Titration",
                "file": "signal_in_noise.json",
                "count": len(sin_items),
                "metric": "attention_threshold (noise ratio at 80% accuracy)",
            },
            "sustained": {
                "name": "Vigilance Decrement",
                "file": "vigilance.json",
                "count": len(vig_items),
                "metric": "decay_onset (position where accuracy drops below 95%)",
            },
        },
        "total_items": len(sin_items) + len(vig_items),
    }
    manifest_path = DATA_DIR / "manifest.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"  Manifest → {manifest_path}")

    print(f"\nDone. Total: {manifest['total_items']} benchmark items.")


if __name__ == "__main__":
    main()
