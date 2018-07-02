import re

strs = ['A64 Dword SIMD4x2 Untyped Atomic Integer Binary Write Only Operation MSD ....... 304',
        'A64 Dword SIMD4x2 Untyped Atomic Integer Binary Write Only Operation MSD ....... 304 ',
        'A64 Dword SIMD4x2 Untyped Atomic Integer Binary Write Only Operation MSD .......304',
       'A64 Dword SIMD4x2 Untyped Atomic Integer Trinary with Return Data Operation MSD305',
       'A64 Dword SIMD4x2 Untyped Atomic Integer Trinary with Return Data Operation MSD 305',
       'A64 Dword SIMD4x2 Untyped Atomic Integer Trinary with Return Data Operation MSD',
       'A64 Dword SIMD4x2 Untyped Atomic Integer Binary Write Only Operation MSD ....... ',
       'A64 Dword SIMD4x2 Untyped Atomic Integer Binary Write Only Operation MSD '
       ]

#print(str[0])

def get_number(str):
    #print("get_number: [{}]".format(str))
    p = re.compile(r'\d+$')
    i = p.search(str.rstrip())

    if i is not None:
        ss = str[0:i.span()[0]]
        number = int(str[i.span()[0]:i.span()[1]])
        # print(ss, number)
        return ss.rstrip(), number
    else:
        return None, None

def get_title(str):
    #print("get_title2: [{}]".format(str))
    #p = re.compile(r'\s*\.+\s*$')
    p = re.compile(r'\s*\.+$')
    i = p.search(str)
    has_dot = False
    if i is not None:
        ss = str[0:i.span()[0]]
        has_dot = True
        # print(ss, number)
        return ss, has_dot
    else:
        return str, has_dot

def parse_line(str):
    s, num = get_number(str)
    has_dot = False
    if s is not None:
        s, has_dot = get_title(s)
        #print("({}),({}),({})".format(s, num, has_dot))
    return s, num, has_dot

def get_title_simple(str):
    p = re.compile(r'\.+\s+$')
    a = p.split(str)
    print(a)

def do_test():
    for i in strs:
        print(get_number(i))


def do_test2():
    for i in strs:
        get_title_simple(i)


def do_test3():
     for i in strs:
        s, num = get_number(i)
        has_dot = False
        if s is not None:
            s, has_dot = get_title(s)
            print("({}),({}),({})".format(s, num, has_dot))


def do_test4():
    for i in strs:
        s, num, has_dot = parse_line(i)
        print(s, num, has_dot)
    pass


if __name__ == '__main__':
    #do_test()
    #do_test2()
    #do_test3()

    #do_test4()
    do_test4()
