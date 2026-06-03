'''heapq 模块
heapq 模块提供了堆队列算法的实现，也称为优先队列算法。堆是一个二叉树，每个父节点的值都小于或等于其任何子节点的值（最小堆）。'''
# 1. 导入 heapq 模块
import heapq

# 创建空堆
heap = []

# 添加元素
heapq.heappush(heap, 3)
heapq.heappush(heap, 1)
heapq.heappush(heap, 2)
print(heap)  # [1, 3, 2] (堆顶是最小元素)

#2. 弹出最小元素
min_elem = heapq.heappop(heap)
print(min_elem)  # 1
print(heap)      # [2, 3]

# 3. 查看堆顶元素
min_elem = heap[0]
print(min_elem)  # 2
# 4. 堆排序
unsorted_list = [5, 3, 8, 1, 2]
heapq.heapify(unsorted_list)  # 将列表转换为堆
sorted_list = [heapq.heappop(unsorted_list) for _ in range(len(unsorted_list))]
print(sorted_list)  # [1, 2, 3, 5, 8]
# 5. 合并多个已排序的输入流
list1 = [1, 4, 7]
list2 = [2, 5, 8]
list3 = [3, 6, 9]
merged = list(heapq.merge(list1, list2, list3))
print(merged)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]
# 6. 查找前 k 个最小元素
nums = [5, 1, 8, 3, 2]
k = 3
smallest_k = heapq.nsmallest(k, nums)
print(smallest_k)  # [1, 2, 3]
# 7. 查找前 k 个最大元素
largest_k = heapq.nlargest(k, nums)
print(largest_k)  # [8, 5, 3]
# 8. 自定义排序
class Item:
    def __init__(self, name, priority):
        self.name = name
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority
item1 = Item("task1", 3)
item2 = Item("task2", 1)
item3 = Item("task3", 2)
heap = []
heapq.heappush(heap, item1)
heapq.heappush(heap, item2)
heapq.heappush(heap, item3)
while heap:
    item = heapq.heappop(heap)
    print(item.name, item.priority)
# 输出：
# task2 1
# task3 2
# task1 3

# 9. 实现优先队列
class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        heapq.heappush(self.heap, (priority, self.count, item))
        self.count += 1

    def pop(self):
        return heapq.heappop(self.heap)[-1]

    def is_empty(self):
        return len(self.heap) == 0
pq = PriorityQueue()
pq.push("task1", 3)
pq.push("task2", 1)
pq.push("task3", 2)
while not pq.is_empty():
    print(pq.pop())
# 输出：
# task2
# task3
# task1
#10. 实现 Dijkstra 算法
def dijkstra(graph, start):
    heap = []
    heapq.heappush(heap, (0, start))
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    while heap:
        current_distance, current_node = heapq.heappop(heap)
        if current_distance > distances[current_node]:
            continue
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(heap, (distance, neighbor))
    return distances
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}
start_node = 'A'
distances = dijkstra(graph, start_node)
print(distances)  # {'A': 0, 'B': 1, 'C': 3, 'D': 4}
print("行驶")
  