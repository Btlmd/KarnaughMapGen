from tqdm import tqdm
from itertools import product
import os
from qmc import QuineMcCluskey
from multiprocessing import Queue, Manager, Pool
from time import sleep
from copy import deepcopy

"""
    bits: number of variables
    root: the path to generate the table
    reverse: when set to True, A denotes the lowest bit
"""
bits = 4
root = "E:\\Kmap4bf\\"
reverse = True


def exec_buffer(_f_buf, _d_buf):
    # print("Dumping", len(_f_buf), "files ...")
    for _d in _d_buf:
        if not os.path.exists(_d):
            os.makedirs(_d)
    for k, v in _f_buf.items():
        with open(k, "a") as f:
            f.write(v)


def calc(prelude, iterator, q: Queue):
    buffer = {}
    directory_buffer = set()
    prev = 0
    for cnt, o_expr in iterator:
        o_expr = tuple(list(prelude) + list(o_expr))

        expr = list(enumerate(o_expr))
        f_minimum = list(filter(lambda x: x[1] == 1, expr))
        f_arbitrary = list(filter(lambda x: x[1] == 2, expr))

        if len(f_minimum) <= 1:
            continue

        in_minimum = [e[0] for e in f_minimum]
        in_arbitrary = [e[0] for e in f_arbitrary]

        out_minimum = [str(e[0]) for e in f_minimum]
        out_arbitrary = [str(e[0]) for e in f_arbitrary]

        step = 4
        assert 2 ** bits % step == 0

        splits = []
        for i in range(2 ** bits)[::step][:-1]:
            splits += [
                "".join(map(str, o_expr[i: i + step]))
                    .replace('2', 'X')
            ]
        directory = root + '\\'.join(splits[:-1])
        path = directory + "\\" + splits[-1] + ".md"

        # print(out_minimum, out_arbitrary)

        _, result = QuineMcCluskey() \
            .find_result(in_minimum, in_arbitrary, bits)

        TOC = f"\n- min:{' '.join(out_minimum)}; "
        TOC += f"arb:{' '.join(out_arbitrary)}; "
        TOC += f"$F={result}$\n"

        if path in buffer:
            buffer[path] += TOC
        else:
            buffer[path] = TOC
        directory_buffer.add(directory)

        if (cnt + 1) % (3 ** 7) == 0:
            exec_buffer(buffer, directory_buffer)
            buffer = {}
            directory_buffer = set()
            q.put(cnt - prev)
            prev = cnt

    exec_buffer(buffer, directory_buffer)
    q.put(None)


if __name__ == "__main__":
    prelude_log = 3
    preludes = list(product(*(((0, 1, 2),) * prelude_log)))
    print(len(preludes))
    iterator = enumerate(product(*(((0, 1, 2),) * ((2 ** bits) - prelude_log))))
    Q = Manager().Queue()
    with tqdm(total=3 ** (2 ** bits)) as t:
        with Pool() as p:
            returns = 0
            groups = [(pl, deepcopy(iterator), Q) for pl in preludes]
            grp = p.starmap_async(calc, groups)
            while returns != 3:
                sleep(0.5)
                while not Q.empty():
                    q = Q.get()
                    if type(q) == int:
                        t.update(q)
                    else:
                        returns += 1
