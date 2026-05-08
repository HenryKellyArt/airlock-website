"""Generate 8 dedicated stage pages (stage-X.html) from a shared template."""
from pathlib import Path
import html as _html

# Stage-level metadata
STAGES = [
    {
        "id": "concept",
        "num": "01",
        "title": "The Idea That Wouldn't Die",
        "kicker": "Stage 01 · Concept",
        "status": "declassified",
        "stamp": "DECLASSIFIED",
        "hero": "screenshots/airlock_screenshot_01.jpg",
        "summary": "The proof of concept. Was it fun? Did it look good? Yes and yes — that was the green light to build everything else.",
        "intro": "Before AIRLOCK had lore, before it had art, before it had a single Settler — it had to prove it could be a game. That's what this stage was. A throwaway military compound, ALS V4 dropped in, a custom dollhouse camera written from scratch, and a minute of footage that answered the question: yes, this works.",
        "substages": ["01.01"],
        "prev": None,
        "next": "foundation",
    },
    {
        "id": "foundation",
        "num": "02",
        "title": "The World Built First",
        "kicker": "Stage 02 · Foundation",
        "status": "declassified",
        "stamp": "DECLASSIFIED",
        "hero": "screenshots/4_mainmenu.png",
        "summary": "Documentation, lore, audio direction, visual identity. Locked before code touched it. Every system built since references this foundation.",
        "intro": "Most indie projects discover their world while they build it. AIRLOCK locked the world first. The Sonic War. The collapse of the UGA. The four locked proper nouns: Ashgate, the Airlock, the Settlers, the Altered. The painted concept-art aesthetic. 'Calm Before The Storm' written and scored. Every system that came after had a fixed star to navigate by.",
        "substages": ["02.01", "02.02", "02.03", "02.04"],
        "prev": "concept",
        "next": "architecture",
    },
    {
        "id": "architecture",
        "num": "03",
        "title": "The Engine of Everything",
        "kicker": "Stage 03 · Pre-Production · Architecture",
        "status": "declassified",
        "stamp": "DECLASSIFIED",
        "hero": "screenshots/airlock_underworld_03.jpg",
        "summary": "The C++ backbone. Grid system, modules, AI, HUD, combat, mining, skills, MetaHumans, the Marv companion. Every system the game depends on.",
        "intro": "The thirteen sub-systems the demo cannot exist without — and which any post-demo expansion will lean on. Built in C++ first, exposed to Blueprint where designers need to touch it, locked through repeated PIE testing. The mid-flight pivot from monolithic Blueprints to Level Instance modules happened here, and it 10x'd authoring speed without breaking a single placed module.",
        "substages": ["03.01", "03.02", "03.03", "03.04", "03.05", "03.06", "03.07", "03.08", "03.09", "03.10", "03.11", "03.12", "03.13"],
        "prev": "foundation",
        "next": "vertical-slice",
    },
    {
        "id": "vertical-slice",
        "num": "04",
        "title": "The Demo Comes Alive",
        "kicker": "Stage 04 · Pre-Production · Vertical Slice",
        "status": "in-progress",
        "stamp": "PARTIALLY DECLASSIFIED",
        "hero": "screenshots/airlock_underworld_05.jpg",
        "summary": "The V2 polish + content build. Painted UI in engine. Power. Voice. NPCs. Procedural city. Currently dressing Ashgate. Then the demo ships.",
        "intro": "Where AIRLOCK is right now. Painted UI shipped in engine. The voice pipeline real and end-to-end. Power systems with audible, visible cause-and-effect. The procedural city tool laying down Ashgate's bones. Module concept art turning into module reality. The demo arc — wake up, find Mara, reach the airlock, build, sleep, fetch, repeat — is being assembled stage by stage.",
        "substages": ["04.01", "04.02", "04.03", "04.04", "04.05", "04.06", "04.07", "04.08", "04.09", "04.10", "04.11", "04.12", "04.13", "04.14", "04.15"],
        "prev": "architecture",
        "next": "funding",
    },
    {
        "id": "funding",
        "num": "05",
        "title": "The Public Reveal",
        "kicker": "Stage 05 · Funding & Marketing",
        "status": "classified",
        "stamp": "CLASSIFIED",
        "hero": "screenshots/city_bg_airlockF.jpg",
        "summary": "Demo lands on Steam. Players play. The Kickstarter campaign. The push that funds full-time development.",
        "intro": "Five years of work goes public. The Steam page goes live with screenshots, trailer, descriptions. The demo drops. The first Discord notification pings. The first review lands. The Kickstarter pitch turns the proof into a runway. Henry leaves the day job. Ironbridge stops being one person and starts being a studio.",
        "substages": ["05.01", "05.02", "05.03", "05.04", "05.05"],
        "prev": "vertical-slice",
        "next": "production",
    },
    {
        "id": "production",
        "num": "06",
        "title": "The Funded Build",
        "kicker": "Stage 06 · Production",
        "status": "classified",
        "stamp": "CLASSIFIED",
        "hero": "screenshots/airlock_underworld_04.jpg",
        "summary": "The studio scales. Animator, character artist, AI programmer, level designer, narrative writer. The systems that ship in 1.0 land here.",
        "intro": "With Kickstarter funding, the studio scales. Specialists in: animation, character art, AI, narrative, level design. The systems left for 1.0 — Stalker AI, boss fights, full crop and irrigation, livestock, module customisation, original score, voice acting, cinematics — all land here. Production is the slow build that makes the game feel finished, not prototyped.",
        "substages": ["06.01", "06.02", "06.03", "06.04", "06.05", "06.06", "06.07", "06.08", "06.09", "06.10", "06.11", "06.12", "06.13"],
        "prev": "funding",
        "next": "early-access",
    },
    {
        "id": "early-access",
        "num": "07",
        "title": "Open Development",
        "kicker": "Stage 07 · Early Access",
        "status": "classified",
        "stamp": "CLASSIFIED",
        "hero": "screenshots/airlock_world_04.jpg",
        "summary": "AIRLOCK goes live on Steam Early Access. The community is in the room. Players play, break, tell us what works. Updates ship every quarter.",
        "intro": "Early Access is where the community moves into the room. Discord. Steam discussions. Public dev diaries. Quarterly content drops. 'Where the money goes' transparency reports. Players watch the game grow and steer it. The roadmap stops being one person's vision and becomes a conversation.",
        "substages": ["07.01", "07.02", "07.03", "07.04"],
        "prev": "production",
        "next": "full-release",
    },
    {
        "id": "full-release",
        "num": "08",
        "title": "The Vision Realised",
        "kicker": "Stage 08 · Full Release",
        "status": "classified",
        "stamp": "CLASSIFIED",
        "hero": "screenshots/airlock_world_05.jpg",
        "summary": "1.0 ships. Console builds follow. Trading economies, multi-airlock networks, the underground metro, global maps, eventually multiplayer.",
        "intro": "The full vision. Multiple airlocks per save. The underground metro stitching them together. Trading economies. Global maps — Ashgate, Tokyo, New York, Berlin, Moscow. Console launches. Localisation. And eventually, the horizon: multiplayer, where your airlock and a friend's are connected by the same dark tunnels. Every step before this is the road that leads here.",
        "substages": ["08.01", "08.02", "08.03", "08.04", "08.05", "08.06", "08.07", "08.08", "08.09"],
        "prev": "early-access",
        "next": None,
    },
]

