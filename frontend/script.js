let playerLevel = 1;
let playerPoints = 0;

let selectedLevel = null;

let currentGame = {
    length: 0,
    revealed: [],
    hintsUsed: 0,
    maxHints: 0,
    totalAttempts: 0,
    clueAvailable: false,
    forfeitAvailable: false
};


const levelNames = {

    1: "Easy",
    2: "Normal",
    3: "Intermediate",
    4: "Advanced",
    5: "Expert",
    6: "Master",
    7: "Legend"

};


function showScreen(screenId) {

    document.querySelectorAll(".screen").forEach(function (screen) {

        screen.classList.remove("active");

    });

    document.getElementById(screenId).classList.add("active");

}


function showMessage(message) {

    const messageBox = document.getElementById("message-box");
    const messageText = document.getElementById("message-text");

    messageText.textContent = message;

    messageBox.classList.add("show");

    setTimeout(function () {

        messageBox.classList.remove("show");

    }, 2500);

}


function displayProgress() {

    document.getElementById("player-level").textContent = playerLevel;

    document.getElementById("player-points").textContent = playerPoints;

}


function updateLevelCards() {

    const levelCards = document.querySelectorAll(".level-card");

    levelCards.forEach(function (card) {

        const level = Number(card.dataset.level);

        card.classList.remove("locked");

        const oldButton = card.querySelector(".play-button");
        const oldLock = card.querySelector(".lock");

        if (oldButton) {
            oldButton.remove();
        }

        if (oldLock) {
            oldLock.remove();
        }


        if (level <= playerLevel) {

            const playButton = document.createElement("button");

            playButton.classList.add("play-button");

            playButton.textContent = "PLAY";

            playButton.addEventListener("click", function () {

                startGame(level);

            });

            card.appendChild(playButton);

        }

        else {

            card.classList.add("locked");

            const lock = document.createElement("span");

            lock.classList.add("lock");

            lock.textContent = "\u{1F512}";

            card.appendChild(lock);

        }

    });

}


async function startGame(level) {

    selectedLevel = level;

    try {

        const response = await fetch("/api/start-game", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                level: level
            })

        });


        if (!response.ok) {

            throw new Error("Unable to start the game.");

        }


        const data = await response.json();


        currentGame.length = data.length;

        currentGame.revealed = data.revealed;

        currentGame.hintsUsed = data.hints_used;

        currentGame.maxHints = data.max_hints;

        currentGame.totalAttempts = data.total_attempts;
        currentGame.clueAvailable = data.clue_available;
        currentGame.forfeitAvailable = data.forfeit_available;


        document.getElementById("game-level").textContent =
            "LEVEL " + level;

        document.getElementById("word-length").textContent =
            data.length;


        displayWord(data.revealed);

        clearGuessResult();

        updateGameActions();

        showScreen("game-screen");


        document.getElementById("guess-input").focus();

    }

    catch (error) {

        showMessage(error.message);

    }

}


function displayWord(revealed) {

    const wordBoard = document.getElementById("word-board");

    wordBoard.innerHTML = "";


    revealed.forEach(function (letter) {

        const letterBox = document.createElement("div");

        letterBox.classList.add("letter-box");

        if (letter) {

            letterBox.textContent = letter.toUpperCase();

        }
        else {

            letterBox.textContent = "";

        }

        wordBoard.appendChild(letterBox);

    });

}


async function makeGuess() {

    const input = document.getElementById("guess-input");

    const guess = input.value.trim();


    if (guess === "") {

        showMessage("Please enter a word.");

        return;

    }


    try {


        const response = await fetch("/api/guess", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                guess: guess
            })

        });


        if (!response.ok) {

            throw new Error("Unable to submit the guess.");

        }


        const data = await response.json();


        input.value = "";


        if (data.status === "invalid") {

            showMessage(
                "Invalid word or outside of the game's word list."
            );

            return;

        }


        currentGame.totalAttempts = data.total_attempts;
        currentGame.clueAvailable = data.clue_available;
        currentGame.forfeitAvailable = data.forfeit_available;
        currentGame.revealed = data.revealed;

        if (data.status === "won") {

            displayWord(data.revealed);

            showFinalResult(data);

            return;

        }


        if (data.status === "wrong") {

            displayWord(data.revealed);

            displayGuessResult(data);

            updateGameActions();

        }

    }

    catch (error) {

        showMessage(error.message);

    }

}


