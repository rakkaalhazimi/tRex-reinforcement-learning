import { runner } from "./index.js";

// Parameters
// ========================
var tRexDist = 0;
var obsWidth = 0;
var obsVGap = 0;
var reward = 1;
var episode = 1
var attempt = document.getElementById("attempt")


// Environtment state getter
// =========================

// Obstacle width
const getObsWidth = () => runner.horizon.obstacles[0].width / 100;

// Current game speed
const getSpeed = () => Math.round(runner.currentSpeed * 100) / 1000;

// Set reward based on state
const getReward = () => {
  if (runner.crashed) {
    rewards -= 100
  } else {
    rewards += 0.1
  }

  return Math.round(rewards * 100) / 100
};

// Distance between trex and obstacle
const getDistance = () => {
  let tRexPos = runner.tRex.xPos;
  let obsXPos = runner.horizon.obstacles[0].xPos;
  return (obsXPos - tRexPos) / 100;
}

// Dino y-position
const getDinoYPos = () => {
  return runner.tRex.yPos / 100
}

// Vertical gap between ground and obstacle
const getVGap = () => {
  const GROUND_YPOS = runner.dimensions.HEIGHT - runner.config.BOTTOM_PAD;
  let obstacleHeight = runner.horizon.obstacles[0].typeConfig.height;
  let obstacleYPos = runner.horizon.obstacles[0].yPos;
  return (GROUND_YPOS - (obstacleHeight + obstacleYPos)) / 100
}



// Environment Report
// =========================
var reportStarter
var rewards = 0

function reportEnv() {
  let distanceObs = 0;
  let obsWidth = 0;
  let dinoYPos = getDinoYPos();
  let vgap = 0;
  let speed = getSpeed();
  rewards = getReward();
  let collide = runner.crashed ? 1 : 0;
  let isStart = runner.runningTime > 3000;


  // When see obstacle
  if (runner.horizon.obstacles[0] != undefined) {
    distanceObs = getDistance();
    obsWidth = getObsWidth();
    vgap = getVGap();
  }

  var report = `
    distanceObs: ${distanceObs}, 
    speed: ${speed}, 
    obsWidth: ${obsWidth},
    dinoHeight: ${dinoYPos}, 
    vgap: ${vgap},
    reward: ${rewards}, 
    collide: ${collide}
  `

  if (runner.playing && isStart) {
    console.log(report);

  } else if (runner.crashed) {
    console.log(report);
    rewards = 0                                        // Reset rewards
    
    clearInterval(reportStarter);                      // Clear interval
    window.addEventListener("keypress", startReport);  // Register new event to start interval again

  } else { };
}

function startReport(event) {
  if ([" "].includes(event.key)) {

    episode++                                          // Count and update episode
    attempt.innerHTML = `Attempt: ${episode}`
    window.removeEventListener("keypress", startReport);  // Remove event
    setTimeout(() => {
      reportStarter = setInterval(reportEnv, 100);
    }, 200)
    
  }
}



// Main function
// =========================
reportStarter = setInterval(reportEnv, 100);
