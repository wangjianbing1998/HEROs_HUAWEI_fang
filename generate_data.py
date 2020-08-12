# coding=gbk
def generate_data(file_in, file_out, ratio=2, step=2):
    with open(file_out, 'w+') as fw:

        for s in range(step):
            with open(file_in, 'r') as fr:
                for line in fr.readlines():
                    line = line.strip()
                    if len(line) > 0:
                        x, y, money = line.split(',')
                        new_x = x + ''.join(['0'] * (ratio * s))
                        new_y = y + ''.join(['0'] * (ratio * s))

                        fw.write(','.join([new_x, new_y, money]) + '\n')

    return -1


if __name__ == '__main__':
    generate_data('data/test_data.txt', 'data/T.txt', 2, 56)
