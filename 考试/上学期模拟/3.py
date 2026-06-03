
import sys

def simplify_path(path: str) -> str:
    parts = path.split('/')
    stack = []
    for part in parts:
        if part == '' or part == '.':
            continue
        elif part == '..':
            if stack:
                stack.pop()
        else:
            stack.append(part)
    return '/' + '/'.join(stack)

def main():
    path = sys.stdin.readline().strip()
    print(simplify_path(path))

if __name__ == "__main__":
    main()