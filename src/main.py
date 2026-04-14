"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import argparse
import os
from recommender import load_songs, recommend_songs


USER_PROFILES = {
    "High-Energy Pop": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.90,
        "tempo": 125,
        "danceability": 0.85,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.38,
        "tempo": 76,
        "danceability": 0.60,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.92,
        "tempo": 150,
        "danceability": 0.65,
        "likes_acoustic": False,
    },
}


def main(profile: str = None, adversarial_only: bool = False) -> None:
    csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")
    songs = load_songs(csv_path)

    if profile:
        if profile in USER_PROFILES:
            profiles_to_run = {profile: USER_PROFILES[profile]}
            adversarial = False
        elif profile in ADVERSARIAL_PROFILES:
            profiles_to_run = {}
            adversarial = True
            # run_adversarial filtered to just the named profile
            user_prefs = ADVERSARIAL_PROFILES[profile]
            print(f"\n{'='*50}")
            print(f"ADVERSARIAL: {profile}")
            print(f"{'='*50}")
            for song, score, explanation in recommend_songs(user_prefs, songs, k=5):
                acoustic_note = f"  [acousticness={song['acousticness']}]" if "likes_acoustic" in user_prefs else ""
                tempo_note = f"  [tempo={song['tempo_bpm']} BPM, distance={abs(song['tempo_bpm'] - user_prefs['tempo'])} BPM]" if "tempo" in user_prefs else ""
                print(f"{song['title']} ({song['genre']}, {song['mood']}) - Score: {score:.2f}")
                print(f"Because: {explanation}{acoustic_note}{tempo_note}")
                print()
            return
        else:
            all_names = list(USER_PROFILES) + list(ADVERSARIAL_PROFILES)
            print(f"Unknown profile '{profile}'. Available profiles:")
            for name in all_names:
                print(f"  {name}")
            return
    elif adversarial_only:
        profiles_to_run = {}
    else:
        profiles_to_run = USER_PROFILES

    for profile_name, user_prefs in profiles_to_run.items():
        print(f"\n{'='*50}")
        print(f"Profile: {profile_name}")
        print(f"{'='*50}")

        for song, score, explanation in recommend_songs(user_prefs, songs, k=5):
            print(f"{song['title']} - Score: {score:.2f}")
            print(f"Because: {explanation}")
            print()

    if adversarial_only or not profile:
        if not adversarial_only:
            print("\n\n*** ADVERSARIAL / EDGE CASE PROFILES ***")
        run_adversarial(songs)


ADVERSARIAL_PROFILES = {
    "Phantom Genre": {
        # 'classical' and 'zen' do not exist in the dataset.
        # Genre (+2.0) and mood (+1.0) bonuses can never fire.
        # Bug exposed: the entire ranking collapses to pure energy proximity,
        # so the top results have nothing to do with classical or zen.
        "genre": "classical",
        "mood": "zen",
        "energy": 0.50,
    },
    "Silent Acoustic Contradiction": {
        # Wants metal but also likes_acoustic=True.
        # Every metal song has acousticness 0.04–0.15, far below the 0.70 threshold.
        # Bug exposed: likes_acoustic silently contributes 0 points with no warning.
        # The preference is stated but completely ignored in scoring.
        "genre": "metal",
        "mood": "ferocious",
        "energy": 0.97,
        "tempo": 170,
        "likes_acoustic": True,
    },
    "Tempo Binary Cliff": {
        # tempo=121 puts Sunrise City (118 BPM, distance=3) just inside the ±10 window
        # and Gym Hero (132 BPM, distance=11) just outside — a 1 BPM difference at the
        # boundary flips the score by 0.5. Songs anywhere from 1–10 BPM away all earn
        # the same flat +0.5; there is no gradient reward for being closer.
        "genre": "pop",
        "mood": "happy",
        "energy": 0.90,
        "tempo": 121,
    },
}


def run_adversarial(songs: list) -> None:
    for profile_name, user_prefs in ADVERSARIAL_PROFILES.items():
        print(f"\n{'='*50}")
        print(f"ADVERSARIAL: {profile_name}")
        print(f"{'='*50}")

        recommendations = recommend_songs(user_prefs, songs, k=5)

        for song, score, explanation in recommendations:
            acoustic_note = f"  [acousticness={song['acousticness']}]" if "likes_acoustic" in user_prefs else ""
            tempo_note = f"  [tempo={song['tempo_bpm']} BPM, distance={abs(song['tempo_bpm'] - user_prefs['tempo'])} BPM]" if "tempo" in user_prefs else ""
            print(f"{song['title']} ({song['genre']}, {song['mood']}) - Score: {score:.2f}")
            print(f"Because: {explanation}{acoustic_note}{tempo_note}")
            print()


if __name__ == "__main__":
    all_profiles = list(USER_PROFILES.keys()) + list(ADVERSARIAL_PROFILES.keys())

    parser = argparse.ArgumentParser(description="Music Recommender Simulation")
    parser.add_argument(
        "--profile",
        metavar="NAME",
        help="Run a single profile by name (use quotes for names with spaces)",
    )
    parser.add_argument(
        "--adversarial",
        action="store_true",
        help="Run only the adversarial/edge-case profiles",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available profile names and exit",
    )
    args = parser.parse_args()

    if args.list:
        print("Normal profiles:")
        for name in USER_PROFILES:
            print(f"  {name}")
        print("Adversarial profiles:")
        for name in ADVERSARIAL_PROFILES:
            print(f"  {name}")
    else:
        main(profile=args.profile, adversarial_only=args.adversarial)
