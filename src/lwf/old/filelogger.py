def logToFile():
    with open('lwf_output.txt', 'w'):
        pass


def log(string):
    # print(string)
    with open('lwf_output.txt', 'a') as file:
        file.write(string + '\n')
