import pytest
from src.structural_matrix import Truss2D

def test_simple_truss_solve():
    truss = Truss2D()
    truss.add_node(0, 0.0, 0.0, fix_x=True, fix_y=True)
    truss.add_node(1, 4.0, 0.0, fix_x=False, fix_y=True)
    truss.add_node(2, 2.0, 3.0, fix_x=False, fix_y=False)

    truss.add_member(0, 1, E=200e9, A=0.0025)
    truss.add_member(1, 2, E=200e9, A=0.0025)
    truss.add_member(0, 2, E=200e9, A=0.0025)

    truss.add_load(node_id=2, fx=0.0, fy=-50000.0)
    results = truss.solve()
    disp = results['displacements']
    
    assert disp[0]['ux'] == 0.0
    assert disp[0]['uy'] == 0.0
    assert disp[1]['uy'] == 0.0
    assert disp[2]['uy'] < 0.0  # Downward deflection
