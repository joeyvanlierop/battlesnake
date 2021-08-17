package main

type Battlesnake struct {
	ID     string        `json:"id"`
	Health int           `json:"health"`
	Length int           `json:"length"`
	Body   []Coordinates `json:"body"`
	Head   Coordinates   `json:"head"`
}

const (
	MaxHealth = 100
)

// Move moves the snake in the given direction according to the Battlesnake game engine rules:
// https://docs.battlesnake.com/references/rules//3-moves-are-resolved-by-the-game-engine
func (snake *Battlesnake) Move(direction string) {
	// Initialize the coordinates of the new head
	newX := snake.Head.X
	newY := snake.Head.Y

	// Move the new head according to the direction
	switch direction {
	case "up":
		newY += 1
	case "right":
		newX += 1
	case "down":
		newY -= 1
	case "left":
		newX -= 1
	}

	// Initialize the new head and assign it to the snake
	newHead := Coordinates{
		X: newX,
		Y: newY,
	}
	snake.Head = newHead
	snake.Body = append([]Coordinates{newHead}, snake.Body...)

	// Remove the tail
	snake.Body = (snake.Body)[:len(snake.Body)-1]

	// Reduce the health by 1
	snake.Health -= 1
}

func (snake *Battlesnake) Eat() {
	// Reset health to maximum
	snake.Health = MaxHealth

	// Additional body part placed on top of current tail
	snake.Body = append(snake.Body, snake.Body[len(snake.Body)-1])
	snake.Length += 1
}
