// Vars
let gameOver = true;
let score = 0;
let alreadyGuessedWords = [];
// DOM elements
let highScoreEl = document.querySelector("#high-score");
let scoreEl = document.querySelector("#score");
const submitForm = document.querySelector("#submit-guess-form");
const timerEl = document.querySelector("#timer");
const startGameButton = document.querySelector("#start-button");
const gameBoardUl = document.querySelector((".game-board-ul"));
const submitGuessForm = document.querySelector("#submit-guess-form");
const gamesPlayed = document.querySelector(".games-played");


// If submit button clicked, check word to see if user guessed correct.
submitForm.addEventListener("submit", async function(e) {
    e.preventDefault()
    if (gameOver === false) {
        let guessInput = document.querySelector("#user-guess");
        const response = await submitGuess(guessInput.value);
    
        // If word is correct (in gameboard), then update score
        if (response.data["result"] === "ok" && !alreadyGuessedWords.includes(guessInput.value)) {
            alreadyGuessedWords.push(guessInput.value)
            score += guessInput.value.length;
            scoreEl.innerText = score;
        }
        // Clear the input after every guess
        guessInput.value = "";
    }
})

// Start game function
async function startGame() {
    submitGuessForm.classList.remove("hidden");
    startGameButton.style.display = "none";
    gameBoardUl.innerHTML = "";
    gameOver = false;
    score = 0;
    scoreEl.innerText = score;
    timerEl.innerText = 0;
    alreadyGuessedWords = [];
    const gameBoard = await getNewGameBoard();
    createGameBoardDOM(gameBoard)
    await incrementTimesPlayed();

}

// Create the DOM elements for the boggle board
function createGameBoardDOM(gameBoard) {
    for(row of gameBoard) {
        let newLi = document.createElement("li");
        newLi.innerText = row; 
        gameBoardUl.appendChild(newLi);
    }
}

// Get a brand new game board each time new game is started
async function getNewGameBoard() {
    try {
        const response = await axios.get("/start-game")
        return response.data["game-board"]  
    } 
    catch (error) {
      console.error(error);
    }
}

// Every time the game ends, we add 1 to how many times the user has played.
async function incrementTimesPlayed() {
    try {
        const response = await axios.post("/game-over", {"highScore" : score})
        gamesPlayed.innerText = response.data["games-played"];
    } 
    catch (error) {
      console.error(error);
    }
}

// Function to submit our guess to the server
async function submitGuess(guess) {
    try {
        const response = await axios.post("/submit-guess", {guess : guess})
        return response;
    } 
    catch (error) {
      console.error(error);
    }
}

// Start the game
startGameButton.addEventListener("click", function() {
    startGame()
    
    // Set timer initial val
    let timer = 60;
    timerEl.innerText = timer;

    // Logic for the timer when it starts
    let timeInterval = setInterval(async function() {
        timer--;
        timerEl.innerText = timer;
        if (timer <= 0) {
            startGameButton.classList.remove("hidden");
            submitGuessForm.classList.add("hidden")
            gameOver = true;
            clearInterval(timeInterval);
            startGameButton.style.display = "inline-block";
            gameBoardUl.innerHTML = "";
            if(score > parseInt(highScoreEl.innerText)) {
                highScoreEl.innerText = score;
            }
        }
    }, 1000);
});

 