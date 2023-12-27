from flask import Flask, render_template, request, flash
from flask_bootstrap import Bootstrap
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'be3f708d4e087cd44d801a2c878c8a78' 
bootstrap = Bootstrap(app)

class WordSearchGame:
    def __init__(self):
        self.grid_size = 12
        self.all_words = self.get_word_lists()
        self.word_search_grid = self.create_word_search(self.grid_size, self.all_words)
        self.correct_guesses = []
        self.incorrect_attempts = 0

    def get_word_lists(self):
        kenya_words = ['MUZE', 'CAMPING', 'HIKING', 'RAIN', 'ZIPLINING', 'BOARDGAMES', 'BIRTHDAY', 'PUSSINBOOTS',
                       'LAMB', 'GRINCH', 'ABERDARES', 'NAIROBI', 'SAMAWATI', 'DRAGONSTEETH', 'CHAPATI']

        countries_words = ['TANZANIA', 'GHANA', 'ZANZIBAR', 'RWANDA', 'UGANDA', 'TOGO', 'IVORYCOAST']

        all_words = kenya_words + countries_words
        random.shuffle(all_words)
        return all_words

    def create_word_search(self, grid_size, words):
        grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]

        for word in words:
            direction = random.choice(['horizontal', 'vertical', 'diagonal'])
            if direction == 'horizontal':
                row = random.randint(0, grid_size - 1)
                col = random.randint(0, grid_size - len(word))
                for i in range(len(word)):
                    grid[row][col + i] = word[i]
            elif direction == 'vertical':
                row = random.randint(0, grid_size - len(word))
                col = random.randint(0, grid_size - 1)
                for i in range(len(word)):
                    grid[row + i][col] = word[i]
            elif direction == 'diagonal':
                row = random.randint(0, grid_size - len(word))
                col = random.randint(0, grid_size - len(word))
                for i in range(len(word)):
                    grid[row + i][col + i] = word[i]

        for i in range(grid_size):
            for j in range(grid_size):
                if grid[i][j] == ' ':
                    grid[i][j] = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

        return grid

    def get_hint(self, word):
        hints = {
            'MUZE': "Brain feeling fried? Let's refuel with a memory of our laughter and dancing at a club in Nairobi!",
            'CAMPING': "Remember the nights under the stars and the warmth of the fire.",
            'HIKING': "Think of the beautiful trails and the breathtaking views.",
            'RAIN': "Ah, the weather didn't always agree with us during this outdoor adventure!",
            'ZIPLINING': "Recall the thrill of soaring through the trees with the wind in our hair.",
            'BOARDGAMES': "Fun nights filled with laughter and friendly competition!",
            'BIRTHDAY': "A special celebration for someone very dear to my heart.",
            'PUSSINBOOTS': "Stuck? Time for a Puss in Boots power nap!",
            'LAMB': "A cute little creature often seen in the countryside. But you found out its name recently.",
            'GRINCH': "Playfully named after a character we found amusing and gave it to Oscar.",
            'ABERDARES': "Our camping adventure with unexpected encounters with wildlife, waterfalls, and deers everywhere!",
            'NAIROBI': "The vibrant city where we explored the nightlife.",
            'SAMAWATI': "A lodge where we celebrated a special birthday.",
            'DRAGONSTEETH': "Hiking to discover mystical rock formations on a special occasion.",
            'CHAPATI': "Our delicious cooking experiment with local African dishes which you can find also in Tanzania. But no other places.",
            'TANZANIA': "A country you explored with its rich culture and landscapes.",
            'GHANA': "Vibrant and full of history, you were there for a year 5 or four years ago.",
            'ZANZIBAR': "An exotic island with beautiful beaches and spice plantations.",
            'RWANDA': "A country known for its scenic beauty and gorilla trekking.",
            'UGANDA': "Your adventure in the 'Pearl of Africa.' Very close to Kenya and ends with an A.",
            'TOGO': "Remember the unique culture and friendly people of a French-speaking country in West Africa where you struggled a bit.",
            'IVORYCOAST': "A country with diverse landscapes and cultural richness where you met two friends from Germany."
        }
        return hints.get(word, "Hint not available.")

word_search_game = WordSearchGame()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        guess = request.form['guess'].upper()
        if guess in word_search_game.all_words and guess not in word_search_game.correct_guesses:
            flash(f"Correct! {guess} is a match. {get_random_encouragement()} 😊🎉")
            word_search_game.correct_guesses.append(guess)
            if len(word_search_game.correct_guesses) == len(word_search_game.all_words):
                flash("Congratulations! You found all the words! Love you 🎉✨")
        else:
            word_search_game.incorrect_attempts += 1
            flash(f"Sorry, {guess} is not a match. {get_random_motivation()} {get_random_emoji()}")

            # Provide a hint after three incorrect attempts
            if word_search_game.incorrect_attempts % 3 == 0:
                hint_word = random.choice(word_search_game.all_words)
                hint = word_search_game.get_hint(hint_word)
                flash(f"Need a little help Paula? Here's a hint: '{hint}' {get_random_emoji()}")

    return render_template('index.html', grid=word_search_game.word_search_grid, correct_guesses=word_search_game.correct_guesses)

def get_random_emoji():
    emojis = ['😅', '🤔', '😕', '😩', '🙈', '💔']
    return random.choice(emojis)

def get_random_encouragement():
    encouraging_words = [
        "You're brilliant, keep puzzling!",
        "Your brainpower is incredible!",
        "Almost there, you've got this!",
        "Think like a Pinguen, conquer this puzzle!",
        "Every wrong turn leads closer to the right one!",
        "A sweet memory indeed"
    ]
    return random.choice(encouraging_words)

def get_random_motivation():
    motivation_messages = [
        "Don't give up! You're getting warmer!",
        "Mistakes are proof that you're trying!",
        "Failure is the opportunity to begin again more intelligently.",
        "Every master was once a beginner. Keep going!",
        "You're not alone on this journey. I believe in you!",
        "Success is not final, failure is not fatal: It is the courage to continue that counts."
    ]
    return random.choice(motivation_messages)

if __name__ == '__main__':
    app.run(debug=True)
