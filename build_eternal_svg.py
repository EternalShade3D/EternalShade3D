import re, xml.dom.minidom as M

DARK_LOGO = r"C:\Users\Eternal\github_preview\eternal3d\assets_logo_neg.txt"
LIGHT_LOGO = r"C:\Users\Eternal\github_preview\eternal3d\assets_logo_normal.txt"

def load_logo(path):
    L=[l.rstrip('\n') for l in open(path).read().split('\n')]
    while L and L[0].strip()=='': L.pop(0)
    while L and L[-1].strip()=='': L.pop()
    return L

XK=390
DASH='—'*47
CANVAS_W=985
CANVAS_H=590

# EVERY line (content rows + title bars) = exactly TOTAL characters.
# Content row = '⟩ '(2) + label + ':' + ' '+dots+' ' + value  => dots = TOTAL-5-len(label)-len(value)
# Title bar   = dashes + ' ' + title + ' ' + dashes
TOTAL=61

def dots_for(label, val):
    just = TOTAL - 5 - len(label) - len(val)
    if just < 1: just = 1
    return ' ' + ('.'*just) + ' '

def field(y, label, val, dyn=None):
    vid=f' id="{dyn}"' if dyn else ''
    dots=f'<tspan class="cc" id="{dyn}_dots">{dots_for(label,val)}</tspan>' if dyn else f'<tspan class="cc">{dots_for(label,val)}</tspan>'
    return (f'<tspan x="{XK}" y="{y}" class="cc">⟩ </tspan>'
            f'<tspan class="key">{label}</tspan>:{dots}'
            f'<tspan class="value"{vid}>{val}</tspan>')

def empty(y):
    return f'<tspan x="{XK}" y="{y}" class="cc">⟩ </tspan>'

def section(y, title):
    td = TOTAL - 2 - len(title)      # total dash chars
    sl = td // 2
    sr = td - sl
    return f'<tspan x="{XK}" y="{y}">{"—"*sl} {title} {"—"*sr}</tspan>'

def sdots(n):
    if n < 1: n = 1
    return f'<tspan class="cc"> {"."*n} </tspan>'

# GitHub Stats LOC suffix (visible length drives the LOC dot count).
LOC_SUFFIX = ' ⟩ 73,877++ | 4,165--'
# Column where '(' sits on the LOC line == column where the '⟩' separators must sit
# on the two paired stat lines, so all three lines align vertically.
SEP_COL = TOTAL - len(LOC_SUFFIX) + 1

def stat2(y, L1, v1, L2, v2, bracket=None):
    btxt = f' [{bracket[0]}: {bracket[1]}]' if bracket else ''
    # separator '⟩' must sit at SEP_COL (== LOC '(' column). Fixed chars before it:
    # '⟩ '(2) + L1 + ':'(1) + sdots(d1) + v1 + btxt  => '⟩' col = 6 + L1 + d1 + v1 + btxt
    d1 = SEP_COL - 6 - len(L1) - len(v1) - len(btxt)
    # total width 61: d1 + d2 = 50 - (L1+v1+btxt+L2+v2)
    d2 = 50 - (len(L1)+len(v1)+len(btxt)+len(L2)+len(v2)) - d1
    if d1 < 1: d1 = 1
    if d2 < 1: d2 = 1
    return (f'<tspan x="{XK}" y="{y}" class="cc">⟩ </tspan>'
            f'<tspan class="key">{L1}</tspan>:{sdots(d1)}'
            f'<tspan class="value" id="{L1.lower()}_data">{v1}</tspan>'
            + (f' [<tspan class="key">{bracket[0]}</tspan>: <tspan class="value" id="{bracket[0].lower()}_data">{bracket[1]}</tspan>]' if bracket else '')
            + f'<tspan class="cc"> ⟩ </tspan><tspan class="key">{L2}</tspan>:{sdots(d2)}'
            f'<tspan class="cc" id="{L2.lower()}_data_dots"></tspan>'
            f'<tspan class="value" id="{L2.lower()}_data">{v2}</tspan>')

def stat_loc(y):
    L='Lines of Code on GitHub'; v='69,712'
    d = TOTAL - (2 + len(L) + 1 + 2 + len(v) + len(LOC_SUFFIX))
    if d < 1: d = 1
    return (f'<tspan x="{XK}" y="{y}" class="cc">⟩ </tspan>'
            f'<tspan class="key">{L}</tspan>:{sdots(d)}'
            f'<tspan class="cc" id="loc_data_dots"></tspan>'
            f'<tspan class="value" id="loc_data">{v}</tspan>'
            f'<tspan class="cc"> ⟩ </tspan>'
            f'<tspan class="addColor" id="loc_add">73,877</tspan><tspan class="addColor">++</tspan>'
            f'<tspan class="cc"> | </tspan>'
            f'<tspan class="delColor" id="loc_del">4,165</tspan><tspan class="delColor">--</tspan>')

