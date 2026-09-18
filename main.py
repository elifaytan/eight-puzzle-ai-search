import sys
import numpy as np
import heapq
import time

# Puzzle durumunu temsil eden sınıf. Her bir adım bir nesneyle tanımlanır.
class puzzle_state:
    def __init__(self, state, previous_state=None, moves=0, direction="", kind_of_heuristic=0, goal_state=None):
        self.previous_state = previous_state              # Bu adımın geldiği önceki adım
        self.state = np.array(state)                      # Puzzle'ın şu anki durumu (tek boyutlu)
        self.moves = moves                                # Şu ana kadar yapılan hamle sayısı
        self.direction = direction                        # Bu duruma hangi yönde gelindi
        self.kind_heuristic = kind_of_heuristic           # Heuristik tipi (1: Manhattan, 2: Euclidean)
        self.goal_state = np.array(goal_state) if goal_state is not None else np.arange(9)
        self.cost = 0                                     # A* için toplam maliyet (g + h)

    # Bu adım hedef durum mu?
    def check_for_goal(self):
        return np.array_equal(self.state, self.goal_state)

    # A* için karşılaştırma (heapq kullanımında gereklidir)
    def __lt__(self, other_state):
        return self.cost < other_state.cost


# Puzzle'daki geçerli hareketleri yöneten sınıf
class movement:
    def __init__(self, visited):
        self.visited = visited
        self.space_index = self.find_space_index()  # 0 (boşluk) hangi konumda onu bul

    def find_space_index(self):
        for i in range(9):
            if self.visited.state[i] == 0:
                return i
        return -1

    # Verilen iki indeksin yerini değiştirerek yeni bir durum üretir
    def swap_places(self, element1, element2):
        temp_state = np.array(self.visited.state)
        temp_state[element1], temp_state[element2] = temp_state[element2], temp_state[element1]
        return temp_state

    # Her biri geçerli ise yeni bir puzzle_state nesnesi döner
    def move_up(self):
        if self.space_index > 2:
            return puzzle_state(
                self.swap_places(self.space_index, self.space_index - 3),
                self.visited, self.visited.moves + 1, "UP",
                self.visited.kind_heuristic, self.visited.goal_state)
        return None

    def move_down(self):
        if self.space_index < 6:
            return puzzle_state(
                self.swap_places(self.space_index, self.space_index + 3),
                self.visited, self.visited.moves + 1, "DOWN",
                self.visited.kind_heuristic, self.visited.goal_state)
        return None

    def move_left(self):
        if self.space_index % 3 != 0:
            return puzzle_state(
                self.swap_places(self.space_index, self.space_index - 1),
                self.visited, self.visited.moves + 1, "LEFT",
                self.visited.kind_heuristic, self.visited.goal_state)
        return None

    def move_right(self):
        if self.space_index % 3 != 2:
            return puzzle_state(
                self.swap_places(self.space_index, self.space_index + 1),
                self.visited, self.visited.moves + 1, "RIGHT",
                self.visited.kind_heuristic, self.visited.goal_state)
        return None

    # Geçerli komşu durumların listesini döner
    def find_neighbours(self):
        return list(filter(None, [self.move_up(), self.move_down(), self.move_left(), self.move_right()]))


# Bir puzzle durumunu string olarak tanımlayan yardımcı fonksiyon
def createid(x):
    return str(x)


