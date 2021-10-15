# Main function

The main function for checking the state of the game lies within `Runner > update` you can get whatever parameter you want in there. Perhaps, you can create a contained function by yourself, it's your call.

# Parameters I want

The parameters that I need to build my own Reinforcement Learning Model is:
1. Distance from cactus
2. Width and Height of cactus
3. Velocity of dino
4. Y-Position of dino

# Attributes Source

* `this`, is the main object in this game, **Runner** object.  
  It contains many attributes for the game, but the one that you need is `this.currentSpeed` to monitor the game speed.

* `this.horizon.obstacles`, is an array of **Obstacles** objects.  
  Attributes you can obtain: `xPos`, `yPos`, `width`, `height`, etc.

* `this.tRex`, is a **Trex** object.  
  Attributes you can obtain: `xPos`, `yPos`, `width`, `height`, almost the same with obstacles.

# Calculation of inputs

1. Distance from cactus
   