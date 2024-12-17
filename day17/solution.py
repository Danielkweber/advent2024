from typing import List


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

    def exec(self, program: List[int]):
        output = []
        while self.ip < len(program):
            op = program[self.ip]
            operand = program[self.ip + 1]
            ret = self.exec_op(op, operand)
            print(op, operand, self.a, self.b, self.c, output)
            if ret is not None:
                output.append(ret)
        return output


if __name__ == "__main__":
    comp = Computer(a=44348299, b=0, c=0, ip=0)
    program = [2, 4, 1, 5, 7, 5, 1, 6, 0, 3, 4, 2, 5, 5, 3, 0]
    print(comp.exec(program))