# --- row by row, explicit (23 rows, ends y=510 to match reference) ---
rows = [
 section(30,'EternalShade3D'),
 field(50,'OS','Windows 11, Android'),
 field(70,'Uptime','8 years, 1 month, 2 days','age_data'),
 field(90,'Host','EternalShade3D'),
 field(110,'Kernel','10.0'),
 field(130,'Tools','Blender, ComfyUI, Sublime Text, VS Code'),
 empty(150),
 field(170,'Languages.Programming','Python, JavaScript'),
 field(190,'Languages.Markup','HTML, CSS, JSON'),
 field(210,'Interests.Creative','3D Modeling, Digital Visuals'),
 empty(230),
 field(250,'Interests.Tech','AI, Hermes Agent'),
 field(270,'Tools.Extra','AntiGravity, Hermes Agent'),
 section(310,'Contact'),
 field(330,'Instagram','@eternal.shade3d'),
 field(350,'TikTok','@eternal.shadeon'),
 field(370,'LinkedIn','marcio3drodrigues'),
 field(390,'Website','eternal3d.carrd.co'),
 field(410,'Email','eternalshadeon@gmail.com'),
 section(450,'GitHub Stats'),
 stat2(470,'Repos','14','Stars','3', bracket=('Contributed','16')),
 stat2(490,'Commits','76','Followers','0'),
 stat_loc(510),
]
panel = f'<text x="{XK}" y="30" fill="#c9d1d9">\n'+'\n'.join(rows)+'\n</text>'

specs=[
 (r"C:\Users\Eternal\github_preview\reference\dark_mode.svg", r"C:\Users\Eternal\github_preview\eternal3d\dark_mode.svg", DARK_LOGO),
 (r"C:\Users\Eternal\github_preview\reference\light_mode.svg", r"C:\Users\Eternal\github_preview\eternal3d\light_mode.svg", LIGHT_LOGO),
]
for src,dst,lg in specs:
    logo_lines=load_logo(lg)
    N=28
    pad=(N-len(logo_lines))//2
    if pad<0: pad=0; logo_lines=logo_lines[:N]
    full=['']*pad + logo_lines + ['']*(N-pad-len(logo_lines))
    logo_tspans='\n'.join(f'<tspan x="15" y="{30+i*20}">{l}</tspan>' for i,l in enumerate(full))
    logo=f'<text x="15" y="30" fill="#c9d1d9" class="ascii">\n{logo_tspans}\n</text>'
    t=open(src).read()
    t=re.sub(r'<text[^>]*class="ascii"[^>]*>.*?</text>', logo, t, count=1, flags=re.S)
    t=re.sub(r'<text x="390"[^>]*>.*?</text>', panel, t, count=1, flags=re.S)
    t=re.sub(r'width="\d+px" height="\d+px" font-size', f'width="{CANVAS_W}px" height="{CANVAS_H}px" font-size', t, count=1)
    t=re.sub(r'viewBox="[^"]*"', f'viewBox="0 0 {CANVAS_W} {CANVAS_H}"', t, count=1)
    t=re.sub(r'<rect width="\d+px" height="\d+px"', f'<rect width="{CANVAS_W}px" height="{CANVAS_H}px"', t, count=1)
    M.parseString(t)
    open(dst,'w').write(t)
    print("built+valid:",dst)

# ===== VERIFY: every visible line must be exactly TOTAL chars =====
print(f"\n=== WIDTH VERIFY (every line must be {TOTAL}) ===")
t=open(r"C:\Users\Eternal\github_preview\eternal3d\dark_mode.svg").read()
bad=0
# content rows
for m in re.finditer(r'class="key">([^<]+)</tspan>:<tspan class="cc"[^>]*>([^<]*)</tspan><tspan class="value"[^>]*>([^<]*)', t):
    label,dots,val=m.group(1),m.group(2),m.group(3)
    line='⟩ '+label+':'+dots+val
    w=len(line)
    if w!=TOTAL: bad+=1
    print(f'row  {label:24} dots={dots.count("."):2} width={w} {"OK" if w==TOTAL else "BAD"}')
# title bars
for m in re.finditer(r'x="390" y="\d+">([—\-\u2014]* [A-Za-z. ]+ [—\-\u2014]*)', t):
    line=m.group(1); w=len(line)
    if w!=TOTAL: bad+=1
    print(f'title {"":24} width={w} {"OK" if w==TOTAL else "BAD"} |{line}|')
print("BAD lines:",bad)
