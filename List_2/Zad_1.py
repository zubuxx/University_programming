def Easter_date(year):
    a = year % 19
    b = int(year/100)  # zaokrąglenie w dół
    c = year % 100
    d = int(b / 4)
    e = b % 4
    f = int((b+8) / 25)
    g = int((b-f+1)/3)
    h = (19*a+b-d-g+15)%30
    i = int(c/4)
    k = c % 4
    l = (32+2*e+2*i-h-k)%7
    m = int((a+11*h+22*l)/451)
    p = (h+l-7*m+114)%31
    day = p+1
    month = int((h+l-7*m+114)/31)
    ls = ['', '','', 'Marzec', 'Kwiecień']
    return f"Data wigilii: \n{day} {ls[month]}"


if __name__ == '__main__':
    print(Easter_date(2020))