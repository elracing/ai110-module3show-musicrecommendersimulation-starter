# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

music Judge 

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

The recommender is meant to recommend music from a locally sourced list to listeners based on their trait preferences, using a scoring system to match users with songs that match their preferences. It is mostly a thought experiment, as the data is very small and it would need a much bigger data set to appropiately recommend songs to a person.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

each song is scored using a weighted system in this order: genre > mood > energy >, with some equally significant poitns added if the song has a matching tempo, danceability and is/is not acoustic. The user lists their preferences in each adn the model attempts to match the songs that more closely matches those preferences using ranks by scoring. 


---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

There are 18 songs in the data set right now, some songs were added afterwards to diversify the genres. The model does try to incorporate many genres, but these can be oddly specific or broad and will miss certain genres, hence some testing was done with phantom genres that caused mismatches. 

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

The system does work well when it does work. If your genre is well established in the list, it will actually match the preferences accordingly as long as the profile does to contain contradicting information, such as a preference over high energy metal music but low danceability witha  preference to acoustics. 

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

After some experimentation by removing the mood scoring from the model, the model over-relies on energy to match the users with songs. Mood served as a tie breaker and removing it meant that energy matched songs dominated the model. There were also some songs that consistently ranked very high due to this. 

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

Some of the surprises came from the adversarial profiles, specifically the the silent acoustic cotnradiction where low acoustic rated music that were "metal, ferocious" songs would be the first match, along with other similarly rated songs. 

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

A larger song list with a much more complete genre list would benefit this model greatly. The recommendations are explained clearly as they can be, but the most immediate improvement would simply be adding more genres and more diverse music as to not have profiles that rely exclusively on one trait for the music sicne none of the songs match all of the profile.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

I learned about the hybrid nature of recommender systems and how locally sourced data and community sourced data overall improves the recommendations given. I'm impressed with how popular systems handle edge cases and contradicting cases, something my own model cannot handle well. This has changed how I listen to music, as i'm now more aware that the system is constantly listening to my history in order to recommend me music. 
