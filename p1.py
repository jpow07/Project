"""
This code is written by Isaac Sibley, Jordan Powell, and Jacob Jiang for the Comp Org group project.

The purpose of this code is to read in a mips file and to output up to the first 16 clock cycles.

"""
import sys


# A class to hold all of the characteristics of an input and its state
class Expression:
    stages = ["IF", "ID", "EX", "MEM", "WB"]

    # Initialize the class by taking in an unseparated input statement and offset
    def __init__(self, statement, offset):
        # Store the statement, then split at the space and store the opperand
        self.statement = statement
        temp = statement.split(' ')
        self.operand = temp[0]
        # Split the registers and check if a load operation or not
        self.register = temp[1].split(',')
        if len(self.register) == 3:
            self.format = 'R'
        else:
            self.format = 'L'
        # Set the default values
        self.currentCycle = 1
        self.isWaiting = False
        self.waitCount = 0
        self.offset = offset
        if self.offset > 0:
            self.canExecute = False
        else:
            self.canExecute = True
        self.nopString = ''

    def __str__(self):
        # Keep currentCycle in Bounds
        if self.waitCount > 0:
            self.printNop()

        if self.currentCycle > 5:
            self.currentCycle = 5

        spacing = 16 - self.offset - self.currentCycle
        string = "{:20}".format(self.statement)

        # Print offset decimal
        if self.offset > 0:
            for i in range(self.offset):
                string += '{:4}'.format('.')

        # Print previous to current cycle
        for i in range(self.currentCycle):
            #            if self.waitCount > 0 and i == 1:
            #                string += '{0:4}'.format(self.stages[1])
            #                spacing -= 1
            string += '{0:4}'.format(self.stages[i])

        # Print Trailing decimal points
        for i in range(spacing - 1):
            string += '{0:4}'.format('.')
        string += '.'

        return string

    def printNop(self):
        # Keep currentCycle in Bounds
        if self.currentCycle > 5:
            self.currentCycle = 5

        # Calculate Spacing for trailing decimal point
        spacing = 16 - self.offset - self.currentCycle - self.waitCount
        string = "{:20}".format('nop')

        # Print offset decimal
        if self.offset > 0:
            for i in range(self.offset):
                string += '{:4}'.format('.')

        # Print previous to current cycle
        for i in range(2):
            string += '{0:4}'.format(self.stages[i])

        # print nop bubble
        for i in range(self.waitCount):
            string += '{0:4}'.format('*')

        # Print Trailing decimal points
        for i in range(spacing - 1):
            string += '{0:4}'.format('.')
        string += '.'

        # Return the string with proper spacing (20 spaces)
        print(string)

    def calculateExpression(self, reg):

        if self.format == 'L':
            # L Format [ Operation rt, IMM(rs) ]
            return
        elif self.format == 'R':
            # R Format [ Operation rd, rs, rt ] reg refers to global registers that are printed while self.registers
            # refers to rt, rs, and rd registers after the expression
            if self.operand == 'add':
                reg[self.register[0]] = reg[self.register[1]] + reg[self.register[2]]
            elif self.operand == 'addi':

                reg[self.register[0]] = reg[self.register[1]] + int(self.register[2])
            elif self.operand == 'sub':
                reg[self.register[0]] = reg[self.register[1]] - reg[self.register[2]]
            elif self.operand == 'subi':
                reg[self.register[0]] = reg[self.register[1]] - int(self.register[2])
            elif self.operand == 'and':
                reg[self.register[0]] = reg[self.register[1]] & reg[self.register[2]]
            elif self.operand == 'andi':
                reg[self.register[0]] = reg[self.register[1]] & int(self.register[2])
            elif self.operand == 'or':
                reg[self.register[0]] = reg[self.register[1]] | reg[self.register[2]]
            elif self.operand == 'ori':
                reg[self.register[0]] = reg[self.register[1]] | int(self.register[2])


        else:
            # J Format [ OP Label ]
            return


