from ...classes import Solution


class Scanner:
    def __init__(self, range):
        self.range = range
        self.start_position = 0
        self.end_position = 0
        self.direction = 1

    @property
    def positions(self):
        return self.start_position, self.end_position

    def step(self):
        if self.range is not None:
            self.start_position = self.end_position
            if (self.direction == 1 and self.end_position == self.range - 1) or (self.direction == -1 and self.end_position == 0):
                self.direction *= -1
            self.end_position = self.end_position + self.direction
        else:
            self.start_position = self.end_position = None


class Firewall:
    def __init__(self, scanners):
        self.scanners = scanners
        self.state = [(0,0) for scanner in self.scanners]
        self.width = len(self.scanners)

    def step(self):
        for scanner in self.scanners:
            scanner.step()
        self.state = [scanner.positions for scanner in self.scanners]

    def get_severity(self, position):
        scanner = self.scanners[position]
        if scanner.start_position == 0:
            return position*scanner.range
        return 0

    def detected(self, position):
        if position is None:
            return False
        scanner = self.scanners[position]
        if scanner.start_position == 0:
            return True
        return False

    def reset(self):
        for scanner in self.scanners:
            scanner.__init__(scanner.range)


def parse_input(data):
    ranges = {}
    for line in data:
        depth, scanner_range = (int(i.strip()) for i in line.split(':'))
        ranges[depth] = scanner_range
    return [Scanner(ranges.get(i, None)) for i in range(max(ranges.keys()) + 1 )]


def phase1(data):
    firewall = Firewall(data)
    total_severity = 0
    for i in range(firewall.width):
        firewall.step()
        total_severity += firewall.get_severity(i)
    return total_severity


def phase2(data):
    firewall = Firewall(data)
    delay = 0
    while True:
        positions = [None for picosecond in range(delay)]
        positions.extend(range(firewall.width))

        detected = False
        firewall.reset()
        for position in positions:
            firewall.step()
            if firewall.detected(position):
                detected = True
                break
        if not detected:
            return delay
        delay += 1

solution = Solution(2017, 13, phase1=phase1, phase2=phase2, input_parser=parse_input)