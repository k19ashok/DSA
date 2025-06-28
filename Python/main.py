from time import perf_counter_ns
from timeit import timeit
from dictionary import Dict

def test_basic_functionality():
    t1 = perf_counter_ns()
    d = Dict()

    for i in range(1000):
        d[i] = str(i)

    print(d[56])
    print(d[789])
    print(d.get(555555555))
    print(d.keys())
    print(d.values())
    print(d.items())
    t2 = perf_counter_ns()

    ta = t2 - t1

    t1 = perf_counter_ns()
    d = dict()

    for i in range(1000):
        d[i] = str(i)

    print(d[56])
    print(d[789])
    print(d.get(555555555))
    print(d.keys())
    print(d.values())
    print(d.items())
    t2 = perf_counter_ns()

    td = t2 - t1

    print("Total time in ns by dict: ", td)
    print("Total time in ns by our dict: ", ta)
    print("Difference in ns: time taken by dict - time taken by Dict = ", td)


def analyse_timing():
    ad = timeit(
        """
d = Dict()
for i in range(1000):
    d[i] = str(i)
x = d[56]
x = d[789]
x = d.get(555555555)
x = d.keys()
x = d.values()
x = d.items()
        """,
        number=10000,
        globals={
            "Dict": Dict
        }
    )

    pd = timeit(
        """
d = dict()
for i in range(1000):
    d[i] = str(i)
d[56]
d[789]
d.get(555555555)
d.keys()
d.values()
d.items()
        """,
        number=10000
    )

    print("Dict: ", ad, "dict: ", pd, "seconds")


analyse_timing()