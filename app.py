import streamlit as st
import random
from streamlit_lottie import st_lottie
import requests
import os
import json
# Hangman ASCII art dictionary
hangman_phases = {
    0: """
      +-------+
      |             |
                    |
                    |
                    |
                    |
    ==================
    """,
    1: """
      +-------+
      |             |
     😃        |
                    |
                    |
                    |
    ==================
    """,
    2: """
      +-------+
      |             |
     😶        |
      |             |
                    |
                    |
    ==================
    """,
    3: """
      +-------+
      |             |
     😟        |
     /|             |
                    |
                    |
    ==================
    """,
    4: """
      +-------+
      |             |
     😨        |
     /|\\           |
                    |
                    |
    ==================
    """,
    5: """
      +-------+
      |             |
     😩        |
     /|\\           |
     /              |
                    |
    ==================
    """,
    6: """
      +-------+
      |            |
     😱        |
     /|\\          |
     / \\          |
                   |
    ==================
    """,
 
}


if "reset_game" not in st.session_state:
    st.session_state.reset_game = False
if "counter" not in st.session_state:
    st.session_state.counter = 0
#Function to go to game page 
def go_to_gamepage():
    st.session_state.counter = 1
#Function to go to home page    
def go_to_homepage():
    st.session_state.counter = 0

# Function to reset the game
def reset_game():
    st.session_state.reset_game = True
  # Reset all session state variables
if st.session_state.reset_game:
  
    st.session_state.word = random.choice(['apple', 'banana', 'cherry', 'date', 'elderberry', 'fig', 'grape', 'honeydew', 'jackfruit', 'kiwi', 'lemon', 'mango', 'nectarine', 'orange', 'papaya', 'quince', 'raspberry', 'strawberry', 'tangerine', 'ugli', 'vanilla', 'watermelon', 'ximenia', 'yellow watermelon', 'zucchini']).lower()  
    st.session_state.display = ["_"] * len(st.session_state.word)
    st.session_state.wrong_guesses = 0
    st.session_state.guessed_letters = []
    st.session_state.input_value = ""
    st.session_state.reset_game = False
#--------------------------------------------------------------------------------------------------------------#
#Home page interface
if st.session_state.counter == 0:
    st.title("Welcome to Hangman Game!")
    st.write("This is a simple hangman game where you have to guess the fruit word.")
    st.image(os.path.join(os.getcwd(),"static","download.jpeg"), caption='MADE BY MUDASSIR ABRAR',width=400)
    st.button("Start Game",on_click=go_to_gamepage)


#--------------------------------------------------------------------------------------------------------------#


#--------------------------------------------------------------------------------------------------------------#
#Game page
if st.session_state.counter == 1:
        # Initialize game state
        if "word" not in st.session_state:
            list_of_words = ['apple', 'banana', 'cherry', 'date', 'elderberry', 'fig', 'grape', 'honeydew', 'jackfruit', 'kiwi', 'lemon', 'mango', 'nectarine', 'orange', 'papaya', 'quince', 'raspberry', 'strawberry', 'tangerine', 'ugli', 'vanilla', 'watermelon', 'ximenia', 'yellow watermelon', 'zucchini']
            st.session_state.word = random.choice(list_of_words).lower()
            st.session_state.display = ["_"] * len(st.session_state.word)
            st.session_state.wrong_guesses = 0
            st.session_state.guessed_letters = []
            st.session_state.input_value = ""  # Initialize the input field value

        # Title and Instructions
        st.title("Hangman Game")
        st.write("Guess the word by selecting letters. You have 6 attempts before the game is over!")
        # Display remaining lives
        st.slider(
            "Remaining Lives",
            min_value=0,
            max_value=6,
            value=6 - st.session_state.wrong_guesses,
            format="%d lives",
            disabled=True,
        )
        
        
 #------------------------------------------------------- ANIMATIONS-------------------------------------------------------------#               
        # Function to load Lottie animation
        def load_lottie_url(url):
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        # Load cheering animation
        cheer_animation = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_touohxv0.json")  # Replace with your chosen Lottie animation URL
      
                        
        # Function to load Lottie animation from a JSON file(for wrong and correct guess)
        def load_lottie_file(filepath: str):
            with open(filepath, "r") as f:
                return json.load(f)

        # Load your downloaded animation file
        sad_animation_data = load_lottie_file("static/Animation - 1740584168135.json")
        happy_animation_data = load_lottie_file("static/Animation - 1740580387425.json")
#-------------------------------------------------------------------------------------------------------------#          
        # Display the Hangman ASCII art
        st.text("Hangman Status:")
        st.text(hangman_phases[st.session_state.wrong_guesses])

        # Display the current word progress
        st.subheader("Word Progress")
        st.title(" ".join(st.session_state.display))
        
        
#----------------------------------------ANIMATION PLACEHOLDERS--------------------------------------------#      
        placeholder = st.empty()
        placeholder.warning("CHOOSE CAREFULY.")
        animation_placeholder = st.empty()
        
       
#----------------------------------------------------------------------------------------------------------#       
        
        # Callback function for checking the guess
        def check_guess():
            guess = st.session_state.input_value.lower()
            if not guess or guess in st.session_state.guessed_letters:
                placeholder.warning("Please enter a new letter!")
            elif guess in st.session_state.word:
                # Update the display for correct guesses
                for index, letter in enumerate(st.session_state.word):
                    if letter == guess:
                        st.session_state.display[index] = letter
                placeholder.success(f"Good guess: {guess}")
                 # Display the animation
                with animation_placeholder:
                 st_lottie(happy_animation_data, height=200, width=200,speed=0.01,loop=True)
               
            else:
                # Increment wrong guesses for incorrect guesses
                st.session_state.wrong_guesses += 1
                placeholder.error(f"Wrong guess: {guess}")
                with animation_placeholder:
                 st_lottie(sad_animation_data, height=200, width=200,speed=0.001)
            # Track guessed letters and reset input
            st.session_state.guessed_letters.append(guess)
            st.session_state.input_value = ""  # Clear the input field
            
            
            
#--------------------------------------------INPUT FIELD-----------------------------------------------#
        # Input for guessing a letter
        st.text_input( 
            "Enter a letter:", 
            max_chars=1, 
            key="input_value", 
            on_change=check_guess  # Trigger game logic immediately
        )
        

#--------------------------------- # Check for game over----------------------------------------------#      
    
       
        if "_" not in st.session_state.display:
            st.success(f"🎉 You win! The word was:  {st.session_state.word}")
            st_lottie(cheer_animation, height=200, width=200,) 
            st.balloons()
            st.button("Play Again", on_click=reset_game)
            st.button("Exit Game", on_click=go_to_homepage)
        elif st.session_state.wrong_guesses == 6:
            st.error(f"💀 You lose! The word was:  {st.session_state.word}")
            st.image(os.path.join(os.getcwd(),"static","Animation - 1740578093135.gif"), caption='YOU LOSE')
            st.button("Play Again", on_click=reset_game)
            st.button("Exit Game", on_click=go_to_homepage)
        # Display guessed letters
        st.subheader("Guessed Letters")
        st.write(", ".join(st.session_state.guessed_letters))
