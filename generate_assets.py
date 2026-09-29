"""
Generate cozy pixel-art SVG assets for Quiet Audit (GRC Crisis Management Game).
Generates crisp, retro pixel-art SVGs with exact coordinate grids.
"""
import os

os.makedirs("static/images", exist_ok=True)

def create_pixel_svg(width, height, pixel_size, pixels, defs=""):
    """
    pixels: dict of color -> list of (x, y) coordinates
    """
    svg_w = width * pixel_size
    svg_h = height * pixel_size
    rects = []
    for color, coords in pixels.items():
        for (x, y) in coords:
            rects.append(f'<rect x="{x*pixel_size}" y="{y*pixel_size}" width="{pixel_size}" height="{pixel_size}" fill="{color}" />')
    
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}" shape-rendering="crispEdges">
    {defs}
    {''.join(rects)}
</svg>'''

# 1. Barnaby Neutral (Cozy Cat with spectacles and compliance clipboard)
def generate_barnaby_neutral():
    p = 4
    w, h = 32, 32
    # Colors
    c_fur = "#F4EBD9"       # Warm cream fur
    c_fur_dark = "#E1D2B8"  # Shading
    c_ear_inner = "#F8B195" # Pastel pink
    c_eyes = "#2E4057"      # Deep navy eyes
    c_glass = "#D9534F"     # Coral red wire spectacles
    c_glass_lens = "#A8DADC" # Cyan tint
    c_nose = "#E76F51"      # Cute salmon nose
    c_sweater = "#4A7C59"   # Sage/forest green cozy knit sweater
    c_sweater_trim = "#68A67D" # Lighter knit ribbing
    c_board = "#D4A373"     # Wooden clipboard
    c_paper = "#FAFAFA"     # White paper checklist
    c_check = "#2A9D8F"     # Green checkmark
    c_outline = "#2F3E46"   # Soft charcoal outline

    pixels = {
        c_outline: [],
        c_fur: [],
        c_fur_dark: [],
        c_ear_inner: [],
        c_eyes: [],
        c_glass: [],
        c_glass_lens: [],
        c_nose: [],
        c_sweater: [],
        c_sweater_trim: [],
        c_board: [],
        c_paper: [],
        c_check: []
    }

    # Outline & Fur of Head
    # Ears
    for x in [8, 9, 10, 21, 22, 23]:
        pixels[c_outline].append((x, 4))
    for x in [7, 11, 20, 24]:
        pixels[c_outline].append((x, 5))
    for x in [6, 12, 19, 25]:
        pixels[c_outline].append((x, 6))
    for x in [6, 13, 18, 25]:
        pixels[c_outline].append((x, 7))

    # Inner ear pink
    pixels[c_ear_inner].extend([(8, 5), (9, 5), (8, 6), (9, 6), (10, 6), (9, 7), (10, 7), (11, 7)])
    pixels[c_ear_inner].extend([(22, 5), (23, 5), (21, 6), (22, 6), (23, 6), (20, 7), (21, 7), (22, 7)])

    # Ear fur
    for x, y in [(7, 6), (7, 7), (8, 7), (12, 7), (19, 7), (23, 7), (24, 6), (24, 7)]:
        pixels[c_fur].append((x, y))

    # Head top outline
    for x in range(13, 19):
        pixels[c_outline].append((x, 7))
        pixels[c_fur].append((x, 8))

    # Head sides outline
    for y in range(8, 17):
        pixels[c_outline].append((5, y))
        pixels[c_outline].append((26, y))

    # Head fill
    for y in range(8, 17):
        for x in range(6, 26):
            if (x, y) not in pixels[c_ear_inner] and (x, y) not in pixels[c_outline]:
                pixels[c_fur].append((x, y))

    # Head bottom / chin outline
    for x in range(8, 24):
        pixels[c_outline].append((x, 17))

    # Fur shading around lower cheeks
    for x in range(6, 10):
        pixels[c_fur_dark].append((x, 16))
    for x in range(22, 26):
        pixels[c_fur_dark].append((x, 16))

    # Spectacles (Red wireframes)
    # Left lens frame (x: 8 to 13, y: 10 to 13)
    for x in range(8, 14):
        pixels[c_glass].append((x, 10))
        pixels[c_glass].append((x, 13))
    for y in range(11, 13):
        pixels[c_glass].append((8, y))
        pixels[c_glass].append((13, y))

    # Right lens frame (x: 18 to 23, y: 10 to 13)
    for x in range(18, 24):
        pixels[c_glass].append((x, 10))
        pixels[c_glass].append((x, 13))
    for y in range(11, 13):
        pixels[c_glass].append((18, y))
        pixels[c_glass].append((23, y))

    # Bridge between spectacles
    for x in range(14, 18):
        pixels[c_glass].append((x, 11))

    # Lens glass and eyes
    for y in [11, 12]:
        for x in range(9, 13):
            pixels[c_glass_lens].append((x, y))
        for x in range(19, 23):
            pixels[c_glass_lens].append((x, y))

    # Eyes (behind glass)
    pixels[c_eyes].extend([(10, 11), (11, 11), (10, 12), (11, 12)])
    pixels[c_eyes].extend([(20, 11), (21, 11), (20, 12), (21, 12)])
    # Eye shine
    pixels[c_paper].extend([(10, 11), (20, 11)])

    # Nose & Mouth
    pixels[c_nose].extend([(15, 13), (16, 13)])
    pixels[c_outline].extend([(15, 14), (16, 14), (14, 15), (17, 15)])

    # Whiskers
    for y in [13, 14]:
        pixels[c_outline].extend([(2, y), (3, y), (4, y)])
        pixels[c_outline].extend([(27, y), (28, y), (29, y)])

    # Cozy Knit Sweater (Torso)
    # Collar
    for x in range(12, 20):
        pixels[c_sweater_trim].append((x, 18))
    # Body
    for y in range(19, 29):
        pixels[c_outline].append((7, y))
        pixels[c_outline].append((24, y))
        for x in range(8, 24):
            pixels[c_sweater].append((x, y))
    for x in range(7, 25):
        pixels[c_outline].append((x, 29))
        pixels[c_sweater_trim].append((x, 28))

    # Paws holding clipboard
    # Clipboard on left
    for y in range(19, 28):
        pixels[c_outline].append((14, y))
        pixels[c_outline].append((22, y))
        for x in range(15, 22):
            pixels[c_board].append((x, y))
    for x in range(14, 23):
        pixels[c_outline].append((x, 19))
        pixels[c_outline].append((x, 28))

    # Paper on clipboard
    for y in range(21, 27):
        for x in range(16, 21):
            pixels[c_paper].append((x, y))
    # Green checkmark on paper
    pixels[c_check].extend([(17, 24), (18, 25), (19, 23), (20, 22)])

    # Cat paws
    pixels[c_fur].extend([(13, 23), (14, 23), (13, 24), (14, 24)]) # left paw
    pixels[c_fur].extend([(22, 23), (23, 23), (22, 24), (23, 24)]) # right paw

    return create_pixel_svg(w, h, p, pixels)

# 2. Barnaby Alert / Panicked (Cat during Sev-1 / Audit emergency!)
def generate_barnaby_alert():
    p = 4
    w, h = 32, 32
    c_fur = "#F4EBD9"
    c_fur_dark = "#E1D2B8"
    c_ear_inner = "#F8B195"
    c_eyes = "#D9534F"     # Red alarmed eyes!
    c_sweat = "#64B5F6"    # Little blue sweat drop
    c_nose = "#E76F51"
    c_mouth = "#C0392B"    # Open mouth "O"
    c_sweater = "#D97D64"  # Alert salmon sweater
    c_sweater_trim = "#B55A44"
    c_outline = "#2F3E46"
    c_siren = "#FFD166"    # Tiny flashing alert symbol

    pixels = {
        c_outline: [], c_fur: [], c_fur_dark: [], c_ear_inner: [],
        c_eyes: [], c_sweat: [], c_nose: [], c_mouth: [],
        c_sweater: [], c_sweater_trim: [], c_siren: []
    }

    # Ears pinned back slightly in panic
    for x in [6, 7, 8, 23, 24, 25]:
        pixels[c_outline].append((x, 5))
    for x in [5, 9, 22, 26]:
        pixels[c_outline].append((x, 6))
    for x in [4, 10, 21, 27]:
        pixels[c_outline].append((x, 7))

    pixels[c_ear_inner].extend([(6, 6), (7, 6), (8, 6), (5, 7), (6, 7), (7, 7), (8, 7)])
    pixels[c_ear_inner].extend([(23, 6), (24, 6), (25, 6), (23, 7), (24, 7), (25, 7), (26, 7)])

    # Head top
    for x in range(11, 21):
        pixels[c_outline].append((x, 7))
        pixels[c_fur].append((x, 8))

    # Head sides
    for y in range(8, 17):
        pixels[c_outline].append((4, y))
        pixels[c_outline].append((27, y))
        for x in range(5, 27):
            pixels[c_fur].append((x, y))
    for x in range(7, 25):
        pixels[c_outline].append((x, 17))

    # Wide alarmed eyes! (Big pupils)
    for y in range(10, 14):
        for x in range(8, 13):
            pixels[c_outline].append((x, y))
        for x in range(19, 24):
            pixels[c_outline].append((x, y))
    # Red iris / pupil
    for y in range(11, 13):
        for x in range(9, 12):
            pixels[c_eyes].append((x, y))
        for x in range(20, 23):
            pixels[c_eyes].append((x, y))
    # Eye shine
    pixels["#FFF"].extend([(9, 11), (20, 11)]) if "#FFF" in pixels else None
    if "#FFF" not in pixels:
        pixels["#FFFFFF"] = [(9, 11), (20, 11)]

    # Sweat drop flying off forehead
    pixels[c_sweat].extend([(28, 8), (28, 9), (29, 9), (28, 10)])

    # Nose & open gasp mouth
    pixels[c_nose].extend([(15, 12), (16, 12)])
    pixels[c_outline].extend([(14, 14), (17, 14), (14, 16), (17, 16)])
    for y in range(14, 17):
        for x in range(15, 17):
            pixels[c_mouth].append((x, y))

    # Paws on cheeks in "Home Alone" panic pose!
    pixels[c_fur_dark].extend([(5, 13), (5, 14), (6, 14), (26, 13), (26, 14), (25, 14)])

    # Sweater
    for y in range(18, 29):
        pixels[c_outline].append((7, y))
        pixels[c_outline].append((24, y))
        for x in range(8, 24):
            pixels[c_sweater].append((x, y))
    for x in range(7, 25):
        pixels[c_outline].append((x, 29))
        pixels[c_sweater_trim].append((x, 28))

    # Exclamation mark above head
    for y in range(1, 5):
        pixels[c_eyes].append((15, y))
        pixels[c_eyes].append((16, y))
    pixels[c_eyes].append((15, 6))
    pixels[c_eyes].append((16, 6))

    return create_pixel_svg(w, h, p, pixels)

# 3. Barnaby Happy / Smug (Scenario Cleared / Perfect Compliance)
def generate_barnaby_happy():
    p = 4
    w, h = 32, 32
    c_fur = "#F4EBD9"
    c_fur_dark = "#E1D2B8"
    c_ear_inner = "#F8B195"
    c_eyes = "#2E4057"
    c_nose = "#E76F51"
    c_sweater = "#E76F51"   # Warm coral pink
    c_sweater_trim = "#F4A261"
    c_coffee = "#FFFFFF"   # White ceramic coffee mug
    c_coffee_dark = "#D8D8D8"
    c_brew = "#6F4E37"     # Hot dark roast coffee
    c_steam = "#E0E0E0"    # Cozy steam curling up
    c_star = "#E9C46A"     # Gold compliance star
    c_outline = "#2F3E46"

    pixels = {
        c_outline: [], c_fur: [], c_fur_dark: [], c_ear_inner: [],
        c_eyes: [], c_nose: [], c_sweater: [], c_sweater_trim: [],
        c_coffee: [], c_coffee_dark: [], c_brew: [], c_steam: [],
        c_star: []
    }

    # Relaxed upright ears
    for x in [8, 9, 10, 21, 22, 23]:
        pixels[c_outline].append((x, 4))
    for x in [7, 11, 20, 24]:
        pixels[c_outline].append((x, 5))
    for x in [6, 12, 19, 25]:
        pixels[c_outline].append((x, 6))

    pixels[c_ear_inner].extend([(8, 5), (9, 5), (8, 6), (9, 6), (10, 6)])
    pixels[c_ear_inner].extend([(22, 5), (23, 5), (21, 6), (22, 6), (23, 6)])

    # Head outline & fill
    for x in range(12, 20):
        pixels[c_outline].append((x, 6))
    for y in range(7, 17):
        pixels[c_outline].append((5, y))
        pixels[c_outline].append((26, y))
        for x in range(6, 26):
            if (x, y) not in pixels[c_ear_inner] and (x, y) not in pixels[c_outline]:
                pixels[c_fur].append((x, y))
    for x in range(7, 25):
        pixels[c_outline].append((x, 17))

    # Happy squinty closed eyes ^ . ^
    # Left eye
    pixels[c_eyes].extend([(9, 12), (10, 11), (11, 11), (12, 12)])
    pixels[c_fur_dark].extend([(9, 13), (12, 13)]) # blush underneath
    # Right eye
    pixels[c_eyes].extend([(19, 12), (20, 11), (21, 11), (22, 12)])
    pixels[c_fur_dark].extend([(19, 13), (22, 13)])

    # Cute pink blush cheeks
    pixels[c_ear_inner].extend([(7, 13), (8, 13), (23, 13), (24, 13)])

    # Cute nose and smile
    pixels[c_nose].extend([(15, 12), (16, 12)])
    pixels[c_outline].extend([(14, 14), (17, 14), (15, 15), (16, 15)])

    # Cozy knit sweater
    for y in range(18, 29):
        pixels[c_outline].append((7, y))
        pixels[c_outline].append((24, y))
        for x in range(8, 24):
            pixels[c_sweater].append((x, y))
    for x in range(7, 25):
        pixels[c_outline].append((x, 29))
        pixels[c_sweater_trim].append((x, 28))

    # Holding a warm mug of "Compliance Coffee"
    # Mug
    for y in range(21, 27):
        pixels[c_outline].append((12, y))
        pixels[c_outline].append((19, y))
        for x in range(13, 19):
            pixels[c_coffee].append((x, y))
    for x in range(12, 20):
        pixels[c_outline].append((x, 27))
    # Mug handle
    pixels[c_coffee].extend([(20, 22), (21, 23), (21, 24), (20, 25)])
    pixels[c_outline].extend([(21, 22), (22, 23), (22, 24), (21, 25)])
    # Steam
    pixels[c_steam].extend([(14, 19), (15, 18), (17, 19), (18, 18)])

    # Tiny gold star badge on sweater
    pixels[c_star].extend([(9, 21), (10, 20), (10, 21), (10, 22), (11, 21)])

    return create_pixel_svg(w, h, p, pixels)

# 4. Scenery: Pixel Art Pine Trees & Shoreline Banner (Inspiration image vibe)
def generate_pixel_scenery():
    # Width 800, Height 220
    # Soft sage background, layered pixel pine trees, quiet pond, pier with little fishing rod
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 240" width="100%" height="240" preserveAspectRatio="xMidYMax slice" shape-rendering="crispEdges">
    <!-- Sky background / soft mist -->
    <rect width="900" height="240" fill="#d2e3dc" />
    
    <!-- Floating pastel pixel clouds -->
    <g fill="#EAF3EE" opacity="0.85">
        <!-- Cloud 1 -->
        <rect x="60" y="30" width="120" height="24" rx="4" />
        <rect x="80" y="18" width="80" height="20" rx="4" />
        <rect x="100" y="10" width="40" height="15" rx="3" />
        
        <!-- Cloud 2 center -->
        <rect x="380" y="45" width="160" height="30" rx="4" />
        <rect x="420" y="30" width="90" height="25" rx="4" />
        <rect x="450" y="20" width="45" height="18" rx="3" />
        
        <!-- Cloud 3 right -->
        <rect x="700" y="25" width="140" height="26" rx="4" />
        <rect x="730" y="14" width="70" height="22" rx="4" />
    </g>

    <!-- Distant mountains / tree silhouettes -->
    <g fill="#b5cec3" opacity="0.6">
        <polygon points="40,160 90,80 140,160" />
        <polygon points="110,160 160,95 210,160" />
        <polygon points="260,160 320,110 380,160" />
        <polygon points="620,160 680,90 740,160" />
        <polygon points="720,160 780,75 840,160" />
        <polygon points="800,160 850,105 900,160" />
    </g>

    <!-- Lake / Water base -->
    <rect x="0" y="178" width="900" height="62" fill="#7ba89f" />
    <rect x="0" y="178" width="900" height="4" fill="#658e85" />
    
    <!-- Water ripples (subtle pixel reflections) -->
    <g fill="#a2c7bf">
        <rect x="40" y="186" width="35" height="2" />
        <rect x="120" y="194" width="50" height="2" />
        <rect x="220" y="188" width="40" height="2" />
        <rect x="310" y="202" width="65" height="2" />
        <rect x="430" y="185" width="30" height="2" />
        <rect x="490" y="196" width="55" height="2" />
        <rect x="620" y="189" width="45" height="2" />
        <rect x="740" y="200" width="70" height="2" />
        <rect x="830" y="186" width="35" height="2" />
        
        <rect x="80" y="214" width="60" height="2" />
        <rect x="260" y="222" width="45" height="2" />
        <rect x="520" y="218" width="80" height="2" />
        <rect x="690" y="224" width="50" height="2" />
    </g>

    <!-- Left Island / Ground bank -->
    <!-- Dirt / brick retaining wall -->
    <rect x="30" y="166" width="340" height="12" fill="#936d59" />
    <rect x="30" y="174" width="340" height="4" fill="#6d4c3d" />
    <!-- Lush grass top -->
    <rect x="25" y="160" width="350" height="6" fill="#4d7260" />
    <rect x="25" y="163" width="350" height="3" fill="#395849" />

    <!-- Left Group of Pixel Pine Trees -->
    <!-- Tree 1 Large -->
    <g transform="translate(60, 35)">
        <!-- Trunk -->
        <rect x="44" y="90" width="12" height="35" fill="#5c3d2e" />
        <!-- Foliage layers (dark to light) -->
        <!-- Layer 1 (base) -->
        <polygon points="0,110 50,40 100,110" fill="#3b594b" />
        <polygon points="10,110 50,40 90,110" fill="#4d7260" />
        <!-- Layer 2 (mid) -->
        <polygon points="15,85 50,25 85,85" fill="#58816e" />
        <polygon points="25,85 50,25 75,85" fill="#6a9682" />
        <!-- Layer 3 (top) -->
        <polygon points="30,55 50,10 70,55" fill="#7fa895" />
        <polygon points="38,55 50,10 62,55" fill="#96bcaa" />
    </g>

    <!-- Tree 2 Medium Left -->
    <g transform="translate(140, 55)">
        <rect x="35" y="80" width="10" height="26" fill="#5c3d2e" />
        <polygon points="0,90 40,30 80,90" fill="#3b594b" />
        <polygon points="10,90 40,30 70,90" fill="#4d7260" />
        <polygon points="15,68 40,18 65,68" fill="#58816e" />
        <polygon points="25,44 40,8 55,44" fill="#7fa895" />
    </g>

    <!-- Tree 3 Small -->
    <g transform="translate(210, 75)">
        <rect x="26" y="65" width="8" height="20" fill="#5c3d2e" />
        <polygon points="0,75 30,25 60,75" fill="#3b594b" />
        <polygon points="8,75 30,25 52,75" fill="#4d7260" />
        <polygon points="12,55 30,15 48,55" fill="#6a9682" />
        <polygon points="18,36 30,5 42,36" fill="#96bcaa" />
    </g>

    <!-- Wooden Pier on Left Island -->
    <rect x="290" y="162" width="65" height="6" fill="#a47551" />
    <rect x="290" y="168" width="65" height="2" fill="#744e33" />
    <!-- Pier pilings in water -->
    <rect x="300" y="168" width="6" height="20" fill="#5c3d2e" />
    <rect x="345" y="168" width="6" height="20" fill="#5c3d2e" />

    <!-- Cute Pixel Mascot sitting on pier with fishing line -->
    <g transform="translate(315, 140)">
        <!-- Cozy Cat Silhouette / Bunny sitting -->
        <!-- White body/ears -->
        <rect x="4" y="2" width="3" height="8" fill="#ffffff" />
        <rect x="9" y="2" width="3" height="8" fill="#ffffff" />
        <rect x="3" y="8" width="10" height="9" fill="#ffffff" />
        <!-- Red sweater -->
        <rect x="1" y="15" width="14" height="10" fill="#e07a5f" />
        <!-- Fishing rod (bamboo pole) -->
        <line x1="12" y1="18" x2="36" y2="4" stroke="#5c3d2e" stroke-width="2" />
        <!-- Fishing line down into water -->
        <line x1="36" y1="4" x2="36" y2="44" stroke="#2F3E46" stroke-width="1" stroke-dasharray="2,2" />
        <!-- Red/white bobber float -->
        <circle cx="36" cy="42" r="3" fill="#e76f51" />
        <circle cx="36" cy="40" r="1.5" fill="#ffffff" />
    </g>

    <!-- Right Island / Ground bank -->
    <rect x="520" y="166" width="350" height="12" fill="#936d59" />
    <rect x="520" y="174" width="350" height="4" fill="#6d4c3d" />
    <rect x="515" y="160" width="360" height="6" fill="#4d7260" />
    <rect x="515" y="163" width="360" height="3" fill="#395849" />

    <!-- Right Group of Pixel Pine Trees -->
    <g transform="translate(560, 65)">
        <rect x="30" y="75" width="9" height="20" fill="#5c3d2e" />
        <polygon points="0,80 35,20 70,80" fill="#3b594b" />
        <polygon points="8,80 35,20 62,80" fill="#4d7260" />
        <polygon points="12,58 35,12 58,58" fill="#6a9682" />
        <polygon points="20,38 35,4 50,38" fill="#96bcaa" />
    </g>

    <g transform="translate(635, 40)">
        <rect x="42" y="88" width="12" height="32" fill="#5c3d2e" />
        <polygon points="0,105 48,32 96,105" fill="#3b594b" />
        <polygon points="12,105 48,32 84,105" fill="#4d7260" />
        <polygon points="18,80 48,20 78,80" fill="#58816e" />
        <polygon points="28,52 48,8 68,52" fill="#7fa895" />
    </g>

    <g transform="translate(730, 48)">
        <rect x="38" y="82" width="10" height="30" fill="#5c3d2e" />
        <polygon points="0,96 44,25 88,96" fill="#3b594b" />
        <polygon points="10,96 44,25 78,96" fill="#4d7260" />
        <polygon points="16,72 44,15 72,72" fill="#6a9682" />
        <polygon points="26,46 44,6 62,46" fill="#96bcaa" />
    </g>

    <!-- Little cozy pixel flower on the right shore -->
    <g transform="translate(540, 150)">
        <rect x="4" y="6" width="2" height="6" fill="#2d6a4f" />
        <rect x="2" y="2" width="6" height="4" fill="#e07a5f" />
        <rect x="4" y="3" width="2" height="2" fill="#ffd166" />
    </g>
</svg>'''
    return svg

