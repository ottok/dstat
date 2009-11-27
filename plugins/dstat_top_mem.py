### Authority: Dag Wieers <dag$wieers,com>

class dstat_plugin(dstat):
    """
    Most expensive CPU process.

    Displays the process that uses the CPU the most during the monitored
    interval. The value displayed is the percentage of CPU time for the total
    amount of CPU processing power. Based on per process CPU information.
    """
    def __init__(self):
        self.name = 'most expensive'
        self.vars = ('memory process',)
        self.type = 's'
        self.width = 17
        self.scale = 0
        self.pid = str(os.getpid())

    def extract(self):
        self.val['max'] = 0.0
        for pid in os.listdir('/proc/'):
            try:
                ### Is it a pid ?
                int(pid)

                ### Filter out dstat
                if pid == self.pid: continue

                ### Using dopen() will cause too many open files
#                l = open('/proc/%s/stat' % pid).read().split()
                l = linecache.getline('/proc/%s/stat' % pid, 1).split()

            except ValueError:
                continue
            except IOError:
                continue

            if len(l) < 23: continue
            usage = int(l[23]) * pagesize

            ### Is it a new topper ?
            if usage <= self.val['max']: continue

            self.val['max'] = usage
            self.val['name'] = getnamebypid(pid, l[1][1:-1])
            self.val['pid'] = pid

        self.val['memory process'] = '%-*s%s' % (self.width-5, self.val['name'][0:self.width-5], cprint(self.val['max'], 'f', 5, 1024))

        ### Debug (show PID)
#       self.val['memory process'] = '%*s %-*s' % (5, self.val['pid'], self.width-6, self.val['name'])

    def showcsv(self):
        return '%s / %d%%' % (self.val['name'], self.val['max'])

# vim:ts=4:sw=4:et
