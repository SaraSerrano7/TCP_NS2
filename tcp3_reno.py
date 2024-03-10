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


def calculate_rto():

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
    #############3

    with open('files/problem3_v3/cw.newreno3', 'r') as file:
        trace_data = file.read()

    # Parse the trace data
    lines = trace_data.strip().split('\n')
    new_reno_time_list = []
    new_reno_cw_list = []
    for line in lines:
        new_reno_time, new_reno_cw = map(float, line.split())
        new_reno_cw_list.append(new_reno_cw)
        new_reno_time_list.append(new_reno_time)

    ################
    plt.figure(1)
    plt.plot(reno_time_list, reno_cw_list, color='red', label='TCP Reno CW')
    plt.plot(new_reno_time_list, new_reno_cw_list, color='blue', label='TCP New Reno CW')

    plt.xlabel('Time')
    plt.ylabel('CW')
    plt.title('CW Evolution')
    plt.legend()
    plt.grid(True)
    plt.show()

    ###############

    with open('files/problem3_v3/sor.reno1', 'r') as file:
        trace_data = file.read()

    # Parse the trace data
    lines = trace_data.strip().split('\n')

    RTT, CW, THROUGHPUT = computing_timeout(lines)

    plot_time = []
    plot_rto = []
    for line in RTT:
        time = line[0]
        rto = line[1]

        plot_time.append(time)
        plot_rto.append(rto)

    plot_time, plot_rto = improve_rto(plot_time, plot_rto)
    ##################
    with open('files/problem3_v3/sor.newreno3', 'r') as file:
        trace_data = file.read()

    # Parse the trace data
    new_reno_lines = trace_data.strip().split('\n')

    _, _, new_reno_THROUGHPUT = computing_timeout(new_reno_lines)

    new_reno_plot_time = []
    new_reno_plot_tp = []
    for line in new_reno_THROUGHPUT:
        new_reno_time = line[0]
        new_reno_tp = line[1]

        new_reno_plot_time.append(new_reno_time)
        new_reno_plot_tp.append(new_reno_tp)

    # new_reno_plot_time, new_reno_plot_tp = improve_throughput(new_reno_plot_time, new_reno_plot_tp)


    ##############
    plt.figure(2)

    reno_tp_time = []
    reno_tp_tp = []
    for line in THROUGHPUT:
        time = line[0]
        tp = line[1]

        reno_tp_time.append(time)
        reno_tp_tp.append(tp)

    # reno_tp_time, reno_tp_tp = improve_throughput(reno_tp_time, reno_tp_tp)

    plt.plot(reno_tp_time, reno_tp_tp, color='red', label='TCP Reno Throughput')
    plt.plot(new_reno_plot_time, new_reno_plot_tp, color='blue', label='TCP New Reno Throughput')

    plt.xlabel('Time')
    plt.ylabel('Kbps')
    plt.title('THROUGHPUT Evolution')
    plt.legend()
    plt.grid(True)
    plt.show()

#############3




#     with open('files/problem3_v2/to.slow10.rtt', 'r') as file:
#         to_trace_data = file.read()
#     to_lines = to_trace_data.strip().split('\n')
#     real_time_list = []
#     real_rto_list = []
#     for line in to_lines:
#         real_time, real_rto = map(float, line.split())
#         real_rto_list.append(real_rto)
#         real_time_list.append(real_time)
#     plt.plot(real_time_list, real_rto_list, color='red', label='simulated')
#
#     plt.xlabel('Time')
#     plt.ylabel('RTO')
#     plt.title('RTO Evolution')
#     plt.legend()
#     plt.grid(True)
#     plt.show()
# ###############
#     with open('files/problem3_v2/cw.slow10', 'r') as file:
#         trace_data = file.read()
#
#     # Parse the trace data
#     cw_lines = trace_data.strip().split('\n')
#     real_cw_time_list = []
#     real_cw_rto_list = []
#     for line in cw_lines:
#         real_cw_time, real_cw = map(float, line.split())
#         real_cw_rto_list.append(real_cw)
#         real_cw_time_list.append(real_cw_time)
#
#     plot_cw_time = []
#     plot_cw = []
#     for line in CW:
#         cw_time = line[0]
#         cw = line[1]
#         plot_cw_time.append(cw_time)
#         plot_cw.append(cw)
#
#     plot_cw_time, plot_cw = improve_cw(plot_cw_time, plot_cw)
#     plt.figure(2)
#
#     plt.plot(plot_cw_time, plot_cw, color='blue', label='calculated')
#     plt.plot(real_cw_time_list, real_cw_rto_list, color='red', label='simulated')
#     plt.xlabel('Time')
#     plt.ylabel('CW')
#     plt.title('CW Evolution')
#     plt.legend()
#     plt.grid(True)
#     plt.show()


