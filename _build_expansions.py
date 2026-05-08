"""
Inject expansion details into roadmap.html sub-stages.
Each .substage gets a hidden .substage-details block with extended copy + optional image.
"""
import re
from pathlib import Path

ROADMAP = Path("roadmap.html")

# Map: substage number → (extended_detail, image_filename or None)
DETAILS = {
    "01.01": (
        "ALS V4 dropped in. Custom dollhouse cam written from scratch. The military compound was throwaway, but proved the dual-view loop. The moment that build ran, AIRLOCK stopped being a pitch deck and became a project.",
        "screenshots/airlock_screenshot_01.jpg",
    ),
    "02.01": (
        "Confluence dossier of every faction, every settler class, every place name, every story beat. The Sonic War. The collapse of the UGA. The Legion arc. Memory locked into a single source of truth before a single line of gameplay code went in.",
        None,
    ),
    "02.02": (
        "Reference docs locked: TLOU + TLOU Part II + Days Gone for SFX. Hans Zimmer's emotional register for score. 'Calm Before The Storm' written, scored, performed — the spine the trailer will eventually be cut to.",
        None,
    ),
    "02.03": (
        "Twenty-plus HUD variations across ten distinct directions, side-by-side mockups, ruthless elimination. The painted concept-art aesthetic survived. Cream sumi-ink on near-black. Hand-made energy. Nothing else came close.",
        "screenshots/4_mainmenu.png",
    ),
    "02.04": (
        "Ninety-one painted icons in a single sprite sheet. Cream monochrome masters. CSS-tinted at runtime. Survival bars, weapons, status effects, map pins, the whole UI vocabulary in one consistent painted hand.",
        None,
    ),
    "03.01": (
        "GridManager from blank file. Multi-floor support designed in from day one. World-to-grid coordinate conversion. Cell occupancy tracking. The bedrock everything else stands on.",
        "screenshots/airlock_underworld_03.jpg",
    ),
    "03.02": (
        "ALS V4 dismantled and rewired for AIRLOCK. Custom rotation modes. Stance changes. Crouch flow. The character feels heavy underground and alert above. Two worlds, one pawn.",
        None,
    ),
    "03.03": (
        "Main menu shell, settings, accessibility, brightness calibration, epilepsy warning, press-any-key splash. Every screen on the path from boot to gameplay built from the painted style guide.",
        "screenshots/city_bg_airlockPressAnyKey.jpg",
    ),
    "03.04": (
        "Compass, vitals, status effects, notifications, weapon ammo, day-time clock — modular sub-widgets feeding off a single HUD State Component. Add a new screen, it just plugs in. No legacy spaghetti.",
        None,
    ),
    "03.05": (
        "Weapons that degrade. Ammo that runs out. M4 Carbine, Glock — the demo loadout. Every shot is a trade. Combat designed to feel desperate, not heroic.",
        "screenshots/airlock_screenshot_07.jpg",
    ),
    "03.06": (
        "Ghost placement, snap-to-grid, collision check, neighbour-aware wall toggling, save/load round-trip. Then the big architectural pivot mid-flight: monolithic Blueprints out, Level Instance modules in. Speed of authoring x10.",
        "screenshots/screenshot_buildmode.png.jpg",
    ),
    "03.07": (
        "Days-Gone-style horde architecture. Hundreds of Altered chasing one player without tanking the framerate. Spawn manager, perception, navigation. They hunt. They overwhelm. Daytime tense, night deadly.",
        "screenshots/airlock_screenshot_08.jpg",
    ),
    "03.08": (
        "Cabinets. Drawers. Lockers. Every container a hand-stocked moment of risk-reward. Food, weapons, blueprints, raw materials. The reason every surface trip means something.",
        None,
    ),
    "03.09": (
        "ALS mannequin retired. MetaHuman in. Real face, real hair, real subsurface scattering. The foundation for every cutscene moment that has to land emotionally — not just animations playing on a doll.",
        "screenshots/airlock_screenshot_marv.jpg",
    ),
    "03.10": (
        "Marv has moods. He sniffs. He sits. He chases. He has poses that lock when the player moves. He's not a turret on legs — he's a dog you start to worry about.",
        "screenshots/Marv.jpg",
    ),
    "03.11": (
        "Cave → Structured Cave → Brick + Wood → Concrete + Tile → Metal Sci-Fi. Every upgrade re-skins a module visually and functionally. You see the progress when you walk past it.",
        None,
    ),
    "03.12": (
        "One framework for every interactable in the game. Press, hold, contextual prompt, platform-aware glyph (KB/Xbox/PS). Mining ties into grid depth — deeper rooms surface rarer ore.",
        None,
    ),
    "03.13": (
        "Seventeen parent skill categories. A hundred and thirty plus sub-skills. Eight tiers, ten sub-levels each. Player and Settlers share the tree. XP propagates across related skills. Built for hundreds of hours of progression.",
        None,
    ),
    "04.01": (
        "Faction system. Behaviour state machine. Combat component. Injury component. Dialogue component. Voice component. Bump component. Every NPC inherits the spine; specialisations layer on top.",
        None,
    ),
    "04.02": (
        "Mara has fifty-five voice lines, recorded with inline emotion tags through ElevenLabs and CF Flow. She greets, complains, reacts to power loss. Subtitles stack. NPCs walk between activity anchors. Real life inside the airlock.",
        None,
    ),
    "04.03": (
        "Painted sumi-ink HUD landed in engine. Inventory, build menu, compass, notifications, skill XP popups — every panel rebuilt on the painted style. Module padlocks. Auto-flashlight that engages when night falls or the lights die.",
        "screenshots/airlock_underworld_05.jpg",
    ),
    "04.04": (
        "Ultra Dynamic Sky drives every timer. Hunger drains over twenty-eight in-game days. Thirst over forty-eight hours. Stress and morale react to the base around you. The body keeps score.",
        None,
    ),
    "04.05": (
        "Forty-five real minutes per in-game day. Sky shifts, lighting reacts, NPCs change schedule. Toxic night queued. Going to the surface after dark will not be optional, it will be a calculation.",
        "screenshots/airlock_world_06.jpg",
    ),
    "04.06": (
        "Generators with green/amber/red status LEDs you can read across a room. Networks of generators. Five-second overload trips. Powered lights subscribe to a power source by ID. Pull the plug and the world reacts visually + audibly.",
        "screenshots/airlock_underworld_02.jpg",
    ),
    "04.07": (
        "Subtitle widget supports stack mode — Mara talking, the radio crackling, the generator humming, all on screen at once without overwriting. Italic-paren convention for non-speech. Proximity-gated so the line only shows when you're near.",
        None,
    ),
    "04.08": (
        "Custom PCG cascade node — designer drops a biome volume, the system spawns mature trees, then juveniles around them, then saplings around those, then ground cover. Tag-based include/exclude. Marketplace-ready.",
        "screenshots/airlock_world_03.jpg",
    ),
    "04.09": (
        "Painted hero concepts for every demo module. Operations Room, Workhouse, Bunkroom — the three locked + dressed in engine. Reference paintings for Kitchen, Greenhouse, Aquaculture, Power Room queued.",
        "screenshots/airlock_underworld_01.jpg",
    ),
    "04.10": (
        "Operations Room: Planning Board, salvaged radio desk, lockers, fluorescent buzz, ivy through the cracks. Workhouse: multi-discipline crafting space. Bunkroom: where rescued Settlers sleep before they migrate to their specialist module.",
        "screenshots/airlock_underworld_04.jpg",
    ),
    "04.11": (
        "Ashgate streets traced with the new procedural city tool. Hospital where Kore wakes. Gas station for fuel. Builders merchant. The abandoned airlock entrance — a boarded-up cellar door, not a sci-fi blast hatch. Grounded.",
        "screenshots/airlock_world_01.jpg",
    ),
    "04.12": (
        "Procedural names. Procedural traits. Procedural skill rolls weighted by class. Fourteen Settler classes ready to instantiate. They walk in. They stand at their module. They greet Kore by name when he passes.",
        None,
    ),
    "04.13": (
        "Kingdom Tale-style gating. No Engineer in the airlock means no Tier 2+ upgrades. No Chemist means no explosives. The rescue loop directly determines what your base can become. Strategy from the very first choice.",
        None,
    ),
    "04.14": (
        "Module upgrades stop being instant mesh swaps. A timer runs. Scaffolding visible. If the upgrade digs deeper, ore nodes spawn in the new cells — mine them before the timer ends or lose the haul. Settlers shove Kore back if he tries to walk in mid-build.",
        None,
    ),
    "04.15": (
        "Sixty-plus minutes of the game's bones. Wake alone in the hospital. Step into the silence. Meet Mara. Reach the airlock. Build your first rooms. Survive the night. End on the hook that makes the player need the next chapter.",
        "screenshots/airlock_world_02.jpg",
    ),
    # CLASSIFIED stages — no images, evocative copy
    "05.01": (
        "// Coming soon page locked. Header capsule, screenshots, trailer, descriptions. Wishlist collection from day one. The page lives quiet in Steamworks until the demo is footage-ready, then goes public.",
        None,
    ),
    "05.02": (
        "// First weeks live are listening time. Discord, Steam reviews, recorded sessions, surveys. Iterate based on what players actually do, not what we designed for. Telemetry with respect.",
        None,
    ),
    "05.03": (
        "// Rapid-response month. Crash reports, soft locks, missing tutorials, controller binding edge cases — every loud signal gets a hotfix patch within days, not weeks.",
        None,
    ),
    "05.04": (
        "// Cinematic trailer cut to 'Calm Before The Storm'. Gameplay trailer showing the dollhouse → 3D loop. Press kit. 80 Level submission. Indie communities. Steam Next Fest.",
        None,
    ),
    "05.05": (
        "// Funds full-time development. Henry leaves the day job. Local artists, modellers, designers hired long-term. £200K-300K+ unlocks the full team build.",
        None,
    ),
    "06.01": (
        "// Animator. Character Artist. Concept Artist. AI Programmer. Level Designer. Possibly a senior writer. Ironbridge goes from solo to a real studio.",
        None,
    ),
    "06.02": (
        "// Custom Kore locomotion set. Real combat anims. Settler work anims per class. Reaction anims. Mocap session OR senior hand-key animator.",
        None,
    ),
    "06.03": (
        "// All 14 Settler classes get unique MetaHuman heads, hair, body variation, full voice packs. Each Settler reads as an individual.",
        None,
    ),
    "06.04": (
        "// Companions: Marv proper. Hostile wildlife: irradiated wolves, mutated rats. Livestock: chickens, cows, sheep, rabbits, bees. Ambient critters: insects, sparrows, butterflies.",
        None,
    ),
    "06.05": (
        "// Stalker AI (sneak, retreat, flank). Legion encounters with dialogue. Boss fights at story beats. Melee depth. Weapon variety. Geiger-counter mechanic.",
        None,
    ),
    "06.06": (
        "// 'Calm Before The Storm' is the trailer spine. The full score: ambient layers per biome, reactive music per player state, boss themes, intro and outro. Hans-Zimmer-tier composer.",
        None,
    ),
    "06.07": (
        "// ElevenLabs for procedural Settlers. Hero characters get real human voice actors: Mara, Varek, supporting story NPCs. London talent pool is strong.",
        None,
    ),
    "06.08": (
        "// Opening cinematic where Kore wakes up. Mid-game Legion reveal. Ending sequence. Story-locked moments rendered in-engine using MetaHumans + the painted aesthetic.",
        None,
    ),
    "06.09": (
        "// A professional writer to structure the full story arc, character backgrounds, faction histories, environmental storytelling. Lore turned into something players obsess over.",
        None,
    ),
    "06.10": (
        "// Paint your base your way. Per-module colour and material swaps. Brick, wood, tile, metal finishes per tier. Free basics, premium options cost resources.",
        None,
    ),
    "06.11": (
        "// Beyond the early Greenhouse. Full crop systems, seasonal cycles, soil quality, fertilizer crafting, multi-tier crops. Crop failures become real pressure.",
        None,
    ),
    "06.12": (
        "// Pipes, valves, distribution from Water Tank to Greenhouse, Aquaculture, Sanitation. Pipe blockages, leaks, pressure drops. Wells, runoff, condensation.",
        None,
    ),
    "06.13": (
        "// 60fps locked on PC at recommended specs. Lumen and Nanite tuning. Asset budget audits. Memory profiling. Invisible work that determines whether reviews talk about the game or the framerate.",
        None,
    ),
    "07.01": (
        "// AIRLOCK goes live on Steam Early Access. Core loop complete: build, explore, survive, expand. Not a closed-door project.",
        None,
    ),
    "07.02": (
        "// Discord and Slack communities. Direct line between players and studio. Bug reports, feature requests, lore discussion, screenshot showcase.",
        None,
    ),
    "07.03": (
        "// Public dev diaries. Public roadmap voting. 'Where the money goes' — quarterly breakdown of Kickstarter spend. Players feel like co-builders.",
        None,
    ),
    "07.04": (
        "// Weekly to monthly patches. Bug fixes, balance tweaks, UI improvements. Major content drops every quarter. Suggestions heard and prioritised in public.",
        None,
    ),
    "08.01": (
        "// All systems. Full narrative. Complete economy. The game Henry has carried in his head for over a decade, fully realised.",
        None,
    ),
    "08.02": (
        "// PS5, Xbox Series X|S, Switch 2. Each platform requires certification. Console launches typically follow PC by 3-6 months.",
        None,
    ),
    "08.03": (
        "// French, German, Spanish, Italian, Brazilian Portuguese, Russian, Polish, Simplified Chinese, Japanese, Korean. Subtitles for every voice line.",
        None,
    ),
    "08.04": (
        "// Automated trade routes between your airlocks. Previous airlocks become trading partners. Supply and demand shifts. UGA Credits as the post-war currency.",
        None,
    ),
    "08.05": (
        "// Discover new locations: pre-war military bunkers, research annexes, mine shafts, civic shelters. Each unique. Specialise them. Rebuild civilisation, one airlock at a time.",
        None,
    ),
    "08.06": (
        "// Every airlock has a buried metro station. Excavate down. Restore power. Reconnect the line. Fast-travel through dark tunnels. The spine of your underground civilisation.",
        None,
    ),
    "08.07": (
        "// Ashgate is just one city. Tokyo's metro. New York's subway. Berlin's bunkers. Moscow's deepest. The Australian outback. Brazilian favelas. Each map regional-flavoured.",
        None,
    ),
    "08.08": (
        "// Your airlock. Your friend's airlock. Connected. Trading between real players. Visiting bases. Cooperative surface runs. The horizon. Everything else is the road that leads here.",
        None,
    ),
    "08.09": (
        "// Post-1.0 expansions. New module categories, new Settler classes, new biomes, new story chapters, new Altered variants. Driven by community-voted priorities.",
        None,
    ),
}

