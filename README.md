# Word Ninja 🥷🏼
Word Ninja is a simple but fun game to test your vocabulary knowledge in another language. The goal is to translate words correclty to release as many fish from the boxes before they reach the ocean to gain points.

### Install dependencies
```bash
pip3 install -r requirements.txt
```

### Start the game
You will need an API key to call out to the real-time engine for transcription. It's easy to generate one using the [Speechmatics Portal](https://portal.speechmatics.com/). 
```bash
export API_KEY=<your api key>
python3 -m gui.run_with_menu
```
