# Coursework AI Basics

## Notes

I published my notes for the [Guild] Artificial Intelligence (Fall 2020) lectures and the [CS50’s
Introduction to Artificial Intelligence with Python](https://cs50.harvard.edu/ai/2020/) course.

- [AI Guild](https://www.remnote.io/a/cs50-s-introduction-to-artificial-intelligence-with-python/5fb8ec6ef80fff004588903a)
- [CS50 AI](https://www.remnote.io/a/-guild-artificial-intelligence-e-g-ai-basics-fall-2020-/5fb8ecbdf80fff004588924d)

## Projects
My projects focus on planning because its techniques will be applied in my current CODE project study journey. 
I focused less on reasoning because there isn't much application of its techniques in our project.

### Planning
- Maze
  - Inside the Planning/maze directory run ```python maze.py maze[1-5].txt [DFS | BFS | HS]```   

- TicTacToe
  - Inside the Neural_Networks/tictactoe directory run ```python runner.py``` to play against the ai.

### Optimization
- Crossword
 - Inside the Optimization/minesweeper run ```python generate.py data/structure1.txt data/words1.txt```, to specifying a structure file and a words file. If an assignment is possible, you should see the resulting assignment printed.

  This project is an AI to create a crossword puzzle. It's technically speaking, not an optimization but a constraint satisfaction problem (CSP). It would be one if there were a continuous rating of a produced crossword puzzle. However, with this exercise, the outcome was binary. 

### Reasoning
- Minesweeper
  - Inside the minesweeper directory, run ```python runner.py```



### Neural Networks
- Traffic
  - Download the distribution code from https://cdn.cs50.net/ai/2020/x/projects/5/traffic.zip and unzip it.
  - Download the [data set](https://cdn.cs50.net/ai/2020/x/projects/5/gtsrb.zip) for this project and unzip it. Move the resulting gtsrb directory inside of your traffic directory.
  Inside the traffic directory, run ```pip3 install -r requirements.txt``` to install this project’s dependencies: opencv-python for image processing, scikit-learn for ML-related functions, and tensorflow for neural networks.
  - Inside of the traffic directory, run ```python traffic.py gtsrb``` to train the network.

  This project includes a markdown file in which I document my experimentation process and describe how I was investigating different options.