content = ROADMAP.read_text(encoding='utf-8')

# Pattern: find each substage and inject a details block before its closing </div>
# Each substage looks like:
# <div class="substage classified|in-progress|declassified">
#     <div class="substage-stamp ...">STAMP</div>
#     <div class="substage-number">XX.YY</div>
#     <div class="substage-name">...</div>
#     <p class="substage-body">...</p>
# </div>

def inject_details(match):
    full = match.group(0)
    num_match = re.search(r'<div class="substage-number">(\d+\.\d+)</div>', full)
    if not num_match:
        return full
    num = num_match.group(1)
    if num not in DETAILS:
        return full
    detail, image = DETAILS[num]
    img_html = f'<img class="substage-details-img" src="{image}" alt="" loading="lazy">' if image else ''
    label = "READ MORE" if image else "// EXPANDED FILE"
    block = (
        '<div class="substage-details">'
        '<div class="substage-details-divider"></div>'
        f'{img_html}'
        f'<p class="substage-details-detail">{detail}</p>'
        f'<div class="substage-details-meta">{label}</div>'
        '</div>'
    )
    # inject before final </div> of the substage block
    new = full.rsplit('</div>', 1)
    return new[0] + block + '</div>' + new[1]

# Match a full substage div block. Use non-greedy + DOTALL.
# Pattern needs to capture <div class="substage ..."> ... </div> at the end of the block before the next sibling.
# Be careful: substage has nested divs. We need balanced matching at the substage level.
# Strategy: count divs.

def find_and_replace_substages(text):
    out = []
    i = 0
    while i < len(text):
        m = re.search(r'<div class="substage (?:declassified|in-progress|classified)">', text[i:])
        if not m:
            out.append(text[i:])
            break
        out.append(text[i:i+m.start()])
        start = i + m.start()
        # find matching close by div counting
        depth = 1
        j = i + m.end()
        while j < len(text) and depth > 0:
            open_m = re.search(r'<div\b', text[j:])
            close_m = re.search(r'</div>', text[j:])
            if not close_m:
                break
            if open_m and (open_m.start() < close_m.start()):
                depth += 1
                j += open_m.end()
            else:
                depth -= 1
                j += close_m.end()
        block = text[start:j]
        new_block = inject_details(re.match(r'.*', block, re.DOTALL))
        out.append(new_block)
        i = j
    return ''.join(out)

new_content = find_and_replace_substages(content)
ROADMAP.write_text(new_content, encoding='utf-8')
print(f"Done. New file size: {len(new_content)} bytes")
