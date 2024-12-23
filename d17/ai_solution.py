class Computer:
    def __init__(self, program, reg_a=0, reg_b=0, reg_c=0):
        self.program = program
        self.reg_a = reg_a
        self.reg_b = reg_b
        self.reg_c = reg_c
        self.ip = 0
        self.outputs = []

    def get_combo_value(self, operand):
        if operand <= 3:
            return operand
        elif operand == 4:
            return self.reg_a
        elif operand == 5:
            return self.reg_b
        elif operand == 6:
            return self.reg_c
        else:
            raise ValueError("Invalid combo operand 7")

    def adv(self, operand, target_reg="a"):
        # Get denominator as 2^operand_value
        value = self.get_combo_value(operand)
        denominator = 1 << value  # This is 2^value
        result = self.reg_a // denominator
        if target_reg == "a":
            self.reg_a = result
        elif target_reg == "b":
            self.reg_b = result
        else:
            self.reg_c = result

    def step(self):
        if self.ip >= len(self.program):
            return False

        opcode = self.program[self.ip]
        operand = self.program[self.ip + 1]

        if opcode == 0:  # adv
            self.adv(operand, "a")
            self.ip += 2
        elif opcode == 1:  # bxl
            self.reg_b ^= operand  # XOR with literal
            self.ip += 2
        elif opcode == 2:  # bst
            self.reg_b = self.get_combo_value(operand) % 8
            self.ip += 2
        elif opcode == 3:  # jnz
            if self.reg_a != 0:
                self.ip = operand
            else:
                self.ip += 2
        elif opcode == 4:  # bxc
            self.reg_b ^= self.reg_c
            self.ip += 2
        elif opcode == 5:  # out
            output_value = self.get_combo_value(operand) % 8
            self.outputs.append(output_value)
            self.ip += 2
        elif opcode == 6:  # bdv
            self.adv(operand, "b")
            self.ip += 2
        elif opcode == 7:  # cdv
            self.adv(operand, "c")
            self.ip += 2

        return True

    def run(self):
        while self.step():
            pass
        return ",".join(map(str, self.outputs))


# Parse program
program = [2, 4, 1, 5, 7, 5, 1, 6, 0, 3, 4, 2, 5, 5, 3, 0]

# Create and run computer
computer = Computer(program, reg_a=44348299, reg_b=0, reg_c=0)
result = computer.run()
print(f"Output: {result}")
