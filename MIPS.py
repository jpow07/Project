"""
This code is written by Isaac Sibley, _______, and ______ for the Comp Org group project.

The purpose of this code is to read in a mips file and to output up to the first 16 clock cycles.

"""


def calculation(opp, order, reg):
    c = order.split(",")
    if opp == "add":
        s1 = 0
        s2 = 0
        for i in range(0, len(reg)):
            if reg[i][0] == c[1]:
                s1 = reg[i][1]
            elif reg[i][0] == c[2]:
                s2 = reg[i][1]
        answer = s1 + s2
        return answer
    elif opp == "addi":
        s1 = 0
        for i in range(0, len(reg)):
            if reg[i][0] == c[1]:
                s1 = reg[i][1]
        answer = s1 + int(c[2])
        return answer
    elif opp == "and":
        s1 = 0
        s2 = 0
        for i in range(0, len(reg)):
            if reg[i][0] == c[1]:
                s1 = reg[i][1]
            elif reg[i][0] == c[2]:
                s2 = reg[i][1]
        answer = s1 & s2
        return answer
    elif opp == "andi":
        s1 = 0
        for i in range(0, len(reg)):
            if reg[i][0] == c[1]:
                s1 = reg[i][1]
        answer = s1 & int(c[2])
        return answer
    elif opp == "or":
        s1 = 0
        s2 = 0
        for i in range(0, len(reg)):
            if reg[i][0] == c[1]:
                s1 = reg[i][1]
            elif reg[i][0] == c[2]:
                s2 = reg[i][1]
        answer = s1 | s2
        return answer
    elif opp == "ori":
        s1 = 0
        for i in range(0, len(reg)):
            if reg[i][0] == c[1]:
                s1 = reg[i][1]
        answer = s1 | int(c[2])
        return answer
    elif opp == "slt":
        s1 = 0
        s2 = 0
        for i in range(0, len(reg)):
            if reg[i][0] == c[1]:
                s1 = reg[i][1]
            elif reg[i][0] == c[2]:
                s2 = reg[i][1]
        if s1 < s2:
            answer = 0
        else:
            answer = 1
        return answer
    elif opp == "slti":
        s1 = 0
        for i in range(0, len(reg)):
            if reg[i][0] == c[1]:
                s1 = reg[i][1]
        if s1 < int(c[2]):
            answer = 0
        else:
            answer = 1
        return answer
    elif opp == "beq":
        s1 = 0
        s2 = 0
        for i in range(0, len(reg)):
            if reg[i][0] == c[1]:
                s1 = reg[i][1]
            elif reg[i][0] == c[2]:
                s2 = reg[i][1]
        if s1 == s2:
            answer = "Yj"
        else:
            answer = "Nj"
        return answer
    elif opp == "bne":
        s1 = 0
        s2 = 0
        for i in range(0, len(reg)):
            if reg[i][0] == c[1]:
                s1 = reg[i][1]
            elif reg[i][0] == c[2]:
                s2 = reg[i][1]
        if s1 != s2:
            answer = "Yj"
        else:
            answer = "Nj"
        return answer
    return "opp not found"


def add_nop(i, sblock):
    nop_exist = False
    nop_num = 0
    output = [nop_exist, sblock, nop_num]
    if i == 1:
        if sblock[i][0] != "nop\t" and sblock[i - 1][0] != "nop\t":
            l1 = sblock[i][0].split(' ')[1].split(',')
            l2 = sblock[i - 1][0].split(' ')[1].split(',')
            for elements in range(1, len(l1)):
                if l1[elements] == l2[0]:
                    if "MEM" in sblock[i - 1]:
                        output[0] = True
                        output[2] = output[2] + 2
                        sline = ["", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."]
                        sline[0] = "nop\t"
                        sline[i + 1] = "IF"
                        sline[i + 2] = "ID"
                        sline[i + 3] = "*"
                        sblock.insert(i, sline)
                        sblock.insert(i, sline)
                        output[1] = sblock
    elif i > 1:
        if sblock[i][0] != "nop\t" and sblock[i - 1][0] != "nop\t" and sblock[i - 2][0] != "nop\t":
            l1 = sblock[i][0].split(' ')[1].split(',')
            l2 = sblock[i - 1][0].split(' ')[1].split(',')
            l3 = sblock[i - 2][0].split(' ')[1].split(',')
            for elements in range(1, len(l1)):
                if l1[elements] == l2[0]:
                    if "MEM" in sblock[i - 1]:
                        output[0] = True
                        output[2] = output[2] + 2
                        sline = ["", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."]
                        sline[0] = "nop\t"
                        sline[i + 1] = "IF"
                        sline[i + 2] = "ID"
                        sline[i + 3] = "*"
                        sblock.insert(i, sline)
                        sblock.insert(i, sline)
                        output[1] = sblock
                if l1[elements] == l3[0]:
                    if "MEM" in sblock[i - 1]:
                        output[0] = True
                        output[2] = output[2] + 1
                        sline = ["", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."]
                        sline[0] = "nop\t"
                        sline[i + 1] = "IF"
                        sline[i + 2] = "ID"
                        sline[i + 3] = "*"
                        sblock.insert(i, sline)
                        output[1] = sblock
    return output


def main():
    register = [['$s0', 0], ['$s1', 0], ['$s2', 0], ['$s3', 0], ['$s4', 0], ['$s5', 0], ['$s6', 0], ['$s7', 0],
                ['$t0', 0], ['$t1', 0], ['$t2', 0], ['$t3', 0], ['$t4', 0], ['$t5', 0], ['$t6', 0], ['$t7', 0],
                ['$t8', 0], ['$t9', 0]]
    saparateline = '----------------------------------------------------------------------------------'
    with open('ex03.s', 'r') as f1:
        list1 = f1.readlines()
    sblock = []
    print('START OF SIMULATION')
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
                if sblock[lines][0] != "nop\t":
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
                if sblock[lines][0] != "nop\t":
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
                                            register[r][1] = 1
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
        print()
        #Print the commands
        for l in sblock:
            for j in range(0, len(l)):
                if j == 0:
                    print("{:20}".format(l[j]), end='')
                else:
                    print("{:4s}".format(l[j]), end='')
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


if __name__ == "__main__":
    main()

