import numpy as np
import matplotlib.pyplot as plt
from eventQueue import EventQueue
from line import Line       
from statusStructure import StatusStructure

class FindIntersections():
    def __init__(self):
        self.Q = EventQueue()
        self.T = StatusStructure()        
        self.intersections = []
        
    def find_intersections(self, lines):
        for line in lines:
            self.Q.insert_line(line)
        while not self.Q.is_empty():
            next_event = self.Q.pop_next_event()
            self.handle_event_point(next_event)
            
    def handle_event_point(self, p):
        U_p = p.lines
        L_p, C_p, L_C = self.T.find_segments_contain(p.point)
        U_C = U_p + C_p
        L_U_C = L_C + U_p
        if len(L_U_C) > 1:
            self.intersections.append(p.point)
        for line in L_C:
            self.T.delete(p.point, line)
        self.T.insert(p.point, U_C)
        self.T._print_name()
        if len(U_C) == 0:
            s_l = self.T.find_left_neighbor(p.point)
            s_r = self.T.find_right_neighbor(p.point)
            self.find_new_event(s_l, s_r, p.point)
        else:
            s_lm = self.T.find_leftmost(p.point)
            s_l = self.T.find_left_neighbor(p.point)
            self.find_new_event(s_lm, s_l, p.point)
            s_rm = self.T.find_rightmost(p.point)
            s_r = self.T.find_right_neighbor(p.point)
            self.find_new_event(s_rm, s_r, p.point)
            
            
    def find_new_event(self, s_l, s_r, p):
        if s_l is None or s_r is None:
            return
        i = s_l.intersect(s_r)
        if i is None:
            return
        x_i, y_i = i
        x_p, y_p = p
        if y_i < y_p or (y_i == y_p and x_i > x_p):
            self.Q.insert(i)
        
if __name__ == '__main__':
    line_1 = Line((0, 0), (1, 2))
    line_2 = Line((1, 2), (2, 3))
    line_3 = Line((2, 3), (3, 2))
    line_4 = Line((3, 2), (2, 1))
    line_5 = Line((2, 1), (0, 0))
    line_6 = Line((2, 1), (2, 3))
    line_7 = Line((1, 2), (4, 2))
    line_8 = Line((1, 1), (1, 1.5))
    line_9 = Line((1, 1.5), (1.5, 1))
    line_10 = Line((1.5, 1), (1, 1))
    line_11 = Line((0, 0), (3, 3))
    lines = [line_1, line_2, line_3, line_4, line_5, line_6, line_7, line_8, line_9, line_10, line_11]
    '''
    line_1 = Line((0, 0), (0, 3))
    line_2 = Line((0, 0), (2, 0))
    line_3 = Line((4, 0), (6, 0))
    line_4 = Line((4, 0), (4, 3))
    line_5 = Line((4, 3), (6, 3))
    line_6 = Line((6, 0), (6, 3))
    line_7 = Line((8, 3), (10, 3))
    line_8 = Line((10, 3), (8, 0))
    line_9 = Line((8, 0), (10, 0))
    line_10 = Line ((4, 4), (5, 5))
    line_11 = Line((5, 5), (6, 4))
    line_12 = Line((5, 6), (6, 5))
    lines = [line_1, line_2, line_3, line_4, line_5, line_6, line_7, line_8, line_9, line_10, line_11, line_12]
    '''
    i = 1
    for line in lines:
        line.name = 'line_'+str(i)
        i += 1
    def find_and_plot(lines):
        plt.axis('equal')
        def plot_line(line):
            x = line[0]
            y = line[1]
            plt.plot((x[0], y[0]), (x[1], y[1]), 'ro-')
        for line in lines:
            plot_line((line.upper_endpoint, line.lower_endpoint))
        F = FindIntersections()
        F.find_intersections(lines)
        for point in F.intersections:
            plt.plot(point[0], point[1], marker='x', markersize=10, color="blue")
        return F.intersections
    print(find_and_plot(lines))