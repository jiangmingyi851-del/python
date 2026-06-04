

    
# def can_line(matrix,n):
#     black_cells=[]
#     for i in range(n):
#         for j in range(n):
#             if matrix[i][j]==1:
#                 black_cells.append((i,j))
#     if not black_cells or len(black_cells)==1:
#         return True
#     x_0,y_0=black_cells[0]
#     left_down0=0
#     left_down1=0
#     right_down0=0
#     right_down1=0
#     left=0
#     right=0
#     if len(black_cells)==4 and x_0<n-1 and y_0<n-1 and matrix[x_0+1][y_0]==1 and matrix [x_0+1][y_0+1]==1 and matrix[x_0 ][y_0+1]==1:
#         return True
#     if x_0<n-1 and matrix[x_0+1][y_0]==1:
#         x_0,y_0=x_0+1,y_0
#     for x,y in black_cells[1:]:
#         a=x-x_0
#         b=y-y_0
#         if abs(abs(a)-abs(b))>1:
#             return False
#         elif a<0:
#             right+=1
#         elif b<0:
#             left+=1
#             if a+b<0:
#                 left_down0+=1
#             elif a+b>0:
#                 left_down1+=1
#         elif b>0:
#             right+=1
#             if a-b<0:
#                 right_down0+=1
#             elif a-b>0:
#                 right_down1+=1
#         else:
#             if a!=0:
#                 return False
#     if left>0 and right>0:
#         return False
#     if left_down0>0 and left_down1>0:
#         return False
#     if right_down0>0 and right_down1>0:
#         return False
#     return True
    

t=int(input())
for i in range(t):
    n=int(input())
    matrix=[[0]*n for i in range(n)]
    max_1=float('-inf')
    max_2=float('-inf')
    min_1=float('inf')
    min_2=float('inf')
    count=0
    queue=[]
    for i in range(n):
        li=input()
        for j,s in enumerate(li):
            if s=='#':
                max_1=max(max_1,i+j)
                min_1=min(min_1,i+j)
                max_2=max(max_2,i-j)
                min_2=min(min_2,i-j)
                count+=1
                queue.append((i,j))
    if abs(max_1-min_1)<=1 or abs(max_2-min_2)<=1:
        print("Yes")
    else:
        if count==0:
            print("Yes")
        elif count==4:
            max_x=0
            max_y=0
            min_x=n-1
            min_y=n-1
            for x ,y in queue:
                max_y=max(y,max_y)
                min_x=min(x,min_x)
                min_y=min(y,min_y)
                max_x=max(x,max_x)
            if max_x-min_x==1 and max_y-min_y==1:
                print("Yes")
            else:
                print('No') 
        else:
            print("No")
            
        