# Sub-stage data: (status, name, body, detail, image_or_None)
SUBSTAGES = {
    "01.01": ("declassified", "Original Prototype",
        "Built a military compound blockout in Unreal Engine 5 to prove the concept actually works. Integrated ALS for third-person control. Built the prototype dollhouse camera. AIRLOCK stopped being an idea and started being a game.",
        "ALS V4 dropped in. Custom dollhouse cam written from scratch. The military compound was throwaway, but proved the dual-view loop. The moment that build ran, AIRLOCK stopped being a pitch deck and became a project.",
        "screenshots/airlock_screenshot_01.jpg"),
    "02.01": ("declassified", "Documentation & Lore",
        "Ashgate. The Altered (Feral, Familiars, Stalkers, Legion). The Settlers — 14 distinct classes. The post-war UGA. The Sonic War 300 years ago. The Legion reveal arc. Multi-airlock metro network.",
        "Confluence dossier of every faction, every settler class, every place name, every story beat. Memory locked into a single source of truth before a single line of gameplay code went in.",
        None),
    "02.02": ("declassified", "Audio Direction",
        "TLOU + Days Gone reference lock. Hans Zimmer for the orchestral spine. 'Calm Before The Storm' written and scored. Diegetic SFX rules. Submix routing. Sonic identity locked before any major audio shipped.",
        "Reference docs: TLOU + TLOU Part II + Days Gone for SFX. Hans Zimmer's emotional register for score. 'Calm Before The Storm' written, scored, performed — the spine the trailer will eventually be cut to.",
        None),
    "02.03": ("declassified", "UI Art Direction",
        "After 20+ HUD variations across 10 style directions, the painted concept art aesthetic was locked. Cormorant Garamond. Permanent Marker labels. Brushstroke buttons. Ink-wash backings. Cream on near-black.",
        "Twenty-plus HUD variations across ten distinct directions, side-by-side mockups, ruthless elimination. The painted concept-art aesthetic survived. Cream sumi-ink on near-black. Hand-made energy. Nothing else came close.",
        "screenshots/4_mainmenu.png"),
    "02.04": ("declassified", "Painted Icon Library",
        "91 painted monochrome icons delivered. Survival bars, status effects, weapons, consumables, loot, HUD chrome, banners, structural frames, screen overlays, map pins, Settler activities, skill tree parents.",
        "Ninety-one painted icons in a single sprite sheet. Cream monochrome masters. CSS-tinted at runtime. Survival bars, weapons, status effects, map pins, the whole UI vocabulary in one consistent painted hand.",
        None),
    "03.01": ("declassified", "Grid System",
        "GridManager in C++ from scratch. World-to-grid coordinate conversion, cell states, multi-floor support. The system everything else builds on top of.",
        "GridManager from blank file. Multi-floor support designed in from day one. World-to-grid coordinate conversion. Cell occupancy tracking. The bedrock everything else stands on.",
        "screenshots/airlock_underworld_03.jpg"),
    "03.02": ("declassified", "Character",
        "ALS taken apart and rebuilt for AIRLOCK. Custom movement feel, camera behaviour, transitions between underground and surface. One controller, two very different feels.",
        "ALS V4 dismantled and rewired for AIRLOCK. Custom rotation modes. Stance changes. Crouch flow. The character feels heavy underground and alert above. Two worlds, one pawn.",
        None),
    "03.03": ("declassified", "UI System",
        "Full main menu system from scratch. Epilepsy warning, brightness calibration, press-any-key splash, all sub-screens and settings.",
        "Main menu shell, settings, accessibility, brightness calibration, epilepsy warning, press-any-key splash. Every screen on the path from boot to gameplay built from the painted style guide.",
        "screenshots/city_bg_airlockPressAnyKey.jpg"),
    "03.04": ("declassified", "HUD System",
        "In-game HUD: health, stamina, compass, status effects, notifications. Full inventory system — equip, fire, swap, drop, pick up. Items degrade.",
        "Compass, vitals, status effects, notifications, weapon ammo, day-time clock — modular sub-widgets feeding off a single HUD State Component. Add a new screen, it just plugs in. No legacy spaghetti.",
        None),
    "03.05": ("declassified", "Combat",
        "Weapons you can equip, fire, and feel. Ranged + melee. Every weapon degrades. Ammunition is scarce. Combat designed to feel desperate, not heroic.",
        "Weapons that degrade. Ammo that runs out. M4 Carbine, Glock — the demo loadout. Every shot is a trade. Combat designed to feel desperate, not heroic.",
        "screenshots/airlock_screenshot_07.jpg"),
    "03.06": ("declassified", "Module System",
        "Module system fully integrated. 14+ categories. Place, move, remove. Architecture mid-development transition from Blueprints to Level Instance modules — the speed-of-authoring unlock.",
        "Ghost placement, snap-to-grid, collision check, neighbour-aware wall toggling, save/load round-trip. Then the big architectural pivot mid-flight: monolithic Blueprints out, Level Instance modules in. Speed of authoring x10.",
        "screenshots/screenshot_buildmode.png.jpg"),
    "03.07": ("declassified", "Horde System",
        "Optimised horde — large numbers of The Altered without tanking performance. Spawn, detection, navigation, swarming. They hunt. They overwhelm. Daytime tense. Night deadly.",
        "Days-Gone-style horde architecture. Hundreds of Altered chasing one player without tanking the framerate. Spawn manager, perception, navigation. They hunt. They overwhelm. Daytime tense, night deadly.",
        "screenshots/airlock_screenshot_08.jpg"),
    "03.08": ("declassified", "Loot",
        "Lootable items scattered through ruined buildings. Food, weapons, medicine, blueprints, raw materials. Every surface trip is a risk-reward calculation.",
        "Cabinets. Drawers. Lockers. Every container a hand-stocked moment of risk-reward. Food, weapons, blueprints, raw materials. The reason every surface trip means something.",
        None),
    "03.09": ("declassified", "MetaHuman",
        "ALS mannequin replaced with a fully assembled MetaHuman. Realistic face, hair, skin, expressions. The foundation for cutscenes and characters you care about.",
        "ALS mannequin retired. MetaHuman in. Real face, real hair, real subsurface scattering. The foundation for every cutscene moment that has to land emotionally — not just animations playing on a doll.",
        "screenshots/airlock_screenshot_marv.jpg"),
    "03.10": ("declassified", "Marv (Companion)",
        "Marv follows you. Engages enemies. Sniffs out hidden loot. Reacts to danger. Sit system, full locomotion, pose rules. Personality. Moods. Memory.",
        "Marv has moods. He sniffs. He sits. He chases. He has poses that lock when the player moves. He's not a turret on legs — he's a dog you start to worry about.",
        "screenshots/Marv.jpg"),
    "03.11": ("declassified", "Tier System",
        "Five visual and functional tiers per module: Cave, Structured Cave, Brick + Wood, Concrete + Tile, Metal Sci-fi. Each upgrade visible and earned.",
        "Cave → Structured Cave → Brick + Wood → Concrete + Tile → Metal Sci-Fi. Every upgrade re-skins a module visually and functionally. You see the progress when you walk past it.",
        None),
    "03.12": ("declassified", "Mining & Interact",
        "Universal Press-to-Interact framework. Doors, loot, NPCs, ore nodes, terminals. Platform-aware icons (KB / Xbox / PlayStation). Mining loop integrates with grid depth — deeper = rarer ores.",
        "One framework for every interactable in the game. Press, hold, contextual prompt, platform-aware glyph (KB/Xbox/PS). Mining ties into grid depth — deeper rooms surface rarer ore.",
        None),
    "03.13": ("declassified", "Skill System",
        "Shared skill tree between player and Settlers. 17 parent categories, 130+ sub-skills, 8 tiers × 10 sub-levels. Pistols, cooking, brewing, husbandry, alchemy, fishing, tailoring, medical, more.",
        "Seventeen parent skill categories. A hundred and thirty plus sub-skills. Eight tiers, ten sub-levels each. Player and Settlers share the tree. XP propagates across related skills. Built for hundreds of hours of progression.",
        None),
    "04.01": ("declassified", "NPC Foundation",
        "C++ backbone for every NPC. 9-state behaviour machine. 7-faction team system. Component stack for brains, combat, injury, tasking, dialogue. Every Settler, enemy, wildlife slots in cleanly.",
        "Faction system. Behaviour state machine. Combat component. Injury component. Dialogue component. Voice component. Bump component. Every NPC inherits the spine; specialisations layer on top.",
        None),
    "04.02": ("declassified", "Smart NPCs",
        "Voice pipeline with TTS + emotion tags. Per-NPC Data Tables. Subtitle Widget with stack mode. Activity Anchors so NPCs migrate between content. Bump knockback. Power-aware barks.",
        "Mara has fifty-five voice lines, recorded with inline emotion tags through ElevenLabs and CF Flow. She greets, complains, reacts to power loss. Subtitles stack. NPCs walk between activity anchors. Real life inside the airlock.",
        None),
    "04.03": ("declassified", "Painted HUD",
        "Painted concept art direction landed in engine. Cream sumi-ink on near-black. Cormorant Garamond + Permanent Marker. Ink-wash backings. Module padlocks. Auto-flashlight that engages in the dark.",
        "Painted sumi-ink HUD landed in engine. Inventory, build menu, compass, notifications, skill XP popups — every panel rebuilt on the painted style. Module padlocks. Auto-flashlight that engages when night falls or the lights die.",
        "screenshots/airlock_underworld_05.jpg"),
    "04.04": ("declassified", "Survival Stats",
        "Stamina, hunger (28 days to zero), thirst (48 hours to zero), stress, morale. The body keeps score. Manage them or fall.",
        "Ultra Dynamic Sky drives every timer. Hunger drains over twenty-eight in-game days. Thirst over forty-eight hours. Stress and morale react to the base around you. The body keeps score.",
        None),
    "04.05": ("declassified", "Day & Time Cycle",
        "Fully dynamic day-night. 45 real-world minutes = 1 in-game day. Ultra Dynamic Sky drives every time-aware system. Toxic night queued.",
        "Forty-five real minutes per in-game day. Sky shifts, lighting reacts, NPCs change schedule. Toxic night queued. Going to the surface after dark will not be optional, it will be a calculation.",
        "screenshots/airlock_world_06.jpg"),
    "04.06": ("declassified", "Power & Electricity",
        "Generators with green/amber/red status LEDs. Multi-generator networks. 5-second overload trip. Powered lights and ambient emitters subscribe by ID. Auto-flashlight engages in the dark.",
        "Generators with green/amber/red status LEDs you can read across a room. Networks of generators. Five-second overload trips. Powered lights subscribe to a power source by ID. Pull the plug and the world reacts visually + audibly.",
        "screenshots/airlock_underworld_02.jpg"),
    "04.07": ("declassified", "Dialogue & Voice",
        "Subtitle widget pushes painted-monochrome speech. Stack mode for overlapping voices. Italic-paren for non-speech (humming, sighs). Generators hum, NPCs talk, ambient emitters push their own subtitles.",
        "Subtitle widget supports stack mode — Mara talking, the radio crackling, the generator humming, all on screen at once without overwriting. Italic-paren convention for non-speech. Proximity-gated so the line only shows when you're near.",
        None),
    "04.08": ("declassified", "City & Foliage Tools",
        "Procedural city tool. City Block Breaker for hand-art-direction. Foliage Cascade marketplace-ready PCG node. PCG Foliage Baker. PCG_Include / PCG_Remove tags. Ashgate has its overgrowth.",
        "Custom PCG cascade node — designer drops a biome volume, the system spawns mature trees, then juveniles around them, then saplings around those, then ground cover. Tag-based include/exclude. Marketplace-ready.",
        "screenshots/airlock_world_03.jpg"),
    "04.09": ("declassified", "Module Concepts",
        "Painted concepts for the demo modules. Cream sumi-ink, grounded post-apocalyptic modern. Operations Room, Workhouse, Bunkroom + reference paintings for the next batch.",
        "Painted hero concepts for every demo module. Operations Room, Workhouse, Bunkroom — the three locked + dressed in engine. Reference paintings for Kitchen, Greenhouse, Aquaculture, Power Room queued.",
        "screenshots/airlock_underworld_01.jpg"),
    "04.10": ("declassified", "Module Build-Out",
        "Operations Room with the Planning Board, salvaged radio desk, lockers, fluorescent buzz, ivy creeping in. Workhouse, the multi-discipline crafting space. Bunkroom with the bunk migration mechanic.",
        "Operations Room: Planning Board, salvaged radio desk, lockers, fluorescent buzz, ivy through the cracks. Workhouse: multi-discipline crafting space. Bunkroom: where rescued Settlers sleep before they migrate to their specialist module.",
        "screenshots/airlock_underworld_04.jpg"),
    "04.11": ("in-progress", "City Build-Out",
        "Ashgate streets traced + dressed. Hospital where Kore wakes. Gas station for fuel. Builders merchant. Abandoned airlock entrance. Mission scripting layered on top — survivor encounters, the first rescue, the night escort.",
        "Ashgate streets traced with the new procedural city tool. Hospital where Kore wakes. Gas station for fuel. Builders merchant. The abandoned airlock entrance — a boarded-up cellar door, not a sci-fi blast hatch. Grounded.",
        "screenshots/airlock_world_01.jpg"),
    "04.12": ("classified", "Settlers Live",
        "14 Settler class Blueprints instantiated. Full ALS locomotion. Procedural names, traits, skill rolls. They walk into the airlock. They stand at their module. They react when Kore approaches.",
        "Procedural names. Procedural traits. Procedural skill rolls weighted by class. Fourteen Settler classes ready to instantiate. They walk in. They stand at their module. They greet Kore by name when he passes.",
        None),
    "04.13": ("classified", "Module Unlocks",
        "Settlers unlock modules. No Engineer = no Tier 2+ upgrades. No Chemist = no explosives. Your rescue roster determines what your base can become. Rescue drives unlocks.",
        "Kingdom Tale-style gating. No Engineer in the airlock means no Tier 2+ upgrades. No Chemist means no explosives. The rescue loop directly determines what your base can become. Strategy from the very first choice.",
        None),
    "04.14": ("classified", "Construction State",
        "Module upgrades stop being instant. Time passes. Scaffolding appears. If the upgrade digs deeper, ore nodes spawn — mine them before the timer ends. Settlers shove Kore out of the corridor during construction.",
        "Module upgrades stop being instant mesh swaps. A timer runs. Scaffolding visible. If the upgrade digs deeper, ore nodes spawn in the new cells — mine them before the timer ends or lose the haul. Settlers shove Kore back if he tries to walk in mid-build.",
        None),
    "04.15": ("classified", "Demo Ready",
        "A 60+ minute guided experience. Wake up alone. Discover the airlock. Build your first rooms. Rescue your first Survivors. Survive the night. The hook that makes you need to know what happens next.",
        "Sixty-plus minutes of the game's bones. Wake alone in the hospital. Step into the silence. Meet Mara. Reach the airlock. Build your first rooms. Survive the night. End on the hook that makes the player need the next chapter.",
        "screenshots/airlock_world_02.jpg"),
    "05.01": ("classified", "Steam Coming Soon",
        "The demo lands on Steam with a Coming Soon page. Header capsule, screenshots, trailer, descriptions. Wishlist collection from day one.",
        "// Coming soon page locked. Header capsule, screenshots, trailer, descriptions. Wishlist collection from day one. The page lives quiet in Steamworks until the demo is footage-ready, then goes public.",
        None),
    "05.02": ("classified", "Player Feedback",
        "First weeks after demo lands are about listening. Steam reviews, Discord input, playtester surveys. Iterate based on what players actually do vs what we designed for.",
        "// First weeks live are listening time. Discord, Steam reviews, recorded sessions, surveys. Iterate based on what players actually do, not what we designed for. Telemetry with respect.",
        None),
    "05.03": ("classified", "Bug Bash & Hotfix",
        "Rapid-response month. Crash reports, soft locks, missing tutorials, controller binding edge cases — every loud signal gets a hotfix patch within days, not weeks.",
        "// Rapid-response month. Crash reports, soft locks, missing tutorials, controller binding edge cases — every loud signal gets a hotfix patch within days, not weeks.",
        None),
    "05.04": ("classified", "Trailers & Press",
        "Cinematic trailer cut to 'Calm Before The Storm'. Gameplay trailer showing the dollhouse → 3D loop. Press kit. 80 Level submission. Indie communities. Steam Next Fest.",
        "// Cinematic trailer cut to 'Calm Before The Storm'. Gameplay trailer showing the dollhouse → 3D loop. Press kit. 80 Level submission. Indie communities. Steam Next Fest.",
        None),
    "05.05": ("classified", "Kickstarter Campaign",
        "Funds full-time development. Henry leaves the day job. Local artists, modellers, designers hired long-term. £200K-300K+ unlocks the full team build.",
        "// Funds full-time development. Henry leaves the day job. Local artists, modellers, designers hired long-term. £200K-300K+ unlocks the full team build.",
        None),
    "06.01": ("classified", "Hire Team",
        "Animator. Character Artist. Concept Artist. AI Programmer. Level Designer. Possibly a senior writer. Ironbridge goes from solo to a real studio.",
        "// Animator. Character Artist. Concept Artist. AI Programmer. Level Designer. Possibly a senior writer. Ironbridge goes from solo to a real studio.",
        None),
    "06.02": ("classified", "Animation Pipeline",
        "Custom Kore locomotion set. Real combat anims. Settler work anims per class — Cook, Engineer, Medic, Farmer, Gunsmith. Reaction anims. Mocap session OR senior hand-key animator.",
        "// Custom Kore locomotion set. Real combat anims. Settler work anims per class. Reaction anims. Mocap session OR senior hand-key animator.",
        None),
    "06.03": ("classified", "Character Roster",
        "All 14 Settler classes get unique MetaHuman heads, hair, body variation, full voice packs. Each Settler reads as an individual. The airlock looks populated by people, not mannequins.",
        "// All 14 Settler classes get unique MetaHuman heads, hair, body variation, full voice packs. Each Settler reads as an individual.",
        None),
    "06.04": ("classified", "Wildlife & Animals",
        "Companions: Marv proper. Hostile wildlife: irradiated wolves, mutated rats. Livestock: chickens, cows, sheep, rabbits, bees. Ambient critters: insects, sparrows, butterflies. The world feels alive.",
        "// Companions: Marv proper. Hostile wildlife: irradiated wolves, mutated rats. Livestock: chickens, cows, sheep, rabbits, bees. Ambient critters: insects, sparrows, butterflies.",
        None),
    "06.05": ("classified", "Combat Depth",
        "Stalker AI (sneak, retreat, flank). Legion encounters with dialogue. Boss fights at story beats. Melee depth (parry, dodge). Weapon variety. Geiger-counter mechanic for proximity warning.",
        "// Stalker AI (sneak, retreat, flank). Legion encounters with dialogue. Boss fights at story beats. Melee depth. Weapon variety. Geiger-counter mechanic.",
        None),
    "06.06": ("classified", "Original Soundtrack",
        "'Calm Before The Storm' is the trailer spine. The full score: ambient layers per biome, reactive music per player state, boss themes, intro and outro. Hans-Zimmer-tier composer.",
        "// 'Calm Before The Storm' is the trailer spine. The full score: ambient layers per biome, reactive music per player state, boss themes, intro and outro. Hans-Zimmer-tier composer.",
        None),
    "06.07": ("classified", "Voice Acting",
        "ElevenLabs for procedural Settlers. Hero characters get real human voice actors: Mara, Varek, supporting story NPCs. London talent pool is strong.",
        "// ElevenLabs for procedural Settlers. Hero characters get real human voice actors: Mara, Varek, supporting story NPCs. London talent pool is strong.",
        None),
    "06.08": ("classified", "Cinematics",
        "Opening cinematic where Kore wakes up. Mid-game Legion reveal. Ending sequence. Story-locked moments rendered in-engine using MetaHumans + the painted aesthetic.",
        "// Opening cinematic where Kore wakes up. Mid-game Legion reveal. Ending sequence. Story-locked moments rendered in-engine using MetaHumans + the painted aesthetic.",
        None),
    "06.09": ("classified", "Narrative Writer",
        "A professional writer to structure the full story arc, character backgrounds, faction histories, environmental storytelling. The lore turned into something players obsess over.",
        "// A professional writer to structure the full story arc, character backgrounds, faction histories, environmental storytelling. Lore turned into something players obsess over.",
        None),
    "06.10": ("classified", "Module Customisation",
        "Paint your base your way. Per-module colour and material swaps. Brick, wood, tile, metal finishes per tier. Free basics, premium options cost resources. The 'make it home' feature.",
        "// Paint your base your way. Per-module colour and material swaps. Brick, wood, tile, metal finishes per tier. Free basics, premium options cost resources.",
        None),
    "06.11": ("classified", "Farming Systems",
        "Beyond the early Greenhouse. Full crop systems, seasonal cycles, soil quality, fertilizer crafting, multi-tier crops. Crop failures become real pressure.",
        "// Beyond the early Greenhouse. Full crop systems, seasonal cycles, soil quality, fertilizer crafting, multi-tier crops. Crop failures become real pressure.",
        None),
    "06.12": ("classified", "Irrigation & Water",
        "Pipes, valves, distribution from Water Tank to Greenhouse, Aquaculture, Sanitation. Pipe blockages, leaks, pressure drops. Wells, runoff, condensation.",
        "// Pipes, valves, distribution from Water Tank to Greenhouse, Aquaculture, Sanitation. Pipe blockages, leaks, pressure drops. Wells, runoff, condensation.",
        None),
    "06.13": ("classified", "Performance Pass",
        "60fps locked on PC at recommended specs. Lumen and Nanite tuning. Asset budget audits. Memory profiling. Invisible work that determines whether reviews talk about the game or the framerate.",
        "// 60fps locked on PC at recommended specs. Lumen and Nanite tuning. Asset budget audits. Memory profiling. Invisible work that determines whether reviews talk about the game or the framerate.",
        None),
    "07.01": ("classified", "Early Access Launch",
        "AIRLOCK goes live on Steam Early Access. Core loop complete: build, explore, survive, expand. Not a closed-door project.",
        "// AIRLOCK goes live on Steam Early Access. Core loop complete: build, explore, survive, expand. Not a closed-door project.",
        None),
    "07.02": ("classified", "Community Building",
        "Discord and Slack communities. Direct line between players and studio. Bug reports, feature requests, lore discussion, screenshot showcase.",
        "// Discord and Slack communities. Direct line between players and studio. Bug reports, feature requests, lore discussion, screenshot showcase.",
        None),
    "07.03": ("classified", "Open Development",
        "Public dev diaries. Public roadmap voting. 'Where the money goes' — quarterly breakdown of Kickstarter spend. Players feel like co-builders.",
        "// Public dev diaries. Public roadmap voting. 'Where the money goes' — quarterly breakdown of Kickstarter spend. Players feel like co-builders.",
        None),
    "07.04": ("classified", "Iteration & Patches",
        "Weekly to monthly patches. Bug fixes, balance tweaks, UI improvements. Major content drops every quarter. Suggestions heard and prioritised in public.",
        "// Weekly to monthly patches. Bug fixes, balance tweaks, UI improvements. Major content drops every quarter. Suggestions heard and prioritised in public.",
        None),
    "08.01": ("classified", "1.0 Launch",
        "All systems. Full narrative. Complete economy. The game Henry has carried in his head for over a decade, fully realised.",
        "// All systems. Full narrative. Complete economy. The game Henry has carried in his head for over a decade, fully realised.",
        None),
    "08.02": ("classified", "Console Builds",
        "PS5, Xbox Series X|S, Switch 2. Each platform requires certification. Console launches typically follow PC by 3-6 months.",
        "// PS5, Xbox Series X|S, Switch 2. Each platform requires certification. Console launches typically follow PC by 3-6 months.",
        None),
    "08.03": ("classified", "Localization",
        "French, German, Spanish, Italian, Brazilian Portuguese, Russian, Polish, Simplified Chinese, Japanese, Korean. Subtitles for every voice line.",
        "// French, German, Spanish, Italian, Brazilian Portuguese, Russian, Polish, Simplified Chinese, Japanese, Korean. Subtitles for every voice line.",
        None),
    "08.04": ("classified", "Trading & Economy",
        "Automated trade routes between your airlocks. Previous airlocks become trading partners. Supply and demand shifts. UGA Credits as the post-war currency.",
        "// Automated trade routes between your airlocks. Previous airlocks become trading partners. Supply and demand shifts. UGA Credits as the post-war currency.",
        None),
    "08.05": ("classified", "Multi-Airlock System",
        "Discover new locations: pre-war military bunkers, research annexes, mine shafts, civic shelters. Each unique. Specialise them. Rebuild civilisation, one airlock at a time.",
        "// Discover new locations: pre-war military bunkers, research annexes, mine shafts, civic shelters. Each unique. Specialise them. Rebuild civilisation, one airlock at a time.",
        None),
    "08.06": ("classified", "Underground Metro",
        "Every airlock has a buried metro station. Excavate down. Restore power. Reconnect the line. Fast-travel through dark tunnels. The spine of your underground civilisation.",
        "// Every airlock has a buried metro station. Excavate down. Restore power. Reconnect the line. Fast-travel through dark tunnels. The spine of your underground civilisation.",
        None),
    "08.07": ("classified", "Global Maps",
        "Ashgate is just one city. Tokyo's metro. New York's subway. Berlin's bunkers. Moscow's deepest. The Australian outback. Brazilian favelas. Each map regional-flavoured.",
        "// Ashgate is just one city. Tokyo's metro. New York's subway. Berlin's bunkers. Moscow's deepest. The Australian outback. Brazilian favelas. Each map regional-flavoured.",
        None),
    "08.08": ("classified", "Multiplayer",
        "Your airlock. Your friend's airlock. Connected. Trading between real players. Visiting bases. Cooperative surface runs. The horizon. Everything else is the road that leads here.",
        "// Your airlock. Your friend's airlock. Connected. Trading between real players. Visiting bases. Cooperative surface runs. The horizon. Everything else is the road that leads here.",
        None),
    "08.09": ("classified", "DLC & Beyond",
        "Post-1.0 expansions. New module categories, new Settler classes, new biomes, new story chapters, new Altered variants. Driven by community-voted priorities.",
        "// Post-1.0 expansions. New module categories, new Settler classes, new biomes, new story chapters, new Altered variants. Driven by community-voted priorities.",
        None),
}

