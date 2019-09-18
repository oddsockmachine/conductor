# step_beat with jitter adjustment
#
# circular buffer of 1x jitter and 3x note values
#
# balance between t1 and t3 (or t1,t2,t3 distribution and skew)
#
# create_distribution for distribution/bias/skew
import constants as c
from instruments.instrument import Instrument
from random import gauss, choice, randint
from collections import namedtuple

# nums = {x: 0 for x in range(-30, 30)}
#
# mu = 10
# sigma = 4
# for i in range(500):
#     num = gauss(mu, sigma)
#     nums[int(num)] = nums[int(num)] + 1
#
# for k, v in nums.items():
#     dots = "." * v
#     print(str(k) + " " + dots)

# print(choice('HT', cum_weights=(0.60, 1.00), k=7).count('H'))


class RingBuffer(object):
    def __init__(self, length):
        super(RingBuffer, self).__init__()
        self.max_length = 16
        self.length = max(length, self.max_length)
        self.buffer = [None for x in range(self.length)]
        self.position = 0

    def next(self):
        self.position = (self.position + 1) % self.length

    def set(self, data):
        self.buffer[self.position] = data

    def get(self):
        return self.buffer[self.position]

    def jump(self, place):
        self.position = place % self.length

    def set_length(self, length):
        self.length = length % self.max_length
        self.position = self.position % self.length

    def stats(self):
        print(self.position, str(self.buffer))


DJVPoint = namedtuple('DJVPoint', 't x1 x2 x3')


class Marbles(object):
    def __init__(self):  # , ins_num, mport, key, scale, octave=1, speed=1):
        super(Marbles, self).__init__()  # ins_num, mport, key, scale, octave, speed)
        self.type = "Marbles"
        self.prev_loc_beat = 0
        self.width = 16
        self.division = 3
        self.prev_jitter = 0
        self.ctl_jitter = 0
        self.max_jitter = 4
        self.ctl_clk_speed = 2
        self.ctl_t_bias = 0  # 0 to 10
        self.ctl_t_type = 0  # coin_toss or alternate
        self.last_picked_bias = 0
        self.ring_buffer = RingBuffer(16)
        self.ctl_djv = 0  # 0 to 15
        for i in range(8):
            self.ring_buffer.set(DJVPoint(randint(-3, 3), 0, 0, 0))
            self.ring_buffer.next()

    def calc_t_bias(self):
        if self.ctl_t_type is "coin_toss":
            items = {"1": self.ctl_t_bias, "3": 10-self.ctl_t_bias}
            t_bias = choice([k for k in items for dummy in range(items[k])])
            c.logging.info("t_bias is {}".format(t_bias))
            return t_bias
        else:
            offset = abs(5 - self.ctl_t_bias)
            a, b = ("1", "3") if self.ctl_t_bias > 5 else ("3", "1")
            items = [a] + [b] * offset
            self.last_picked_bias = (self.last_picked_bias + 1) % len(items)
            t_bias = items[self.last_picked_bias]
            c.logging.info("t_bias is {}".format(t_bias))
            return t_bias

    def jitter_source(self):
        self.prev_jitter
        self.ctl_jitter

    def has_beat_changed(self, local_beat):
        if self.prev_loc_beat != local_beat:
            self.prev_loc_beat = local_beat
            return True
        self.prev_loc_beat = local_beat
        return False

    def calc_local_beat(self, global_beat):
        '''Calc local_beat_pos for this instrument'''
        div = self.get_beat_division()
        jitter = self.ring_buffer.get().t
        local_beat = int((global_beat + jitter) / div) % self.width
        # print(local_beat)
        return int(local_beat)

    def get_beat_division(self):
        return 2**self.ctl_clk_speed

    def step_beat(self, global_beat):
        '''Increment the beat counter, and do the math on pages and repeats'''
        local = self.calc_local_beat(global_beat)
        if not self.has_beat_changed(local):
            # Intermediate beat for this instrument, do nothing
            print('.')
            return
        print('!')
        self.ring_buffer.next()
        self.local_beat_position = local
        new_notes = []
        # new_notes = self.get_next_notes()
        # self.output(self.old_notes, new_notes)
        self.old_notes = new_notes  # Keep track of which notes need stopping next beat
        return

    def generate_new_notes(self):
        # TODO put into buffer
        pass

    def get_next_notes(self):
        if self.ctl_djv < 11:
            # Chance of generating new data or using djv buffer
            c = choice(['new'] * self.ctl_djv + ['buffer'] * (11 - self.ctl_djv))
            c.logging.info("Choice is {}".format(c))
            if c is "buffer":
                # Get from ring buffer, if possible
                info = self.ring_buffer.get()
                if not info:  # Buffer needs filling, generate new
                    notes = self.generate_new_notes()
            else:
                # Generate new
                notes = self.generate_new_notes()
        else:
            # Chance of jumping around in buffer
            notes = []  # TODO
        return notes


m = Marbles()
for i in range(100):
    m.step_beat(i)
