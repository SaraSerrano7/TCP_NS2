import matplotlib

matplotlib.use('TkAgg')  # Use the TkAgg backend or another suitable one
import matplotlib.pyplot as plt


# def __init__(self, time: float, length: float, stream: float, bandwidth: float):
#     self.finish_time: float = 0.0
#     self.arrival_time: float = time
#     self.size: float = length
#     self.stream_id: float = stream
#     self.stream_bandwidth: float = bandwidth
#     self.balanced: bool = False

class Packet:
    # event_type = ""
    # time = 0.0
    # source = 0
    # target = 0
    # segment_type = ""
    # segment_size = 0
    # flags = ""
    # flow_id = 0
    # addr_source = ""
    # addr_target = ""
    # seq_num = 0
    # seq_id = 0

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
    # print(lines)

    # result = computing_timeout(lines)
    # print(result)

    # lines = trace_data_2.strip().split('\n')
    # time = []
    # congestion_window = []
    # for line in lines:
    #     t, cwnd = map(float, line.split())
    #     time.append(t)
    #     congestion_window.append(cwnd)

    # Plot congestion window over time
    # plt.plot(time, congestion_window, label='Congestion Window')
    # plt.xlabel('Time')
    # plt.ylabel('Congestion Window')
    # plt.title('Congestion Window Evolution')
    # plt.legend()
    # plt.grid(True)
    # plt.show()

    ###############################3
    # rto = 1 # podria empezar por 3?
    # RTT = find_rtt(lines)
    # print(RTT)
    # #RTT = extend_rtt_time(RTT)
    # RTT = calculate_trace_rto(RTT)

    RTT = computing_timeout(lines)
    # print(RTT)

    plot_time = []
    plot_rto = []
    for line in RTT:
        time = line[0]
        rto = line[1]

        plot_time.append(time)
        plot_rto.append(rto)
    #     t, cwnd = map(float, line.split())
    #     time.append(t)
    #     congestion_window.append(cwnd)
    #
    # Plot congestion window over time
    # print(RTT)

    plot_time, plot_rto = improve_rto(plot_time, plot_rto)
    # print(plot_time, plot_rto)

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

    # plot_real_rto = [line.split()[1] for line in to_lines]
    # print(plot_real_rto)
    # print(real_rto_list)
    plt.plot(real_time_list, real_rto_list, color='red', label='simulated')

    plt.xlabel('Time')
    plt.ylabel('RTO')
    plt.title('RTO Evolution')
    plt.legend()
    plt.grid(True)
    plt.show()

    # print(RTT)
    # CWMAX = 10
    # cwini = 1
    # cwmax = CWMAX
    #######################
    # Let's find rto_ first
    #######################

    # print(lines)
    # find_RTT(lines)
    # SRTT = first_RTT_sample
    # alpha = 1/8
    # beta = 1/4
    # SRTT = alpha * RTT_sample + (1 - alpha) * SRTT
    # RTTVAR = 0.5 * first_RTT_sample
    # RTTVAR = (1 - beta) * RTTVAR + beta * abs(SRTT - RTT_sample)
    # rto = SRTT + 4 * RTTVAR

    # lines = trace_data_2.strip().split('\n')
    # time = []
    # congestion_window = []
    # for line in lines:
    #     t, cwnd = map(float, line.split())
    #     time.append(t)
    #     congestion_window.append(cwnd)
    #
    # # Plot congestion window over time
    # plt.plot(time, congestion_window, label='Congestion Window')
    # plt.xlabel('Time')
    # plt.ylabel('Congestion Window')
    # plt.title('Congestion Window Evolution')
    # plt.legend()
    # plt.grid(True)
    # plt.show()


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
            print(time_counter, rto_counter)


        else:
            improved_time.append(time)
            improved_rto.append(rto)
            rto_counter = rto
            print(time, rto)

    return improved_time, improved_rto


def calculate_trace_rto(rtt):
    rto_list = []

    # rto_list.append([pa])
    # rtt_new = rtt[0][1]
    # actual_rtt = rtt[0][1]
    # # dev_new = abs(rtt_new - rtt_init)
    # actual_dev = abs(rtt_init - actual_rtt)
    # rto = 4 * dev_init + rtt_init

    alpha = 7 / 8  # 1/8
    beta = 1 / 4

    rtt_init = 3
    dev_init = 0
    # packet: [ack arrival time, rtt]
    for packet in rtt:
        diff = packet[1] - rtt_init
        rtt_init = rtt_init + alpha * diff
        dev_init = dev_init + beta * (abs(diff) - dev_init)
        rto = (rtt_init + 4 * dev_init)
        rto_list.append([packet[0], rto])
    ###############
    # rtt_init = alpha * rtt_init + (1 - alpha) * actual_rtt
    # dev_init = beta * dev_init + (1 - beta) * actual_dev
    # rto = (4 * dev_init + rtt_init)
    # rto_list.append([packet[0], rto])
    # actual_rtt = packet[1]
    # actual_dev = abs(rtt_init - actual_rtt)
    ##########################3
    # rtt_new = alpha * rtt_init + (1 - alpha) * rtt_new
    # dev_new = beta * dev_init + (1 - beta) * dev_new
    # rto_new = 4 * dev_new + rtt_new
    # rto_list.append([packet[0], rto_new])

    return rto_list

    # rtt_new = packet[1]
    # packet_arrival = packet[0]
    # dev_new = abs(rto_init - rtt_new)


