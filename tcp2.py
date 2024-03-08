import matplotlib

matplotlib.use('TkAgg')  # Use the TkAgg backend or another suitable one
import matplotlib.pyplot as plt


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
    # trace_data = "" sor.slow7
    with open('files/problem3_v2/sor.slow10', 'r') as file:
        trace_data = file.read()

    # Parse the trace data
    lines = trace_data.strip().split('\n')

    RTT = computing_timeout(lines)

    plot_time = []
    plot_rto = []
    for line in RTT:
        time = line[0]
        rto = line[1]

        plot_time.append(time)
        plot_rto.append(rto)

    plot_time, plot_rto = improve_rto(plot_time, plot_rto)
    plt.plot(plot_time, plot_rto, color='blue', label='calculated')

    with open('files/problem3_v2/to.slow10.rtt', 'r') as file:
        to_trace_data = file.read()
    to_lines = to_trace_data.strip().split('\n')
    real_time_list = []
    real_rto_list = []
    for line in to_lines:
        real_time, real_rto = map(float, line.split())
        real_rto_list.append(real_rto)
        real_time_list.append(real_time)
    plt.plot(real_time_list, real_rto_list, color='red', label='simulated')

    plt.xlabel('Time')
    plt.ylabel('RTO')
    plt.title('RTO Evolution')
    plt.legend()
    plt.grid(True)
    plt.show()


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
    packets_timer = {}
    timeouts = []

    duplicates = {}

    first_dup = []
    second_dup = []
    third_dup = []

    queue = []

    alpha = 1 / 8
    beta = 1 / 4
    timeout = 3
    rttvar = 0
    srtt = None

    rtt_active = 0

    totimer = None
    totimer_active = 0

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
                print(str(current_packet.time) + " timedout! " + str(sent.seq_num))
                packets_sent.remove(sent)
                rtt_active = 0

        for pending_packet in queue:
            sent_time = pending_packet.time
            current_time = current_packet.time
            fake_rtt = current_time - sent_time
            if fake_rtt > timeout:
                print(str(current_packet.time) + " pending packet timedout! " + str(pending_packet.seq_num))
                queue.remove(pending_packet)
                # rtt_active = 0


        # pending_packet = [packet for packet in queue if packet.seq_num == current_packet.seq_num]
        # if pending_packet:
        #     # el paquete que estamos
        #     print(str(current_packet.time) + " ")

        # IF PACKET SENT
        if current_packet.event_type == '-' and current_packet.source == 1 and current_packet.segment_type == 'tcp':


            already_sent = [packet.seq_num for packet in packets_sent]
            print(str(current_packet.time) + " waiting for " + str(already_sent))
            # if current_packet.seq_num in already_sent:
            #     print(str(current_packet.time) + " timed out " + str(current_packet.seq_num))
            #     rtt_active = 0
            if current_packet.seq_num in [packet.seq_num for packet in queue]:
                print(str(current_packet.time) + " sending pending packet " + str(current_packet.seq_num))
                pending_packet = [packet for packet in queue if packet.seq_num == current_packet.seq_num][0]
                print(str(current_packet.time) + " retransmittion from " + str(pending_packet.time))
                rtt_pending_packet = current_packet.time - pending_packet.time
                print(str(current_packet.time) + " rtt: " + str(rtt_pending_packet))
                print(str(current_packet.time) + " timeout timer " + str(timeout))
                print(rtt_pending_packet > timeout)
                if rtt_pending_packet > timeout:
                    rtt_active = 0

            if rtt_active == 0:
                rtt_active = 1
                packets_sent.append(current_packet)
                print(str(current_packet.time) + " sent " + str(current_packet.seq_num))
            else:
                print(str(current_packet.time) + " can't send " + str(current_packet.seq_num))
                queue.append(current_packet)


        # IF ACK RECEIVED
        if current_packet.event_type == 'r' and current_packet.target == 1 and current_packet.segment_type == 'ack':
            print(str(current_packet.time) + " received " + str(current_packet.seq_num))
            if current_packet.seq_num in [sent.seq_num for sent in packets_sent]:
                matching_packet = [sent for sent in packets_sent if sent.seq_num == current_packet.seq_num][0]

                if first_packet:
                    first_packet = False
                    rtt = current_packet.time - matching_packet.time
                    print("Calculating rtt: " + str(rtt))
                    srtt = rtt
                    rttvar = rtt / 2
                    timeout = round(srtt + 4 * rttvar, 2)
                    if timeout < 0.01:
                        timeout = 0.01
                    print("Calculated: " + str(current_packet.time) + ", " + str(timeout))
                    timeouts.append([current_packet.time, timeout])
                else:
                    rtt = current_packet.time - matching_packet.time
                    diff = rtt - srtt
                    srtt = (7 / 8) * srtt + (1 / 8) * rtt
                    rttvar = (3 / 4) * rttvar + (1 / 4) * abs(diff)
                    timeout = round(srtt + 4 * rttvar,2 )
                    print("Calculated: " + str(current_packet.time) + ", " + str(timeout))
                    if timeout < 0.01:
                        timeout = 0.01

                    timeouts.append([current_packet.time, timeout])
                packets_sent.remove(matching_packet)
                rtt_active = 0
            else:
                print(str(current_packet.time) + " didnt expect " + str(current_packet.seq_num))
                print("queue: " + str([packet.seq_num for packet in queue]))



                if current_packet.seq_num not in duplicates.keys():
                    duplicates[current_packet.seq_num] = 1
                    print(str(current_packet.time) + " first duplicate " + str(current_packet.seq_num))
                elif duplicates[current_packet.seq_num] == 3:
                    print(str(current_packet.time) + " third dup! " + str(current_packet.seq_num))
                    duplicates.pop(current_packet.seq_num)
                    rtt_active = 0
                else:
                    print(str(current_packet.time) + " dup! " + str(current_packet.seq_num))
                    duplicates[current_packet.seq_num] += 1

                pending_packet = [packet for packet in queue if packet.seq_num == current_packet.seq_num]
                for packet in pending_packet:
                    print(str(current_packet.time) + " pending packets " + str(packet.seq_num))



                if pending_packet and current_packet.seq_num in pending_packet:#current_packet.seq_num in [packet.seq_num for packet in queue]:
                    print(str(current_packet.time) + " conno dio da! " + str(current_packet.seq_num))
                    print(queue)
                    print(current_packet)
                    queue.remove(current_packet)
                    rtt_active = 0
            #
            #
            # if rtt_active == 1 and current_packet.seq_num in [packet.seq_num for packet in queue]:
            #     print(str(current_packet.time) + " packet " + str(current_packet.seq_num) + " queue ready to accept")
            #     matching_packet = [packet for packet in queue if packet.seq_num == current_packet.seq_num][0]
            #     rtt = current_packet.time - matching_packet.time
            #     if rtt < timeout:
            #         diff = rtt - srtt
            #         srtt = (7 / 8) * srtt + (1 / 8) * rtt
            #         rttvar = (3 / 4) * rttvar + (1 / 4) * abs(diff)
            #         timeout = round(srtt + 4 * rttvar,2 )
            #         print("Calculated: " + str(current_packet.time) + ", " + str(timeout))
            #         if timeout < 0.01:
            #             timeout = 0.01
            #
            #         timeouts.append([current_packet.time, timeout])
            #         queue.remove(matching_packet)
            #         rtt_active = 0
            #

    return timeouts



if __name__ == '__main__':
    calculate_rto()
