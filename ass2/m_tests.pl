#!/usr/bin/perl -w

# Makes tests for Assignment 2

use strict;
use POSIX;

# Get all used ports
sub used_ports {
    open(F, '-|', 'netstat -atun') or die;
    my @data;
    while(my $line = <F>) {
        push(@data, $line);
    }
    close(F);
    @data = @data[2 .. $#data];
    my %used;
    foreach my $line (@data) {
        $line =~ s/\s+/,/g;
        my @l = split(/,/, $line);
        $l[3] =~ /:([0-9]+)$/;
        my $port = $1;
        $used{$port} = 1;
    }
    return %used;    
}

# Generate graph
sub make_graph {
    my $num_nodes = $_[0];
    my $range = ($num_nodes - 1) * ($num_nodes / 2 - 1);
    my $sparse = int(rand($range)) + $num_nodes - 1;
    my $s_count = 0;
    my %graph;
    # Make MST
    my $cur = int(rand($num_nodes));
    my @unseen = (0..($num_nodes - 1));
    splice @unseen, $cur, 1;
    while(@unseen > 0) {
        my $i = int(rand(@unseen));
        my $n = $unseen[$i];
        splice @unseen, $i, 1;
        my $cost = sprintf "%.1f", rand(10);
        $graph{$cur}{$n} = $cost;
        $graph{$n}{$cur} = $cost;
        $cur = $n;
        $s_count ++;
    }
    while($s_count < $sparse) {
        my $n1 = int(rand($num_nodes));
        my $n2 = int(rand($num_nodes));
        while(defined($graph{$n1}{$n2}) or $n1 == $n2) {
            $n1 = int(rand($num_nodes));
            $n2 = int(rand($num_nodes));
        }
        my $cost = sprintf "%.1f", rand(10);
        $graph{$n1}{$n2} = $cost;
        $graph{$n2}{$n1} = $cost;
        $s_count ++;
    }
    return %graph;
    
}

# Get the number of nodes
my $num_nodes = $ARGV[0];
my $port = 1025;
my @letters = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J');
# Make graph
my %graph = make_graph($num_nodes);
# Get alls used ports
my %used = used_ports();
my @ports;
while(@ports < $num_nodes) {
    push(@ports, $port) if(not defined($used{$port}));
    $port ++;
}
# Make config files
mkdir $ARGV[1] or die;
for(my $i = 0; $i < $num_nodes; $i ++) {
    my $f_name = "$ARGV[1]/config" . $letters[$i] . ".txt";
    open(F, ">", $f_name) or die;
    my $num = keys($graph{$i});
    print F "$num\n";
    for my $k (keys($graph{$i})) {
        print F "$letters[$k] $graph{$i}{$k} $ports[$k]\n";
    }
    close(F);
}
# Make run script
open(F, "-|", "xrandr | head -n 1");
my $col = 1 / 9;
my $row = 1 / 15;
my $width;
my $height;
chomp(my $l = <F>);
if($l =~ /current ([0-9]+) x ([0-9]+)/) {
    $width = $1;
    $height = $2;
}
close(F);
my $stack = ceil(($num_nodes + 1) / 3);
my $w = int($col * $width / 3);
my $h = int($row * $height / $stack);
my $f_name = $ARGV[1] . "/run.sh";
my $x;
my $y;
my $depth = 0;
open(F, ">", $f_name) or die;
print F "#!/bin/bash\n";
for(my $i = 0; $i < $num_nodes; $i ++) {
    my $f = "config" . $letters[$i] . ".txt";
    $depth ++ if($i != 0 and $i % 3 == 0);
    $x = sprintf("%.0f", $width / 3) * ($i % 3);
    $y = sprintf("%.0f", $height/ $stack) * $depth;
    print F "xterm -geometry " . $w . "x" . $h . "+" . $x . "+" . $y . " -e \"python3 ../Lsr.py $letters[$i] $ports[$i] $f\" &\n";
    print F "echo \"$letters[$i],\$!\" >> pid.txt\n"
} 
$depth ++ if($num_nodes % 3 == 0);
$x = sprintf("%.0f", $width / 3) * 2;
$y = sprintf("%.0f", $height/ $stack) * $depth;
print F "xterm -geometry " . $w . "x" . $h . "+" . $x . "+" . $y . " -e \"bash ../show_graph.sh graph.txt pid.txt\"\n";
print F "rm pid.txt\n";
close(F);
$f_name = $ARGV[1] . "/graph.txt";
open(F, ">", $f_name);
print F "graph g {\n";
print F " " x 4 . "graph [ size = \"6.5!\" ];\n";
for my $g (sort(keys(%graph))) {
    for my $f (sort(keys($graph{$g}))) {
        if($g < $f) {
            print F " " x 4 . "$letters[$g] -- $letters[$f] [ len = $graph{$g}{$f}, label = $graph{$g}{$f} ];\n";
        }
    }
}
print F "}";
close(F)
