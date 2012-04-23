from commands import getoutput

class topdata:
    cpudata = ['us', 'sy', 'ni', 'id', 'wa','hi', 'si', 'st']
    memdata = ['total','used','free','buffers']
    swapdata = ['total','used','free','cached']

    def __init__(self):
        #get new sample
        self.update()

    def update(self):
        ret = getoutput('top -b -n 1 | head')
        lines = ret.split('\n')
        loadstr = lines[0].split(' ')[12:]
        self.load = []
        for load in loadstr:
            self.load.append(load.replace(',',''))
        cpustr = lines[2].split('  ')[1:]
        self.cpu = []
        for cpu in cpustr:
            self.cpu.append(cpu.split('%')[0])
        memstr = lines[3].split('k ')[:-1]
        self.mem = []
        for mem in memstr:
            self.mem.append(mem.split(' ')[-1])
        swapstr = lines[3].split('k ')[:-1]
        self.swap = []
        for swap in swapstr:
            self.swap.append(swap.split(' ')[-1])
        #TODO - CPU data...



