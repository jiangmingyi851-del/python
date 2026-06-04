

import sys

class Headquarters:
    def __init__(self, side, energy, costs, priority):
        self.side = side  # 'red' 或 'blue'
        self.energy = energy
        self.costs = costs
        self.priority = priority
        self.counts = {name: 0 for name in priority}
        self.total_count = 0
        self.idx = 0
        self.stopped = False

    def produce(self, time):
        if self.stopped:
            return
        
        # 尝试制造武士
        for i in range(5):
            cur_idx = (self.idx + i) % 5
            name = self.priority[cur_idx]
            cost = self.costs[name]
            
            if self.energy >= cost:
                self.total_count += 1
                self.counts[name] += 1
                self.energy -= cost
                self.idx = (cur_idx + 1) % 5
                
                # 注意格式：time(3位), side, name, total_id, cost, type_count, name, side
                # 严格遵守：...strength 5, 1 iceman in red headquarter
                print(f"{time:03d} {self.side} {name} {self.total_count} born with strength {cost},{self.counts[name]} {name} in {self.side} headquarter")
                return
        
        # 无法制造
        self.stopped = True
        print(f"{time:03d} {self.side} headquarter stops making warriors")

def solve():
    # 使用 fast I/O
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    ptr = 0
    num_cases = int(input_data[ptr])
    ptr += 1
    
    for i in range(1, num_cases + 1):
        # 题目要求格式：Case:n (中间没有空格)
        print(f"Case:{i}")
        
        m = int(input_data[ptr])
        ptr += 1
        
        # 初始生命值顺序: dragon, ninja, iceman, lion, wolf
        raw_costs = [int(x) for x in input_data[ptr:ptr+5]]
        ptr += 5
        
        names = ['dragon', 'ninja', 'iceman', 'lion', 'wolf']
        warrior_costs = {names[j]: raw_costs[j] for j in range(5)}
        
        # 优先级顺序
        red_order = ['iceman', 'lion', 'wolf', 'ninja', 'dragon']
        blue_order = ['lion', 'dragon', 'ninja', 'iceman', 'wolf']
        
        red_hq = Headquarters('red', m, warrior_costs, red_order)
        blue_hq = Headquarters('blue', m, warrior_costs, blue_order)
        
        time = 0
        while not (red_hq.stopped and blue_hq.stopped):
            red_hq.produce(time)
            blue_hq.produce(time)
            time += 1

if __name__ == "__main__":
    solve()