package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestMove(t *testing.T) {
	snake := Battlesnake{
		ID:     "abc",
		Health: 50,
		Body: []Coordinates{
			{X: 1, Y: 1},
			{X: 2, Y: 1},
			{X: 3, Y: 1},
		},
		Head:   Coordinates{X: 1, Y: 1},
		Length: 3,
	}

	snake.Move("up")
	assert.Equal(t, 2, snake.Head.Y)

	snake.Move("right")
	assert.Equal(t, 2, snake.Head.X)

	snake.Move("down")
	assert.Equal(t, 1, snake.Head.Y)

	snake.Move("left")
	assert.Equal(t, 1, snake.Head.X)
}

func TestEat(t *testing.T) {
	snake := Battlesnake{
		ID:     "abc",
		Health: 50,
		Body: []Coordinates{
			{X: 1, Y: 1},
			{X: 2, Y: 1},
			{X: 3, Y: 1},
		},
		Head:   Coordinates{X: 1, Y: 1},
		Length: 3,
	}

	snake.Eat()
	assert.Equal(t, MaxHealth, snake.Health)
	assert.Equal(t, 4, snake.Length)
}
