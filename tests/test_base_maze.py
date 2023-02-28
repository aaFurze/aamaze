from typing import List

import pytest

from aamaze.base_maze import (BOTTOM_WALL, LEFT_WALL, RIGHT_WALL, TOP_WALL,
                              GenerationAlgorithm, Maze, MazeNode)


class MockGenerationAlgorithm(GenerationAlgorithm):
    @classmethod
    def generate_maze(cls, maze_body: List[MazeNode]) -> List[MazeNode]:
        return maze_body



@pytest.fixture
def mock_maze() -> Maze:
    return Maze(5, 6, start_filled=True)

@pytest.fixture
def maze_node_all_walls() -> MazeNode:
    return MazeNode(2, 4, 0b00001111)

@pytest.fixture
def maze_node_l_b_walls() -> MazeNode:
    return MazeNode(2, 4, 0b00000110)

@pytest.fixture
def mock_maze_empty() -> Maze:
    return Maze(8, 8, start_filled=False)


class TestMaze:
    def test_generate_maze_returns_correct_length(self, mock_maze: Maze):
        assert len(mock_maze.maze_body) == 30

    @pytest.mark.parametrize("node_num, node_x", [(0, 0), (3, 3), (7, 2), (19, 4)])
    def test_generate_maze_x_values(self, mock_maze: Maze, node_num: int, node_x: int):
        assert mock_maze.maze_body[node_num].x == node_x

    @pytest.mark.parametrize("node_num, node_y", [(0, 0), (3, 0), (6, 1), (15, 3)])
    def test_generate_maze_row_y_values(self, mock_maze: Maze, node_num: int, node_y: int):
        assert mock_maze.maze_body[node_num].y == node_y
    
    def test_get_generated_maze_returns_list(self, mock_maze: Maze):
        assert mock_maze.get_generated_maze(mock_maze, MockGenerationAlgorithm)
    
    @pytest.mark.parametrize("x, y, expected_count", [(0, 0, 2), (0, 1, 3), (2, 1, 4),
     (4, 4, 3), (4, 5, 2)])
    def test_get_node_neighbours_count(self, mock_maze: Maze, x: int, y: int,
     expected_count: int):
        assert len(mock_maze.get_neighbours_from_coordinates(x, y)) == expected_count

    @pytest.mark.parametrize("neighbour_index, expected_x, expected_y", [(0, 2, 4), (1, 2, 2),
     (2, 1, 3), (3, 3, 3)])
    def test_get_node_neighbours_first_node_coordinates(self, mock_maze: Maze,
     neighbour_index, expected_x: int, expected_y: int):
        neighbours = mock_maze.get_neighbours_from_coordinates(2, 3)
        assert neighbours[neighbour_index].x == expected_x
        assert neighbours[neighbour_index].y == expected_y

    @pytest.mark.parametrize("neighbour_index, expected_x, expected_y", [(0, 0, 4), (1, 1, 5)])
    def test_get_node_neighbours_first_node_coordinates_corner(self, mock_maze: Maze,
     neighbour_index, expected_x: int, expected_y: int):
        neighbours = mock_maze.get_neighbours_from_coordinates(0, 5)
        assert neighbours[neighbour_index].x == expected_x
        assert neighbours[neighbour_index].y == expected_y

    @pytest.mark.parametrize("x, y", [(0, 1), (1, 2), (3, 4), (4, 5), (3, 3)])
    def test_get_node_valid_input(self, mock_maze: Maze, x, y):
        node = mock_maze.get_node_from_coordinates(x, y)
        assert node.x == x
        assert node.y == y

    @pytest.mark.parametrize("x, y", [(-1, 1), (100, 200), (3, 400), (40, 5), (-456546, -5)])
    def test_get_node_invalid_input(self, mock_maze: Maze, x, y):
        node = mock_maze.get_node_from_coordinates(x, y)
        assert node is None
    
    @pytest.mark.parametrize("index", [i for i in range(64)])
    def test_empty_maze_middle_is_empty(self, mock_maze_empty: Maze, index: int):
        if index <= mock_maze_empty.w or index >= mock_maze_empty.size - mock_maze_empty.w: return
        if index % mock_maze_empty.w == 0 or index % mock_maze_empty.w == mock_maze_empty.w - 1: return

        assert mock_maze_empty[index].walls == 0

    @pytest.mark.parametrize("index", [i for i in range(64)])
    def test_empty_maze_has_outside_walls(self, mock_maze_empty: Maze, index: int):
        if index > mock_maze_empty.w and index < mock_maze_empty.size - mock_maze_empty.w:
            if index % mock_maze_empty.w != 0 and index % mock_maze_empty.w != mock_maze_empty.w - 1: return
        assert mock_maze_empty[index].walls != 0
    
    @pytest.mark.parametrize("index", [2, 23, 53, 12, 7, 8, 0])
    def test_add_walls_above(self, mock_maze_empty: Maze, index: int):
        GenerationAlgorithm.add_walls(mock_maze_empty[index], mock_maze_empty[index + mock_maze_empty.w])

        assert mock_maze_empty[index].walls & TOP_WALL
        assert mock_maze_empty[index + mock_maze_empty.w].walls & BOTTOM_WALL


    @pytest.mark.parametrize("index", [57, 23, 56, 12, 59, 8, 63])
    def test_add_walls_below(self, mock_maze_empty: Maze, index: int):
        GenerationAlgorithm.add_walls(mock_maze_empty[index], mock_maze_empty[index - mock_maze_empty.w])

        assert mock_maze_empty[index].walls & BOTTOM_WALL
        assert mock_maze_empty[index - mock_maze_empty.w].walls & TOP_WALL

    @pytest.mark.parametrize("index", [58, 23, 56, 12, 59, 16, 63])
    def test_add_walls_left(self, mock_maze_empty: Maze, index: int):
        GenerationAlgorithm.add_walls(mock_maze_empty[index], mock_maze_empty[index - 1])

        assert mock_maze_empty[index].walls & LEFT_WALL
        assert mock_maze_empty[index - 1].walls & RIGHT_WALL

    @pytest.mark.parametrize("index", [57, 23, 56, 12, 59, 8, 0])
    def test_add_walls_right(self, mock_maze_empty: Maze, index: int):
        GenerationAlgorithm.add_walls(mock_maze_empty[index], mock_maze_empty[index + 1])

        assert mock_maze_empty[index].walls & RIGHT_WALL
        assert mock_maze_empty[index + 1].walls & LEFT_WALL
    
    @pytest.mark.parametrize("index1, index2, correct_value1, correct_value2", [
        (0, 2, 6, 4), (9, 42, 0, 0), (63, 61, 9, 8), (41, 39, 0, 1), (15, 16, 1, 2), (15, 15, 1, 1)])
    def test_add_walls_invalid_walls_not_created(self, mock_maze_empty: Maze, index1: int, index2: int, correct_value1, correct_value2):
        GenerationAlgorithm.add_walls(mock_maze_empty[index1], mock_maze_empty[index2])

        assert mock_maze_empty[index1].walls == correct_value1
        assert mock_maze_empty[index2].walls == correct_value2

class TestMazeNode:
    def test_all_walls_filled_direct(self, maze_node_all_walls: MazeNode):
        assert maze_node_all_walls.walls == 15

    def test_left_bottom_walls_filled_direct(self, maze_node_l_b_walls: MazeNode):
        assert maze_node_l_b_walls.walls == 6
    
    @pytest.mark.parametrize("key", [("top"), ("bottom"), ("left"), ("right")])
    def test_get_current_walls_all_walls_case(self, maze_node_all_walls: MazeNode, key: str):
        assert maze_node_all_walls.get_current_walls()[key] == True
    
    @pytest.mark.parametrize("key, value", [("top", False), ("bottom", True),
     ("left", True), ("right", False)])
    def test_get_current_walls_l_b_walls_case(self, maze_node_l_b_walls: MazeNode,
     key: str, value: bool):
        assert maze_node_l_b_walls.get_current_walls()[key] == value
