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
        #Check if a loop statement
        if ':' in statement:
            #Store operand as jump and label in register[0]
            self.operand = "jump"
            self.format = 'J'
            self.register = []
            self.register.append(statement.split(':')[0])
        #Otherwise is a command line
        else:
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
        self.controlHazard = 0
        if self.offset > 0:
            self.canExecute = False
        else:
            self.canExecute = True
        self.nopString = ''
        #Set a line for the jump label to be on
        if self.operand == 'beq' or self.operand == 'bne':
            self.jumpLabel = 0

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
            #if self.controlHazard > i and self.controlHazard > 0:
             #   string += '{0:4}'.format(self.stages[i])
            if (self.controlHazard - i) <= 0 and self.controlHazard > 0:
                string += '{0:4}'.format('*')
            else:
                string += '{0:4}'.format(self.stages[i])

        # Print Trailing decimal points
        for i in range(spacing - 1):
            string += '{0:4}'.format('.')
        string += '.'
        
        #Truncate if beyond bounds
        if (self.currentCycle == 4):
            string = string[:83]
        elif self.currentCycle == 1 or self.currentCycle == 2 or self.currentCycle == 3 or self.currentCycle == 5:
            string = string[:82]
        else:
            string = string[:81]
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
            #Check if slt or slti
            elif self.operand == 'slt':
                if reg[self.register[1]] < reg[self.register[2]]:
                    reg[self.register[0]] = 1
                else:
                    reg[self.register[0]] = 0
            elif self.operand == 'slti':
                if reg[self.register[1]] < int(self.register[2]):
                    reg[self.register[0]] = 1
                else:
                    reg[self.register[0]] = 0                
            #Check if jumping to a loop (stored in register[2])
            elif self.operand == 'beq':
                #Only run if the equals is true
                if reg[self.register[0]] == reg[self.register[1]]:
                    #Tell the variable to move back to where the loop label is located
                    return self.jumpLabel
                return (-1)
                
            elif self.operand == 'bne':
                #Only run if the not equals is true
                if reg[self.register[0]] != reg[self.register[1]]:
                    #Tell the variable to move back to where the loop label is located
                    return self.jumpLabel
                return (-1)
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
                #Commented out test code to try submitting
                #print("rs: " + two.register[0] + '\nreg: ' + MIPSExpressions[index].register[i])
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
            #Decrement if a jump label line to format output
            if ':' in line:
                lineCount = lineCount - 1
            line = file.readline()
            lineCount = lineCount + 1
    file.close()

    #Set up the jump labels to point to the correct points in the code
    i = 0
    j = 0
    while i < (len(MIPSExpressions) - 1):
        #Find beq or bne calls
        if MIPSExpressions[i].operand == 'bne' or MIPSExpressions[i].operand == 'beq':
            #Have them point to the correct jump label in the code
            while j < (len(MIPSExpressions) - 1):
                if MIPSExpressions[j].register[0] == MIPSExpressions[i].register[2]:
                    MIPSExpressions[i].jumpLabel = j
                j += 1
        i += 1
    # Print The Simulation
    print('START OF SIMULATION' + optionForwarding, end='\n')
    print(separateline, end='\n')
    cycles = '{:<20}'.format('CPU Cycles ===>')
    for i in range(1, 16):
        cycles += '{:<4}'.format(i)
    cycles += '{:<0}'.format('16')

    # TODO: I believe were supposed to stop after 48 cycles or something so we might have to change this to correct
    #  number of cycles Loop through MIPS Simulator until all instructions have complete WB stage.
    j = 0
    while MIPSExpressions[len(MIPSExpressions) - 1].currentCycle != 6 and j < 16:

        print(cycles)
        for i in range(len(MIPSExpressions)):
            #Skip over any jump labels
            if MIPSExpressions[i].operand == "jump":
                MIPSExpressions[i].currentCycle += 1
                continue
            # Check the last expression to see if its completed the IF stage before the second node can execute
            if i > 0 and MIPSExpressions[i - 1].currentCycle > 2:
                MIPSExpressions[i].canExecute = True

            # Calculate Registers on WB Cycle
            if MIPSExpressions[i].currentCycle == 5:
                #Check if a jump operation
                if MIPSExpressions[i].operand == "beq" or MIPSExpressions[i].operand == "bne":
                    #Check if jump
                    temp = MIPSExpressions[i].calculateExpression(registers)
                    #Check if a value line value recieved (gets -1 if not true)
                    if temp >= 0:
                        #NEED TO GO TO THIS LINE NEXT (whatever value is stored in temp + 1, as temp points to the jump label)
                        #Needs to tell next 3 registers to print '*' and to immediately start printing what is stored in line after temp
                        #TENTATIVE: REPLACE ALL REGISTERS AFTER THE CONTROL ERRORED WITH INPUT FROM THE temp+1 value
                        while len(MIPSExpressions) > (i + 4):
                            MIPSExpressions.pop()
                        #Replace any remaining inputs with new ones fresh from the jump line
                        file = open(sys.argv[2], 'r')
                        lineCount = 0
                        line = file.readline()
                        while line:
                            if lineCount > (temp):
                                MIPSExpressions.append(Expression(line.rstrip('\n'), (lineCount + (i-temp) + 2)))
                                #Decrement if a jump label line to format output
                                if ':' in line:
                                    lineCount = lineCount - 1
                            line = file.readline()
                            lineCount = lineCount + 1
                        file.close()
                        #Increment control hazard of any used values
                        MIPSExpressions[i+1].controlHazard = 3
                        MIPSExpressions[i+2].controlHazard = 2
                        MIPSExpressions[i+3].controlHazard = 1
                else:
                    MIPSExpressions[i].calculateExpression(registers)

            # If the Expression can execute increment cycle so next step can execute
            if MIPSExpressions[i].canExecute:
                # Print the Expression
                print(MIPSExpressions[i], end='\n')
                #Only print nop's when there is no forwarding
                if sys.argv[1].upper() == 'N':
                    add_nop(i, MIPSExpressions)

                if MIPSExpressions[i].isWaiting is False:
                    MIPSExpressions[i].currentCycle += 1

                # if MIPSExpressions[i].isWaiting is True:
                #    MIPSExpressions[i].waitCount += 1
        if (len(MIPSExpressions) > (i + 1)):
            if MIPSExpressions[i+1].operand == "jump":
                MIPSExpressions[i+1].currentCycle += 1
                MIPSExpressions[i+2].canExecute = True
                print(MIPSExpressions[i+2], end='\n')
                MIPSExpressions[i+2].currentCycle += 1
            else:
                MIPSExpressions[i+1].canExecute = True
                print(MIPSExpressions[i+1], end='\n')
                MIPSExpressions[i+1].currentCycle += 1
            
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
        j += 1
        print(separateline, end='\n')
    print('END OF SIMULATION', end='\n')


if __name__ == "__main__":
    main()
