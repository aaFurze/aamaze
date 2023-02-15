from typing import List

import pytest

from src.base_maze import GenerationAlgorithm, Maze, MazeNode


class MockGenerationAlgorithm(GenerationAlgorithm):
    @classmethod
    def generate_maze(cls, maze_body: List[MazeNode]) -> List[MazeNode]:
        return maze_body



@pytest.fixture
def mock_maze() -> Maze:
    return Maze(5, 6)

@pytest.fixture
def maze_node_all_walls() -> MazeNode:
    return MazeNode(2, 4, 0b00001111)

@pytest.fixture
def maze_node_l_b_walls() -> MazeNode:
    return MazeNode(2, 4, 0b00000110)



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
        assert len(mock_maze.get_node_neighbours(x, y)) == expected_count

    @pytest.mark.parametrize("neighbour_index, expected_x, expected_y", [(0, 2, 4), (1, 2, 2),
     (2, 1, 3), (3, 3, 3)])
    def test_get_node_neighbours_first_node_coordinates(self, mock_maze: Maze,
     neighbour_index, expected_x: int, expected_y: int):
        neighbours = mock_maze.get_node_neighbours(2, 3)
        assert neighbours[neighbour_index].x == expected_x
        assert neighbours[neighbour_index].y == expected_y

    @pytest.mark.parametrize("neighbour_index, expected_x, expected_y", [(0, 0, 4), (1, 1, 5)])
    def test_get_node_neighbours_first_node_coordinates_corner(self, mock_maze: Maze,
     neighbour_index, expected_x: int, expected_y: int):
        neighbours = mock_maze.get_node_neighbours(0, 5)
        assert neighbours[neighbour_index].x == expected_x
        assert neighbours[neighbour_index].y == expected_y



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
