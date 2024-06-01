def calendar(y: int, m: int, d: int):
    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    if y < 2000:
        return "year is lower than 2000"
    elif y > 2100:
        return "year exceeded"

    if m <= 0:
        return "month is lower than 1"
    elif m > 12:
        return "month exceeded"

    if_leap_year = (y % 400 == 0 or ((y % 4 == 0) and (y % 100 != 0)))
    month_days[1] += (1 if if_leap_year else 0)

    if d <= 0:
        return "day is lower than 1"
    elif d > month_days[m - 1]:
        return "day exceeded"

    ret_y = y
    ret_m = m
    ret_d = d

    if d == month_days[m - 1]:
        if m == 12:
            ret_y += 1
            ret_m = 1
            ret_d = 1
        else:
            ret_m += 1
            ret_d = 1
    else:
        ret_d += 1

    return f"{ret_y}/{ret_m}/{ret_d}"


if __name__ == "__main__":
    print(calendar(2000, 2, 29))
