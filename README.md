# Voxlet Assets: Voxlet's own picture pack

Voxlet's videos use about 24,000 downloaded icons and illustrations (Tabler, Phosphor, Lucide,
Material, Fluent Emoji, Open Doodles…). Most are UI symbols that never belong in a video, styles
are mixed, and names follow the icon authors' words, not the words scripts use. The plan: build
**our own pack**, in one style, made for the engine's animations, named with the words people
actually say in quiz and explainer videos. This repo holds the catalogue, the drawing scripts and
the drawings; the Voxlet app (separate repo) downloads the built pack from this repo's GitHub
Releases. Licence: see [LICENSE](LICENSE) (own pack, for use through Voxlet only).

## Publishing a new version of the pack

```powershell
python tools/build_pack.py
```

This writes `dist/voxlet-own.zip` (index plus every drawn SVG; `dist/` is not in git). Make a
GitHub Release in this repo (tag like `v2026.11.23`) and attach `dist/voxlet-own.zip` with exactly
that name. The app's pack list (`native/video/assets/packs.json` in the voxlet repo, pack
`voxlet-own`) downloads `releases/latest/download/voxlet-own.zip`, so the newest release is what
users get when they install or re-install the pack. Update `size_mb` there when it grows a lot.

**Made so far**: the viewer (with a border on/off toggle), the drawing helpers
(`tools/draw_lib.py`), 4,572 drawings, the pack builder (`tools/build_pack.py`), the catalogue checker (`tools/check_catalog.py`) and the full
catalogue (47 categories, 467 groups, 7,824 items).