def computing_timeout(trace: list[str]):
    first_packet = True
    packets_sent = []
    packets_timer = {}
    timeouts = []

    duplicates = {}

    first_dup = []
    second_dup = []
    third_dup = []


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

        # for sent in packets_sent:
        #     sent_time = sent.time
        #     current_time = current_packet.time
        #     fake_rtt = current_time - sent_time
        #     if fake_rtt > timeout:
                # print(str(current_packet.time) + " timedout! " + str(current_packet.seq_num))
                # packets_sent.remove(sent)
                # rtt_active = 0

        # IF PACKET SENT
        if current_packet.event_type == '-' and current_packet.source == 1 and current_packet.segment_type == 'tcp':
            # paquete enviado
            # packets_timer[current_packet] = rtt_active
            print(str(current_packet.time) + " - reading packet " + str(current_packet.seq_num) + " - timer " + str(rtt_active))
            # cuenta atrás para el timeout
            if totimer_active == 0:
                totimer = timeout
                totimer_active = 1


            # Se cuenta lo que tarda en ir y volver
            if rtt_active == 0:
                rtt_active = 1

                packets_sent.append(current_packet)
                print("added: " + str(current_packet.seq_num))
                # añadir paquete a los que esperan ack
                # rtt_seq = nseq # ???

            # si el paquete que llega ya se ha enviado --> retransmision --> ha habido timeout
            already_sent = [sent_packet.seq_num for sent_packet in packets_sent if sent_packet.time != current_packet.time]
            print(str(current_packet.time) + ", packets sent: " + str(already_sent))
            if current_packet.seq_num in already_sent:
                print("retransmitted: " + current_packet.to_string())
                rtt_active = 0

                # totimer = 0

        # IF ACK RECEIVED
        elif current_packet.event_type == 'r' and current_packet.target == 1 and current_packet.segment_type == 'ack':

            # totimer

            if not packets_sent:
                rtt_active = 0
                print("no packets were sent")

            matching_packet = [packet for packet in packets_sent if packet.seq_num == current_packet.seq_num]
            # print(str(matching_packet) + ' - ' + current_packet.to_string())
            # print(current_packet.seq_num == matching_packet[0].seq_num)

            if matching_packet:
                print("matching_packet: " + str(len(matching_packet)))
                rtt = current_packet.time - matching_packet[0].time
                if rtt > timeout:
                    print("timeout! - " + current_packet.to_string())
                    rtt_active = 0
            else:  # duplicated ack

                # if current_packet.seq_num not in duplicates.keys():
                #     duplicates[current_packet.seq_num] = 1
                # else:
                #     duplicates[current_packet.seq_num] += 1
                #
                # if duplicates[current_packet.seq_num] == 3:
                #     print(str(current_packet.time) + " " + str(duplicates[current_packet.seq_num]) + " duplicates of " + str(current_packet.seq_num))
                #     rtt_active = 0
                #     duplicates.pop(current_packet.seq_num)




                if current_packet.seq_num in third_dup:
                # if duplicates.count(current_packet.seq_num) == 3:
                    # TODO: esto debe ser al tercer duplicado. third_dup tiene la 3a copia --> segundo duplicado!!
                    # print(str(current_packet.time) + ' third ' + str(current_packet.seq_num) + '! - ' + str(duplicates.count(current_packet.seq_num)))
                    # print(str(duplicates.count(current_packet.seq_num)) + "duplicated from " + str(current_packet.seq_num))
                    rtt_active = 0
                    third_dup.remove(current_packet.seq_num)
                    # duplicates.remove(current_packet.seq_num)
                    # duplicates.remove(current_packet.seq_num)
                    # duplicates.remove(current_packet.seq_num)
                else:
                    print('duplicate! ' + current_packet.to_string())

                    third_dup.append(current_packet.seq_num)
                    # duplicates.append(current_packet.seq_num)
                    # print(
                    #     str(current_packet.seq_num) + " has " + str(duplicates.count(current_packet.seq_num)) + " dups")



            if rtt_active == 1 and matching_packet and current_packet.seq_num == matching_packet[0].seq_num:
                # in [packet.seq_num for packet in packets_sent]: #nack == rtt_seq:

                if first_packet:
                    first_packet = False
                    rtt = current_packet.time - matching_packet[0].time
                    srtt = rtt
                    rttvar = rtt / 2
                    timeout = srtt + 4 * rttvar
                    if timeout < 0.01:
                        timeout = 0.01
                    # timeout *= 0.01
                    timeouts.append([current_packet.time, timeout])
                else:
                    rtt = current_packet.time - matching_packet[0].time
                    diff = rtt - srtt
                    srtt = (7 / 8) * srtt + (1 / 8) * rtt
                    rttvar = (3 / 4) * rttvar + (1 / 4) * abs(diff)
                    timeout = srtt + 4 * rttvar
                    print("Calculated: " + str(current_packet.time) + ", " + str(timeout))
                    if timeout < 0.01:
                        timeout = 0.01
                    # timeout *= 0.01

                    timeouts.append([current_packet.time, timeout])

                # timeout = get_timeout()
                # timeouts.append([current_packet.time, timeout])
                # packet_index = packets_sent.index(matching_packet[0])
                packets_sent.remove(matching_packet[0])
                rtt_active = 0  # todo: change to boolean
                print("packet " + str(current_packet.seq_num) + " accepted")

            # esta comprobacion va aqui?
            # if current_packet.time - [pack] > timeout:
            #     rtt_active = 0
            # if current_packet.rtt > timeout:
            #     rtt_active = 0

            # if third duplicate:
            #     rtt_active = 0
    return timeouts


