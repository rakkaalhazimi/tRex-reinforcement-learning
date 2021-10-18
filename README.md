# Description

This is a prebuilt trex runner from [wayou](https://github.com/wayou) repo's in here [link](git@github.com:rakkaalhazimi/tRex-reinforcement-learning.git)

![chrome offline game cast](src/assets/screenshot.gif)

This is my first time to build a reinforce learning project. Hope I can improve more, feel free to reproduce or modify the code.  

# Author
Rakka Alhazimi, October 2021

# Requirements
First, let me tell you the summary of what I was use here

Software:
* Python v.3.7.7
* OS : Windows 10

Python side-libraries:
* Selenium
* Keyboard
* Tensorflow

Web-Driver for Selenium:
* Chrome

Any version is okay I guess, as long as the dependencies are fulfilled.  

# Installation
To make this project runs well on your machine, what you need to do is:

1. **Install Python** 

   After you install python, I suggest you to make an venv with command:  
   ```
   python -m venv [name]
   ```
   it'll build a folder in your directory right away, and to activate the env use:
   ```
   [name]\Scripts\activate.bat
   ```
   Then install all the dependencies using:
   ```
   pip install selenium, keyboard, tensorflow
   ```
   You can jump right into installing the dependencies if you already have python
   and venv intact.

2. **Install Chrome Web-browser**
   
   Chrome lets us to access console.log message from selenium. Therefore, Google Chrome
   is a must.

3. **Download webdriver for chrome** [here](https://sites.google.com/chromium.org/driver/)
   
   Match the driver with your Chrome version, after you download it, move the driver in
   your current directory (repo directory).

4. **Start the code**
   
   The main file is `main.py`, run this file to start the program.
   ```
   python main.py
   ```

# Current Status
It's still under-development though, so I'm afraid you couldn't do much here.

# Main Idea
I try to make a reinforcement learning project with the in-game parameters. Other peoples are likely to snipe the screen pixel or taking multiple screenshot to gain the parameters of the state. Therefore, I would like to try different approach by peeking the game-code and get its variable. It's much faster and memory-friendly. The rest is still the same, the approach, model and etc.  

I hope you can enjoy training your agent using the default model or you can also build your owns model to beat
this game, any modification is welcomed. You can also change how the parameters is recorded inside the `src/js/watcher.js` file.