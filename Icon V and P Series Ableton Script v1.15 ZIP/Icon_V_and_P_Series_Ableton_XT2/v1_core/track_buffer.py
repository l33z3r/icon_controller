# === IMPORTS ===
from ..v1_core import switch_manager as SW

# === DEFINE HARDWARE TRACK ===
class HardwareTrack:
    def __init__(self, live_track, index):
        self.live_track = live_track  # DAW object or None
        self.TrackNum = index         # Hardware CH number

# === SHARED TRACK BUFFER FOR ABLETON ===
class TrackBuffer:
    def __init__(self, ctrl_surface=None):
        self.ctrl_surface = ctrl_surface
        self.first_track = 0
        self.visible_slots = 8
        self.track_count = 0
        self.min_track = 0

    def get_current_tracks(self):
        try:
            if not self.ctrl_surface:
                return []

            song = self.ctrl_surface.song()
            use_returns = SW.get("return_tracks")
            all_tracks = (
                list(song.return_tracks)
                if use_returns else
                list(song.visible_tracks)
            )
            self.track_count = len(all_tracks)

            tracks = []
            for i in range(self.visible_slots):
                index = self.first_track + i
                live_track = all_tracks[index] if index < self.track_count else None
                tracks.append(HardwareTrack(live_track, index))

            return tracks

        except:
            return []

    def bank(self, amount):
        try:
            self.first_track = max(self.min_track, self.first_track + amount)
            return self.get_current_tracks()
        except:
            return []