function displayGuessResult(data) {

    const message = document.getElementById("result-message");

    const correct = document.getElementById("correct-position");

    const wrong = document.getElementById("wrong-position");

    const notPresent = document.getElementById("not-present");


    message.textContent = "Guess Result";


    correct.textContent =
        "Correct Position: " +
        formatPositions(data.correct_position);


    wrong.textContent =
        "Wrong Position: " +
        formatPositions(data.wrong_position);


    notPresent.textContent =
        "Not Present: " +
        formatPositions(data.not_present);

}


function formatPositions(positions) {

    if (!positions || positions.length === 0) {

        return "None";

    }

    return positions.join(", ");

}


function clearGuessResult() {

    document.getElementById("result-message").textContent = "";

    document.getElementById("correct-position").textContent = "";

    document.getElementById("wrong-position").textContent = "";

    document.getElementById("not-present").textContent = "";

}


function updateGameActions() {

    const clueArea = document.getElementById("clue-area");

    const forfeitArea = document.getElementById("forfeit-area");


    clueArea.innerHTML = "";

    forfeitArea.innerHTML = "";


    if (currentGame.clueAvailable) {
    

        const clueButton = document.createElement("button");

        clueButton.id = "clue-button";

        clueButton.textContent = "USE CLUE";

        clueButton.addEventListener("click", useClue);

        clueArea.appendChild(clueButton);

    }


    if (currentGame.forfeitAvailable) {

        const forfeitButton = document.createElement("button");

        forfeitButton.id = "forfeit-button";

        forfeitButton.textContent = "FORFEIT";

        forfeitButton.addEventListener("click", forfeitGame);

        forfeitArea.appendChild(forfeitButton);

    }

}


async function useClue() {

    const confirmed = confirm(
        "Do you want to use a clue?"
    );


    if (!confirmed) {

        return;

    }


    try {

        const response = await fetch("/api/clue", {

            method: "POST"

        });


        if (!response.ok) {

            throw new Error("A clue is not available.");

        }


        const data = await response.json();


        if (data.status !== "hint") {

            showMessage(data.message);

            return;

        }

        currentGame.hintsUsed = data.hints_used;
        currentGame.clueAvailable = data.clue_available;
        currentGame.forfeitAvailable = data.forfeit_available;
        currentGame.revealed = data.revealed;

        displayWord(data.revealed);

        updateGameActions();


        showMessage(
            "Clue revealed position " + data.position + "."
        );

    }

    catch (error) {

        showMessage(error.message);

    }

}


async function forfeitGame() {

    const confirmed = confirm(
        "Do you want to forfeit this game?"
    );


    if (!confirmed) {

        return;

    }


    try {

        const response = await fetch("/api/forfeit", {

            method: "POST"

        });


        if (!response.ok) {

            throw new Error("Forfeit is not available yet.");

        }


        const data = await response.json();


        if (data.status !== "forfeited") {

            showMessage(data.message);

            return;

        }


        showFinalResult(data);

    }

    catch (error) {

        showMessage(error.message);

    }

}


function showFinalResult(data) {

    document.getElementById("final-word").textContent =
        data.word || "";

    document.getElementById("final-attempts").textContent =
        data.total_attempts || currentGame.totalAttempts;

    document.getElementById("final-hints").textContent =
        data.hints_used || currentGame.hintsUsed;

    document.getElementById("final-points").textContent =
        data.points !== undefined ? data.points : 0;


    if (data.status === "forfeited") {

        document.getElementById("final-title").textContent =
            "GAME OVER";

    }
    else {

        document.getElementById("final-title").textContent =
            "CONGRATULATIONS!";

    }


    showScreen("result-screen");

}


document.getElementById("play-again-button")
    .addEventListener("click", function () {

        if (selectedLevel !== null) {

            startGame(selectedLevel);

        }

    });


document.getElementById("home-button")
    .addEventListener("click", function () {

        showScreen("home-screen");

        loadProgress();

    });


document.getElementById("guess-button")
    .addEventListener("click", makeGuess);



document.getElementById("guess-input")
    .addEventListener("keydown", function (event) {

        if (event.key === "Enter") {

            makeGuess();

        }

    });


async function loadProgress() {

    try {

        const response = await fetch("/api/progress");


        if (!response.ok) {

            throw new Error("Unable to load player progress.");

        }


        const data = await response.json();


        playerLevel = data.level;

        playerPoints = data.points;


        displayProgress();

        updateLevelCards();

    }

    catch (error) {

        displayProgress();

        updateLevelCards();

    }

}

loadProgress();