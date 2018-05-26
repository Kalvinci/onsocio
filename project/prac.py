def change(number):
    a=str(number)
    c=a
    b=len(a)
    if b >= 7:
        if a[1] == '0':
            c = a[0:1] + 'M'
        else:
            c = a[0:1] + '.' + a[1:2] + 'M'
    elif b>=6:
        c=a[0:3]+'K'
    elif b>=5:
        c=a[0:2]+'K'
    elif b>=4:
        c=a[0:1]+'K'
    return c



