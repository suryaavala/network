#!/usr/bin/python3

from igraph import *
import sys
import re
import os
import signal

def load_graph(file_name, v_style):
    g = Graph.Read_Ncol(file_name, True, True, False)
    set_default(g, v_style)
    return g

def set_default(g, v_style):
    v_style['vertex_label'] = g.vs['name']
    v_style['edge_label'] = g.es['weight']
    v_style['vertex_color'] = ['cyan' for v in g.vs['name']]
    v_style['edge_color'] = ['black' for e in g.es['weight']]

def find_shortest(g, routes, s_style, node):
    paths = g.get_all_shortest_paths(node, None, g.es['weight'], 'ALL')
    set_default(g, s_style)
    s_style['vertex_color'][g.vs['name'].index(node)] = 'green'
    e = g.get_edgelist()
    for p in paths:
        if len(p) == 1:
            continue
        cost = 0
        route = node
        for i in range(1, len(p)):
            try:
                edge = e.index((p[i-1], p[i]))
            except ValueError:
                edge = e.index((p[i], p[i-1]))

            s_style['edge_color'][edge] = 'red'
            cost += g.es['weight'][edge]
            route += g.vs['name'][p[i]]
        routes.append((route, cost))

if __name__ == '__main__':
    v_style = {}
    g = load_graph(sys.argv[1], v_style)
    pids = {}
    s_style = {}
    ver = sys.version_info[0] > 2
    with open(sys.argv[2], 'r') as f:
        for l in f.readlines():
            l = l.rstrip()
            node, pid = l.split()
            pids[node] = int(pid)
    routes = []
    while True:
        try:
            if ver:
                u = raw_input('> ')
            else:
                u = raw_input('> ')
            u = u.rstrip()
            u = re.sub('^\s+', '', u)
            u = re.sub('\s+', ' ', u)
            if u == 'plot':
                plot(g, **v_style)
            elif u == 'clear':
                os.system('clear')
            elif re.search('^shortest', u):
                routes = []
                find_shortest(g, routes, s_style, u.split()[1])
            elif re.search('^paths', u):
                mode = u.split()[1]
                if mode == 'both' or mode == 'plot':
                    plot(g, **s_style)
                if mode == 'route' or mode == 'both':
                    for r in routes:
                        print("%s %.1f" %(r[0], r[1]))
            elif re.search('^delete', u):
                node = u.split()[1]
                if node in g.vs['name']:
                    g.delete_vertices(node)
                    set_default(g, v_style)
                    try:
                        os.kill(pids[node], signal.SIGINT)
                    except OSError:
                        pass
                    pids.pop(node)
            else:
                print('Commands:')
                print('\tclear - Clears the screen')
                print('\tshortest <node> - Finds shortest paths to <node>')
                print('\tpaths <mode> - Shows the shortest paths found via shortest command (plot|route|both)')
                print('\tplot - Plots the graph')
                print('\tdelete <node> - Deletes the node from graph and kills the router')
        except (KeyboardInterrupt, EOFError):
            for node in pids:
                try:
                    os.kill(pids[node], signal.SIGINT)
                except OSError:
                    pass
            print()
            break



