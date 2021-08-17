package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestNextBoard(t *testing.T) {
	// Arrange
	board := Board{
		Height: 5,
		Width:  5,
		Food: []Coordinates{
			{
				X: 3,
				Y: 3,
			},
		},
		Snakes: []Battlesnake{
			{
				ID:     "abc",
				Health: 50,
				Body: []Coordinates{
					{X: 2, Y: 0},
					{X: 1, Y: 0},
					{X: 0, Y: 0},
				},
				Head:   Coordinates{X: 2, Y: 0},
				Length: 3,
			},
		},
	}

	// Act
	nextBoard := NextBoard(board, "abc", "right")
	board.Snakes = []Battlesnake{
		{
			ID:     "abc",
			Health: 49,
			Body: []Coordinates{
				{X: 3, Y: 0},
				{X: 2, Y: 0},
				{X: 1, Y: 0},
			},
			Head:   Coordinates{X: 3, Y: 0},
			Length: 3,
		},
	}

	// Assert
	assert.Equal(t, board, nextBoard)
}

func TestNextBoardEat(t *testing.T) {
	// Arrange
	board := Board{
		Height: 5,
		Width:  5,
		Food: []Coordinates{
			{
				X: 3,
				Y: 0,
			},
			{
				X: 4,
				Y: 0,
			},
		},
		Snakes: []Battlesnake{
			{
				ID:     "abc",
				Health: 50,
				Body: []Coordinates{
					{X: 2, Y: 0},
					{X: 1, Y: 0},
					{X: 0, Y: 0},
				},
				Head:   Coordinates{X: 2, Y: 0},
				Length: 3,
			},
		},
	}

	// Act
	nextBoard := NextBoard(board, "abc", "right")
	board.Food = []Coordinates{
		{
			X: 4,
			Y: 0,
		},
	}
	board.Snakes = []Battlesnake{
		{
			ID:     "abc",
			Health: MaxHealth,
			Body: []Coordinates{
				{X: 3, Y: 0},
				{X: 2, Y: 0},
				{X: 1, Y: 0},
				{X: 1, Y: 0},
			},
			Head:   Coordinates{X: 3, Y: 0},
			Length: 4,
		},
	}

	// Assert
	assert.Equal(t, board, nextBoard)
}
