from collections import deque
n, d = map(int, input().split())
points = []
for _ in range(n):
        x, y = map(int, input().split())
        points.append((x, y))
ans=float('inf')
points.sort(key=lambda x: x[0])
stack1=deque(points[0])
stack2=deque([points[0]])
left=0
for i in range(n):
    while stack1 and stack1[-1][1]<=points[i][1]:
        stack1.pop()
    while stack2 and stack2[-1][1]>=points[i][1]:
        stack2.pop()
    stack1.append(points[i])
    stack2.append(points[i])
    while stack1 and stack2 and stack1[0][1]-stack2[0][1]>=d:
         if stack1[0][0]-stack2[0][0]<ans:
             ans=stack1[0][0]-stack2[0][0]
         x_left=points[left][0]
         while stack1 and stack1[0][0]<=x_left:
             stack1.popleft()
         while stack2 and stack2[0][0]<=x_left:
             stack2.popleft()
         left+=1
if ans==float('inf'):
    print(-1)
else:
    print(ans)
         


        