# Tic-Tac-Toe-using-reinforcement-learning
Learn computer to play Tic Tac Toe using reinforcement learning.

This is an excersice problem(1.4) in this [Book](webdocs.cs.ualberta.ca/~sutton/book/ebook/the-book.html). Here computer play with itself. There are 10,000 episodes to train computer which data is stored in [data.csv](https://github.com/shark-S/Tic-Tac-Toe-using-reinforcement-learning/blob/master/data.csv) and graph is in this [image](https://github.com/shark-S/Tic-Tac-Toe-using-reinforcement-learning/blob/master/Selfplay%20random_-1loss.png).

After 10,000 episodes it show good result with its opponent player which is human :) .

Reward for winning state is 1.0, for losing and draw 0.0 and otherwise 0.5. In every iteration it calculate is possible reward 

V(s) = V(s) + alpha * [V(s')-V(s)]

Computer player play with 90%  greedy(try to get winning state) while 10% in exploration state in which it play randomly in available choice. Where it explore state and learn something new :p .

