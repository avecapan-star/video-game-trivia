
from drafter import *
from dataclasses import dataclass


set_website_title("Corgi Cafe")
set_site_information(
    author="Your Name",
    description="Order snacks for very good dogs.",
    sources="Thanks to the Drafter docs and my study group.",
    planning=["plan.pdf", "design.pdf"],
    links=["https://github.com/your-username/your-repository"]
)
hide_debug_information()
set_website_framed(False)



# DATA CLASSES

@dataclass
class Question:
    question_text: str
    answer_options: list[str]
    correct_answer: str
    user_answer: str
    category: str
    hint: str


@dataclass
class State:
    player_name: str
    questions: list[Question]
    current_question: int
    score: int
    selected_category: str
    show_hints: bool


# TRIVIA QUESTIONS

def make_questions() -> list[Question]:
    """Create the ten video game trivia questions."""

    return [
        Question(
            "What company created Minecraft?",
            ["Mojang", "Nintendo", "Sony", "Ubisoft"],
            "Mojang", "", "Minecraft",
            "The company's name starts with M."
        ),
        Question(
            "What is the name of Call of Duty's battle royale game?",
            ["Zombies", "Warzone", "Black Ops", "Modern Warfare"],
            "Warzone", "", "Call of Duty",
            "It has the word 'war' in its name."
        ),
        Question(
            "What vehicle takes players to the island in Fortnite?",
            ["Battle Bus", "Helicopter", "Airplane", "Train"],
            "Battle Bus", "", "Fortnite",
            "It is a large blue bus."
        ),
        Question(
            "What is Spider-Man's real name?",
            ["Bruce Wayne", "Tony Stark", "Peter Parker", "Clark Kent"],
            "Peter Parker", "", "Spider-Man",
            "His first name is Peter."
        ),
        Question(
            "Who is the princess in The Legend of Zelda?",
            ["Peach", "Zelda", "Daisy", "Rosalina"],
            "Zelda", "", "The Legend of Zelda",
            "The princess shares the game's name."
        ),
        Question(
            "What is the main city in Grand Theft Auto V?",
            ["Vice City", "Liberty City", "Los Santos", "San Fierro"],
            "Los Santos", "", "Grand Theft Auto",
            "The name starts with Los."
        ),
        Question(
            "In Among Us, what is the enemy player called?",
            ["The Hunter", "The Impostor", "The Monster", "The Spy"],
            "The Impostor", "", "Among Us",
            "This player tries to trick the crew."
        ),
        Question(
            "What item makes Mario grow bigger?",
            ["Fire Flower", "Star", "Super Mushroom", "Coin"],
            "Super Mushroom", "", "Super Mario",
            "It is a red and white mushroom."
        ),
        Question(
            "Which Overwatch character is known for saying 'Cheers, love!'?",
            ["Mercy", "D.Va", "Tracer", "Widowmaker"],
            "Tracer", "", "Overwatch",
            "She can teleport and rewind time."
        ),
        Question(
            "What is the name of the currency used in Fortnite?",
            ["Coins", "V-Bucks", "Gems", "Gold Bars"],
            "V-Bucks", "", "Fortnite",
            "The name starts with the letter V."
        )
    ]


# WEBSITE INFORMATION

set_website_title("Video Game Trivia")

set_site_information(
    author="Your Name",
    description="A multiple-choice video game trivia game.",
    sources="Trivia questions written for this project.",
    planning="See the brainstorming and design worksheets "
             "in the project repository.",
    links=[]
)


# PAGE 1: HOME

@route
def index(state: State) -> Page:
    """Show the welcome page."""

    return Page(state, [
        Header("Video Game Trivia"),
        "Welcome to the ultimate video game trivia challenge!",
        "Test your knowledge of popular video games.",
        "There are 10 questions in each game.",
        Button("Start Playing", "setup")
    ])


# PAGE 2: SETUP

@route
def setup(state: State) -> Page:
    """Ask the player for their name and hint preference."""

    return Page(state, [
        Header("Game Setup"),
        "Enter your name:",
        TextBox("player_name", state.player_name),
        "\n",
        "Would you like hints during the game?",
        CheckBox("show_hints", True),
        "\n",
        "You will get 10 mixed video game questions.",
        Button("Start Quiz", "start_quiz"),
        Button("Back Home", "index")
    ])


# ROUTE: START QUIZ

@route
def start_quiz(state: State, player_name: str,
               show_hints: bool) -> Page:
    """Save the player's choices and begin the quiz."""

    if player_name.strip() == "":
        return Page(state, [
            Header("Please Enter Your Name"),
            "You need to enter a name before starting.",
            Button("Go Back", "setup")
        ])

    state.player_name = player_name
    state.show_hints = show_hints
    state.selected_category = "All"
    state.questions = make_questions()
    state.current_question = 0
    state.score = 0

    return quiz(state)


# PAGE 3: QUIZ

