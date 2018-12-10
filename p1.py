"""
This code is written by Isaac Sibley, Jordan Powell, and Jacob Jiang for the Comp Org group project.

The purpose of this code is to read in a mips file and to output up to the first 16 clock cycles.

"""
import sys


class Expression:
    stages = ["IF", "ID", "EX", "MEM", "WB"]

    def __init__(self, statement, offset):
        self.statement = statement
        temp = statement.split(' ')
        self.operand = temp[0]
        self.register = temp[1].split(',')
        if len(self.register) == 3:
            self.format = 'R'
        else:
            self.format = 'L'
        self.currentCycle = 1
        self.isWaiting = 0
        self.offset = offset
        if self.offset > 0:
            self.canExecute = False
        else:
            self.canExecute = True

    def __str__(self):
        # Keep currentCycle in Bounds
        if self.currentCycle > 5:
            self.currentCycle = 5

        # Calculate Spacing for trailing decimal point
        if self.isWaiting:
            spacing = 16 - self.offset - self.currentCycle - self.isWaiting
            string = "{0:20}".format('nop')
        else:
            spacing = 16 - self.offset - self.currentCycle
            string = "{0:20}".format(self.statement)

        # Print blank Line if Cannot execute
        if not self.canExecute:
            return "{0:20}".format(self.statement) + '.\t.\t.\t.\t.\t.\t.\t.\t.\t.\t.\t.\t.\t.\t.\t.'

        # Print offset decimal
        if self.offset > 0:
            for i in range(self.offset):
                string += '.\t'
        # Print previous to current cycle
        for i in range(self.currentCycle):

            string += self.stages[i] + '\t'
        # Print asterisk if waiting

        if self.isWaiting:
            print("{0:20}".format('nop') + '.\t.\t.\t.\t.\t.\t.\t.\t.\t.\t.\t.\t.\t.\t.\t.')
            for i in range(self.isWaiting):


                string += '*\t'

        # Print Trailing decimal points
        for i in range(spacing):
            string += '.\t'
        # Return the string with proper spacing (20 spaces)
        return string

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
def add_nop(i, MIPSExpressions):
    nop_exist = False
    nop_num = 0
    line = MIPSExpressions[i].operand
    up_line = MIPSExpressions[i-1].operand
    upper_line = MIPSExpressions[i-2].operand

    output = [nop_exist, nop_num]
    # Check if the first line
    if i == 1:
        # Check if the previous values of nops
        if line != "nop" and up_line != "nop":
            l1 = MIPSExpressions[i].register
            l2 = MIPSExpressions[i - 1].register
            # Run through all the elements and determine what to print
            for elements in range(1, len(l1)):
                if l1[elements] == l2[0]:
                        output[0] = True
                        output[1] = output[1] + 2
    # Else if any other line
    elif i > 1:
        # Check if previous are nops
        if line != "nop" and up_line != "nop" and upper_line != "nop":
            l1 = MIPSExpressions[i].register
            l2 = MIPSExpressions[i - 1].register
            l3 = MIPSExpressions[i - 2].register
            # RUn through the elements and determine what to print
            for elements in range(1, len(l1)):
                if l1[elements] == l2[0]:
                        output[0] = True
                        output[1] = output[1] + 2
                if l1[elements] == l3[0]:
                        output[0] = True
                        output[1] = output[1] + 1
    return output


# A main function to be the driver for our code
def main():
    # Variables
    MIPSExpressions = []  # Hold the MIPS Expressions
    saparateline = '{:-^82}'.format('')  # Print a dashed Line
    registers = {  # Hold the registers as a dictionary
        "$zero": 0,
        # S Registers
        "$s0": 0, "$s1": 0, "$s2": 0, "$s3": 0,
        "$s4": 0, "$s5": 0, "$s6": 0, "$s7": 0,

        # T Registers
        "$t0": 0, "$t1": 0, "$t2": 0, "$t3": 0, "$t4": 0,
        "$t5": 0, "$t6": 0, "$t7": 0, "$t8": 0, "$t9": 0,
    }

    # Check Command line Arguments
    if len(sys.argv) != 3:
        print("error")
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

    # Print The Simulation
    print('START OF SIMULATION' + optionForwarding)
    print(saparateline)

    # TODO: I believe were supposed to stop after 48 cycles or something so we might have to change this to correct
    #  number of cycles Loop through MIPS Simulator until all instructions have complete WB stage.
    while MIPSExpressions[len(MIPSExpressions) - 1].currentCycle != 6:
        print("CPU Cycles ===>\t\t1\t2\t3\t4\t5\t6\t7\t8\t9\t10\t11\t12\t13\t14\t15\t16")
        for i in range(len(MIPSExpressions)):
            # Check the last expression to see if its completed the IF stage before the second node can execute
            if i > 0 and MIPSExpressions[i - 1].currentCycle > 2:
                MIPSExpressions[i].canExecute = True

            # Calculate Registers on WB Cycle
            if MIPSExpressions[i].currentCycle == 5:
                MIPSExpressions[i].calculateExpression(registers)

            # Print the Expression
            print(MIPSExpressions[i])
            # If the Expression can execute increment cycle so next step can execute
            if MIPSExpressions[i].canExecute:
                MIPSExpressions[i].currentCycle += 1

        print(end='\n')  # Print Newline

        # Print Dictionary; set newline every 4 registers
        i = 0
        for key, value in registers.items():
            if(key == '$zero' or key == '$at'):
                continue
            if i % 4 == 0 and i != 0:
                print(end='\n')
            print("{0:20}".format(key + ' = ' + str(value)), end='')

            i += 1
        print(end='\n')
        print(saparateline)
    print('END OF SIMULATION')


