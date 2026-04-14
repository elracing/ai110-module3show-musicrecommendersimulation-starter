# 🎵 Music Recommender Simulation

## Project Summary

I understand that modern real-world recommendations use a hybrid model of collaborative filtering and content-based filtering, bridging recommendations from people alike and songs alike. My algorithm, as I am a very instrumental person, will prioritize scores calculated from genre, mood, danceability and acousticness, weighted in that order. UserProfile will list preferences in these attributes as to make matching possible with the attributes given to a Song

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

the algorithm will involve the following: total = 0.4*genre_score + 0.3*mood_score + 0.18*dance_score + 0.12*acoustic_score

here is the mermaid.JS flowchart:

flowchart TD
    A["User Prefs (genre, mood, energy, tempo, danceability, acousticness)"] --> B["Load songs.csv"]
    B --> C["For each song"]
    C --> D["Compare genre"]
    C --> E["Compare mood"]
    C --> F["Compute energy similarity"]
    C --> G["Apply tie-breakers (tempo, danceability, acousticness)"]
    D --> H["Add genre points (+2.0 if match)"]
    E --> I["Add mood points (+1.0 if match)"]
    F --> J["Add energy score (2.0 * max(0, 1 - abs(song_energy - target_energy)))"]
    G --> K["Add bonus points (+0.5 each when matched)"]
    H --> L["Total score for song"]
    I --> L
    J --> L
    K --> L
    L --> M["Collect scored songs"]
    M --> N["Sort by score descending"]
    N --> O["Output top K recommendations"]


for a visual, look for ![
](<Song Recommendation Scoring-2026-04-13-142603.png>)


The song scoring algorithm will look like this:

Genre match: +2.0
Mood match: +1.0
Energy similarity: up to +2.0 using:
energy_score = 2.0 * max(0, 1 - abs(song_energy - target_energy))
Optional tie-breakers:
Tempo within ±10 bpm of target: +0.5
Danceability near target or user preference: +0.5
Acousticness match for mellow user intent: +0.5

This will definitely be more biased towards the categories of the music, rather than the individual traits of such.

this is an example of the cli output:

![alt text](image.png)



---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

