from os import stat
from Pyro4 import expose


class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers

    def solve(self):
        inp = self.read_input()
        a, b = inp.split('\n\n')
        a = [[int(j) for j in i.split(' ')] for i in a.split('\n')]
        b = [[int(j) for j in i.split(' ')] for i in b.split('\n')[:-1]]

        res = []
        for i in range(0, len(a)*len(a[0])):
            index = i%len(a)
            res.append(self.workers[i%len(self.workers)].mymap(a[index], [j[index] for j in b]))
        self.write_output(res, len(a))

    # [1, 2, 3, 4, 5 ,6]
    @staticmethod
    @expose
    def mymap(a, b):
        return sum([a[i]*b[i] for i in range(len(a))])

    def read_input(self):
        with open(self.input_file_name, 'r') as f:
            return f.read()

    def write_output(self, output_src, step):
        f = open(self.output_file_name, 'w')
        output = []
        buf = []
        for i, s in enumerate(output_src):
            buf.append(str(s.value))
            if (i+1)%step == 0:
                output.append(' '.join(buf))
                buf = []
        output = '\n'.join(output)

        f.write(output)

        f.close()