'''



# This is a function to take in the operation, the unseperated registers and the array to registers
# and then return the desired calculation

def calculation(opp, order, reg):
    # Separate the input based on comma's
    c = order.split(",")

    # Check if the 'add' operation
    if opp == "add":
        s1 = 0
        s2 = 0
        # Find the correct registers and add the values
        for i in range(0, len(reg)):
            if reg[i][0] == c[1]:
                s1 = reg[i][1]
            elif reg[i][0] == c[2]:
                s2 = reg[i][1]
        answer = s1 + s2
        return answer
    # Check if the 'addi' operation
    elif opp == "addi":
        s1 = 0
        # Find the one register and add the constant
        for i in range(0, len(reg)):
            if reg[i][0] == c[1]:
                s1 = reg[i][1]
        answer = s1 + int(c[2])
        return answer
    # Check if the 'and' operation
    elif opp == "and":
        s1 = 0
        s2 = 0
        # Find the two registers and logical 'and' them
        for i in range(0, len(reg)):
            if reg[i][0] == c[1]:
                s1 = reg[i][1]
            elif reg[i][0] == c[2]:
                s2 = reg[i][1]
        answer = s1 & s2
        return answer
    # Check if the 'andi' operation
    elif opp == "andi":
        s1 = 0
        # Find the one register and then logical 'and' with constant
        for i in range(0, len(reg)):
            if reg[i][0] == c[1]:
                s1 = reg[i][1]
        answer = s1 & int(c[2])
        return answer
    # Check if the 'or' operation
    elif opp == "or":
        s1 = 0
        s2 = 0
        # Find the two registers and logical 'or' them
        for i in range(0, len(reg)):
            if reg[i][0] == c[1]:
                s1 = reg[i][1]
            elif reg[i][0] == c[2]:
                s2 = reg[i][1]
        answer = s1 | s2
        return answer
    # Check if the 'ori' function
    elif opp == "ori":
        s1 = 0
        # Find the one register and logical 'or' with the constant
        for i in range(0, len(reg)):
            if reg[i][0] == c[1]:
                s1 = reg[i][1]
        answer = s1 | int(c[2])
        return answer
    # Check if 'slt' operation
    elif opp == "slt":
        s1 = 0
        s2 = 0
        # Find the two registers and then check if s1 is less than s2
        for i in range(0, len(reg)):
            if reg[i][0] == c[1]:
                s1 = reg[i][1]
            elif reg[i][0] == c[2]:
                s2 = reg[i][1]
        # Return either 0 or 1 based on result
        if s1 < s2:
            answer = 0
        else:
            answer = 1
        return answer
    # Check if 'slti' operation
    elif opp == "slti":
        s1 = 0
        # Find the one register and then check if less than constant
        for i in range(0, len(reg)):
            if reg[i][0] == c[1]:
                s1 = reg[i][1]
        # Return either 0 or 1 based on result
        if s1 < int(c[2]):
            answer = 0
        else:
            answer = 1
        return answer
    # Check if operation is 'beq'
    elif opp == "beq":
        s1 = 0
        s2 = 0
        # Find the two registers
        for i in range(0, len(reg)):
            if reg[i][0] == c[1]:
                s1 = reg[i][1]
            elif reg[i][0] == c[2]:
                s2 = reg[i][1]
        # Return either Yj, yes jump, or Nj, no jump, based on equaltiy
        if s1 == s2:
            answer = "Yj"
        else:
            answer = "Nj"
        return answer
    # Check if operation is 'bne'
    elif opp == "bne":
        s1 = 0
        s2 = 0
        # Find the two registers
        for i in range(0, len(reg)):
            if reg[i][0] == c[1]:
                s1 = reg[i][1]
            elif reg[i][0] == c[2]:
                s2 = reg[i][1]
        # Check if they are not equal and return Yj, yes jump, or Nj, no jump
        if s1 != s2:
            answer = "Yj"
        else:
            answer = "Nj"
        return answer
    # Else the operation is not found
    return "opp not found"





# A main function to be the driver for our code
def main():
    # Variables
    MIPSExpressions = []  # Hold the MIPS Expressions
    saparateline = '{:-^82}'.format('')  # Print a dashed Line
    registers = {  # Hold the registers as a dictionary
        # S Registers
        "$s0": 0, "$s1": 0, "$s2": 0, "$s3": 0,
        "$s4": 0, "$s5": 0, "$s6": 0, "$s7": 0,

        # T Registers
        "$t0": 0, "$t1": 0, "$t2": 0, "$t3": 0, "$t4": 0,
        "$t5": 0, "$t6": 0, "$t7": 0, "$t8": 0, "$t9": 0,
    }

    # Check Command line Arguments 
    if len(sys.argv) != 3:
        print("error")
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

    # Print The Simulation
    print('START OF SIMULATION' + optionForwarding)
    print(saparateline)

    # TODO: I believe were supposed to stop after 48 cycles so we might have to change this to correct number of cycles
    # Loop through MIPS Simulator until all instructions have WB.
    while MIPSExpressions[len(MIPSExpressions) - 1].currentCycle != 6:
        print("CPU Cycles ===>\t\t1\t2\t3\t4\t5\t6\t7\t8\t9\t10\t11\t12\t13\t14\t15\t16")
        for i in range(len(MIPSExpressions)):
            nop_opp = add_nop(i, MIPSExpressions)
            if nop_opp[0] is True:
                MIPSExpressions[i].isWaiting += nop_opp[1]
            # Check the last expression to see if its completed the IF stage before the second node can execute
            if i > 0 and MIPSExpressions[i - 1].currentCycle > 2:
                MIPSExpressions[i].canExecute = True
            # Calculate Registers on WB Cycle
            if MIPSExpressions[i].currentCycle == 5:
                MIPSExpressions[i].calculateExpression(registers)

            # Print the Expression
            print(MIPSExpressions[i])
            # If the Expression can execute increment cycle so next step can execute
            if MIPSExpressions[i].canExecute:
                MIPSExpressions[i].currentCycle += 1

        print(end='\n')  # Print Newline

        # Print Dictionary; set newline every 4 registers
        i = 0
        for key, value in registers.items():
            if i % 4 == 0 and i != 0:
                print(end='\n')
            print("{0:20}".format(key + ' = ' + str(value)), end='')

            i += 1
        print(end='\n')
        print(saparateline)
    print('END OF SIMULATION')





    register = [['$s0', 0], ['$s1', 0], ['$s2', 0], ['$s3', 0], ['$s4', 0], ['$s5', 0], ['$s6', 0], ['$s7', 0],
                ['$t0', 0], ['$t1', 0], ['$t2', 0], ['$t3', 0], ['$t4', 0], ['$t5', 0], ['$t6', 0], ['$t7', 0],
                ['$t8', 0], ['$t9', 0]]
    sblock = []
    print('START OF SIMULATION' + optionForwarding)
    print(saparateline)

    n = 0
    nopfinish =True
    for i in range(0, len(list1)):

        sline = ["", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."]
        sline[0] = list1[i].strip('\n')
        sblock.append(sline)
        for lines in range(0, len(sblock)):
            re = add_nop(lines, sblock)
            nopexist = re[0]
            if nopexist is True:
                nopfinish = False
                sblock = re[1]
                n = re[2]
                lines = lines + n
                for elements in range(1, i + 2):
                    if sblock[lines][elements] == ".":
                        if elements == lines + i:
                            sblock[lines][elements] = "IF"
                        if sblock[lines][elements - 1] == "IF":
                            sblock[lines][elements] = "IF"
                        elif sblock[lines][elements - 1] == "ID":
                            sblock[lines][elements] = "ID"

            elif nopexist is False:
                if sblock[lines][0] != "nop":
                    if nopfinish is True:
                        for elements in range(1, i + 2):
                            if sblock[lines][elements] == ".":
                                if elements == lines - n + 1:
                                    sblock[lines][elements] = "IF"
                                elif sblock[lines][elements - 1] == "IF":
                                    sblock[lines][elements] = "ID"
                                elif sblock[lines][elements - 1] == "ID":
                                    sblock[lines][elements] = "EX"
                                elif sblock[lines][elements - 1] == "EX":
                                    sblock[lines][elements] = "MEM"
                                elif sblock[lines][elements - 1] == "MEM":
                                    sblock[lines][elements] = "WB"
                                    opp = sblock[lines][0].split(' ')[0]
                                    order = sblock[lines][0].split(' ')[1]
                                    answer = calculation(opp, order, register)
                                    if type(answer) == int:
                                        for r in range(0, len(register)):
                                            a = register[r][0]
                                            b = order[0].split(',')[0]
                                            if register[r][0] == order.split(',')[0]:
                                                register[r][1] = int(answer)

                # print nop lines
                else:
                    for elements in range(1, i + 2):
                        star_num = 0
                        for elements2 in range(1, len(sblock[lines])):
                            if sblock[lines][elements2] == "*":
                                star_num = star_num + 1
                        if star_num < 3:
                            if sblock[lines][elements - 1] == "ID" or sblock[lines][elements - 1] == "*":
                                sblock[lines][elements] = "*"
        #Print the header and command
        print("CPU Cycles ===>     1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16")
        for l in sblock:
            for j in range(0, len(l)):
                if j == 0:
                    print("{:20}".format(l[j]), end='')
                else:
                    print("{:4s}".format(l[j]), end='')
            print()
        print()
        #Print the registers
        for l in range(0, len(register)):
            print(register[l][0], '=', end=' ')
            print("{:14s}".format(str(register[l][1])), end='')
            if (l + 1) % 4 == 0:
                print()
        print()
        print(saparateline)
    counter1 = len(list1)
    #
    #
    #
    #
    nopfinish = True
    while "WB" not in sblock[len(sblock) - 1]:

        lines = 0
        while lines < len(sblock):
            re = add_nop(lines, sblock)
            nopexist = re[0]
            if nopexist is True:
                sblock = re[1]
                lines = lines + re[2]
                nopfinish = False
                for elements in range(1, counter1 + 2):
                    if sblock[lines][elements] == ".":
                        if sblock[lines][elements - 1] == "IF":
                            sblock[lines][elements] = "IF"
                        elif sblock[lines][elements - 1] == "ID":
                            sblock[lines][elements] = "ID"

            elif nopexist is False or nopfinish is True:
                if sblock[lines][0] != "nop":
                    for elements in range(1, counter1 + 2):
                        if sblock[lines][elements] == ".":
                            if elements == lines + 1:
                                sblock[lines][elements] = "IF"
                            elif sblock[lines][elements - 1] == "IF":
                                sblock[lines][elements] = "ID"
                            elif sblock[lines][elements - 1] == "ID":
                                sblock[lines][elements] = "EX"
                            elif sblock[lines][elements - 1] == "EX":
                                sblock[lines][elements] = "MEM"
                            elif sblock[lines][elements - 1] == "MEM":
                                sblock[lines][elements] = "WB"
                                opp = sblock[lines][0].split(' ')[0]
                                order = sblock[lines][0].split(' ')[1]
                                answer = calculation(opp, order, register)
                                if type(answer) == int:
                                    for r in range(0, len(register)):
                                        if register[r][0] == order.split(',')[0]:
                                            register[r][1] = int(answer)
                else:
                    for elements in range(1, counter1 + 2):
                        star_num = 0
                        for elements2 in range(1, len(sblock[lines])):
                            if sblock[lines][elements2] == "*":
                                star_num = star_num + 1
                        if star_num < 3:
                            if sblock[lines][elements - 1] == "ID" or sblock[lines][elements - 1] == "*":
                                sblock[lines][elements] = "*"
            elif nopfinish is False:
                for elements in range(1, counter1 + 2):
                    if sblock[lines][elements] == ".":
                        if sblock[lines][elements - 1] == "IF":
                            sblock[lines][elements] = "IF"
                        elif sblock[lines][elements - 1] == "ID":
                            sblock[lines][elements] = "ID"
                        elif sblock[lines][elements - 1] == "EX":
                            sblock[lines][elements] = "EX"
                        elif sblock[lines][elements - 1] == "MEM":
                            sblock[lines][elements] = "MEM"
            lines = lines + 1
        #Print the header and the command
        print("CPU Cycles ===>     1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16")
        #Print the commands
        for l in sblock:
            for j in range(0, len(l)):
                if j == 0:
                    print("{:20}".format(l[j]), end='')
                else:
                    print("{:4s}".format(l[j]), end='')
            print()
        print()
        #Print the registers
        for l in range(0, len(register)):
            print(register[l][0], '=', end=' ')
            print("{:14s}".format(str(register[l][1])), end='')
            if (l + 1) % 4 == 0:
                print()
        print()
        print(saparateline)
        counter1 = counter1 + 1
    print('END OF SIMULATION')

'''
if __name__ == "__main__":
    main()
