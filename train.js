import { runner } from "./index.js";


var tRexDist = 0;
var obsWidth = 0;
var obsVGap = 0;
var reward = 1;


function getDistance() {
  // Distance between trex and obstacle
  let tRexPos = runner.tRex.xPos;
  let obsXPos = runner.horizon.obstacles[0].xPos;

  return obsXPos - tRexPos;
}

function getVGap() {
  // Vertical gap between ground and obstacle
  const GROUND_YPOS = runner.dimensions.HEIGHT - runner.config.BOTTOM_PAD;
  let obstacleHeight = runner.horizon.obstacles[0].typeConfig.height;
  let obstacleYPos = runner.horizon.obstacles[0].yPos;

  return GROUND_YPOS - (obstacleHeight + obstacleYPos)
}

function getObsWidth() {
  // Obstacle width
  return runner.horizon.obstacles[0].width
}

function getSpeed() {
  // Current game speed
  return Math.round(runner.currentSpeed * 100) / 100;
}

function getReward() {
  // Set reward based on state
  return runner.crashed ? -1 / 10: 1 / 100;
}

// ===================================================================================

var reportStarter

function reportEnv() {
  let distance = 0;
  let width = 0;
  let vgap = 0;
  let speed = getSpeed();
  let reward = getReward()

  if (runner.horizon.obstacles[0] != undefined) {
    distance = getDistance();
    width = getObsWidth();
    vgap = getVGap();
  }

  var report =
  `
  distance: ${distance},
  speed: ${speed}, 
  width: ${width}, 
  Vgap: ${vgap},
  reward: ${reward},
  collide: ${runner.crashed}
  `

  if (runner.playing) {
    console.log(report);

  } else if (runner.crashed) {
    console.log(report);
    clearInterval(reportStarter);                      // Clear interval
    window.addEventListener("keypress", startReport);  // Set event to start interval again

  } else {};
}

function startReport(event) {
  if ([" ", "ArrowUp"].includes(event.key)) {
    reportStarter = setInterval(reportEnv, 1000);
  }
}

reportStarter = setInterval(reportEnv, 100);
