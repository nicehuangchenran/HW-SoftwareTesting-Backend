host_price = 25
max_host_num = 70
monitor_price = 30
max_monitor_num = 80
peripheral_price = 45
max_peripheral_num = 90


def computer(host: int, monitor: int, peripheral: int):
    if host <= 0:
        return "host must be positive"
    elif host > max_host_num:
        return "host exceeded"

    if monitor <= 0:
        return "monitor must be positive"
    elif monitor > max_monitor_num:
        return "monitor exceeded"

    if peripheral <= 0:
        return "peripheral must be positive"
    elif peripheral > max_peripheral_num:
        return "peripheral exceeded"

    sale_volume = host * host_price + monitor * monitor_price + peripheral * peripheral_price
    proportion = 0.0

    if sale_volume <= 1000:
        proportion = 0.1
    elif 1000 < sale_volume <= 1800:
        proportion = 0.15
    elif sale_volume > 1800:
        proportion = 0.2

    return str(sale_volume * proportion)


if __name__ == "__main__":
    print(computer(13, 26, 40))