# Stamp label per status
STAMP_LABEL = {"declassified": "CLEAR", "in-progress": "IN PROGRESS", "classified": "CLASSIFIED"}

CSS = """:root{--black:#050505;--bg:#0A0A0A;--bg-2:#141414;--bg-3:#1C1C1C;--bone:#ECE6D6;--bone-dim:rgba(236,230,214,0.7);--bone-faint:rgba(236,230,214,0.18);--accent:#D4A046;--accent-bright:#E8B86C;--crit:#C8463A;--green:#6FB85C;--classified:#8B2A2A;}
*{box-sizing:border-box;margin:0;padding:0;}
html{scroll-behavior:smooth;}
body{background:var(--black);color:var(--bone);font-family:'Inter',system-ui,sans-serif;font-size:17px;line-height:1.65;min-height:100vh;overflow-x:hidden;}
body::before{content:'';position:fixed;inset:0;pointer-events:none;opacity:0.04;mix-blend-mode:overlay;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' /%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");z-index:200;}
nav{position:fixed;top:0;left:0;right:0;z-index:95;padding:1.5rem 4%;display:flex;align-items:center;justify-content:space-between;background:linear-gradient(to bottom,rgba(5,5,5,0.85),rgba(5,5,5,0.5));transition:all 0.4s ease;backdrop-filter:blur(8px);border-bottom:1px solid var(--bone-faint);}
nav.scrolled{padding:0.9rem 4%;background:rgba(5,5,5,0.97);}
.nav-logo img{height:36px;filter:drop-shadow(0 4px 14px rgba(0,0,0,0.85));transition:transform 0.2s;}
.nav-logo:hover img{transform:scale(1.04);}
.nav-links{display:flex;gap:2.5rem;list-style:none;}
.nav-links a{color:var(--bone);text-decoration:none;font-family:'Bebas Neue',sans-serif;font-size:1rem;letter-spacing:0.3em;text-transform:uppercase;transition:color 0.2s;position:relative;}
.nav-links a::after{content:'';position:absolute;bottom:-6px;left:50%;right:50%;height:1px;background:var(--accent);transition:left 0.25s,right 0.25s;}
.nav-links a:hover{color:var(--accent);}
.nav-links a:hover::after{left:0;right:0;}
.nav-links a.active{color:var(--accent);}
.nav-links a.active::after{left:0;right:0;}
.nav-cta{font-family:'Bebas Neue',sans-serif;font-size:1rem;letter-spacing:0.3em;text-transform:uppercase;color:var(--black);background:var(--bone);padding:0.6rem 1.6rem;text-decoration:none;transition:all 0.2s;}
.nav-cta:hover{background:var(--accent);transform:translateY(-2px);}
.nav-toggle{display:none;background:none;border:none;color:var(--bone);font-size:1.5rem;cursor:pointer;padding:0;}
/* HERO */
.stage-hero{min-height:78vh;position:relative;display:flex;align-items:flex-end;padding:0 0 5rem;background-size:cover;background-position:center;border-bottom:1px solid var(--bone-faint);}
.stage-hero::before{content:'';position:absolute;inset:0;background:linear-gradient(to bottom,rgba(5,5,5,0.55) 0%,rgba(5,5,5,0.2) 35%,rgba(5,5,5,0.6) 70%,rgba(5,5,5,0.95) 100%);}
.stage-hero-content{position:relative;z-index:2;max-width:1200px;margin:0 auto;padding:0 4%;width:100%;}
.stage-hero-meta{font-family:'Inter',sans-serif;font-weight:500;font-size:0.78rem;color:var(--accent);letter-spacing:0.4em;text-transform:uppercase;margin-bottom:1.2rem;}
.stage-hero-num{font-family:'Bebas Neue',sans-serif;font-size:clamp(5rem,12vw,10rem);line-height:0.9;color:var(--accent);letter-spacing:0.02em;margin-bottom:0.5rem;text-shadow:0 6px 30px rgba(0,0,0,0.7);}
.stage-hero-title{font-family:'Bebas Neue',sans-serif;font-size:clamp(2.6rem,5.5vw,5rem);letter-spacing:0.04em;color:var(--bone);text-transform:uppercase;line-height:1;margin-bottom:1.5rem;text-shadow:0 6px 30px rgba(0,0,0,0.85);}
.stage-hero-summary{font-family:'Crimson Pro',serif;font-style:italic;font-size:clamp(1.05rem,1.6vw,1.4rem);color:var(--bone);max-width:760px;line-height:1.55;text-shadow:0 4px 20px rgba(0,0,0,0.85);}
.stage-stamp{display:inline-block;font-family:'Bebas Neue',sans-serif;font-size:0.95rem;letter-spacing:0.3em;padding:0.5rem 1.2rem;border:2px solid;transform:rotate(-2deg);margin-top:1.8rem;}
.stage-stamp.declassified{color:var(--green);border-color:var(--green);}
.stage-stamp.in-progress{color:var(--accent);border-color:var(--accent);}
.stage-stamp.classified{color:var(--classified);border-color:var(--classified);}
/* INTRO */
.stage-intro{padding:6rem 4%;max-width:900px;margin:0 auto;}
.stage-intro p{font-family:'Crimson Pro',serif;font-size:1.35rem;line-height:1.65;color:var(--bone);}
.stage-intro p::first-letter{font-family:'Bebas Neue',sans-serif;font-size:4rem;float:left;line-height:0.9;margin-right:1rem;margin-top:0.4rem;color:var(--accent);}
/* SUB-STAGES */
.stage-substages{padding:2rem 4% 7rem;max-width:1300px;margin:0 auto;}
.stage-substage{display:grid;grid-template-columns:1fr 1.2fr;gap:3.5rem;align-items:center;padding:5rem 0;border-bottom:1px solid var(--bone-faint);}
.stage-substage:last-child{border-bottom:none;}
.stage-substage.no-image{grid-template-columns:1fr;max-width:820px;}
.stage-substage-image{position:relative;aspect-ratio:16/10;overflow:hidden;border:1px solid var(--bone-faint);}
.stage-substage-image img{width:100%;height:100%;object-fit:cover;transition:transform 0.6s;}
.stage-substage-image:hover img{transform:scale(1.04);}
.stage-substage:nth-child(even):not(.no-image){direction:rtl;}
.stage-substage:nth-child(even):not(.no-image) > *{direction:ltr;}
.stage-substage-content{position:relative;}
.stage-substage-stamp{display:inline-block;font-family:'Bebas Neue',sans-serif;font-size:0.65rem;letter-spacing:0.2em;padding:0.18rem 0.55rem;border:1.5px solid;margin-bottom:1rem;transform:rotate(-1deg);}
.stage-substage-stamp.declassified{color:var(--green);border-color:var(--green);}
.stage-substage-stamp.in-progress{color:var(--accent);border-color:var(--accent);}
.stage-substage-stamp.classified{color:var(--classified);border-color:var(--classified);}
.stage-substage-num{font-family:'Inter',sans-serif;font-weight:500;font-size:0.78rem;color:var(--accent);letter-spacing:0.35em;text-transform:uppercase;margin-bottom:0.6rem;}
.stage-substage-name{font-family:'Bebas Neue',sans-serif;font-size:clamp(1.7rem,3vw,2.4rem);letter-spacing:0.03em;color:var(--bone);text-transform:uppercase;line-height:1.05;margin-bottom:1.2rem;}
.stage-substage-body{font-size:1.05rem;color:var(--bone-dim);line-height:1.6;margin-bottom:1rem;}
.stage-substage-detail{font-family:'Crimson Pro',serif;font-style:italic;font-size:1.05rem;color:var(--bone);line-height:1.55;padding-left:1.2rem;border-left:2px solid var(--accent);}
/* NAV PILLS */
.stage-nav{padding:4rem 4%;max-width:1200px;margin:0 auto;display:flex;justify-content:space-between;align-items:stretch;gap:1.5rem;flex-wrap:wrap;}
.stage-nav-pill{flex:1;min-width:280px;padding:1.8rem 1.6rem;background:var(--bg-2);border:1px solid var(--bone-faint);text-decoration:none;transition:all 0.25s;display:flex;flex-direction:column;gap:0.4rem;}
.stage-nav-pill:hover{border-color:var(--accent);background:var(--bg-3);transform:translateY(-3px);}
.stage-nav-pill.disabled{opacity:0.35;pointer-events:none;}
.stage-nav-meta{font-family:'Inter',sans-serif;font-size:0.7rem;color:var(--accent);letter-spacing:0.3em;text-transform:uppercase;}
.stage-nav-name{font-family:'Bebas Neue',sans-serif;font-size:1.3rem;color:var(--bone);letter-spacing:0.05em;text-transform:uppercase;}
.stage-nav-pill.next{text-align:right;}
.stage-nav-pill.center{text-align:center;justify-content:center;background:transparent;border-color:var(--bone-faint);}
.stage-nav-pill.center:hover{background:var(--bg-2);}
/* FOOTER */
footer{background:var(--black);padding:5rem 4% 2rem;border-top:1px solid var(--bone-faint);}
.footer-grid{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:3rem;max-width:1300px;margin:0 auto 3rem;}
.footer-brand img{height:50px;margin-bottom:1rem;}
.footer-brand p{color:var(--bone-dim);font-style:italic;font-size:0.95rem;line-height:1.6;}
.footer-col h5{font-family:'Bebas Neue',sans-serif;font-size:0.95rem;letter-spacing:0.3em;color:var(--accent);text-transform:uppercase;margin-bottom:1rem;}
.footer-col ul{list-style:none;}
.footer-col li{margin-bottom:0.5rem;}
.footer-col a{color:var(--bone-dim);text-decoration:none;font-size:0.95rem;transition:color 0.2s;}
.footer-col a:hover{color:var(--bone);}
.footer-bottom{text-align:center;color:var(--bone-dim);font-family:'Bebas Neue',sans-serif;font-size:0.85rem;letter-spacing:0.4em;padding-top:2rem;border-top:1px solid var(--bone-faint);max-width:1300px;margin:0 auto;}
.reveal{opacity:0;transform:translateY(30px);transition:opacity 0.9s ease,transform 0.9s ease;}
.reveal.visible{opacity:1;transform:translateY(0);}
@media (max-width:1100px){.nav-links{display:none;position:absolute;top:100%;left:0;right:0;background:rgba(5,5,5,0.98);flex-direction:column;padding:2rem;gap:1.5rem;border-bottom:1px solid var(--bone-faint);}.nav-links.open{display:flex;}.nav-toggle{display:block;}}
@media (max-width:900px){.footer-grid{grid-template-columns:1fr;}.stage-substage{grid-template-columns:1fr!important;direction:ltr!important;}.stage-substage > *{direction:ltr!important;}.stage-nav{flex-direction:column;}.stage-nav-pill.next{text-align:left;}}"""


