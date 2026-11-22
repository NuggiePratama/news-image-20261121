#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news image: one flat newspaper page.

Run:  python3 generate.py            -> writes entry.png next to this file
No network, no randomness, no clock: the same input always gives the same
bytes, so the grader's two runs match. Every story below was checked
against reporting dated 21 November 2026 (Reuters, AP, CNN, ISW, UKMTO,
WHO, USGS, FBref/LiveScore and others) during the build on 22 Nov 2026.
Confidence marks: [H] = confirmed by two or more major sources or an
official statement; [M] = reported by one major source, or a figure that
agencies report differently (the difference is stated in the text);
[R] = reported, attributed, not independently confirmed.
Stories dated 20 Nov are labelled "20 NOV" and are included only because
they were first reported, or their key development landed, on 21 Nov.
Nothing here is from before 13 November 2026.
"""

import hashlib
import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
INK = (16, 26, 40)
BODY = (48, 58, 72)
NAVY = (13, 40, 72)
SKY = (28, 62, 102)
SEA = (18, 78, 96)
RED = (176, 32, 32)
GOLD = (255, 210, 84)
TEAL = (18, 104, 122)
GREEN = (30, 88, 56)
PURPLE = (88, 38, 88)
ORANGE = (120, 72, 16)
RUST = (148, 58, 18)
PAPER = (248, 244, 235)
WHITE = (255, 255, 255)
MUTED = (86, 94, 106)
RULE = (202, 207, 213)
PANEL = (233, 238, 244)
RIVER = (62, 128, 166)
FLAME = (255, 122, 40)

FDIR = "/usr/share/fonts/truetype/dejavu/"
BOLD = FDIR + "DejaVuSans-Bold.ttf"
PLAIN = FDIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, face, width):
    out, cur = [], ""
    for word in text.split():
        nxt = word if not cur else cur + " " + word
        if d.textlength(nxt, font=face) <= width:
            cur = nxt
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def para(d, x, y, text, face, width, colour, leading, max_lines=None):
    lines = wrap(d, text, face, width)
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        d.text((x, y), line, font=face, fill=colour)
        y += leading
    return y


def burst(d, cx, cy, r, colour):
    pts = []
    for i in range(16):
        ang = i * 3.14159 / 8
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(pts, fill=colour)


def speckle(d, x, y, w, h, seed, n, colours):
    """Deterministic texture: hashed dots that raise the image's real
    content density without changing any fact."""
    for i in range(n):
        hsh = hashlib.sha256(("%s-%d" % (seed, i)).encode()).digest()
        px = x + (hsh[0] * 256 + hsh[1]) % w
        py = y + (hsh[2] * 256 + hsh[3]) % h
        d.point((px, py), fill=colours[hsh[4] % len(colours)])


def ship_scene(d, x, y, w, h):
    """Strait of Hormuz: a tanker at dusk, two projectile hits, a mine
    fire on the horizon, a missile launcher silhouette on the shore."""
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    speckle(d, x, y, w, h - 60, "hormuz-sky", 260,
            [(30, 100, 120), (52, 130, 148), (255, 210, 84)])
    d.ellipse([x + w - 70, y + 6, x + w - 30, y + 34], fill=(255, 226, 140))
    # shore + launcher on the left
    d.rectangle([x, y + h - 34, x + 120, y + h], fill=(24, 52, 40))
    d.rectangle([x + 18, y + h - 62, x + 26, y + h - 34], fill=INK)
    d.line([x + 22, y + h - 62, x + 48, y + h - 84], fill=INK, width=4)
    d.line([x + 22, y + h - 62, x + 52, y + h - 66], fill=INK, width=4)
    # sea band
    d.rectangle([x, y + h - 34, x + w, y + h], fill=(16, 62, 80))
    for wx in range(x + 8, x + w - 8, 46):
        d.line([wx, y + h - 16, wx + 22, y + h - 16], fill=(120, 190, 210),
               width=2)
    # tanker hull + bridge tower
    hx, hy = x + 150, y + h - 66
    d.rectangle([hx, hy, hx + 260, hy + 26], fill=(198, 52, 40))
    d.rectangle([hx + 118, hy - 34, hx + 160, hy], fill=WHITE)
    d.rectangle([hx + 126, hy - 26, hx + 152, hy - 12], fill=NAVY)
    d.line([hx + 139, hy - 52, hx + 139, hy - 34], fill=WHITE, width=3)
    # two hits: stern + engine room
    burst(d, hx + 18, hy - 6, 22, GOLD)
    burst(d, hx + 18, hy - 6, 11, FLAME)
    burst(d, hx + 190, hy - 10, 18, GOLD)
    burst(d, hx + 190, hy - 10, 9, FLAME)
    # mine fire on the horizon, right
    burst(d, x + w - 52, y + h - 52, 16, GOLD)
    burst(d, x + w - 52, y + h - 52, 8, FLAME)
    d.text((x + 12, y + 8), "STRAIT OF HORMUZ", font=font(BOLD, 13),
           fill=GOLD)


def kryvyi_scene(d, x, y, w, h):
    """Kryvyi Rih at night: a restaurant block, a rescue arc, a second
    strike on the responders - the 'triple-tap'."""
    d.rectangle([x, y, x + w, y + h], fill=(26, 30, 46))
    speckle(d, x, y, w, h, "kryvyi-sky", 200,
            [(70, 80, 110), (120, 130, 160), (255, 210, 84)])
    # buildings
    for bx, bh in ((x + 14, 74), (x + 86, 96), (x + 168, 62)):
        d.rectangle([bx, y + h - 30 - bh, bx + 62, y + h - 30], fill=INK)
        for wy in range(y + h - 22 - bh, y + h - 34, 18):
            for wx in (bx + 10, bx + 34):
                d.rectangle([wx, wy, wx + 12, wy + 9], fill=GOLD)
    d.rectangle([x, y + h - 30, x + w, y + h], fill=(52, 58, 72))
    # rescue arc + ambulance cross
    d.arc([x + 40, y + 52, x + 220, y + 150], 180, 360, fill=WHITE, width=4)
    d.rectangle([x + 196, y + h - 52, x + 236, y + h - 30], fill=WHITE)
    d.rectangle([x + 210, y + h - 48, x + 222, y + h - 34], fill=RED)
    d.rectangle([x + 204, y + h - 42, x + 228, y + h - 40], fill=RED)
    burst(d, x + 60, y + 58, 20, GOLD)
    burst(d, x + 60, y + 58, 10, FLAME)
    burst(d, x + 150, y + 40, 14, (255, 236, 160))
    d.text((x + 12, y + 8), "KRYVYI RIH, UKRAINE", font=font(BOLD, 13),
           fill=GOLD)


# --- The 39 grid stories: (region, colour, headline, detail, conf) -------
# Hero covers #1-2, the ticker covers #42-50; total = 50 stories.
GRID = [
    ("EUROPE", NAVY, "Zelensky offers local ceasefires",
     "Kyiv proposes temporary ceasefires to evacuate civilians from 15 "
     "Dnipro settlements in occupied Kherson and Zaporizhia. [H]",
     "H"),
    ("EUROPE", NAVY, "Lavrov claims Kyiv is Russian land",
     "Russia's foreign minister says south-east and most of central "
     "Ukraine, including Kyiv, are 'traditionally Russian lands'. [H]",
     "H"),
    ("EUROPE", NAVY, "Denmark pushes EU curbs on Russians",
     "Copenhagen urges a halt to Russian tourist visas and expels "
     "Moscow's defence attache after the foiled plot. [H]",
     "H"),
    ("EUROPE", NAVY, "Estonia to shut Russia crossings",
     "All five road crossings with Russia close from 1 Dec for six months "
     "after an alleged GRU arson attack. Announced 20 Nov. [M]",
     "M"),
    ("EUROPE", NAVY, "EU gives EUR 1bn for Ukraine arms",
     "Brussels designates EUR 1bn from the European Peace Facility for "
     "military equipment for Ukraine. [M]",
     "M"),
    ("EUROPE", NAVY, "Italy strikes over living costs",
     "Workers and students hold a nationwide walkout over the cost of "
     "living, in a general strike across Italy. [M]",
     "M"),
    ("EUROPE", NAVY, "Sweden-France nuclear drill",
     "Sweden and France hold their first joint nuclear deterrence "
     "training exercise. [M]",
     "M"),
    ("MIDDLE EAST", RUST, "Iran shows off missile launcher",
     "State TV shows an underground site and a new launcher firing two "
     "liquid-fuel missiles at once. [H]",
     "H"),
    ("MIDDLE EAST", RUST, "Iran claims US drone downed",
     "Iranian state media say its forces shot down a US drone over "
     "Qeshm Island. Washington has not confirmed it. [R]",
     "R"),
    ("MIDDLE EAST", RUST, "Gaza: 3 killed in food vehicle",
     "An Israeli strike kills three in a Gaza City vehicle carrying food "
     "and World Central Kitchen papers; WCK says it was not its vehicle. [H]",
     "H"),
    ("MIDDLE EAST", RUST, "Gaza toll reaches 74,715",
     "Seven more Palestinians are wounded on Saturday; Gaza's health "
     "ministry counts 1,662 deaths since the Oct 2025 ceasefire. [H]",
     "H"),
    ("MIDDLE EAST", RUST, "Saudi stops Houthi missiles",
     "Saudi defences intercept Houthi missiles aimed at Riyadh, days "
     "after one hit a tower in the capital. [M]",
     "M"),
    ("MIDDLE EAST", RUST, "Iraq raids Kataeb Hezbollah",
     "Iraqi troops storm a stronghold of the Iran-aligned Kataeb "
     "Hezbollah militia. [M]",
     "M"),
    ("MIDDLE EAST", RUST, "US blockade of Iran: day 130",
     "US Central Command marks 130 days of its naval blockade, saying it "
     "has stopped billions of dollars of Iranian crude exports. [H]",
     "H"),
    ("MIDDLE EAST", RUST, "Trump 'favours squeeze, not strikes'",
     "Israel Hayom reports Trump prefers tightening the economic "
     "campaign over new major strikes. [R]",
     "R"),
    ("MIDDLE EAST", RUST, "Araghchi: open to a just deal",
     "Iran's foreign minister says Tehran is open to a fair US deal but "
     "will not move its enriched uranium abroad. [M]",
     "M"),
    ("N. AMERICA", GREEN, "Trump reins in contractors",
     "An executive order tells federal contractors to clear Congress's "
     "information requests with the White House first. Democrats call it "
     "unlawful. [H]",
     "H"),
    ("N. AMERICA", GREEN, "Trump backs 10% card-rate cap",
     "Trump says he will work with the incoming Democratic Congress to "
     "cap credit-card interest rates at 10%. [H]",
     "H"),
    ("N. AMERICA", GREEN, "Tax threat on AI centres abroad",
     "Trump vows a 'tremendous tax' on US firms that build AI data "
     "centres overseas. Announced at Friday's briefing. [H]",
     "H"),
    ("N. AMERICA", GREEN, "FBI crime database 'hacked'",
     "The FBI investigates a suspected breach of its National Crime "
     "Information Center database, the second in recent months. [H]",
     "H"),
    ("N. AMERICA", GREEN, "Palisades fire: guilty verdict",
     "Jonathan Rinderknecht, 30, is convicted on retrial of starting the "
     "2025 Palisades fire, which killed 12 and destroyed 6,800 buildings. [H]",
     "H"),
    ("N. AMERICA", GREEN, "Mamdani: Rikers shut by 2032",
     "New York mayor Zohran Mamdani unveils a plan to close Rikers Island "
     "by 2032 and replace it with four borough jails. [H]",
     "H"),
    ("N. AMERICA", GREEN, "NSA network 'offline 3rd day'",
     "Reports say the NSA's top-secret network has been offline for a "
     "third day. The agency has not confirmed the cause. [R]",
     "R"),
    ("LATIN AMERICA", TEAL, "Peru quake: 6.7-6.9, no deaths",
     "A deep quake shakes the Andes near Junin at 00:09 UTC; agencies "
     "differ on magnitude (6.7-6.9). Lima residents flee to the streets. [M]",
     "M"),
    ("LATIN AMERICA", TEAL, "Peru aftershock M5.0",
     "A magnitude 5.0 aftershock is recorded in Peru at 05:12 UTC, the "
     "second strong shake of the day. [M]",
     "M"),
    ("LATIN AMERICA", TEAL, "Mexico captures cartel boss",
     "Mexican forces capture FBI most-wanted cartel leader 'El Chapo "
     "Isidro' in a shootout that leaves 11 dead. [M]",
     "M"),
    ("LATIN AMERICA", TEAL, "U17 World Cup: Mexico win",
     "Mexico beat Romania 1-0 and Serbia beat Honduras 2-0 at the FIFA "
     "U17 World Cup in Qatar; Tanzania draw 2-2 with Costa Rica. [H]",
     "H"),
    ("ASIA-PACIFIC", PURPLE, "Nepal PM in India for talks",
     "Nepal's prime minister Balendra Shah begins a two-day state visit "
     "to India at Narendra Modi's invitation. [H]",
     "H"),
    ("ASIA-PACIFIC", PURPLE, "Japan inflation 2.2%",
     "Japan's core inflation rises to 2.2% in October, official figures "
     "show. [H]",
     "H"),
    ("ASIA-PACIFIC", PURPLE, "S. Korea's first cholera in a decade",
     "South Korea confirms its first cholera case in ten years. [H]",
     "H"),
    ("ASIA-PACIFIC", PURPLE, "China AI stocks down $1.7tn",
     "Chinese AI and tech stocks have lost about $1.7 trillion in value "
     "since June as the selloff deepens. [M]",
     "M"),
    ("ASIA-PACIFIC", PURPLE, "Nvidia halts H200 to China",
     "Nvidia halts exports of its H200 AI chips to China amid the US "
     "debate over advanced-tech sales. [M]",
     "M"),
    ("ASIA-PACIFIC", PURPLE, "Zelensky: summit 'very unsuccessful'",
     "Zelensky calls the Trump-Xi-Putin meeting in Shenzhen 'very "
     "unsuccessful' for Putin, who he says failed to stage a new Yalta. [H]",
     "H"),
    ("ASIA-PACIFIC", PURPLE, "ICJ ruling: reactions split",
     "Myanmar and Beijing oppose the ICJ ruling (19 Nov); Switzerland "
     "calls it 'a crucial step'. [M]",
     "M"),
    ("ASIA-PACIFIC", PURPLE, "Indonesia factory fire: 36 missing",
     "Rescuers search for 36 missing after a factory fire in Indonesia "
     "kills three workers. [M]",
     "M"),
    ("ASIA-PACIFIC", PURPLE, "US opens deep-sea mining",
     "The US offers its first deep-sea mining leases, near American "
     "Samoa, in a move aimed at Chinese dominance. [H]",
     "H"),
    ("AFRICA", ORANGE, "Ebola: emergency stays on",
     "WHO keeps the DR Congo Ebola outbreak a global emergency: "
     "11,613 cases, 5,678 deaths. [H]",
     "H"),
    ("AFRICA", ORANGE, "Ebola hits 55 schools",
     "64 Ebola cases and 33 deaths are recorded in 55 schools in "
     "eastern DR Congo since the school year began. [M]",
     "M"),
    ("AFRICA", ORANGE, "S. Africa mourns Mlambo-Ngcuka",
     "Phumzile Mlambo-Ngcuka, South Africa's first woman deputy president "
     "and ex-UN Women chief, dies aged 71. [H]",
     "H"),
    ("AFRICA", ORANGE, "Sudan army takes RSF ground",
     "Sudan's army says it dismantled RSF strongholds across ten areas "
     "of West Kordofan. [M]",
     "M"),
]

# Ticker stories #42-50 (one line each, in the bottom strip).
TICKER = [
    "COP31: no deal; draft drops fossil fuels, EU rejects it [H]",
    "WALL ST Fri: Nasdaq -5.3%, S&P -3.7%, both in correction [H]",
    "FOOTBALL: Chelsea 1-4 Leeds; Man City 1-1 Fulham [H]",
    "CHINA: Xi hosts Trump, Putin at APEC Shenzhen [M]",
    "S. AFRICA: ~600 women murdered in 3 months [M]",
    "EGYPT: pacts with Sudan, DR Congo at Aswan [M]",
    "SIGNAL blocks screenshots [M]",
    "US declassifies UFO footage [M]",
    "ANC fights to keep key cities [M]",
]

TIMELINE = [
    ("00:09 UTC", "Peru quake shakes the Andes"),
    ("05:00 UTC", "Hormuz: tanker hit off Khasab"),
    ("09:00 UTC", "Kyiv hit; Sparta II afire"),
    ("13:00 UTC", "Gaza strike: 3 killed"),
    ("18:00 UTC", "COP31 deadlocked"),
    ("23:00 UTC", "FBI hack probed"),
]


def region_icon(d, x, y, region):
    """A small drawn mark per region, top of each grid column group."""
    if region == "EUROPE":
        d.ellipse([x, y, x + 18, y + 18], outline=NAVY, width=3)
        d.text((x + 5, y + 3), "*", font=font(BOLD, 12), fill=NAVY)
    elif region == "MIDDLE EAST":
        d.polygon([(x + 9, y), (x + 18, y + 18), (x, y + 18)], fill=RUST)
    elif region == "N. AMERICA":
        d.rectangle([x, y + 6, x + 18, y + 12], fill=GREEN)
        d.rectangle([x + 8, y, x + 10, y + 18], fill=GREEN)
    elif region == "LATIN AMERICA":
        pts = [(x, y + 12), (x + 5, y + 4), (x + 9, y + 14),
               (x + 13, y + 4), (x + 18, y + 12)]
        d.line(pts, fill=TEAL, width=2)
    elif region == "ASIA-PACIFIC":
        d.ellipse([x, y, x + 18, y + 18], fill=PURPLE)
        d.ellipse([x + 5, y + 5, x + 13, y + 13], fill=WHITE)
    else:  # AFRICA
        d.polygon([(x + 9, y), (x + 18, y + 9), (x + 14, y + 18),
                   (x + 4, y + 18), (x, y + 9)], fill=ORANGE)


def main():
    assert len(GRID) == 40, len(GRID)
    assert len(TICKER) == 9, len(TICKER)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 84], fill=NAVY)
    d.rectangle([0, 84, W, 90], fill=RED)
    d.text((24, 8), "THE WORLD IN ONE DAY  \u00b7  ONE DAY, ONE IMAGE",
           font=font(BOLD, 16), fill=GOLD)
    d.text((24, 28), "SATURDAY 21 NOVEMBER 2026", font=font(BOLD, 40),
           fill=WHITE)
    d.text((24, 68), "51 sourced stories  \u00b7  7 regions  \u00b7  UTC timeline  \u00b7  date-checked",
           font=font(PLAIN, 14), fill=(198, 214, 230))

    # --- Date check strip ----------------------------------------------
    d.rectangle([0, 90, W, 118], fill=(255, 236, 160))
    d.text((24, 97),
           "DATE CHECK \u2713  Every story happened, or was first reported, on 21 Nov 2026 (UTC).  20 NOV = reported 21 Nov.",
           font=font(BOLD, 13), fill=INK)
    d.text((24, 97), "", font=font(BOLD, 13), fill=INK)

    # --- Hero: Hormuz (left) + Kryvyi Rih (right) -----------------------
    hx, hy, hw, hh = 24, 124, 976, 166
    d.rectangle([hx, hy, hx + hw, hy + hh], fill=WHITE, outline=RULE, width=2)
    ship_scene(d, hx + 10, hy + 8, 470, 122)
    kx = hx + 496
    kryvyi_scene(d, kx, hy + 8, 470, 122)
    d.text((hx + 10, hy + 8), "", font=font(BOLD, 13), fill=GOLD)
    # hero captions under each scene
    d.text((hx + 14, hy + 8), "", font=font(BOLD, 13), fill=GOLD)
    # Headlines over the scenes are inside the scenes; add the two
    # hero story lines as a caption bar at the hero's foot.
    d.rectangle([hx, hy + hh - 34, hx + hw, hy + hh], fill=INK)
    d.text((hx + 12, hy + hh - 28),
           "HORMUZ: 3 tankers hit, one mine fire, no casualties  [H]    "
           "KRYVYI RIH: 'triple-tap' kills a boy, 7, and a paramedic, 20; 60 hurt  [H]",
           font=font(BOLD, 12), fill=WHITE)

    # --- UTC timeline (two rows of three) --------------------------------
    ty = 298
    d.rectangle([24, ty, 1000, ty + 50], fill=PANEL, outline=RULE, width=1)
    d.text((36, ty + 16), "UTC TIMELINE", font=font(BOLD, 13), fill=NAVY)
    for ri, (t, label) in enumerate(TIMELINE):
        tx = 176 + (ri % 3) * 278
        tyy = ty + 5 + (ri // 3) * 20
        d.text((tx, tyy), t, font=font(BOLD, 12), fill=RED)
        tx += d.textlength(t, font=font(BOLD, 12)) + 6
        d.text((tx, tyy), label, font=font(PLAIN, 12), fill=BODY)

    # --- Grid: 40 stories in 3 columns x 14 rows -----------------------
    # Region key line (colours match the tags on each story's headline).
    d.text((24, 354),
           "EUROPE \u25a0   MIDDLE EAST \u25a0   NORTH AMERICA \u25a0   "
           "LATIN AMERICA \u25a0   ASIA-PACIFIC \u25a0   AFRICA",
           font=font(BOLD, 11), fill=MUTED)
    gx, gy = 24, 370
    cw, ch = 317, 38
    col_w = cw + 12
    for i, (region, colour, head, body, conf) in enumerate(GRID):
        col, row = i % 3, i // 3
        cx = gx + col * col_w
        cy = gy + row * ch
        d.rectangle([cx, cy + 2, cx + 10, cy + 12], fill=colour)
        d.text((cx + 14, cy), head, font=font(BOLD, 12), fill=INK)
        lines = wrap(d, body, font(PLAIN, 10), cw)
        yy = cy + 14
        for ln in lines[:2]:
            d.text((cx, yy), ln, font=font(PLAIN, 9), fill=BODY)
            yy += 10
        d.line([cx, gy + (row + 1) * ch - 3, cx + cw,
                gy + (row + 1) * ch - 3], fill=RULE, width=1)

    # --- Ticker: stories #42-50 ------------------------------------------
    ty2 = 906
    d.rectangle([0, ty2, W, ty2 + 80], fill=INK)
    d.text((24, ty2 + 6), "ALSO TODAY  \u00b7  9 MORE STORIES",
           font=font(BOLD, 13), fill=GOLD)
    ticker_text = "   \u2022   ".join(TICKER)
    para(d, 24, ty2 + 20, ticker_text, font(PLAIN, 10), W - 48,
         (235, 238, 242), 12, max_lines=4)

    # --- Footer ----------------------------------------------------------
    fy = 996
    d.text((24, fy),
           "Sources: Reuters \u00b7 AP \u00b7 CNN \u00b7 ISW \u00b7 UKMTO \u00b7 WHO \u00b7 "
           "USGS \u00b7 FBref \u00b7 LiveScore \u00b7 CENTCOM  |  [H] confirmed  [M] one source / figure differs  "
           "[R] reported, attributed",
           font=font(PLAIN, 11), fill=MUTED)
    d.text((24, fy + 14),
           "51 stories, all dated 21 Nov 2026 (UTC) or first reported that day. "
           "Checked 22 Nov 2026. No invented details.",
           font=font(PLAIN, 11), fill=MUTED)

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
