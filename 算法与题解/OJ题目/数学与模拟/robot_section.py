import sys
M=10**9

def main():
    t=int(sys.stdin.readline().strip())
    for _ in range(t):
        n=int(sys.stdin.readline().strip())
        anchors=[]
        for i in range(n):
            x,y=map(int,sys.stdin.readline().strip().split())
            anchors.append((x,y))
        r_u=min(2*M-x-y for x,y in anchors)
        r_d=min(x-y for x,y in anchors)
        print("?R",M)
        sys.stdout.flush()
        s1=int(sys.stdin.readline().strip())
        if s1==-1:
            return
        
        print("?R",M)
        sys.stdout.flush()
        s2=int(sys.stdin.readline().strip())
        if s2==-1:
            return
        
        print("?U",M)
        sys.stdout.flush()
        s3=int(sys.stdin.readline().strip())
        if s3==-1:
            return
        
        print("?U",M)
        sys.stdout.flush()
        s4=int(sys.stdin.readline().strip())
        if s4==-1:
            return
        
        print("D?",M)
        sys.stdout.flush()
        d1=int(sys.stdin.readline().strip())
        if d1==-1:
            return
        
        print("D?",M)
        sys.stdout.flush()
        d2=int(sys.stdin.readline().strip())
        if d2==-1:
            return
        
        print("D?",M)
        sys.stdout.flush()
        d3=int(sys.stdin.readline().strip())
        if d3==-1:
            return
        
        print("D?",M)
        sys.stdout.flush()
        d4=int(sys.stdin.readline().strip())
        if d4==-1:
            return
        x_plus_y=s4-r_u-2*M
        x_minus_y=d4-r_d
        x=(x_plus_y+x_minus_y)//2
        y=(x_plus_y-x_minus_y)//2
        print("! {} {}".format(x,y))
        sys.stdout.flush()

if __name__ == "__main__":
    main()

