#!/bin/bash

cp "$1" ./.g.dot
head -n 2 ./.g.dot > ./.s.dot
tail -n 1 ./.g.dot >> ./.s.dot
touch ./.routes.txt
PID="$2"


# Plots the graph given
plot ()
{
    neato -Tps "$1" -o ./.g.ps
    display ./.g.ps
    rm ./.g.ps
}

# Deletes a node and kills the router
delete ()
{
    pid=`egrep "^$1" "$PID" | cut -d"," -f2`
    kill -INT "$pid"
    egrep -v "^$1" "$PID" > tmp.txt
    mv tmp.txt "$PID"
    egrep -v "\b$1\b" ./.g.dot > tmp.txt
    rm ./.g.dot
    mv tmp.txt ./.g.dot
    rm ./.s.dot
    rm ./.routes.txt
    touch .routes.txt
    head -n 2 ./.g.dot > ./.s.dot; echo "}" >> ./.s.dot
}

# Dijkstra 
find_route () {
    route=`dijkstra -p "$1" ./.g.dot | egrep "^\s"`
    head -n 2 ./.g.dot > ./.s.dot
    echo $route | sed -r 's/\s*;\s*/;\n/g' | egrep "prev" | \
        sed -r 's/^([A-Z]).*prev=([A-Z]).*/[\1\2] -- [\1\2]/' > r.txt
    egrep -f r.txt ./.g.dot >> ./.s.dot
    echo "}" >> ./.s.dot
    echo $route | sed -r 's/\s*;\s*/\n/g' | egrep "dist"
    rm r.txt
}

# Kill all
kill_all () {
    pid=`cut -d"," -f2 "$PID"`
    for x in $pid
    do
        kill -INT $x
    done
}
select x in "Plot graph" "Delete node" "Find routes" "Show routes" "Quit"
do
    case "$x" in
        "Plot graph")
            plot ./.g.dot
            ;;
        "Delete node")
            nodes=`cut -d"," -f1 "$PID"`
            select y in $nodes
            do
                r2="\b$y\b"
                r1="^[A-Z]$"
                if [[ "$y" =~ $r1 && "$nodes" =~ $regex ]]
                then
                    delete $y
                fi
                break
            done
            ;;
        "Find routes")
            nodes=`cut -d"," -f1 "$PID"`
            select y in $nodes
            do 
                r2="\b$y\b"
                r1="^[A-Z]$"
                if [[ "$y" =~ $r1 && "$nodes" =~ $regex ]]
                then
                    find_route $y
                fi
                break
            done
            ;;
        "Show routes")
            plot ./.s.dot
            ;;
        "Quit")
            kill_all
            rm ./.g.dot
            rm ./.s.dot
            rm ./.routes.txt
            break 
            ;;
        *)
            echo Invalid command
    esac
done