# 5. Badge: SOC 2 Compliant Star Badge
def generate_soc2_badge():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64" shape-rendering="crispEdges">
    <rect x="16" y="8" width="32" height="48" fill="#58816e" rx="6" />
    <rect x="20" y="12" width="24" height="40" fill="#faf8f5" rx="3" />
    <rect x="26" y="18" width="12" height="4" fill="#e07a5f" />
    <rect x="24" y="26" width="16" height="2" fill="#527a6c" />
    <rect x="24" y="32" width="16" height="2" fill="#527a6c" />
    <rect x="24" y="38" width="10" height="2" fill="#527a6c" />
    <circle cx="32" cy="46" r="6" fill="#e9c46a" />
    <rect x="30" y="44" width="4" height="4" fill="#2b4c3f" />
</svg>'''

# 6. Badge: Incident Commander Shield
def generate_incident_badge():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64" shape-rendering="crispEdges">
    <path d="M32 6 L52 14 L52 34 C52 46 42 56 32 60 C22 56 12 46 12 34 L12 14 Z" fill="#e07a5f" />
    <path d="M32 10 L48 16 L48 34 C48 43 40 52 32 55 C24 52 16 43 16 34 L16 16 Z" fill="#faf8f5" />
    <polygon points="32,20 35,27 42,28 37,33 39,40 32,36 25,40 27,33 22,28 29,27" fill="#e76f51" />
</svg>'''

