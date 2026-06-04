
def main():
    first_line = input().strip()
    if not first_line:
        return None
    n, w = map(int, first_line.split())
    items = []
    for i in range(n):
        line = input().strip()
        if not line:
            continue
        value, weight = map(int, line.split())
        average = value / weight
        items.append((average,value, weight))
    ans=0
    items.sort(reverse=True, key=lambda x: x[0])  # Sort by average value in descending order
    for average, value, weight in items:
        if w <= 0:
            break
        if weight <= w:
            ans += value
            w -= weight
        else:
            ans += average * w
            break
    return ans
if __name__ == "__main__":
    result = main()
    if result is not None:
        print("{0:.1f}".format(result))
    

        