def get_timeout():
    # Ceil up to a minimoum value: 0.01
    return 0.01
    pass


def calculate_cw(trace: list[str]):
    pass


# todo warning: el rto se multiplica por el timetick!
def extend_rtt_time(rtt):
    # tenemos los rtt de todos los paquetes, pero nos falta saber el
    # rtt por cada 0.01s. Vamos a asumir que entre paquetes se mantiene igual
    # ordered_rtt = rtt.copy()
    # ordered_rtt.sort(key=lambda x: float(x[0]))
    # sorted(rtt, )
    # print(ordered_rtt)
    rto = 3.0
    extended_rtt = []
    timeTick = 0.01
    # print(rtt)
    srtt = rtt[0][1]
    alpha = 7 / 8
    beta = 1 / 4
    rttvar = rtt[0][1] / 2
    # print(f'first srtt: {srtt}')
    for packet in rtt:
        srtt = alpha * packet[1] + (1 - alpha) * srtt
        rttvar = (1 - beta) * rttvar + beta * abs(srtt - packet[1])
        rto = (srtt + 4 * rttvar)  # * timeTick
        extended_rtt.append([packet[0], rto])

    # while timeTick <= 200.0:
    #
    #     timeTick += 0.01
    # for timeTick in range(0.0, 200.0, 0.01):
    #     print(timeTick)

    # time = 0.00
    # while time < 200.0:
    #     rtt_moment = rtt[0]
    #     time += 0.01
    # print(len(extended_rtt))
    return extended_rtt


def find_rtt(trace: list[str]):
    sent = []
    rtt = []
    rtt2 = []
    result = []
    for line in trace:
        line = line.strip().split(' ')
        # print(round(float(line[1]), 2))
        # print(type(line))
        # print(line[0])
        # print(line[2])

        #  and line[2] == "1"
        if line[0] == '-' and line[4] == 'tcp':  # nos quedamos con los paquetes del agente tcp
            # print('sent')
            # print(line)
            pkt = Packet(line[0], float(line[1]), int(line[2]), int(line[3]), line[4], int(line[5]), line[6],
                         int(line[7]), line[8], line[9],
                         int(line[10]), int(line[11]))
            sent.append(pkt)
            rtt.append(0.0)
            # sent_time = pkt.time
        #      and line[3] == '1'
        elif line[0] == 'r' and line[4] == 'ack':
            for p in sent:
                # print(p.seq_num == int(line[10]) and p.source == line[3])
                # print(f'{p.source} == {line[3]}, {p.target} == {line[2]}')
                if p.seq_num == int(line[10]) and p.source == int(line[3]):
                    # print('received' + p.to_string())
                    # print(line[1], line[10])
                    pkt_index = sent.index(p)
                    arrival_time = float(line[1])
                    rtt_time = arrival_time - p.time
                    rtt[pkt_index] = [round(float(line[1]), 2), rtt_time]
                    rtt2.append(
                        [round(float(line[1]), 2), rtt_time])  # todo maybe deberia appendear el paquete y su rtt
                    break
    # print(sent)
    # print(rtt)
    # print(len(sent), len(rtt))

    # return rtt
    return rtt2


if __name__ == '__main__':
    calculate_rto()
