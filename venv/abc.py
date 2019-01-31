a=True

def b():
    global a
    b=a
    print(b)
    a=False

b()
print(a)