import { runner } from "./index.js";

// Parameters
// ========================
var tRexDist = 0;
var obsWidth = 0;
var obsVGap = 0;
var reward = 1;


// Environtment state getter
// =========================

// Obstacle width
const getObsWidth = () => runner.horizon.obstacles[0].width / 1000;

// Current game speed
const getSpeed = () => Math.round(runner.currentSpeed * 100) / 1000;

// Set reward based on state
const getReward = () => runner.crashed ? -10 : 0.1;

// Distance between trex and obstacle
const getDistance = () => {
  let tRexPos = runner.tRex.xPos;
  let obsXPos = runner.horizon.obstacles[0].xPos;
  return (obsXPos - tRexPos) / 1000;
}

// Dino y-position
const getDinoYPos = () => {
  return runner.tRex.yPos / 1000
}

// Vertical gap between ground and obstacle
const getVGap = () => {
  const GROUND_YPOS = runner.dimensions.HEIGHT - runner.config.BOTTOM_PAD;
  let obstacleHeight = runner.horizon.obstacles[0].typeConfig.height;
  let obstacleYPos = runner.horizon.obstacles[0].yPos;
  return (GROUND_YPOS - (obstacleHeight + obstacleYPos)) / 1000
}



// Environment Report
// =========================
var reportStarter

function reportEnv() {
  let distanceObs = 0;
  let obsWidth = 0;
  let dinoYPos = getDinoYPos();
  let vgap = 0;
  let speed = getSpeed();
  let reward = getReward();
  let collide = runner.crashed ? 1 : 0;


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
    reward: ${reward}, 
    collide: ${collide}
  `

  if (runner.playing && distanceObs) {
    console.log(report);

  } else if (runner.crashed) {
    console.log(report);

    clearInterval(reportStarter);                      // Clear interval
    window.addEventListener("keypress", startReport);  // Register new event to start interval again

  } else { };
}

function startReport(event) {
  if ([" "].includes(event.key)) {
    
    window.removeEventListener("keypress", startReport);
    setTimeout(() => {
      reportStarter = setInterval(reportEnv, 100);
    }, 200)
    
  }
}



// Main function
// =========================
reportStarter = setInterval(reportEnv, 100);