> **New session?** Say **"start asset studio"**. Claude reads this file, finds the first unchecked
> box in [Next steps](#next-steps), does that step only, ticks it, and stops to show the result.

## Watching drawings appear (viewer)

`viewer.html` shows every drawing in `svg/<category>/<id>.svg` and checks for new ones every 3
seconds (new ones get a green outline). You can pick a category, search an id, switch to a dark
background, click a drawing to see it big, and see which catalogue items aren't drawn yet.

```powershell
python -m http.server 8765 --directory D:\voxlet-assets
```

Then open http://localhost:8765/viewer.html. In the Claude app the same server is saved as
`asset-viewer` in `.claude/launch.json`.

## Next steps

Tick each box here when it is done.

### Phase 1: the catalogue (the list of what to draw)
- [x] Write `tools/check_catalog.py` (standard-library Python), as described in
      [Catalogue format](#catalogue-format) (checks, `--find`, `--todo`, progress).
- [x] Write `catalog/<category>.json` for every category in
      [Categories](#categories), following the format and ownership rules below. Do it in batches
      (a few categories per step) and run the checker after each batch. Tick the parent box when
      every batch is done. Owners come before the files that `see` them.
      - [x] 1. `symbols-signs`, `concepts-ideas`, `brain-teasers-logic` (714 items)
      - [x] 2. `emotions-expressions`, `jobs-people`, `time-calendar` (436 items)
      - [x] 3. `science`, `math` (all 118 elements: large)
      - [x] 4. `space`, `weather-climate`, `energy-environment`
      - [x] 5. `animals`, `ocean-underwater`, `plants-nature`
      - [x] 6. `human-body`, `health-medicine`, `psychology-mind`
      - [x] 7. `food-drink`, `agriculture`
      - [x] 8. `earth-geography` (all countries, flags, states: large, alone)
      - [x] 9. `cities-capitals`, `landmarks`, `travel-tourism`
      - [x] 10. `religion-faith`, `celebrations-holidays`
      - [x] 11. `history`, `inventions-discoveries`, `future-tech`
      - [x] 12. `fantasy-mythology`, `mysteries-unexplained`, `world-records`, `law-government`
      - [x] 13. `languages-writing`, `education-school`, `communication-media`
      - [x] 14. `transport-vehicles`, `tools-industry`, `technology`
      - [x] 15. `buildings-places`, `home-household`, `clothing-accessories`
      - [x] 16. `movies-entertainment`, `music-arts`, `hobbies-leisure`, `sports-games`
      - [x] 17. `money-business`, `safety-emergency`
- [x] Write `catalog/playlists.json`: for each quiz playlist in
      [Quiz playlists](#quiz-playlists), the categories and groups it draws from, so drawing can
      follow the playlists.

### Phase 2: style sheet (decide the look)
- [x] Draw 12 test SVGs in two candidate styles (A: flat with no outline, B: flat with a soft dark
      outline): lion, heart (organ), earth, Kaaba, rocket, apple, doctor, idea, volcano, flag of
      India, arrow right, trophy. Put them in `svg/_style-test/`.
- [ ] Render a frame with each through the engine (`cargo run --example vidtool -- render …`), make
      a contact sheet, and show it to the user.
- [x] The user picks the style and the licence for our pack (style B; licence later); update the
      [Style guide](#style-guide) and save the colour palette in `style/palette.json`.

### Phase 3: drawing pipeline
- [ ] `vidtool draw <item-id|category> [--count N]` in `native/video/examples/vidtool.rs`: builds a
      prompt from the style guide and the item (name, other names, kind, recolor), asks Gemini
      (key from `GEMINI_API_KEY`), cleans the SVG with the existing `svgcheck`, normalises it with
      `usvg`, saves `svg/<category>/<id>.svg`, and skips ids already drawn.
- [ ] `vidtool sheet <category>`: a contact sheet PNG of a category (light and dark theme) for
      review.
- [ ] Review loop: delete bad drawings, draw again (Gemini, or Claude by hand), repeat.
- [ ] Optional `vidtool trace <png>` with vtracer, to turn hand sketches into SVG.

### Phase 4: ship the pack in the app
- [x] `tools/build_pack.py`: builds the `voxlet-own` pack zip (`index.json`: id, name, category, group,
      kind, recolor, motion, tags = name, other names, group and category) from `svg/` and the catalogue.
- [x] The app downloads it like the other packs (pack `voxlet-own` in the app's `packs.json`, format
      `voxlet-own`, from this repo's latest GitHub Release); it is listed first.
- [x] Search ranks `voxlet-own` first; the downloaded packs become the fallback.
- [x] First GitHub Release of this repo with `voxlet-own.zip` (v2026.11.23).
- [ ] Gemini's storyboard and quiz prompts get the catalogue's names, so they ask for pictures we
      have.

### Phase 5: animated parts in the engine
- [x] Engine (`native/video/src/parts.rs` in the voxlet repo): pictures with `part-*` groups and a
      `data-pivot` get an idle loop (2.4 s): `part-eye-*` blink, `part-wing-*` flap, `part-flame`
      flickers, `part-glow` pulses, `part-hand-minute`/`part-hand-hour` turn, `part-wheel`/`part-globe`
      spin. Each picture is parsed at 24 loop steps, once each, and cached.
- [x] Tested with the real pack (`vidtool install-local`, then `vidtool render`): wings flap and eyes
      blink in rendered frames.
- [ ] More motions when drawings need them: sway (plants, flags), wave (hands), beat (hearts),
      breathe (sleeping animals), needle (compass).

### Phase 6: draw everything, playlist by playlist
Drawn by Claude by hand (decided November 2026), about 50 to 100 drawings per batch, reviewed
after each. Each category has a script `drawings/<category>.py` using
`tools/draw_lib.py`; run `python drawings/<category>.py [ids…]` to (re)draw.
- [ ] Engine: a `border` on/off option when loading own-pack SVGs (uses the `data-outline` marks).

Progress (4,572 of 7,824): finished: `symbols-signs`, `concepts-ideas`, `brain-teasers-logic`,
`religion-faith`, `celebrations-holidays`, `animals`, `ocean-underwater`, `space`, `human-body`,
`health-medicine`, `psychology-mind`, `earth-geography`, `cities-capitals`, `landmarks`, `science`, `math`,
`inventions-discoveries`, `future-tech`, `technology`, `history`.
In progress (step 8): `fantasy-mythology` has its 42 classic creatures (`fantasy_a.py`); still to draw: world-myth
creatures, magic items, Greek/Norse/Egyptian myth objects, fantasy places (60 items). Then `mysteries-unexplained` (56).
`history` is in `history_a.py` (origins to ancient Americas) and `history_b.py` (Islamic golden age to archaeology).

`science` (`science_elements.py`: the 118 element tiles, colour = element family; `science.py`, `science2.py`,
`science3.py`: lab equipment, atoms, matter, forces, electricity, light/sound/heat, biology, experiments), `math`
(`math_a.py`: mono symbols, number tiles, fractions, 2D/3D shapes; `math_b.py`: geometry, tools, charts,
probability, measurement), `technology` (`technology_a.py`, `technology_b.py`), `future-tech` (`future_tech.py`) and
`inventions-discoveries` (`inventions_a.py` natural colours, `inventions_b.py` themed). Technology, future-tech and
recent inventions use the themed palette only (helpers in `drawings/_tech.py`). `tools/sheet.html` is a contact
sheet for review: `http://localhost:8765/tools/sheet.html?cat=science&cols=8&ids=a,b,c` (also `from`, `n`, `skip`,
`match`, `dark=1`, `noborder=1`).

`cities-capitals` (`drawings/cities_capitals.py`): the country's map with a pin at the city, the
country's flag and the city's name (coordinates typed by hand; Jerusalem shows Israel and Palestine
together with no flag). `landmarks` (`drawings/landmarks.py`): hand-drawn scenes.

Animals: four-legged mammals use `quad()` in `drawings/_animals.py` (one silhouette: back line, deep
chest, haunch, tapered neck, skull + muzzle head, legs with knees and hocks; patterns clipped to the body).

`earth-geography` scripts: `earth_geography.py` (maps from Natural Earth: countries, continents, oceans,
seas, rivers, lakes, peaks, ranges, deserts, islands, Indian and US states), `earth_geography_hand.py`
(landforms, earth layers, volcanoes, rocks, gems, fossils, biomes, maps and navigation) and `flags.py`
(flags drawn from a spec table; emblems and coats of arms simplified for icon size; Afghanistan is the
tricolour seated at the UN).
- [x] Text-tile tool (`tools/text_tile.py`): lettering as paths, shaped with HarfBuzz (Arabic joining,
      Devanagari, Gurmukhi) and outlined with fontTools, so SVGs need no font. Tiles are in
      `drawings/text_tiles.py` (labels, stamps, explainer and riddle cards, greetings, surahs, 99 Names,
      Islamic months, calligraphy, pillars and articles of faith, Talbiyah, Om, Ik Onkar); the Arabic
      flags use it too.
- [ ] Arabic check: the Arabic (surah names, 99 Names, months, phrases, flags) was typed by hand without
      tashkeel. Have someone who reads Arabic check it before publishing.

#### Text tiles: fonts
Needs `pip install fonttools uharfbuzz` and these OFL fonts in `_source-data/fonts/` (not in git; the
OFL texts are saved beside them):
- Noto Sans Bold and Black, Noto Sans Devanagari Bold, Noto Sans Gurmukhi Bold:
  `https://raw.githubusercontent.com/notofonts/notofonts.github.io/main/fonts/<Family>/hinted/ttf/<File>.ttf`
- Amiri Bold: `https://raw.githubusercontent.com/google/fonts/main/ofl/amiri/Amiri-Bold.ttf`

Order:
1. [x] Symbols and ideas used in every video (`concepts-ideas`, `symbols-signs`, `brain-teasers-logic`)
2. [x] Islamic and religious topics (`religion-faith`, `celebrations-holidays`)
3. [x] Animal Quiz, Ocean & Underwater (`animals`, `ocean-underwater`)
4. [x] Space Quiz (`space`)
5. [x] Human Body Quiz, Psychology (`human-body`, `health-medicine`, `psychology-mind`)
6. [x] Geography, Flags & Capitals (`earth-geography`, `cities-capitals`, `landmarks`)
7. [x] Science, Inventions, Future (`science`, `math`, `inventions-discoveries`, `future-tech`, `technology`)
8. [ ] History (done), Human Origins (done), Mythology (partly), Mysteries (not started) (`history`, `fantasy-mythology`, `mysteries-unexplained`)
9. [ ] Food, Sports, Daily Life, Money, Movies, World Records, Words (the rest)
10. [ ] Everything else in the catalogue

### Phase 7: tidy up
- [ ] Log the searches that still fall back to downloaded packs ("no own picture for…") and add
      those items to the catalogue.
- [ ] Decide whether the downloaded packs stay optional or go.

## Quiz playlists

The pack must cover these playlists (and religious quizzes). The catalogue's `playlists.json`
maps each one to its categories.

| # | Playlist | Main categories |
|---|---|---|
| 1 | General Knowledge Quiz | everything; especially `concepts-ideas`, `symbols-signs`, `landmarks`, `world-records` |
| 2 | Animal Quiz | `animals`, `ocean-underwater` |
| 3 | Space Quiz | `space` |
| 4 | Human Body Quiz | `human-body`, `health-medicine` |
| 5 | Geography Quiz | `earth-geography`, `landmarks`, `weather-climate` |
| 6 | World Records Quiz | `world-records` (+ `see` links into animals, landmarks, geography, sports) |
| 7 | Brain Teaser Quiz | `brain-teasers-logic`, `math` |
| 8 | Inventions Quiz | `inventions-discoveries`, `history`, `technology` |
| 9 | Science Quiz | `science`, `math`, `energy-environment` |
| 10 | History Quiz | `history`, `landmarks` |
| 11 | Psychology Quiz | `psychology-mind`, `emotions-expressions` |
| 12 | Daily Life Quiz | `home-household`, `food-drink`, `clothing-accessories`, `buildings-places`, `time-calendar`, `transport-vehicles` |
| 13 | Food Quiz | `food-drink` |
| 14 | Sports Quiz | `sports-games` |
| 15 | Technology & AI Quiz | `technology`, `future-tech` |
| 16 | Movies & Entertainment Quiz | `movies-entertainment`, `music-arts` |
| 17 | Flags & Capitals Quiz | `earth-geography` (flags), `cities-capitals` |
| 18 | Mythology Quiz | `fantasy-mythology` |
| 19 | Human Origins & Ancient Civilizations Quiz | `history` (human origins, ancient civilizations) |
| 20 | Money & Economics Quiz | `money-business` |
| 21 | Mysteries & Unexplained Quiz | `mysteries-unexplained`, `space` |
| 22 | Ocean & Underwater Quiz | `ocean-underwater`, `animals` |
| 23 | Inventions of the Future Quiz | `future-tech` |
| 24 | Words & Language Quiz | `languages-writing` |
| 25 | Islamic / Religious Quiz | `religion-faith`, `celebrations-holidays`, `history` (Islamic golden age) |

## Categories

One catalogue file per category. Each line lists what the file must cover; be complete for closed
sets (all planets, all countries, all elements, all surahs…).

| File | Covers |
|---|---|
| `animals` | every living animal: mammals, primates, big cats, marine mammals, birds, birds of prey, water birds, fish, sharks and rays, sea invertebrates, reptiles, amphibians, insects, spiders and other bugs, worms and molluscs, dinosaurs and extinct animals, animal homes, animal body parts (tail, wing, fin, beak, horn…); `farm-animals` and `pets` groups that only use `see` |
| `ocean-underwater` | ocean zones (sunlight, twilight, midnight, abyss, trench), Mariana Trench, hydrothermal vents, tides, currents, bioluminescence, shipwreck, sunken treasure, diving gear (scuba tank, mask, fins, snorkel), underwater volcano, marine research ship, ocean exploration (animals stay in `animals`) |
| `plants-nature` | trees, flowers, houseplants, cacti, grasses, water plants, fungi, plant parts, plant life cycle, photosynthesis |
| `human-body` | body parts, face, hands and feet, organs (`heart-organ`, brain, lungs…), skeleton and bones, muscles, body systems, senses, teeth, blood, skin and hair, growth stages |
| `health-medicine` | medical equipment, medicines, illnesses and symptoms, germs, hospital equipment, first aid, dental care, hygiene, healthy habits, mental health, disability aids |
| `psychology-mind` | memory, dreams, sleep cycle, personality types, introvert/extrovert, phobias, cognitive biases, optical-illusion-of-the-mind items, habits, motivation, Maslow's pyramid, left/right brain, therapy, déjà vu, IQ, conditioning |
| `food-drink` | fruits, vegetables, grains, pulses, nuts, spices, dairy, eggs, meat and fish as food, breads (roti, naan, pita), sweets (Indian, Arab, world), snacks, breakfast, drinks, Indian, Middle Eastern, Asian, European, African and Latin dishes, ingredients, sauces, dates |
| `agriculture` | farm buildings, farm machines, farm tools, sowing, harvesting, irrigation, beekeeping; crops and livestock via `see` |
| `space` | sun, planets, dwarf planets, moons and moon phases (incl. crescent / hilal), stars, galaxies, black holes, asteroids, comets, eclipses, aurora, constellations and zodiac, rockets, satellites, space station, rovers, astronauts, telescopes, UFO, alien |
| `earth-geography` | landforms, water bodies, layers of the earth, volcano, earthquake, tsunami, rocks, minerals, gems, fossils, biomes, maps and navigation, 7 continents, 5 oceans and major seas, **all 195+ countries** (map outlines), **a flag for each** (`flag-<country>`), named rivers, mountains, deserts, lakes, islands, Indian states and union territories, US states |
| `cities-capitals` | the capital city of every country, plus major world cities (ids qualified where a city shares a country's name: `kuwait-city`, `singapore-city`) |
| `weather-climate` | weather, clouds, rain, snow, wind, weather instruments, rainbow, lightning, seasons (incl. monsoon), storms, floods, drought, wildfire, water cycle, climate change |
| `landmarks` | named non-religious landmarks of every continent (Taj Mahal, Red Fort, Qutub Minar, Burj Khalifa, Petra, Pyramids of Giza, Eiffel Tower, Great Wall…) and natural wonders |
| `science` | lab equipment (beaker, test tube, flask, microscope, magnifying glass, Bunsen burner, goggles), scientific method, **all 118 elements** (tiles, `element-<name>`), atoms and molecules, states of matter, chemical reactions, acids and bases, forces and motion, gravity, magnets, light and colour (prism, lenses, reflection), sound waves, heat, electricity and circuits, simple machines, cells, DNA, microorganisms, food webs as diagrams, classification of living things, famous experiments as objects |
| `math` | operators and symbols (plus, minus, times, divide, equals, percent, infinity, pi, square root), 2D and 3D shapes, angles, geometry tools (ruler, protractor, `geometry-compass`, set square), fractions, decimals, number line, place value, abacus, counting, times tables, patterns and sequences (Fibonacci, golden ratio), graphs and charts, Venn diagram, probability (dice, coin toss, spinner), measurement units, symmetry, coordinates, famous constants and numbers (zero, googol) |
| `energy-environment` | renewable and fossil energy, power grid, pollution, recycling, conservation, food chains, ecosystems, deforestation |
| `travel-tourism` | luggage, tickets, hotel, camping, beach, sightseeing, souvenirs, visa stamp |
| `history` | **human origins** (early humans, stone tools, fire, cave art, hunter-gatherers), **ancient civilizations** (Egypt, Mesopotamia, Indus Valley, ancient India, China, Greece, Rome, Persia, Maya, Aztec, Inca), Islamic golden age, medieval world, Mughal and Ottoman eras, age of exploration, renaissance, industrial revolution, world wars (generic), independence movements, historic weapons and armour, castles, archaeology |
| `inventions-discoveries` | inventions through time (wheel, paper, printing press, compass, telescope, steam engine, light bulb, telephone, aeroplane, radio, TV, computer, internet, smartphone, vaccine…) and discoveries (penicillin, gravity, electricity, DNA, X-rays, atoms…) |
| `future-tech` | flying car, hyperloop, Mars base, space colony, space elevator, humanoid robot, brain-computer link, hologram, smart city, vertical farm, lab-grown meat, quantum computer, fusion reactor, exoskeleton, delivery drone, AR glasses, asteroid mining, underwater city, 3D-printed house, nanobots, gene editing, time machine and teleporter (fiction) |
| `religion-faith` | see [Religious topics](#religious-topics) |
| `celebrations-holidays` | party items, Eid al-Fitr and Eid al-Adha, Ramadan decorations, Diwali, Holi, Raksha Bandhan, Navratri, Pongal, Onam, Christmas, Hanukkah, Lunar New Year, New Year, birthdays, weddings (incl. nikah), national days |
| `fantasy-mythology` | dragon, unicorn, phoenix, griffin, pegasus, mermaid, Cerberus, Minotaur, Hydra, kraken, yeti, fairies, giants, magic items (wand, crystal ball, genie lamp, magic carpet), symbols of Greek, Norse and Egyptian myths as objects (trident, thunderbolt, war hammer, winged sandals) |
| `mysteries-unexplained` | Bermuda Triangle, lake monster, Bigfoot, crop circles, Stonehenge, Nazca lines, Easter Island heads, Atlantis, ghost ship, Voynich manuscript, Tunguska event, ball lightning, mysterious signal, haunted castle |
| `world-records` | record certificate, record book, tallest / longest / fastest / heaviest / oldest / smallest markers, size-comparison scales, record podium; `see` links to the record holders in other categories |
| `brain-teasers-logic` | riddles, mazes, logic grids, sequences, odd one out, matchstick puzzles, magic squares, tangram, optical illusions (impossible triangle, endless stairs), spot the difference, missing piece, lateral thinking |
| `law-government` | courthouse, gavel, scales of justice, constitution, parliament, voting, ID documents, passport, police badge, contract, tax, human rights |
| `languages-writing` | letters A–Z, all Arabic letters, Devanagari letters, digits 0–9 and Arabic-Indic digits (tiles), writing systems, dictionary, sign language, braille, grammar tiles, idioms and word-play items |
| `transport-vehicles` | cars, two-wheelers, auto-rickshaw, buses, trucks, trains, metro, ships, boats, dhow, planes, helicopters, construction, emergency and military vehicles, animal carts, roads and traffic, vehicle parts |
| `tools-industry` | hand tools, power tools, construction, machines, factories, mining, materials |
| `technology` | devices, computer parts, internet and networks, AI and robots, programming, smart home, telecom |
| `communication-media` | phone calls, messages, speech and thought bubbles, email, post, newspaper, TV, radio, podcast, megaphone, social-media symbols (no brand logos) |
| `movies-entertainment` | film genres, cinema items, streaming, TV series, cartoons, generic superhero (cape, mask), red carpet, award show, movie poster, 3D glasses, theme park rides, comics |
| `music-arts` | instruments (incl. tabla, sitar, oud, daf, harmonium), music symbols, art supplies, art forms (calligraphy, Islamic geometry, Madhubani, Warli), dance, theatre |
| `buildings-places` | home types, rooms, city buildings (school, hospital, bank, shop, market, mall, museum, station…), village and city scenes, building parts |
| `home-household` | furniture, kitchenware (tawa, kadai, pressure cooker…), appliances, bathroom, cleaning, household items, garden tools |
| `clothing-accessories` | clothes, footwear, headwear, accessories, jewellery, traditional dress worldwide (hijab, abaya, thobe, sari, kurta, sherwani, kimono…) |
| `jobs-people` | generic people: professions, family members, ages, groups, people with disabilities shown positively |
| `emotions-expressions` | facial expressions, hand gestures (incl. dua hands), body language |
| `safety-emergency` | fire safety, emergency kit, life jacket, road and home safety, disaster drills |
| `hobbies-leisure` | reading, gardening, photography, fishing, sewing, knitting, origami, kite flying, picnic, collecting |
| `sports-games` | all major sports (incl. cricket, kabaddi, kho-kho), equipment, trophies and medals, venues, toys, board games (chess, ludo, carrom, snakes and ladders), playground |
| `education-school` | stationery, classroom, books, school subjects, exams and results, graduation |
| `money-business` | coins, notes (rupee, dollar, riyal…), currency symbols, banking, cards, digital payments, finance, business, office, shopping, economy |
| `time-calendar` | clocks, clock faces for each hour, calendars, weekdays, Gregorian and Hindu months, times of day (dawn, sunrise, noon, sunset, night) |
| `symbols-signs` | arrows, check and cross marks, question and exclamation marks, `heart` (love), `star-symbol`, badges, UI symbols, punctuation, road signs, hazard and public signs |
| `concepts-ideas` | abstract ideas for explainers and motivation: idea, growth, success, failure, goal, teamwork, patience, gratitude, honesty, focus, habits, problem and solution, myth vs fact, did you know, true or false, before and after |

### Religious topics
`religion-faith` gets the most depth, Islam first:
- **Places**: Kaaba, Masjid al-Haram, Masjid an-Nabawi (green dome), Al-Aqsa, Dome of the Rock,
  Quba Mosque, Cave Hira, Cave Thawr, Mount Uhud, Mount Arafat, Mina, Muzdalifah, Jamarat, Safa and
  Marwa, Badr, Jannat al-Baqi (as places only).
- **Objects and practice**: mosque, minaret, dome, mihrab, minbar, Quran, rehal, prayer mat,
  tasbih, wudu steps, salah positions as faceless silhouettes, adhan, crescent and star, zakat,
  sadaqah box, ihram, Zamzam water, tawaf, Hajj and Umrah stages, suhoor, iftar, Laylat al-Qadr.
- **Tiles (text cards)**: the 114 surah names, the 12 Islamic months, the five pillars, the six
  articles of faith, the 99 Names (as text tiles), Arabic letters (`languages-writing`).
- **Prophets' stories shown through objects only**: the ark, the whale, the fire, the staff, the
  parted sea, the ants, the well, the shirt, the she-camel, the cave.
- **Other faiths**: Christianity (church, cross, Bible, rosary, candle), Judaism (synagogue, Star
  of David, menorah, Torah scroll), Hinduism (temple, Om, diya, kalash, conch, aarti plate),
  Sikhism (gurdwara, Khanda, Golden Temple, the five Ks, langar), Buddhism (stupa, dharma wheel,
  prayer wheel), Jainism, Zoroastrianism, Shinto (torii), Taoism (yin yang), and named sites
  worldwide.
- **Never drawn**: God, prophets, companions, angels, or any sacred figure. Use places, objects,
  text tiles and symbols instead. Respectful names, with the spellings people type ("salah",
  "salat", "namaz").

## Catalogue format

- One file per category: `catalog/<category>.json`, UTF-8, 2-space indent.
- `{"id", "name", "description", "groups": [...]}`; `id` equals the file name.
- Group: `{"id", "name", "kind", "recolor", "motion", "items", "see"?}`
  - `kind`: `illustration`, `icon`, `scene`, `tile` (generated card: letters, flags, elements,
    surah names), `emoji` (faces), `character` (people).
  - `recolor`: `keep` (natural colours: animals, food, flags, planets), `themed` (takes the
    video's theme colours), `mono` (one colour: arrows, line symbols).
  - `motion`: 1–3 of: pop, rise, slide, drop, draw, morph, fade, float, pulse, wiggle, spin, flap,
    swim, walk, run, hop, sway, blink, wave, glow, twinkle, flicker, orbit, bounce, rotate, pour,
    drip, grow, beat, breathe, launch, fly, roll, tick, ring, shake, splash, open.
  - `items`: `"name"`, or `["name", "other name", …]`, or
    `{"id": "…", "name": "…", "aka": […], "note": "…"}`. The id is the name in lower-case words
    joined by `-` ("polar bear" → `polar-bear`).
  - `see`: ids owned by another group that belong here too (instead of copying them).

Example:

```json
{ "id": "moons", "name": "Moons", "kind": "illustration", "recolor": "keep", "motion": ["orbit", "spin"],
  "items": [ ["moon", "the moon", "earth's moon"], ["crescent moon", "hilal"], "europa" ],
  "see": ["sun"] }
```

### No duplicates
- Every id is unique across all files; an item lives in exactly one group.
- Same word, different thing: qualify both ids (`bat-animal` / `cricket-bat`,
  `heart-organ` / `heart`, `computer-mouse` / `mouse-animal`, `crane-bird` / `crane-machine`,
  `star` (space) / `star-symbol`).
- Each overlapping thing has one owner file (see the Covers column above; for example the sun and
  moon belong to `space`, every living animal to `animals`, anything eaten to `food-drink`,
  places of worship and religious sites to `religion-faith`, all vehicles except spacecraft to
  `transport-vehicles`). Other files point at it with `see`.
- Drawn files are named `svg/<category>/<id>.svg`, so one id can't be drawn twice.

### The checker (`tools/check_catalog.py`)

```powershell
python tools\check_catalog.py --warnings
```

- Errors (exit code 1): repeated ids, a category id that does not match its file name, repeated
  group ids (across all files), `see` pointing at an id that does not exist, unknown
  `kind`/`recolor`/`motion` or more than 3 motions, missing or unknown keys, ids that aren't
  lower-case words joined by `-`, JSON that doesn't parse.
- Warnings: a name or other name used by two different items, a `see` that repeats the group's
  own item, an empty group, an SVG whose id isn't in its category's catalogue file.
- `--find <word>`: is it already in the catalogue? (run before adding anything)
- `--todo <category>`: items with no SVG yet. Default output: groups, items and drawn per category.
- Ids come from names the same way in the checker and `viewer.html` (accents dropped, `&` →
  "and", apostrophes dropped: "Déjà vu" → `deja-vu`, "Earth's moon" → `earths-moon`).

## What we found (research, November 2026)

### Skills and plugins
No skill in your skills library covers SVG drawing or animation. In the plugin directory:

| Plugin | Useful for | Fit |
|---|---|---|
| **SVG.new** | picture to SVG, simplifying paths, recolouring, background removal, batches | Handy for cleaning drawings and tracing sketches. Online service: check its terms first. |
| **Icons8** (icons, Ouch! illustrations, animator to Lottie) | ideas, style reference | **Not for the pack**: Icons8 art can't be redistributed inside our app. |
| **animation-studio** | hand-drawn animated shorts drawn in code | Reference for drawing and motion ideas. |
| **Codesign** (IMG.LY) | editable designs, an "animate" skill | Reference only. |

None is needed to start: Claude can write SVG directly, and the app already asks Gemini for SVG
drawings and cleans them (`native/video/src/svgcheck.rs`).

### Packages and models

| Tool | Licence | What it gives us |
|---|---|---|
| **Gemini** (already in the app) | API terms | Draws SVGs from a prompt; the app cleans and saves them. Quality varies, so every drawing is reviewed. |
| **Claude** (in these sessions) | — | Writes SVG by hand to the style guide; good for the style sheet and fixes. |
| [vtracer](https://github.com/visioncortex/vtracer) | MIT / Apache-2.0, Rust | PNG (sketch, scan, AI image) to colour SVG; could be a `vidtool trace` command. |
| [SVGO](https://github.com/svg/svgo) | MIT, Node | Shrinks SVGs; `usvg` (already in the engine) can normalise them too. |
| [OmniSVG](https://huggingface.co/OmniSVG/OmniSVG) | Apache-2.0 model; its dataset is CC BY-NC-SA | Open text-to-SVG model (needs a GPU). The non-commercial dataset is a licence question to settle first. |
| [StarVector](https://arxiv.org/abs/2312.11556) | Apache-2.0 (check its data terms) | Image-to-SVG and text-to-SVG model; same caution. |
| [rasterlottie](https://docs.rs/rasterlottie) | Apache-2.0, Rust, renders with **tiny-skia** (our renderer) | Could play Lottie animations in our frames; partial Lottie support. |
| [velato](https://github.com/linebender/velato) | Linebender, Rust | Fuller Lottie renderer, but for Vello (GPU); poor fit for our CPU renderer. |
| [GSAP](https://gsap.com/) incl. MorphSVG, DrawSVG | free "no charge" licence since April 2025 | Browser only; for prototyping motion, not usable in the Rust engine. |
| [LottieFiles free animations](https://help.lottiefiles.com/animation-licensing-basics-) | Lottie Simple License | Allowed in apps, but collecting them to build our own library is not allowed. |

**Decision**: draw our own static SVGs with named parts and animate the parts in our engine (it
already does springs, squash and stretch, and line draw-on). Lottie stays optional. Only our own
drawings, or CC0/MIT/Apache art, go into the pack (no unDraw, no Icons8).

## Style guide (style B, chosen November 2026)

Reference drawings: `svg/_style-test/b-*.svg` (open `svg/_style-test/compare.html`). Colours and
sizes are in `style/palette.json`.

- **Look**: flat, rounded, friendly; 2-tone shading (a lighter highlight upper-left, no outline on
  the highlight); **one soft dark outline** (`#2E2A3B`, 10 px, round joins) on every filled shape;
  no gradients, no text (except tiles), no photos.
- **Canvas**: `viewBox="0 0 512 512"`, square, subject centred, about 6% margin (30 px).
- **Elements**: only `path`, `circle`, `ellipse`, `rect`, `polygon`, `line`, `g`; inline
  `fill`/`stroke` (no `<style>`, classes, filters, masks, `<image>`, `<text>`); under about 15 KB
  and 60 shapes.
- **Colours**: `keep` items use the 24 colours in `palette.json` (flags use official colours);
  `themed` items use accent, accent-2 and the greys only (the engine maps them to the theme);
  `mono` items are one colour (`#2E2A3B`) with 24 px round-capped strokes and no outline, so they
  draw on line by line.
- **Both styles from one file (border on/off)**: every drawing is saved once, in style B, with
  its outline pieces marked: outlined shapes carry `data-outline="stroke"`, and tube under-strokes
  are elements with `data-outline="under"`. Removing those strokes and elements gives style A (no
  border). `flat()` in `tools/draw_lib.py` does it, the viewer's **Border** checkbox does it live,
  and the engine and pack get the same switch (Phase 4/5).
- **Tubes** (handles, stems, vessels, cords): a coloured stroke drawn over an ink stroke 20 px
  wider, so they get the same outline.
- **Parts for animation**: moving parts are groups `part-<name>` with a pivot, e.g.
  `<g id="part-wing-left" data-pivot="256 300">`. Names: `eye-left`, `eye-right`, `mouth`,
  `wing-left`, `wing-right`, `tail`, `arm-left`, `arm-right`, `leg-*`, `head`, `flame`, `blade`,
  `needle`, `hand-hour`, `hand-minute`, `ring`, `petals`, `wave`, `glow`, `wheel`, `globe`.
- **People and faith**: generic people only; never real people or sacred figures; no brand logos.
- **Licence**: to decide later. Current idea: publish the pack in its own GitHub repository and
  let the app download it (like the other downloadable packs) instead of shipping it inside the
  app. Phase 4 follows whichever is chosen.

## Sources
- [velato (GitHub)](https://github.com/linebender/velato), [velato on lib.rs](https://lib.rs/crates/velato)
- [rasterlottie (docs.rs)](https://docs.rs/rasterlottie)
- [vtracer (GitHub)](https://github.com/visioncortex/vtracer), [vtracer on docs.rs](https://docs.rs/crate/vtracer/0.6.5)
- [OmniSVG (Hugging Face)](https://huggingface.co/OmniSVG/OmniSVG), [OmniSVG paper](https://arxiv.org/abs/2504.06263)
- [StarVector paper](https://arxiv.org/abs/2312.11556)
- [GSAP is free (Webflow)](https://webflow.com/blog/gsap-becomes-free), [GSAP standard licence](https://gsap.com/community/standard-license/)
- [LottieFiles licensing basics](https://help.lottiefiles.com/animation-licensing-basics-)
- [SVGO (GitHub)](https://github.com/svg/svgo)
