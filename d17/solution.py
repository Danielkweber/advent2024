from typing import List
from tqdm import tqdm
from multiprocessing import Manager, Pool
from functools import partial


class Computer:
    a: int
    b: int
    c: int
    ip: int

    def __init__(self, a, b, c, ip) -> None:
        self.a = a
        self.b = b
        self.c = c
        self.ip = ip

    def translate_combo(self, operand: int) -> int:
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4:
                return self.a
            case 5:
                return self.b
            case 6:
                return self.c
            case _:
                raise Exception

    def adv(self, operand: int) -> None:
        operand_val = 2 ** self.translate_combo(operand)
        self.a //= operand_val

    def bxl(self, operand: int) -> None:
        self.b ^= operand

    def bst(self, operand: int) -> None:
        self.b = self.translate_combo(operand) % 8

    def jnz(self, operand: int) -> bool:
        if self.a == 0:
            return False
        self.ip = operand
        return True

    def bxc(self, operand: int) -> None:
        self.b ^= self.c

    def out(self, operand: int) -> int:
        return self.translate_combo(operand) % 8

    def bdv(self, operand: int) -> None:
        operand_val = 2 ** self.translate_combo(operand)
        self.b = self.a // operand_val

    def cdv(self, operand: int) -> None:
        operand_val = 2 ** self.translate_combo(operand)
        self.c = self.a // operand_val

    def exec_op(self, op: int, operand: int):
        ret = None
        match op:
            case 0:
                ret = self.adv(operand)
            case 1:
                ret = self.bxl(operand)
            case 2:
                ret = self.bst(operand)
            case 3:
                ret = self.jnz(operand)
                self.ip = self.ip - 2 if ret else self.ip
                ret = None
            case 4:
                ret = self.bxc(operand)
            case 5:
                ret = self.out(operand)
            case 6:
                ret = self.bdv(operand)
            case 7:
                ret = self.cdv(operand)
        self.ip += 2
        return ret

    def exec_gen(self, program: List[int]):
        while self.ip + 1 < len(program):
            op = program[self.ip]
            operand = program[self.ip + 1]
            ret = self.exec_op(op, operand)
            if ret is not None:
                yield ret

    def exec(self, program: List[int]):
        return [val for val in self.exec_gen(program)]

    def is_program_quine(self, program: List[int]):
        for j, val in enumerate(self.exec_gen(program)):
            if j >= len(program) or program[j] != val:
                return False
        return j == len(program) - 1


def is_a_val_quiny(a: int, program: List[int]):
    comp = Computer(a=a, b=0, c=0, ip=0)
    return a if comp.is_program_quine(program) else -1


def search_for_quine(program: List[int], min_val: int, max_val: int):
    for i in range(min_val, max_val):
        comp = Computer(a=i, b=0, c=0, ip=0)
        if comp.is_program_quine(program):
            return i
    return -1


# (2,4) (1,5) (7,5) (1,6) (0,3) (4,2) (5,5) (3,0)
def part_one():
    comp = Computer(a=0o3066170352646271, b=0, c=0, ip=0)
    program = [2, 4, 1, 5, 7, 5, 1, 6, 0, 3, 4, 2, 5, 5, 3, 0]
    print(comp.exec(program))


def part_two_gpu():
    res = quiny_gpu(a)
    print(res)


# (2,4) (1,5) (7,5) (1,6) (0,3) (4,2) (5,5) (3,0)
# b <- a % 8            (2,4)
# b <- b ^ 5            (1,5)
# c <- a // 2**b        (7,5)
# b <- b ^ 6            (1,6)
# a <- a // 2**3        (0,3)
# b <- b ^ c            (4,2)
# ret b                 (5,5)
# jmp 0 if a != 0       (3,0)

# a <- a // 2**3
# b <- (a % 8) ^ 5 ^ 6 ^ (a // 2**((a % 8) ^ 5))
# c <- a // 2**((a % 8) ^ 5)


def part_two_brute():
    program = [2, 4, 1, 5, 7, 5, 1, 6, 0, 3, 4, 2, 5, 5, 3, 0]
    length = len(program)
    # Must be between 8 ** 15 and 8 ** 16
    # This doesn't really help because this is a range of 250 trillion
    # 107752139522048
    for i in tqdm(range(127543348822016, 8**16)):
        a = i
        b = 0
        c = 0
        count = 0
        while a != 0:
            tmp = a & 7
            c = a >> ((tmp) ^ 5)
            b = (tmp) ^ 3 ^ c
            a = a >> 3
            if program[count] != (b & 7):
                break
            if count == length - 1:
                print(i)
                return i
            count += 1


def solve_like_a_smart_person():
    program = [2, 4, 1, 5, 7, 5, 1, 6, 0, 3, 4, 2, 5, 5, 3, 0]

    soln = ["0"]
    for val in reversed(program):
        print(val)
        tmp_soln = []
        for sol in soln:
            out = []
            for i in range(8):
                a = (int(sol, 8) << 3) + i if soln != "" else i
                tmp = a & 7
                c = a >> (tmp ^ 5)
                b = (tmp) ^ 3 ^ c
                print(f"i: {i}, A: {a}, B: {b}, C: {c}")
                a = a >> 3
                if (b & 7) == val:
                    out.append(i)
            for j in out:
                tmp_soln.append(sol + str(j))
        soln = tmp_soln
    min_sol = min([int(sol, 8) for sol in soln])
    comp = Computer(a=min_sol, b=0, c=0, ip=0)
    program = [2, 4, 1, 5, 7, 5, 1, 6, 0, 3, 4, 2, 5, 5, 3, 0]
    print(min_sol)
    print(comp.exec(program))


def part_two_multi():
    test_program = [0, 3, 5, 4, 3, 0]
    program = [2, 4, 1, 5, 7, 5, 1, 6, 0, 3, 4, 2, 5, 5, 3, 0]
    with Manager() as manager:
        stop_event = manager.Event()
        with Pool() as pool:
            for result in pool.imap(
                partial(is_a_val_quiny, program=program),
                range(100_000_000_000, 1_000_000_000_000),
                chunksize=10_000_000,
            ):
                if result != -1:
                    # Found what we're looking for, stop everything
                    stop_event.set()
                    pool.terminate()
                    return result


if __name__ == "__main__":
    print(f"Last Digit is 0: Most significant A bits are 3 = 011")
    print(f"2nd Last Digit is 3: Next significant A bits are 0 or 5 = 101")
    print(f"3rd Last Digit is 5: Next significant A bits are 4 = 100 or 6 = 110")
    for i in range(7):
        c = i >> (i ^ 5)
        b = (i) ^ 3 ^ c
        a = i >> 3
        print(f"i: {i}, A: {a}, B: {b}, C: {c}")
    solve_like_a_smart_person()
    part_one()