# Çözüm algoritmalarını (BFS, DFS, A*) barındıran ana sınıf
class puzzle_solver:
    def __init__(self, goal_state):
        self.solved_puzzle = None
        self.total_cost = 0
        self.nodes_expanded = 0
        self.goal_state = np.array(goal_state)

    # Derinlik öncelikli arama
    def dfs_search(self, puzzle):
        frontierqueue = {}
        explored = {}
        frontierqueue[createid(puzzle.state)] = puzzle
        while frontierqueue:
            visited = frontierqueue.popitem()[1]
            explored[createid(visited.state)] = visited
            if visited.check_for_goal():
                self.solved_puzzle = visited
                self.nodes_expanded = len(explored) - 1
                return
            for neighbour in reversed(movement(visited).find_neighbours()):
                sid = createid(neighbour.state)
                if sid not in explored and sid not in frontierqueue:
                    frontierqueue[sid] = neighbour

    # Genişlik öncelikli arama
    def bfs_search(self, puzzle):
        frontierqueue = {}
        explored = {}
        frontierorg = []
        frontierqueue[createid(puzzle.state)] = puzzle
        frontierorg.append(puzzle)
        while frontierqueue:
            visited = frontierorg.pop(0)
            frontierqueue.pop(str(visited.state))
            explored[createid(visited.state)] = visited
            if visited.check_for_goal():
                self.solved_puzzle = visited
                self.nodes_expanded = len(explored)
                return
            for neighbour in movement(visited).find_neighbours():
                sid = createid(neighbour.state)
                if sid not in explored and sid not in frontierqueue:
                    frontierqueue[sid] = neighbour
                    frontierorg.append(neighbour)

    # A* arama algoritması
    def A_star_search(self, puzzle):
        neighbours_heap = []
        explored_states_list = []
        puzzle.cost = puzzle.moves + (self.euclidean_cost(puzzle) if puzzle.kind_heuristic == 2 else self.manhatten_cost(puzzle))
        heapq.heappush(neighbours_heap, puzzle)
        while neighbours_heap:
            least_cost_state = heapq.heappop(neighbours_heap)
            explored_states_list.append(least_cost_state)
            if least_cost_state.check_for_goal():
                self.solved_puzzle = least_cost_state
                self.nodes_expanded = len(explored_states_list) - 1
                return
            for neighbour in movement(least_cost_state).find_neighbours():
                if not any(np.array_equal(neighbour.state, i.state) for i in explored_states_list):
                    neighbour.cost = neighbour.moves + (self.euclidean_cost(neighbour) if neighbour.kind_heuristic == 2 else self.manhatten_cost(neighbour))
                    heapq.heappush(neighbours_heap, neighbour)

    # Manhattan uzaklığına dayalı heuristik maliyeti hesaplar
    def manhatten_cost(self, puzzle):
        state = puzzle.state
        goal = puzzle.goal_state
        cost = 0
        for val in range(1, 9):
            pos1 = np.where(state == val)[0][0]
            pos2 = np.where(goal == val)[0][0]
            cost += abs(pos1 // 3 - pos2 // 3) + abs(pos1 % 3 - pos2 % 3)
        return cost

    # Öklid uzaklığına dayalı heuristik maliyeti hesaplar
    def euclidean_cost(self, puzzle):
        state = puzzle.state
        goal = puzzle.goal_state
        cost = 0
        for val in range(1, 9):
            pos1 = np.where(state == val)[0][0]
            pos2 = np.where(goal == val)[0][0]
            cost += np.sqrt((pos1 // 3 - pos2 // 3) ** 2 + (pos1 % 3 - pos2 % 3) ** 2)
        return cost

    # Hedefe ulaşan adım listesini çıkarır
    def get_best_path(self):
        path_list_array = []
        path_list_objects = []
        current_state = self.solved_puzzle
        while current_state:
            path_list_objects.append(current_state)
            path_list_array.append(current_state.state)
            current_state = current_state.previous_state
        return list(reversed(path_list_array)), list(reversed(path_list_objects))

    # İzlenen yönlerin listesini döner
    def get_goal_directions(self):
        _, path_obj_list = self.get_best_path()
        return [item.direction for item in path_obj_list if item.direction]

    # Hedefe ulaşmak için gereken toplam adım sayısı
    def get_total_cost(self):
        _, path_list_obj = self.get_best_path()
        return len(path_list_obj) - 1


# Ana fonksiyon: kullanıcıdan giriş alır ve çözüm algoritmasını çalıştırır
def main():
    goal_state = [1, 2, 3, 8, 0, 4, 7, 6, 5]  # Belirlenen özel hedef durumu
    initial_state = [0] * 9
    print("*" * 50, "welcome to 8-puzzle game", "*" * 50)

    while True:
        print("please enter initial state ::")
        for i in range(9):
            initial_state[i] = int(input(f"Tile {i+1}: "))
        print("Entered state:")
        for i in range(9):
            print(initial_state[i], end=" ")
            if (i + 1) % 3 == 0:
                print()

        puzzle_helper = puzzle_solver(goal_state)

        print("*" * 50)
        print("select the algorithm to solve the puzzle ::")
        print("1- BFS\n2- DFS\n3- A*\n4- exit")
        choice = int(input())

        if choice == 4:
            break

        heauristic_choice = 0
        if choice == 3:
            print("please choose the heuristic function to be used ::")
            print("1- manhatten\n2- euclidean")
            heauristic_choice = int(input())

        puzzle = puzzle_state(initial_state, None, 0, "", heauristic_choice, goal_state)

        print("*" * 50)

        if choice == 1:
            print("you chose BFS algorithm")
            t0 = time.time()
            puzzle_helper.bfs_search(puzzle)
            t1 = time.time()
        elif choice == 2:
            print("you chose DFS algorithm")
            t2 = time.time()
            puzzle_helper.dfs_search(puzzle)
            t3 = time.time()
        elif choice == 3:
            print("you chose A* algorithm")
            t4 = time.time()
            puzzle_helper.A_star_search(puzzle)
            t5 = time.time()
        else:
            print("Invalid choice.")
            continue

        print("solving the puzzle please wait....")
        path, _ = puzzle_helper.get_best_path()

        print("path taken to reach goal >>")
        for step_index, step in enumerate(path):
            print(f"\nStep {step_index}:")
            for i in range(0, 9, 3):
                print(step[i:i + 3])

        print("\ndirection taken to reach goal >> ", puzzle_helper.get_goal_directions())
        print("goal reached >> ")
        for i in range(0, 9, 3):
            print(puzzle_helper.solved_puzzle.state[i:i+3])
        print("total cost to reach goal is ", puzzle_helper.get_total_cost())
        print("nodes expanded >> ", puzzle_helper.nodes_expanded)
        print("depth is ", puzzle_helper.solved_puzzle.moves)

        if choice == 1:
            print("running time of BFS is >> {} secs".format(t1 - t0))
        elif choice == 2:
            print("running time of DFS is >> {} secs".format(t3 - t2))
        elif choice == 3:
            print("running time of A* is >> {} secs".format(t5 - t4))

        print("*" * 50)


if __name__ == "__main__":
    main()
