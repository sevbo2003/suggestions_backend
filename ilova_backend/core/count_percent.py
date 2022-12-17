def count_percent(a,b):
    if a < b:
        if a != 0:
            return "down: " + str(int((a/b)*100))
        else:
            return "down: " + str(100 * b) if b != 0 else 0
    else:
        if b != 0:
            return "up: " + str(float((b/a)*100))
        else:
            return "up: " + str(100 * a) if a != 0 else 0