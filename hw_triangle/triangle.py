def triangle(a, b, c):
    if a < 0:
        return "edge A is negative"
    elif a == 0:
        return "edge A can't be 0"
    elif a > 100:
        return "edge A exceed"

    if b < 0:
        return "edge B is negative"
    elif b == 0:
        return "edge B can't be 0"
    elif b > 100:
        return "edge B exceed"

    if c < 0:
        return "edge C is negative"
    elif c == 0:
        return "edge C can't be 0"
    elif c > 100:
        return "edge C exceed"

    if not (a + b > c and a + c > b and b + c > a):
        return "not a triangle"

    if a == b and b == c:
        return "equilateral triangle"
    elif a == b or a == c or b == c:
        return "isosceles triangle"
    else:
        return "normal triangle"


if __name__ == "__main__":
    data = input().split(' ')
    e1 = int(data[0])
    e2 = int(data[1])
    e3 = int(data[2])
    print(triangle(e1, e2, e3))