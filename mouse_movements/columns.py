#test file

with open(r'/home/alex/Desktop/mouselog.txt', 'r') as f:
    for line in f:
        data = line.split()    # Splits on whitespace
        print("{0[0]:<15}{0[1]:<15}{0[2]:<7}{0[3]:<7}{0[4]:>7}{0[5]:>15}".format(data))