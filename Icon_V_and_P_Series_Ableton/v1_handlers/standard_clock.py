# === HELPERS ===
_MODE  = 'bars' # 'bars' | 'time'
_cache = ['\0'] * 10
def set_mode(m):  global _MODE; _MODE = m if m in ('bars','time') else _MODE
def toggle_mode(): global _MODE; _MODE = 'time' if _MODE == 'bars' else 'bars'
BLANK = lambda s: (' ' * (4 - len(s[:4].lstrip('0'))) + s[:4].lstrip('0')) + s[4:] # blank leading zeros only in BAR field (first 4 chars)

def FORMAT_BARS(song) -> str:
    p = str(song.get_current_beats_song_time()).split(':')
    b, bt, sb = (int(p[i]) if i < len(p) and p[i].isdigit() else 0 for i in range(3))
    return f"{str(b).rjust(4)}:{str(bt).rjust(2)}:{str(sb).rjust(2)}"[:10]

def FORMAT_TIME(DM, payload) -> str:
    hh, mm, ss, ff = (int(x) for x in str(DM.SMPTE_25(payload)).replace(';', ':').split(':')[:4])
    cs   = int(round(ff * (100.0 / 25.0)))   # frames → centiseconds @25fps
    mins = hh * 60 + mm
    return f"{str(mins).rjust(4)}:{ss:02d}:{cs:02d}"[:10]

# === REFRESH: DAW → HARDWARE
def refresh(payload):
    # PAYLOAD IMPORTS
    DM = payload["daw_map"]
    AD = payload["addr"]

    # CALCULATIONS
    TEXT = FORMAT_TIME(DM, payload) if _MODE == 'time' else BLANK(FORMAT_BARS(DM.SONG(payload)))
    msg = (TEXT or "").ljust(10)[:10]

    # SEND: DAW → HARDWARE
    for i, ch in enumerate(msg):
        if _cache[i] != ch:
            DM.SEND_DAW(payload, (0xB0, AD.CLOCK_DISPLAY[i], ord(ch) & 0x7F))
            _cache[i] = ch

# ONIDLE CONTROL
tick = refresh

# === RESET: DAW → HARDWARE
def reset(payload):
    # PAYLOAD IMPORTS
    DM = payload["daw_map"]
    AD = payload["addr"]
    for i, cc in enumerate(AD.CLOCK_DISPLAY): # expects 10 addrs (0x49..0x40)
        DM.SEND_DAW(payload, (0xB0, cc, ord(' ') & 0x7F))
