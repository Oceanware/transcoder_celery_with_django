import concurrent.futures as cf
import time


def toUpper(i):
    return i.upper()


# with concurrent.futures as cf:
start = time.time()
with cf.ThreadPoolExecutor() as executor:
    print([i for i in executor.map(toUpper, ['hello', 'world', 'hello', 'world'])])
end = time.time()

print(end - start)

print('-----------------------------------------------------')

start = time.time()
# without concurrent.futures as cf:
print([toUpper(x) for x in ['hello', 'world', 'hello', 'world']])
end = time.time()

print(end - start)