def improve_throughput(plot_tp_time: list[float], plot_tp: list[float]):
    improved_tp_time = []
    improved_tp = []

    tp_counter = 1
    time_counter = 0.00
    time_tick = 0.01

    for time, tp in zip(plot_tp_time, plot_tp):
        while time_counter < time:
            improved_tp_time.append(time_counter)
            improved_tp.append(tp_counter)
            time_counter += time_tick
        improved_tp_time.append(time)
        improved_tp.append(tp)
        tp_counter = tp
        time_counter = time
    while time_counter < 200.0:
        improved_tp_time.append(time_counter)
        improved_tp.append(tp_counter)
        time_counter += time_tick
    return improved_tp_time, improved_tp


def improve_cw(plot_cw_time: list[float], plot_cw: list[float]):
    improved_cw_time = []
    improved_cw = []

    cw_counter = 1
    time_counter = 0.00
    time_tick = 0.01

    for time, cw in zip(plot_cw_time, plot_cw):
        while time_counter < time:
            improved_cw_time.append(time_counter)
            improved_cw.append(cw_counter)
            time_counter += time_tick
        improved_cw_time.append(time)
        improved_cw.append(cw)
        cw_counter = cw
        # time_counter = time
        # while time_counter < 200.0:
        #     improved_cw_time.append(time_counter)
        #     improved_cw.append(cw_counter)
        #     time_counter += time_tick
    return improved_cw_time, improved_cw



def improve_rto(plot_time: list[float], plot_rto: list[float]):
    improved_time = []
    improved_rto = []

    rto_counter = 3
    time_counter = 0.00
    time_tick = 0.01

    for time, rto in zip(plot_time, plot_rto):
        time = round(time, 2)

        while time_counter < time:

            # if time_counter < time:
            improved_time.append(time_counter)
            improved_rto.append(rto_counter)
            time_counter += time_tick
            # print(time_counter, rto_counter)
        else:
            improved_time.append(time)
            improved_rto.append(rto)
            rto_counter = rto
            # print(time, rto)

    return improved_time, improved_rto


