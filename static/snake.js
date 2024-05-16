const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const scoreDisplay = document.getElementById('scoreDisplay');
const startGameButton = document.getElementById('startGame');
const restartGameButton = document.getElementById('restartGame');
const quitGameButton = document.getElementById('quitGame');
const usernameInput = document.getElementById('username');

let snake, dx, dy, food, score, gameInterval;

function initializeGame() {
    snake = [{x: 200, y: 200}, {x: 190, y: 200}, {x: 180, y: 200}];
    dx = 10;
    dy = 0;
    score = 0;
    placeFood();
    if (gameInterval) clearInterval(gameInterval);
    gameInterval = setInterval(gameLoop, 100);
    scoreDisplay.textContent = "Score: " + score;
}

function drawSnakePart(snakePart) {
    ctx.fillStyle = 'green';
    ctx.fillRect(snakePart.x, snakePart.y, 10, 10);
}

function drawSnake() {
    snake.forEach(drawSnakePart);
}

function drawFood() {
    ctx.fillStyle = 'red';
    ctx.fillRect(food.x, food.y, 10, 10);
}

function moveSnake() {
    const head = {x: snake[0].x + dx, y: snake[0].y + dy};
    snake.unshift(head);
    if (head.x === food.x && head.y === food.y) {
        score += 10;
        placeFood();
        scoreDisplay.textContent = "Score: " + score;
    } else {
        snake.pop();
    }
}

function gameLoop() {
    if (endGame()) {
        return;
    }
    clearCanvas();
    drawFood();
    moveSnake();
    drawSnake();
}

function clearCanvas() {
    ctx.fillStyle = 'black';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}

function placeFood() {
    food = {
        x: Math.floor(Math.random() * (canvas.width / 10)) * 10,
        y: Math.floor(Math.random() * (canvas.height / 10)) * 10
    };
}

function endGame() {
    const hitWall = snake[0].x < 0 || snake[0].x >= canvas.width || snake[0].y < 0 || snake[0].y >= canvas.height;
    const hitSelf = snake.slice(1).some(part => part.x == snake[0].x && part.y == snake[0].y);
    return hitWall || hitSelf;
}

document.addEventListener('keydown', function(e) {
    let direction = null;
    if ((e.key === 'ArrowLeft' || e.key === 'a' || e.key === 'A') && dx === 0) {
        direction = { dx: -10, dy: 0 }; // Move left
    } else if ((e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D') && dx === 0) {
        direction = { dx: 10, dy: 0 }; // Move right
    } else if ((e.key === 'ArrowUp' || e.key === 'w' || e.key === 'W') && dy === 0) {
        direction = { dx: 0, dy: -10 }; // Move up
    } else if ((e.key === 'ArrowDown' || e.key === 's' || e.key === 'S') && dy === 0) {
        direction = { dx: 0, dy: 10 }; // Move down
    } else if (e.key === 'r' || e.key === 'R') {
        initializeGame();
    } else if (e.key === 'x' || e.key === 'X') {
        clearInterval(gameInterval);
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        alert('Game has been quit!');
    }

    if (direction) {
        dx = direction.dx;
        dy = direction.dy;
    }
});



startGameButton.onclick = () => {
    if (usernameInput.value.trim() === '') {
        alert('Please enter a username.');
        return;
    }
    initializeGame();
};

restartGameButton.onclick = () => {
    initializeGame();
};

quitGameButton.onclick = () => {
    clearInterval(gameInterval);
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    alert('Game has been quit!');
};

// Store game result
function storeGameResult(username, score) {
    $.ajax({
        url: '/store_game_result',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ 'username': username, 'score': score }),
        success: function(response) {
            console.log('Game result stored successfully:', response);
        },
        error: function(response) {
            console.error('Error storing game result:', response);
        }
    });
}

function dumpDataToServer() {
    $.ajax({
        url: '/dump_data_to_json',
        type: 'POST',
        success: function(response) {
            console.log('Data dumped to JSON file successfully:', response);
        },
        error: function(response) {
            console.error('Error dumping data to JSON:', response);
        }
    });
}



document.addEventListener('keydown', function(e) {
    // key controls are handled here
    if (e.key === 'x' || e.key === 'X') {
        storeGameResult(usernameInput.value, score);
        dumpScoreToFile(usernameInput.value, score);
        clearInterval(gameInterval);
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        alert('Game has been quit!');
    }
});

startGameButton.onclick = function() {
    if (usernameInput.value.trim() === '') {
        alert('Please enter a username.');
        return;
    }
    initializeGame();
};

restartGameButton.onclick = function() {
    storeGameResult(usernameInput.value, score); // Save the current game result before restarting
     dumpDataToServer();
    initializeGame();
};

quitGameButton.onclick = function() {
    storeGameResult(usernameInput.value, score);


    clearInterval(gameInterval);
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    alert('Game has been quit!');
};

