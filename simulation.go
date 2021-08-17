package main

import "errors"

// IsAlive determines if the Battlesnake with the given id shuold be considered alive
// The Battlesnake is determined to be alive according to the Battlesnake game engine rules:
// https://docs.battlesnake.com/references/rules//3-moves-are-resolved-by-the-game-engine
func IsAlive(board Board, id string) (bool, error) {
	// Loop over all the snakes in the board and find a snake with the given id
	var snake *Battlesnake
	for i := range board.Snakes {
		s := &board.Snakes[i]
		if s.ID == id {
			snake = s
		}
	}
	if snake == nil {
		return false, errors.New("invalid battlesnake")
	}

	// Die if health less than or equal to 0
	if snake.Health <= 0 {
		return false, nil
	}

	// Die if moved out of bounds
	if snake.Head.X < 0 || snake.Head.Y < 0 || snake.Head.X >= board.Width || snake.Head.Y >= board.Height {
		return false, nil
	}

	// Die if collided with itself
	headCount := 0
	for _, body := range snake.Body {
		if body == snake.Head {
			headCount += 1
		}
	}
	if headCount > 1 {
		return false, nil
	}

	// Collision with another Battlesnake
	for _, otherSnake := range board.Snakes {
		if snake.ID != otherSnake.ID {
			// Collided head-to-head
			if snake.Head == otherSnake.Head {
				// Die if we are are equal or shorter than the other snake
				if snake.Length <= otherSnake.Length {
					return false, nil
				}
			} else {
				for _, body := range otherSnake.Body {
					// Die if collided with the body
					if snake.Head == body {
						return false, nil
					}
				}
			}
		}
	}

	// Not dead :)
	return true, nil
}

// NextBoard determines the next board with the given move according to the Battlesnake game engine rules:
// https://docs.battlesnake.com/references/rules//3-moves-are-resolved-by-the-game-engine
func NextBoard(board Board, ID, direction string) Board {
	for i := range board.Snakes {
		// Find the snake with the correct id
		snake := &board.Snakes[i]
		if snake.ID == ID {
			// Move the snake
			snake.Move(direction)
			// Any Battlesnake that has found food will consume it
			for j, food := range board.Food {
				if snake.Head == food {
					// Snake eats the food
					snake.Eat()
					// The food is removed from the board
					board.Food = append((board.Food)[:j], (board.Food)[j+1:]...)
				}
			}
		}
	}

	return board
}