def render_substage(num, idx):
    if num not in SUBSTAGES:
        return ""
    status, name, body, detail, image = SUBSTAGES[num]
    stamp_label = STAMP_LABEL[status]
    has_image = image is not None
    cls = "stage-substage reveal" + ("" if has_image else " no-image")
    parts = []
    parts.append(f'<article class="{cls}">')
    if has_image:
        parts.append(f'<div class="stage-substage-image"><img src="{image}" alt="" loading="lazy"></div>')
    parts.append('<div class="stage-substage-content">')
    parts.append(f'<div class="stage-substage-stamp {status}">{stamp_label}</div>')
    parts.append(f'<div class="stage-substage-num">{num}</div>')
    parts.append(f'<h3 class="stage-substage-name">{name}</h3>')
    parts.append(f'<p class="stage-substage-body">{body}</p>')
    parts.append(f'<p class="stage-substage-detail">{detail}</p>')
    parts.append('</div></article>')
    return "\n".join(parts)


def render_nav_pill(stage_id, label):
    if stage_id is None:
        return ""
    s = next((x for x in STAGES if x["id"] == stage_id), None)
    if not s:
        return ""
    side = "prev" if label == "PREV" else "next"
    arrow = "←" if label == "PREV" else "→"
    name_str = s["title"] if label == "PREV" else s["title"]
    if label == "NEXT":
        meta = f'{arrow} STAGE {s["num"]} · NEXT'
    else:
        meta = f'{arrow} STAGE {s["num"]} · PREV'
    return f'<a class="stage-nav-pill {side}" href="stage-{stage_id}.html"><div class="stage-nav-meta">{meta}</div><div class="stage-nav-name">{s["title"]}</div></a>'


