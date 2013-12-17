
debug = True

def err(x):
    print(x)


if debug:
    def out(x):
        print(x)

    def out2(a,x):
        print("{:24} {!s}".format(a+':',x))

else:
    def out(x):
        pass

    def out2(a,x):
        pass
