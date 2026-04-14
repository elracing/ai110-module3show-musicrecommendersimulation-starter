from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

NUMERIC_FIELDS = ["energy", "tempo_bpm", "valence", "danceability", "acousticness"]

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_tempo: Optional[float] = None
    target_danceability: Optional[float] = None

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored = [(song, self._score_song(user, song)) for song in self.songs]
        scored.sort(key=lambda item: item[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        components = self._score_components(user, song)
        parts = []

        if components["genre"] > 0:
            parts.append(f"genre match (+{components['genre']:.1f})")
        if components["mood"] > 0:
            parts.append(f"mood match (+{components['mood']:.1f})")
        if components["energy"] > 0:
            parts.append(f"energy closeness (+{components['energy']:.1f})")
        if components["tempo"] > 0:
            parts.append(f"tempo fit (+{components['tempo']:.1f})")
        if components["danceability"] > 0:
            parts.append(f"danceability fit (+{components['danceability']:.1f})")
        if components["acousticness"] > 0:
            parts.append(f"acoustic preference (+{components['acousticness']:.1f})")

        if not parts:
            return "No strong matches, but it is still a valid recommendation."
        return " + ".join(parts)

    def _score_song(self, user: UserProfile, song: Song) -> float:
        components = self._score_components(user, song)
        return sum(components.values())

    def _score_components(self, user: UserProfile, song: Song) -> Dict[str, float]:
        genre_score = 2.0 if song.genre == user.favorite_genre else 0.0
        mood_score = 1.0 if song.mood == user.favorite_mood else 0.0
        energy_score = 2.0 * max(0.0, 1.0 - abs(song.energy - user.target_energy))

        tempo_score = 0.0
        dance_score = 0.0
        acoustic_score = 0.0

        if user.target_tempo is not None and abs(song.tempo_bpm - user.target_tempo) <= 10:
            tempo_score = 0.5

        if user.target_danceability is not None and abs(song.danceability - user.target_danceability) <= 0.1:
            dance_score = 0.5

        if user.likes_acoustic and song.acousticness >= 0.7:
            acoustic_score = 0.5

        return {
            "genre": genre_score,
            "mood": mood_score,
            "energy": energy_score,
            "tempo": tempo_score,
            "danceability": dance_score,
            "acousticness": acoustic_score,
        }


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row = {**row}
            for field in NUMERIC_FIELDS:
                row[field] = float(row[field])
            row["id"] = int(row["id"])
            songs.append(row)
    return songs


def _energy_similarity(song_energy: float, target_energy: float) -> float:
    return 2.0 * max(0.0, 1.0 - abs(song_energy - target_energy))


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    def score(song: Dict) -> float:
        score_value = 0.0
        score_value += 2.0 if song["genre"] == user_prefs.get("genre") else 0.0
        score_value += 1.0 if song["mood"] == user_prefs.get("mood") else 0.0
        score_value += _energy_similarity(song["energy"], user_prefs.get("energy", 0.0))

        if "tempo" in user_prefs and abs(song["tempo_bpm"] - user_prefs["tempo"]) <= 10:
            score_value += 0.5

        if "danceability" in user_prefs and abs(song["danceability"] - user_prefs["danceability"]) <= 0.1:
            score_value += 0.5

        if user_prefs.get("likes_acoustic") and song["acousticness"] >= 0.7:
            score_value += 0.5

        return score_value

    def explain(song: Dict) -> str:
        parts = []
        if song["genre"] == user_prefs.get("genre"):
            parts.append("genre match (+2.0)")
        # if song["mood"] == user_prefs.get("mood"):
        #     parts.append("mood match (+1.0)")
        energy_bonus = _energy_similarity(song["energy"], user_prefs.get("energy", 0.0))
        if energy_bonus > 0:
            parts.append(f"energy closeness (+{energy_bonus:.1f})")
        if "tempo" in user_prefs and abs(song["tempo_bpm"] - user_prefs["tempo"]) <= 10:
            parts.append("tempo fit (+0.5)")
        if "danceability" in user_prefs and abs(song["danceability"] - user_prefs["danceability"]) <= 0.1:
            parts.append("danceability fit (+0.5)")
        if user_prefs.get("likes_acoustic") and song["acousticness"] >= 0.7:
            parts.append("acoustic preference (+0.5)")
        if not parts:
            return "No strong matches, but it is still a valid recommendation."
        return " + ".join(parts)

    scored = [(song, score(song), explain(song)) for song in songs]
    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
