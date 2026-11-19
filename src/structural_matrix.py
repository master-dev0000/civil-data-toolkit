import numpy as np

class Truss2D:
    """
    Direct Stiffness Method solver for 2D Trusses.
    Utilizes vectorized operations for member coordinate transformation and global assembly.
    """
    def __init__(self):
        self.nodes = {}
        self.members = []
        self.loads = {}

    def add_node(self, node_id: int, x: float, y: float, fix_x: bool = False, fix_y: bool = False):
        self.nodes[node_id] = {
            'x': float(x),
            'y': float(y),
            'fix_x': bool(fix_x),
            'fix_y': bool(fix_y)
        }

    def add_member(self, n1: int, n2: int, E: float, A: float):
        self.members.append({
            'n1': n1,
            'n2': n2,
            'E': float(E),
            'A': float(A)
        })

    def add_load(self, node_id: int, fx: float = 0.0, fy: float = 0.0):
        self.loads[node_id] = (float(fx), float(fy))

    def solve(self):
        num_nodes = len(self.nodes)
        dof = num_nodes * 2
        K_global = np.zeros((dof, dof))
        F_global = np.zeros(dof)

        for mem in self.members:
            p1 = self.nodes[mem['n1']]
            p2 = self.nodes[mem['n2']]
            dx = p2['x'] - p1['x']
            dy = p2['y'] - p1['y']
            L = np.hypot(dx, dy)
            if L == 0:
                raise ValueError("Member length cannot be zero.")
            c = dx / L
            s = dy / L

            k_local = (mem['E'] * mem['A'] / L) * np.array([
                [ c*c,  c*s, -c*c, -c*s],
                [ c*s,  s*s, -c*s, -s*s],
                [-c*c, -c*s,  c*c,  c*s],
                [-c*s, -s*s,  c*s,  s*s]
            ])

            indices = [
                mem['n1']*2, mem['n1']*2 + 1,
                mem['n2']*2, mem['n2']*2 + 1
            ]
            for i in range(4):
                for j in range(4):
                    K_global[indices[i], indices[j]] += k_local[i, j]

        for node_id, (fx, fy) in self.loads.items():
            F_global[node_id * 2] += fx
            F_global[node_id * 2 + 1] += fy

        # Boundary conditions
        free_dofs = []
        for node_id, node in self.nodes.items():
            if not node['fix_x']:
                free_dofs.append(node_id * 2)
            if not node['fix_y']:
                free_dofs.append(node_id * 2 + 1)

        K_reduced = K_global[np.ix_(free_dofs, free_dofs)]
        F_reduced = F_global[free_dofs]

        U_reduced = np.linalg.solve(K_reduced, F_reduced)
        U_full = np.zeros(dof)
        U_full[free_dofs] = U_reduced

        displacements = {node_id: {'ux': U_full[node_id*2], 'uy': U_full[node_id*2+1]} for node_id in self.nodes}
        return {'displacements': displacements, 'K_shape': K_global.shape}
