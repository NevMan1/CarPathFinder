#This one is solid
import math
from queue import PriorityQueue
def valid_neighbors(pos,car_positions, map):
        x, y = pos
        return (0 <= x < len(map) and 0 <= y < len(map[0]) and
                map[x][y] != 'wall' and pos not in car_positions)
def neighbors(pos, car_positions, map):
        directions = {'W': (0, -1), 'A': (-1, 0), 'S': (0, 1), 'D': (1, 0)}
        neighbors = []
        for direction, (x_change, y_change) in directions.items():
            neighbor = (pos[0] + x_change, pos[1] + y_change)
            if valid_neighbors(neighbor, car_positions, map):
                neighbors.append((direction, neighbor))
        return neighbors
def manhatten(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
def a_star(start, goal, car_positions, map):
        open_set = PriorityQueue()
        open_set.put((0, start))
        previous = {}
        score = {start: 0}

        while not open_set.empty():
            _, current = open_set.get()

            if current == goal:
                
                path = []
                while current in previous:
                    path.append(previous[current][1])  
                    current = previous[current][0]
                return path

            for direction, neighbor in neighbors(current, car_positions, map):
                possible = score[current] + 1
                if neighbor not in score or possible < score[neighbor]:
                    score[neighbor] = possible
                    priority = possible + manhatten(neighbor, goal)
                    open_set.put((priority, neighbor))
                    previous[neighbor] = (current, direction)

        return None  

def logic_A(map, position, coins, car_positions, penalty_k):
    if not hasattr(logic_A, "state"):
        logic_A.state = 'collecting_coins'
        logic_A.initial_coin_count = len(coins)  

    x, y = position

   
    goals = [
        (gx, gy)
        for gx in range(len(map))
        for gy in range(len(map[0]))
        if map[gx][gy] == 'goal'
    ]

    
    area_min_x, area_max_x = max(0, x - 3), min(len(map) - 1, x + 4)
    area_min_y, area_max_y = max(0, y - 3), min(len(map[0]) - 1, y + 4)

   
    no_coins_in_5x5_area = not any(
        (area_min_x <= cx <= area_max_x and area_min_y <= cy <= area_max_y)
        for cx, cy in coins
    )

    
    remaining_coins_ratio = len(coins) / logic_A.initial_coin_count

    
    if no_coins_in_5x5_area or remaining_coins_ratio <= 0.3:
        logic_A.state = 'going_to_goal'
    else:
        logic_A.state = 'collecting_coins'

    
    if logic_A.state == 'collecting_coins':
        def coin_priority(coin):
            distance_to_player = manhatten(position, coin)
            distance_to_nearest_goal = min(manhatten(coin, goal) for goal in goals)
            obstacle_penalty = sum(1 for _, neighbor in neighbors(coin, car_positions, map) if map[neighbor[0]][neighbor[1]] == 'wall')
            
            goal_incentive = 1 / (1 + math.exp(-0.1 * (distance_to_nearest_goal - 5))) 
            
            return (
                distance_to_player 
                - penalty_k * distance_to_nearest_goal 
                + goal_incentive 
                + obstacle_penalty * 0.5
            )


        targets = sorted(coins, key=coin_priority)
    else:
        targets = goals

    
    best_path_set = None
    for target in targets:
        path = a_star(position, target, car_positions, map)
        if path:
            if best_path_set:
                best_path_set = min([best_path_set, path], key=len)
            else:
                best_path_set = path

    
    if best_path_set:
        return best_path_set[-1]
    else:
        return 'I'