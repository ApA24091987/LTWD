import random
from typing import List, Tuple, Set


class Animal:
    symbol = ''

    def can_defeat(self, other: 'Animal') -> bool:
        return False

    def __str__(self):
        return self.symbol


class Deer(Animal):
    symbol = 'D'


class Wolf(Animal):
    symbol = 'W'

    def can_defeat(self, other: Animal) -> bool:
        return isinstance(other, Deer)


class Tiger(Animal):
    symbol = 'T'

    def can_defeat(self, other: Animal) -> bool:
        return isinstance(other, (Wolf, Deer))


class Lion(Animal):
    symbol = 'L'

    def can_defeat(self, other: Animal) -> bool:
        return isinstance(other, (Tiger, Wolf, Deer))


class SafariField:
    def __init__(self, size=10):
        self.size = size
        self.board = self._populate_board()
        self.conquered = set()

    def _populate_board(self) -> List[List[Animal]]:
        """Создает случайное поле с животными"""
        animal_types = [Deer, Wolf, Tiger, Lion]
        return [[random.choice(animal_types)() for _ in range(self.size)]
                for _ in range(self.size)]

    def display_board(self):
        """Выводит поле в консоль"""
        for row in range(self.size):
            row_str = " "
            for col in range(self.size):
                if (row, col) in self.conquered:
                    row_str += "- "
                else:
                    row_str += f"{self.board[row][col]} "
            print(row_str)

    def pick_random_cell(self) -> Tuple[int, int]:
        """Выбирает случайную клетку"""
        return random.randint(0, self.size - 1), random.randint(0, self.size - 1)

    def find_conquerable_cells(self, start: Tuple[int, int]) -> Set[Tuple[int, int]]:
        """
        Находит все клетки, которые может завоевать животное из стартовой клетки
        используя чистую рекурсию.
        """
        row, col = start
        start_animal = self.board[row][col]
        self.conquered = set()

        def conquer_recursive(r: int, c: int):
            if not (0 <= r < self.size and 0 <= c < self.size):
                return

            if (r, c) in self.conquered:
                return

            if (r, c) == start:

                self.conquered.add((r, c))

                check_neighbors(r, c)
            else:
                target_animal = self.board[r][c]

                if type(target_animal) == type(start_animal):
                    return

                if start_animal.can_defeat(target_animal):
                    self.conquered.add((r, c))

                    check_neighbors(r, c)

        def check_neighbors(r: int, c: int):
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    conquer_recursive(r + dr, c + dc)

        conquer_recursive(row, col)
        return self.conquered


def main():
    field = SafariField()

    print("Board at start:")
    field.display_board()

    start_cell = field.pick_random_cell()
    animal = field.board[start_cell[0]][start_cell[1]]
    print(f"\nChosen cell: [{start_cell[0] + 1},{start_cell[1] + 1}]: {animal}")

    field.find_conquerable_cells(start_cell)

    print("\nBoard after conquer:")
    field.display_board()

    print(f"\nTotal conquered cells: {len(field.conquered)}")


if __name__ == "__main__":
    main()
