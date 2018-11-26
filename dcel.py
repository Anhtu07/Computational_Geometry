from matplotlib import pyplot as plt
import matplotlib.cm as cm

import numpy as np
class Vertex:
    def __init__(self, coordinates=None, incident_edge=None, event_type=1):
        self.coordinates = coordinates
        self.incident_edge = incident_edge
        self.involves_both = False
        self.belong_to = None
        # Dinh nghia 1 la chi thuoc 1 dcel
        # 2 la giao 2 doan thuoc 2 dcel
        # 3 la 1 doan cua dcel di qua dinh cua dcel khac
        # 4 la 2 dinh cua 2 dcel trung nhau
        self.event_type = event_type
        self.left_hedge = None
    
    def find_hedges_w_origin(self):
        edges = [self.incident_edge]
        current = self.incident_edge
        while True:
            if self.incident_edge == current.twin.next:
                break
            current = current.twin.next
            edges.append(current)
        return edges
    
    def find_hedges_w_des(self):
        edges = [self.incident_edge.twin]
        current = self.incident_edge.twin
        while True:
            if self.incident_edge.twin == current.next.twin:
                break
            current = current.next.twin
            edges.append(current)
        return edges

    def __repr__(self):
        return str(self.coordinates)
                
    def __eq__(self, other):
        if isinstance(other, Vertex):
            return np.linalg.norm([self.coordinates[0] - other.coordinates[0], self.coordinates[1] - other.coordinates[1]]) < 1e-4
        return False
    
    def __hash__(self):
        return hash(self.coordinates)
             
class Face:
    def __init__(self, outer_component=None, name=None):
        self.outer_component = outer_component
        self.inner_components = []
        self.segment = None
        self.belong_to = None
        self.name = name

    def __repr__(self):
        return ('Face{outer='+(str(self.outer_component) if self.outer_component is not None else 'none'))+',inner='+str(self.inner_components)+'}'

class HalfEdge:
    def __init__(self, origin=None):
        self.origin = origin
        self.twin = None
        self.incident_face = None
        self.next = None
        self.prev = None
        self.belong_to = None
        self.cycle = None
    
    def __repr__(self):
        return ('HalfEdge{O=' + str(self.origin) + ', D=' + (str(self.next.origin) if self.next is not None else 'none')) + '}'

    def copy_next(self, he):
        self.next = he.next
        self.prev = he.prev
        self.incident_face = he.incident_face

    def set_next(self, he):
        self.next = he
        he.prev = self

    def set_prev(self, he):
        self.prev = he
        he.next = self

    def set_twin(self, he):
        self.twin = he
        he.twin = self

    def cal_angle(self):
        if self.next is None or self.next.origin is None:
            return None
        x1, y1 = self.origin.coordinates
        x2, y2 = self.next.origin.coordinates
        angle = np.arctan2(y2-y1, x2-x1)*180/np.pi
        if angle <= 0:
            angle += 360
        return angle

    def clockwise_angle(self, he):
        x1, y1 = self.origin.coordinates
        x2, y2 = self.next.origin.coordinates
        x_v2, y_v2 = (x2-x1, y2-y1)
        x3, y3 = he.origin.coordinates
        x4, y4 = he.next.origin.coordinates
        x_v1, y_v1 = (x4-x3, y4-y3)
        dot = x_v1*x_v2 + y_v1*y_v2
        det = x_v1*y_v2 - y_v1*x_v2
        angle = np.arctan2(-det, -dot) + np.pi
        if angle >= 2*np.pi or angle < 0:
            angle = 0
        return angle*180/np.pi
    
    def inside_angle(self, next_he):
        return self.twin.clockwise_angle(next_he)

class DCEL:
    def __init__(self, vertices, halfedges, faces, name=None):
        if name is None:
            self.vertices = vertices
            self.halfedges = halfedges
            self.faces = faces
        else:
            for v in vertices + halfedges + faces:
                v.belong_to = name
            self.vertices = vertices
            self.halfedges = halfedges
            self.faces = faces

    def plot_segment(self):
        for he in self.halfedges:
            x = he.origin
            y = he.next.origin
            plt.plot((x.coordinates[0], y.coordinates[0]), (x.coordinates[1], y.coordinates[1]), 'ro-')
        plt.show()

    def plot_dcel(self, ax=None):
        if ax is not None:
            splt = ax
        else:
            splt = plt.subplot()
        def detect_cycle():
            cycles = []
            he_set = set(self.halfedges)
            while len(he_set) != 0:
                first_he = he_set.pop()
                current_cycle = [first_he]
                current_he = first_he
                while current_he.next != first_he:
                    current_he = current_he.next
                    he_set.remove(current_he)
                    current_cycle.append(current_he)
                cycles.append(current_cycle)
            return cycles

        def shift_left_he(halfedge):
            x1, y1 = halfedge.origin.coordinates
            x2, y2 = halfedge.next.origin.coordinates
            v = np.array([x2-x1, y2-y1])
            xv, yv = v
            norm = np.linalg.norm([xv, yv])
            a = np.array([[xv, yv], [-yv, xv]])
            b = [0, 0.03*norm]
            dx, dy = np.linalg.solve(a,b)
            dxv, dyv = v/norm*0.03
            return x1+dx+dxv, y1+dy+dyv, x2-x1-2*dxv, y2-y1-2*dyv
        cycles = detect_cycle()
        #splt.set_aspect('equal', 'datalim')
        splt.set_aspect('equal',adjustable='box')
        splt.set_xlim(min([p.coordinates[0] for p in self.vertices]) - 1, max([p.coordinates[0] for p in self.vertices]) + 1)
        splt.set_ylim(min([p.coordinates[1] for p in self.vertices]) - 1, max([p.coordinates[1] for p in self.vertices]) + 1)
        color = iter(cm.rainbow(np.linspace(0,1,len(cycles))))
        he_list = set(self.halfedges)
        for cycle in cycles:
            c = next(color)
            for he in cycle:
                splt.quiver(*shift_left_he(he), scale=1, scale_units='xy', angles='xy', color=c, width=0.002, headwidth=7)
        for face in self.faces:
            if face.outer_component is not None and face.name is not None:
                first_he = face.outer_component
                current_he = face.outer_component
                list_he = [face.outer_component]
                while current_he.next != first_he:
                    current_he = current_he.next
                    list_he.append(current_he)
                x_max = max([he.origin.coordinates[0] for he in list_he])
                x_min = min([he.origin.coordinates[0] for he in list_he])
                y_max = max([he.origin.coordinates[1] for he in list_he])
                y_min = min([he.origin.coordinates[1] for he in list_he])
                cx = (x_max+x_min)/2
                cy = (y_max+y_min)/2
                splt.annotate(face.name, (cx, cy), color='black', weight='bold', 
                    fontsize=6, ha='center', va='center')
            elif face.name is not None:
                splt.set_title('Outer face: ' + face.name)
        if ax is None:
            plt.show()

        
    