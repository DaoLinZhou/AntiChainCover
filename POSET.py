import json
import random
import sys
import argparse
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


class Node:

    def __init__(self, label):
        self.label = label
        self.in_node = set()
        self.out_node = set()
        self.in_degree_counter = 0

    def reset_counter(self):
        self.in_degree_counter = self.in_degree()

    def decrease_counter(self):
        self.in_degree_counter -= 1

    def counter_is_zero(self):
        return self.in_degree_counter == 0

    def in_degree(self):
        return len(self.in_node)

    def out_degree(self):
        return len(self.out_node)

    def add_in_node(self, node):
        self.in_degree_counter += 1
        self.in_node.add(node)

    def add_out_node(self, node):
        self.out_node.add(node)


class POSET:

    def __init__(self, nodes_number):
        self.nodes_number = nodes_number
        self.nodes = [Node(i) for i in range(nodes_number)]
        self.levels = []

    def reset_node_counter(self):
        for node in self.nodes:
            node.reset_counter()
        return self

    def add_edge(self, vi, wi):
        v = self.nodes[vi]
        w = self.nodes[wi]
        v.add_out_node(w)
        w.add_in_node(v)

    def analysis(self):
        self.levels = []
        curr_level = []

        for node in self.nodes:
            if node.counter_is_zero():
                curr_level.append(node)

        while len(curr_level) > 0:
            next_level = []
            for node in curr_level:
                # delete node
                for sucessor in node.out_node:
                    sucessor.decrease_counter()
                    if sucessor.counter_is_zero():
                        next_level.append(sucessor)
            self.levels.append(sorted(curr_level, key=lambda node: node.label))
            curr_level = next_level

        for node in self.nodes:
            if not node.counter_is_zero():
                raise "There exist cycle, given graph is not a poset"

        return self

    def draw(self, g, first_level_red=False, start_level=0):
        g.add_nodes_from(range(self.nodes_number))
        for v in self.nodes:
            for w in v.out_node:
                g.add_edge(v.label, w.label)

        max_node = max([len(level) for level in self.levels])
        pos = {}
        color = {}

        for i, level in enumerate(self.levels):
            positions = np.linspace(0, max_node, len(level)+2)
            for node, p in zip(level, positions[1:-1]):
                if i < start_level:
                    g.remove_node(node.label)
                else:
                    pos[node.label] = (p, i)
                    color[node.label] = "red" if i == start_level and first_level_red else "blue"
        color_map = [color[self.nodes[node].label] for node in g.nodes]
        nx.draw(g, node_color=color_map, pos=pos, with_labels=True)
        plt.draw()
        plt.show()

    def random_color(self, num):
        return ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                    for i in range(num)]

    def draw_color(self, g):

        g.add_nodes_from(range(self.nodes_number))
        for v in self.nodes:
            for w in v.out_node:
                g.add_edge(v.label, w.label)

        max_node = max([len(level) for level in self.levels])
        pos = {}
        color = {}


        rand_color = self.random_color(len(self.levels)+1)

        for i, level in enumerate(self.levels):

            positions = np.linspace(0, max_node, len(level) + 2)
            for node, p in zip(level, positions[1:-1]):
                pos[node.label] = (p, i)
                color[node.label] = rand_color[i]
        color_map = [color[self.nodes[node].label] for node in g.nodes]
        nx.draw(g, node_color=color_map, pos=pos, with_labels=True)
        plt.draw()
        plt.show()

    @staticmethod
    def from_json(json_file):
        with open(json_file) as file:
            poset_data = json.load(file)
            poset = POSET(poset_data['nodes'])
            for edge in poset_data['edges']:
                for node in edge[1:]:
                    poset.add_edge(edge[0], node)
            return poset.analysis().reset_node_counter()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AntiChainCover')
    parser.add_argument('--show_steps', help='show all the steps',  action='store', nargs='*')
    parser.add_argument('--file', type=str, help='POSET file path')
    args = parser.parse_args()

    filename = args.file
    steps = args.show_steps is not None

    poset = POSET.from_json(filename)
    levels = len(poset.levels)
    g = nx.DiGraph()
    if steps:
        for i in range(levels):
            poset.draw(g, first_level_red=False, start_level=i)
            poset.draw(g, first_level_red=True, start_level=i)
    poset.draw_color(g)