# 7. Barnaby Detective / Glasses inspection
def generate_barnaby_detective():
    p = 4
    w, h = 32, 32
    c_fur = "#F4EBD9"
    c_ear_inner = "#F8B195"
    c_eyes = "#2E4057"
    c_glass = "#D9534F"
    c_nose = "#E76F51"
    c_sweater = "#3D5A80"   # Sleek investigator blue
    c_sweater_trim = "#98C1D9"
    c_hat = "#8D6E63"       # Tweed detective flat cap
    c_hat_band = "#4E342E"
    c_lens = "#A8DADC"      # Magnifying lens
    c_lens_rim = "#E9C46A"  # Brass frame
    c_outline = "#2F3E46"

    pixels = {
        c_outline: [], c_fur: [], c_ear_inner: [], c_eyes: [],
        c_glass: [], c_nose: [], c_sweater: [], c_sweater_trim: [],
        c_hat: [], c_hat_band: [], c_lens: [], c_lens_rim: []
    }

    # Detective Cap
    for x in range(6, 26):
        pixels[c_hat].append((x, 5))
        pixels[c_hat].append((x, 6))
    for x in range(8, 24):
        pixels[c_hat].append((x, 4))
        pixels[c_hat].append((x, 3))
    for x in range(5, 27):
        pixels[c_hat_band].append((x, 7))
    for x in range(4, 28):
        pixels[c_outline].append((x, 8)) # cap visor shadow

    # Head & cheeks
    for y in range(9, 17):
        pixels[c_outline].append((5, y))
        pixels[c_outline].append((26, y))
        for x in range(6, 26):
            pixels[c_fur].append((x, y))
    for x in range(7, 25):
        pixels[c_outline].append((x, 17))

    # Winking / Inspecting eyes
    # Left eye wide behind magnifying glass
    pixels[c_eyes].extend([(9, 11), (10, 11), (9, 12), (10, 12)])
    # Right eye squinted
    pixels[c_eyes].extend([(20, 11), (21, 11), (22, 12)])

    # Magnifying glass over left eye
    for x in range(7, 13):
        pixels[c_lens_rim].append((x, 9))
        pixels[c_lens_rim].append((x, 14))
    for y in range(10, 14):
        pixels[c_lens_rim].append((6, y))
        pixels[c_lens_rim].append((13, y))
    for y in range(10, 14):
        for x in range(7, 13):
            if (x, y) not in pixels[c_eyes]:
                pixels[c_lens].append((x, y))
    # Handle
    pixels[c_lens_rim].extend([(5, 15), (4, 16), (3, 17)])

    # Whiskers & nose
    pixels[c_nose].extend([(16, 13), (17, 13)])
    pixels[c_outline].extend([(16, 14), (17, 14), (15, 15), (18, 15)])
    for y in [13, 14]:
        pixels[c_outline].extend([(27, y), (28, y)])

    # Sweater
    for y in range(18, 29):
        pixels[c_outline].append((7, y))
        pixels[c_outline].append((24, y))
        for x in range(8, 24):
            pixels[c_sweater].append((x, y))
    for x in range(7, 25):
        pixels[c_outline].append((x, 29))
        pixels[c_sweater_trim].append((x, 28))

    return create_pixel_svg(w, h, p, pixels)

# Write files
with open("static/images/barnaby_neutral.svg", "w") as f:
    f.write(generate_barnaby_neutral())

with open("static/images/barnaby_alert.svg", "w") as f:
    f.write(generate_barnaby_alert())

with open("static/images/barnaby_happy.svg", "w") as f:
    f.write(generate_barnaby_happy())

with open("static/images/barnaby_detective.svg", "w") as f:
    f.write(generate_barnaby_detective())

with open("static/images/badge_soc2.svg", "w") as f:
    f.write(generate_soc2_badge())

with open("static/images/badge_incident.svg", "w") as f:
    f.write(generate_incident_badge())

with open("static/images/pixel_scenery.svg", "w") as f:
    f.write(generate_pixel_scenery())

print("SVG assets created successfully!")

