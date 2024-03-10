import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')


class Packet:
    def __init__(self, event_type, time, source, target, segment_type, segment_size,
                 flags, flow_id, addr_source, addr_target, seq_num, seq_id):
        self.event_type = event_type
        self.time = time
        self.source = source
        self.target = target
        self.segment_type = segment_type
        self.segment_size = segment_size
        self.flags = flags
        self.flow_id = flow_id
        self.addr_source = addr_source
        self.addr_target = addr_target
        self.seq_num = seq_num
        self.seq_id = seq_id

    def to_string(self) -> str:
        """
        This function returns the content of the packet as a string
        :return: string
        """
        return f'event_type: {self.event_type},\t ' \
               f'time: {self.time},\t ' \
               f'source: {self.source},\t ' \
               f'target: {self.target},\t ' \
               f'segment_type: {self.segment_type}\t' \
               f'segment_size: {self.segment_size},\t ' \
               f'flags: {self.flags},\t ' \
               f'flow_id: {self.flow_id},\t ' \
               f'addr_source: {self.addr_source}\t' \
               f'addr_target: {self.addr_target},\t ' \
               f'seq_num: {self.seq_num},\t ' \
               f'seq_id: {self.seq_id},\t '


def plot():
    with open('files/problem3_v3/cw.reno1', 'r') as file:
        trace_data = file.read()

    # Parse the trace data
    lines = trace_data.strip().split('\n')
    reno_time_list = []
    reno_cw_list = []
    for line in lines:
        reno_time, reno_cw = map(float, line.split())
        reno_cw_list.append(reno_cw)
        reno_time_list.append(reno_time)

##########################

    with open('files/problem3_v2/cw.slow10', 'r') as file:
        trace_data = file.read()

    # Parse the trace data
    lines = trace_data.strip().split('\n')
    tahoe_time_list = []
    tahoe_cw_list = []
    for line in lines:
        tahoe_time, tahoe_cw = map(float, line.split())
        tahoe_cw_list.append(tahoe_cw)
        tahoe_time_list.append(tahoe_time)

    plt.plot(tahoe_time_list, tahoe_cw_list, color='blue', label='TCP Tahoe (No fast retransmit)')
    plt.plot(reno_time_list, reno_cw_list, color='red', label='TCP Reno (Fast retransmit)')

    plt.xlabel('Time')
    plt.ylabel('CW')
    plt.title('CW Evolution')
    plt.legend()
    plt.grid(True)
    plt.show()

# ###############



    # plt.figure(2)


    # plt.xlabel('Time')
    # plt.ylabel('CW')
    # plt.title('CW Evolution')
    # plt.legend()
    # plt.grid(True)
    # plt.show()

if __name__ == '__main__':
    plot()