def render_stage(stage):
    sub_html = "\n".join(render_substage(n, i) for i, n in enumerate(stage["substages"]))
    prev_html = render_nav_pill(stage["prev"], "PREV") if stage["prev"] else '<span class="stage-nav-pill prev disabled"><div class="stage-nav-meta">← BEGINNING</div><div class="stage-nav-name">First Stage</div></span>'
    next_html = render_nav_pill(stage["next"], "NEXT") if stage["next"] else '<span class="stage-nav-pill next disabled"><div class="stage-nav-meta">END →</div><div class="stage-nav-name">Final Stage</div></span>'
    back_html = '<a class="stage-nav-pill center" href="roadmap.html"><div class="stage-nav-meta">⌂ ROADMAP</div><div class="stage-nav-name">All Stages</div></a>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AIRLOCK · {stage["kicker"]}</title>
<meta name="description" content="{stage["summary"]}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Crimson+Pro:ital,wght@0,400;0,500;1,400&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>

<nav id="nav">
    <a href="index.html" class="nav-logo"><img src="airlock_menulogo.png" alt="AIRLOCK"></a>
    <button class="nav-toggle" id="navToggle" aria-label="Menu">☰</button>
    <ul class="nav-links" id="navLinks">
        <li><a href="index.html">Home</a></li>
        <li><a href="roadmap.html" class="active">Roadmap</a></li>
        <li><a href="diary.html">Updates</a></li>
        <li><a href="media.html">Media</a></li>
        <li><a href="index.html#support">Support</a></li>
    </ul>
    <a href="#" class="nav-cta">Wishlist</a>