# A function to determine if a nop is needed at any given line, i
# It takes in: i, as well as the array of lines
def add_nop(index, MIPSExpressions):
    # Edge Cases: Index at zero wont be checked and if its not reached the execute phase
    if index == 0 or index == 1 or MIPSExpressions[index].currentCycle < 2:
        return

    # print(MIPSExpressions[index].waitCount)

    try:
        two = MIPSExpressions[index - 2]
        for i in range(1, len(MIPSExpressions[index].register)):
            if two.register[0] == MIPSExpressions[index].register[i]:
                print("rs: " + two.register[0] + '\nreg: ' + MIPSExpressions[index].register[i])
                MIPSExpressions[index].isWaiting = True
                MIPSExpressions[index].waitCount += 1

    except IndexError:
        return

    if MIPSExpressions[index].isWaiting is True:
        if two.currentCycle > 5:
            MIPSExpressions[index].isWaiting = False


# A main function to be the driver for our code
def main():
    # Variables
    MIPSExpressions = []  # Hold the MIPS Expressions
    separateline = '{:-^82}'.format('')  # Print a dashed Line
    registers = {  # Hold the registers as a dictionary
        "$zero": 0, "$ra": 0,
        # S Registers
        "$s0": 0, "$s1": 0, "$s2": 0, "$s3": 0,
        "$s4": 0, "$s5": 0, "$s6": 0, "$s7": 0,

        # T Registers
        "$t0": 0, "$t1": 0, "$t2": 0, "$t3": 0, "$t4": 0,
        "$t5": 0, "$t6": 0, "$t7": 0, "$t8": 0, "$t9": 0,
    }

    # Check Command line Arguments
    if len(sys.argv) != 3:
        print("Invalid number of inputs, needs 2!\n")
        exit(1)

    # Check argv[1] for forwarding option
    if sys.argv[1].upper() == 'N':
        optionForwarding = " (no forwarding)"
    else:
        optionForwarding = " (forwarding)"

    # Read the File; Create Expressions with statement and Offset
    lineCount = 0
    with open(sys.argv[2], 'r') as file:
        line = file.readline()
        while line:
            MIPSExpressions.append(Expression(line.rstrip('\n'), lineCount))
            line = file.readline()
            lineCount = lineCount + 1
    file.close()

    # Print The Simulation
    print('START OF SIMULATION' + optionForwarding, end='\n')
    print(separateline, end='\n')
    cycles = '{:<20}'.format('CPU Cycles ===>')
    for i in range(1, 16):
        cycles += '{:<4}'.format(i)
    cycles += '{:<0}'.format('16')

    # TODO: I believe were supposed to stop after 48 cycles or something so we might have to change this to correct
    #  number of cycles Loop through MIPS Simulator until all instructions have complete WB stage.
    while MIPSExpressions[len(MIPSExpressions) - 1].currentCycle != 6:

        print(cycles)
        for i in range(len(MIPSExpressions)):
            # Check the last expression to see if its completed the IF stage before the second node can execute
            if i > 0 and MIPSExpressions[i - 1].currentCycle > 2:
                MIPSExpressions[i].canExecute = True

            # Calculate Registers on WB Cycle
            if MIPSExpressions[i].currentCycle == 5:
                MIPSExpressions[i].calculateExpression(registers)

            # If the Expression can execute increment cycle so next step can execute
            if MIPSExpressions[i].canExecute:

                # Print the Expression
                print(MIPSExpressions[i], end='\n')
                add_nop(i, MIPSExpressions)

                if MIPSExpressions[i].isWaiting is False:
                    MIPSExpressions[i].currentCycle += 1

                # if MIPSExpressions[i].isWaiting is True:
                #    MIPSExpressions[i].waitCount += 1

        print(end='\n')  # Print Newline

        # Print Dictionary; set newline every 4 registers
        i = 0
        for key, value in registers.items():
            if key == '$zero' or key == '$ra':
                continue
            if i == 3 or i == 7 or i == 11 or i == 15 or i == 17:
                print("{0:<7}".format(key + ' = ' + str(value)), end='\n')
            else:
                print("{0:<20}".format(key + ' = ' + str(value)), end='')

            i += 1
        print(separateline, end='\n')
    print('END OF SIMULATION', end='\n')


if __name__ == "__main__":
    main()
