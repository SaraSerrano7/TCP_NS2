if {$argc == 1} {
    set flag  [lindex $argv 0] 

} else {
    puts "      CBR0-UDP n0"
    puts "                \\"
    puts "                 n2 ---- n3"
    puts "                /"
    puts "      CBR1-TCP n1 "
    puts ""
    puts "  Usage: ns $argv0 (0: original, 1: incr lineal, 2: slow start) "
    puts ""
    exit 1
}


if {$flag==0} {
	set trailer .tcporig
}
if {$flag==1} {
	set trailer .linc
}
if {$flag==2} {
	set trailer .slow7
}


set tracefile sor$trailer
set cwfile cw$trailer

# File with rto_
set timeoutFile to$trailer


# Creating the simulator object
set ns [new Simulator]

#file to store results
set nf [open $tracefile  w]
$ns trace-all $nf

set nff [open $cwfile  w]

set nfff [open $timeoutFile.rtt w]


#Finishing procedure
proc finish {} {
        global ns nf nff tracefile cwfile trailer 
        $ns flush-trace
	# Process "sor.tr" to get sent packets
	exec awk {{ if ($1=="-" && $3==1 && $4=2) print $2, 49}}  $tracefile > tx$trailer
	# Process "sor.tr" to get dropped packets
	exec awk {{ if ($1=="d" && $3==2 && $4=3) print $2, 44}}  $tracefile  > drop$trailer
	exec awk {{  print $2,$3}}  $tracefile  > out$trailer

        close $nf
        close $nff
        exit 0
}
# TCP times recording procedure
proc record { } {
	global ns tcp1 nff nfff tcp1
	# Getting the congestion window
    set cw  [$tcp1 set cwnd_] 
	set now [$ns now]
	puts $nff "$now $cw"

	$ns at [expr $now+0.1] "record"
	
	set rto [expr [$tcp1 set rto_] * [$tcp1 set tcpTick_]]
	puts $nfff "$now $rto"
}
#Create 4 nodes
#
#  n0
#  \
#   \
#    n2--------n3
#   /
#  /
# n1
 
set n0 [$ns node]
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]

#Duplex lines between nodes
#$ns duplex-link $n0 $n2 5Mb 20ms DropTail
#$ns duplex-link $n0 $n2 250Kb 20ms DropTail
$ns simplex-link $n0 $n2 250Kb 20ms DropTail
$ns simplex-link $n2 $n0 250Kb 20ms DropTail
# Node 2 buffer size: 20 (default es 20 packets)
$ns queue-limit $n2 $n0 20

#$ns duplex-link $n1 $n2 5Mb 20ms DropTail
#$ns duplex-link $n1 $n2 250Kb 20ms DropTail
$ns simplex-link $n1 $n2 250Kb 20ms DropTail
$ns simplex-link $n2 $n1 250Kb 20ms DropTail	
# Node 2 buffer size: 20 (default es 20 packets)		
$ns queue-limit $n2 $n1 20


#$ns duplex-link $n2 $n3 1Mb 50ms DropTail
#$ns duplex-link $n2 $n3 50Kb 500ms DropTail
$ns simplex-link $n2 $n3 50Kb 500ms DropTail
$ns simplex-link $n3 $n2 50Kb 500ms DropTail
# Node 2 buffer size: 20 (default es 20 packets)
$ns queue-limit $n2 $n3 20				

# Node 0:  UDP agent with Exponential  traffic generator
set udp0 [new Agent/UDP]

$udp0 set packetSize_ 1000								# set MSS to 1000 bytes (default)

$ns attach-agent $n0 $udp0

# Exponential traffic generator for TCP agent
set cbr0 [new Application/Traffic/Exponential]
$cbr0 set rate_ 50Kbps #0.5Mbps
$cbr0 attach-agent $udp0
$udp0 set class_ 0

set null0 [new Agent/Null]
$ns attach-agent $n3 $null0



$ns connect $udp0 $null0

# UDP traffic activates 20s after start
$ns at 20.0 "$cbr0 start"

# and ends 20s before ending simulation
$ns at 180.0 "$cbr0 stop"

# Modify congention control procedures (slow start and linial increasing)
# Modify CWMAX (window_)


# Two different TCP agents will be used: RFC793 with slow start. TODO: add Jakobson-Karels estimator
set tcp1 [new Agent/TCP/RFC793edu]
# set tcpReno [new Agent/TCP/Reno]							# TODO: add a Reno TCP agent

$tcp1 set segsize_ 1000 								# set MSS to 1000 bytes
$tcp1 set add793jacobsonrtt_ true							# TODO Both agents employ Jacobson/karels estimator

$tcp1 set class_ 1

$tcp1 set add793karnrtt_ false
$tcp1 set add793expbackoff_ false
if {$flag==1} {
	$tcp1 set add793additiveinc_ true
} elseif {$flag==2} {
	$tcp1 set add793slowstart_ true						# TODO: always true
}

$ns attach-agent $n1 $tcp1
$tcp1 set tcpTick_ 0.01								# Time resolution = 0.01s
$tcp1 set window_ 10 #40	
#$tcp1 set ssthresh_ 10 # 40					
#$tcp1 set cwnd_ 10									# CWMAX = 10 MSS


set null1 [new Agent/TCPSink]
$ns attach-agent $n3 $null1


# Add a  CBR  traffic generator

# CBR traffic generator for TCP agent
set cbr1 [new Application/Traffic/CBR]						
$cbr1 set rate_  50Kbps #0.5Mbps
$cbr1 attach-agent $tcp1
$ns at 0.0 "$cbr1 start"
$ns at 0.0 "record"

$ns connect $tcp1 $null1 

# Stop simulation at  20 s.

# Simulation time = 200s								
$ns at 200.0 "finish"


#Run simulation
$ns run