@route
def quiz(state: State) -> Page:
    """Display the current trivia question."""

    if state.current_question >= len(state.questions):
        return results(state)

    question = state.questions[state.current_question]

    page_content = [
        Header("Question " + str(state.current_question + 1)
               + " of 10"),
        "Player: " + state.player_name,
        "Score: " + str(state.score),
        question.category,
        question.question_text
    ]

    if state.show_hints:
        page_content.append("Hint: " + question.hint)

    page_content.append(
        SelectBox("answer", question.answer_options)
    )
    page_content.append("\n")
    page_content.append(
        Button("Submit Answer", "submit_answer")
    )

    return Page(state, page_content)


# ROUTE: SUBMIT ANSWER

@route
def submit_answer(state: State, answer: str) -> Page:
    """Check the answer and update the score."""

    question = state.questions[state.current_question]

    question.user_answer = answer

    if answer == question.correct_answer:
        state.score = state.score + 1

        return Page(state, [
            Header("Correct!"),
            "Great job, " + state.player_name + "!",
            "Your answer was correct.",
            "Your score is now " + str(state.score) + ".",
            Button("Next Question", "next_question")
        ])

    else:
        return Page(state, [
            Header("Incorrect!"),
            "The correct answer was: "
            + question.correct_answer,
            "Your score is still " + str(state.score) + ".",
            Button("Next Question", "next_question")
        ])


# ROUTE: NEXT QUESTION

@route
def next_question(state: State) -> Page:
    """Move to the next question."""

    state.current_question = state.current_question + 1

    if state.current_question < len(state.questions):
        return quiz(state)

    else:
        return results(state)


# PAGE 4: RESULTS

@route
def results(state: State) -> Page:
    """Show the player's final score."""

    page_content = [
        Header("Quiz Complete!"),
        "Great job, " + state.player_name + "!",
        "You answered all 10 questions.",
        "Your final score is "
        + str(state.score) + " out of 10."
    ]

    if state.score >= 8:
        page_content.append("Amazing job! You really know your games!")

    elif state.score >= 5:
        page_content.append("Good work! You know quite a bit about gaming.")

    else:
        page_content.append("Keep practicing! You can try again.")

    page_content.append(
        Button("Review My Answers", "review")
    )
    page_content.append(
        Button("Play Again", "restart")
    )

    return Page(state, page_content)


# PAGE 5: REVIEW ANSWERS

@route
def review(state: State) -> Page:
    """Show every question and the player's answers."""

    page_content = [
        Header("Answer Review"),
        "Here are your answers, " + state.player_name + "."
    ]

    for question in state.questions:
        page_content.append("\n")
        page_content.append(question.question_text)
        page_content.append(
            "Your answer: " + question.user_answer
        )
        page_content.append(
            "Correct answer: " + question.correct_answer
        )

        if question.user_answer == question.correct_answer:
            page_content.append("Result: Correct!")

        else:
            page_content.append("Result: Incorrect.")

    page_content.append("\n")
    page_content.append(
        Button("Play Again", "restart")
    )
    page_content.append(
        Button("Home", "index")
    )

    return Page(state, page_content)


# ROUTE: RESTART

@route
def restart(state: State) -> Page:
    """Reset the game and return to setup."""

    state.questions = make_questions()
    state.current_question = 0
    state.score = 0
    state.player_name = ""
    state.selected_category = "All"
    state.show_hints = True

    return setup(state)


# START THE WEBSITE

start_server(State(
    player_name="",
    questions=make_questions(),
    current_question=0,
    score=0,
    selected_category="All",
    show_hints=True
))



# UNIT TESTS

def test_make_questions():
    """Test that the trivia questions are created correctly."""

    questions = make_questions()

    assert_equal(len(questions), 10)
    assert_equal(questions[0].category, "Minecraft")
    assert_equal(questions[0].correct_answer, "Mojang")
    assert_equal(questions[1].category, "Call of Duty")


def test_question_answers():
    """Test that questions have answer choices."""

    questions = make_questions()

    assert_equal(
        questions[0].answer_options,
        ["Mojang", "Nintendo", "Sony", "Ubisoft"]
    )

    assert_equal(questions[0].hint, "The company's name starts with M.")


def test_score():
    """Test that the score can be updated."""

    state = State(
        player_name="Player",
        questions=make_questions(),
        current_question=0,
        score=0,
        selected_category="All",
        show_hints=True
    )

    state.score = state.score + 1

    assert_equal(state.score, 1)


def test_player_name():
    """Test that the player name is saved."""

    state = State(
        player_name="Avery",
        questions=make_questions(),
        current_question=0,
        score=0,
        selected_category="All",
        show_hints=True
    )

    assert_equal(state.player_name, "Avery")


def test_game_settings():
    """Test the initial game settings."""

    state = State(
        player_name="Player",
        questions=make_questions(),
        current_question=0,
        score=0,
        selected_category="All",
        show_hints=True
    )

    assert_equal(state.current_question, 0)
    assert_equal(state.score, 0)
    assert_equal(state.selected_category, "All")
    assert_equal(state.show_hints, True)


# Run the tests
test_make_questions()
test_question_answers()
test_score()
test_player_name()
test_game_settings()