def computing_timeout(trace: list[str]):
    first_packet = True
    packets_sent = []
    timeouts = []

    duplicates = {}
    third_dup_retrans = False

    queue = []

    alpha = 1 / 8
    beta = 1 / 4
    timeout = 3
    rttvar = 0
    srtt = None

    rtt_active = 0

    ######################
    cw = []
    CWMAX = 10
    cwini = 1
    cwmax = CWMAX

    cwnd = cwini
    previous_cwnd = cwnd
    previous_cwmax = cwmax

    acks_number = 0

    throughpput_list = []

    for line in trace:
        data = line.strip().split(' ')
        current_packet = Packet(data[0], float(data[1]), int(data[2]), int(data[3]), data[4], int(data[5]),
                                data[6], int(data[7]), data[8], data[9], int(data[10]), int(data[11]))

        # CHECK FOR TIMEOUTS
        for sent in packets_sent:
            sent_time = sent.time
            current_time = current_packet.time
            fake_rtt = current_time - sent_time
            if fake_rtt > timeout:
                # print(str(current_packet.time) + " timedout! " + str(sent.seq_num))
                packets_sent.remove(sent)
                rtt_active = 0

                ##############
                timeout *= 2
                ##############


                previous_cwnd = cwnd
                previous_cwmax = cwmax
                cwnd = cwini
                cwmax = max(cwini, int(cwmax/2))
                cw.append([current_packet.time, cwnd])
                # print(str(current_packet.time) + " TIMEOUT: added cw - cwmax " + str(cwnd) + " " + str(cwmax))

        for pending_packet in queue:
            sent_time = pending_packet.time
            current_time = current_packet.time
            fake_rtt = current_time - sent_time
            if fake_rtt > timeout:
                # print(str(current_packet.time) + " pending packet timedout! " + str(pending_packet.seq_num))
                queue.remove(pending_packet)

                ############
                # cwnd = cwini
                # cwmax = max(cwini, int(cwmax / 2))
                # cw.append([current_packet.time, cwnd])

        # IF PACKET SENT
        if current_packet.event_type == '-' and current_packet.source == 1 and current_packet.segment_type == 'tcp':



            already_sent = [packet.seq_num for packet in packets_sent]
            # print(str(current_packet.time) + " waiting for " + str(already_sent))
            if current_packet.seq_num in [packet.seq_num for packet in queue]:
                # print(str(current_packet.time) + " sending pending packet " + str(current_packet.seq_num))
                pending_packet = [packet for packet in queue if packet.seq_num == current_packet.seq_num][0]
                # print(str(current_packet.time) + " retransmittion from " + str(pending_packet.time))
                rtt_pending_packet = current_packet.time - pending_packet.time
                # print(str(current_packet.time) + " rtt: " + str(rtt_pending_packet))
                # print(str(current_packet.time) + " timeout timer " + str(timeout))
                # print(rtt_pending_packet > timeout)
                if rtt_pending_packet > timeout:
                    rtt_active = 0
                    timeout *= 2
                    ############
                    # cwnd = cwini
                    # cwmax = max(cwini, int(cwmax / 2))
                    # cw.append([current_packet.time, cwnd])

            # if third_dup:
            # if current_packet.time < no_more_packets:
            # queue.append(current_packet)
            # third_dup = False
            # continue

            if rtt_active == 0:
                rtt_active = 1
                packets_sent.append(current_packet)
                # print(str(current_packet.time) + " sent " + str(current_packet.seq_num))
            else:
                # print(str(current_packet.time) + " can't send " + str(current_packet.seq_num))
                queue.append(current_packet)

        # IF ACK RECEIVED
        if current_packet.event_type == 'r' and current_packet.target == 1 and current_packet.segment_type == 'ack':
            ########
            # si en el mismo momento ha habido timeout y ack --> no se reduce cw
            # if cw and cw[-1][0] == current_packet.time:
            #     print("found invalid cw reduction")
            #     cw.pop(len(cw) -1)
            #     cwnd = previous_cwnd
            #     cwmax = previous_cwmax


            if cwnd < cwmax:
                cwnd += 1
                cw.append([current_packet.time, cwnd])
            else:
                cwnd += 1 / cwnd
                cwmax = min(CWMAX, cwnd)
                cw.append([current_packet.time, cwnd])
            # print(str(current_packet.time) + " ACK: added cw - cwmax " + str(cwnd) + " " + str(cwmax))
            ############

            # print(str(current_packet.time) + " received " + str(current_packet.seq_num))
            if current_packet.seq_num in [sent.seq_num for sent in packets_sent]:



                matching_packet = [sent for sent in packets_sent if sent.seq_num == current_packet.seq_num][0]

                if first_packet:
                    first_packet = False
                    rtt = current_packet.time - matching_packet.time
                    # print("Calculating rtt: " + str(rtt))
                    srtt = rtt
                    rttvar = rtt / 2
                    timeout = round(srtt + 4 * rttvar, 2)
                    if timeout < 0.01:
                        timeout = 0.01
                    # print("Calculated: " + str(current_packet.time) + ", " + str(timeout))
                    print("Contributed to RTT update: " + str(current_packet.seq_num))
                    acks_number += 1
                    timeouts.append([current_packet.time, timeout])

                    throughput = ( (matching_packet.segment_size * 8) / rtt ) / 1024
                    print(throughput)
                    throughpput_list.append([current_packet.time, throughput])

                    ############
                    # if cwnd < cwmax:
                    #     cwnd += 1
                    #     cw.append([current_packet.time, cwnd])
                    # else:
                    #     cwnd += 1/cwnd
                    #     cwmax = min(CWMAX, cwnd)
                    #     cw.append([current_packet.time, cwnd])

                else:
                    rtt = current_packet.time - matching_packet.time
                    diff = rtt - srtt
                    srtt = (7 / 8) * srtt + (1 / 8) * rtt
                    rttvar = (3 / 4) * rttvar + (1 / 4) * abs(diff)
                    timeout = round(srtt + 4 * rttvar, 2)
                    # print("Calculated: " + str(current_packet.time) + ", " + str(timeout))
                    print("Contributed to RTT update: " + str(current_packet.seq_num))
                    if timeout < 0.01:
                        timeout = 0.01
                    acks_number += 1
                    timeouts.append([current_packet.time, timeout])

                    throughput = ((matching_packet.segment_size * 8) / rtt) / 1024
                    print(throughput)
                    throughpput_list.append([current_packet.time, throughput])

                    ############
                    # if cwnd < cwmax:
                    #     cwnd += 1
                    #     cw.append([current_packet.time, cwnd])
                    # else:
                    #     cwnd += 1 / cwnd
                    #     cwmax = min(CWMAX, cwnd)
                    #     cw.append([current_packet.time, cwnd])

                packets_sent.remove(matching_packet)
                rtt_active = 0
            else:
                # print(str(current_packet.time) + " didnt expect " + str(current_packet.seq_num))
                # print("queue: " + str([packet.seq_num for packet in queue]))

                if current_packet.seq_num not in duplicates.keys():
                    duplicates[current_packet.seq_num] = 1
                    # print(str(current_packet.time) + " first duplicate " + str(current_packet.seq_num))
                elif duplicates[current_packet.seq_num] == 3:
                    # print(str(current_packet.time) + " third dup! " + str(current_packet.seq_num))
                    # print(str(current_packet.time) + " wont accept packets until " + str(current_packet.time + timeout))
                    duplicates.pop(current_packet.seq_num)
                    rtt_active = 0
                    third_dup_retrans = True
                else:
                    # print(str(current_packet.time) + " dup! " + str(current_packet.seq_num))
                    duplicates[current_packet.seq_num] += 1

                pending_packet = [packet for packet in queue if packet.seq_num == current_packet.seq_num]
                # for packet in pending_packet:
                    # print(str(current_packet.time) + " pending packets " + str(packet.seq_num))

    print("Throughtput = Successfully transmitted data / Simulation time")
    print("Throughtput = " + str(acks_number) + " / 200 = " + str(acks_number / 200))

    return timeouts, cw, throughpput_list


if __name__ == '__main__':
    calculate_rto()