</nav>

<section class="stage-hero" style="background-image:url('{stage["hero"]}');">
    <div class="stage-hero-content">
        <div class="stage-hero-meta">// {stage["kicker"]}</div>
        <div class="stage-hero-num">{stage["num"]}</div>
        <h1 class="stage-hero-title">{stage["title"]}</h1>
        <p class="stage-hero-summary">{stage["summary"]}</p>
        <div class="stage-stamp {stage["status"]}">{stage["stamp"]}</div>
    </div>
</section>

<section class="stage-intro">
    <p>{stage["intro"]}</p>
</section>

<section class="stage-substages">
{sub_html}
</section>

<nav class="stage-nav">
    {prev_html}
    {back_html}
    {next_html}
</nav>

<footer>
    <div class="footer-grid">
        <div class="footer-brand">
            <img src="airlock_logo_front.png" alt="AIRLOCK">
            <p>An Ironbridge Games title.<br>Built in the dark. Made for the surface.</p>
        </div>
        <div class="footer-col"><h5>The Game</h5><ul><li><a href="index.html">Home</a></li><li><a href="roadmap.html">Roadmap</a></li><li><a href="media.html">Media</a></li></ul></div>
        <div class="footer-col"><h5>Channel</h5><ul><li><a href="diary.html">Dev Diary</a></li><li><a href="index.html#newsletter">Newsletter</a></li><li><a href="#">Discord</a></li></ul></div>
        <div class="footer-col"><h5>Studio</h5><ul><li><a href="#">Ironbridge Games</a></li><li><a href="index.html#support">Support</a></li><li><a href="#">Press Kit</a></li></ul></div>
    </div>
    <div class="footer-bottom">© 2026 Ironbridge Games Ltd · Company No. 16882669</div>
</footer>

<script>
const nav=document.getElementById('nav');
function onScroll(){{if(window.scrollY>80)nav.classList.add('scrolled');else nav.classList.remove('scrolled');}}
window.addEventListener('scroll',onScroll,{{passive:true}});onScroll();
const navToggle=document.getElementById('navToggle');
const navLinks=document.getElementById('navLinks');
if(navToggle)navToggle.addEventListener('click',()=>navLinks.classList.toggle('open'));
const observer=new IntersectionObserver((entries)=>{{entries.forEach(e=>{{if(e.isIntersecting){{e.target.classList.add('visible');observer.unobserve(e.target);}}}});}},{{threshold:0.12,rootMargin:'0px 0px -60px 0px'}});
document.querySelectorAll('.reveal').forEach(el=>observer.observe(el));
</script>

</body>
</html>"""


for stage in STAGES:
    out_path = Path(f"stage-{stage['id']}.html")
    out_path.write_text(render_stage(stage), encoding='utf-8')
    print(f"Wrote {out_path} ({out_path.stat().st_size} bytes)")
