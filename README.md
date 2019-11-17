# My Minesweeper project
	
A computer program utilizing AI methods/techniques/concepts to solve a problem.

	I used two theorems and equation strategy to support my algorithms. It was fun to think of these strategies because every player implicitly understands the logic. It was the same logic what a player will do to play the game. 

## Definitions:

	A square is the tile which contains a bomb or number
	A board is the grid and its component squares
	Given a board B and a square B_(x,y), K (B_(x,y)) is the contents of B_(x,y)
	Given a board B and a square B_(x,y), denote R_(x,y)^B as the set of all squares adjacent to B_(x,y)

## Theorem 1: 

	Given a board B and square B_(x,y), if the number of unrevealed squares in R_(x,y)^B is equal to K (B_(x,y)) (minus the number of flagged squares in R_(x,y)^B), then all of those unrevealed squares contain a bomb.

## Theorem 2:

	Given a board B and square B_(x,y), if the number of flagged squares surrounding B_(x,y) is equal to K (B_(x,y)), every unrevealed square in R_(x,y)^B does not contain a bomb.


### (A) Apply Theorem 1 and 2
	
	Besides the theorem/ strategies I used for minimal AI, I improved the algorithm by using constraint satisfaction problem 

### (B) CSP/ Equation Strategy

	Given a board, every unrevealed square which is adjacent to revealed squares is x_i , for i is equal to the number of unrevealed squares adjacent to revealed squares. The sum of each linear equation is equal to K (B_(x,y)) (minus the number of flagged squares in R_(x,y)^B). Solve multiple linear equations by comparing two of them each time. If each constraint resulted to x_i=0 or 1, that means that square (x_i) has either 0 bomb or 1 bomb. Then, we can return those tiles and add them to flag list or frontier list to uncover. 

## Results:

	Difficulty              | Board Size |	Sample Size   | Score  	| Worlds Complete
	Simple (1 mine)         | 5x5	     |  1000	      | 1000	| 100%
	Beginner (10 mines)     | 8x8	     |  1000	      | 844	| 84.4% (61 seconds)
	Intermediate (40 mines) | 16x16	     |  1000	      | 1574	| 79.7% (2563 seconds = 42 minutes)
	Expert (99 mines)       | 16x30	     |  1000	      | 591	| 19.7% (3687 seconds = 61 minutes)
