"""
This script is here to let user test the complexity of the problem that can be solved on their machine given
their hardware constraints and their software configuration. Can be used to measure possible performance enhancements
in the future as well.
"""

from __future__ import division
import time, logging
import pyvoronoi


def build_and_solve_voronoi_problem(max_x, max_y):
    """
    A function used to test the library performance. It created a set of point and segments and then solve the voronoi
    problem. It starts from a origin of a grid and then build vertical segments with a length of 1 unit until it reaches
    max_x and max_y.
    :param max_x: The maximum x value used for building segments.
    :param max_y: The maximum y_value used for building segments.
    :return: 
    """

    factor = 10
    pyvoronoi.SILENT = True
    pv = pyvoronoi.Pyvoronoi(factor)
    count_points = 0
    for x in xrange(max_x):
        for y in xrange(max_y):
            pv.AddPoint([x + 0.5, y + 0.5])
            count_points += 1

    count_segment = 0
    for x in xrange(max_x):
        for y in xrange(max_y):
            pv.AddSegment([[x,y], [x, y + 1]])
            count_segment += 1

    time_before = time.time()
    pv.Construct()
    time_after = time.time()
    logging.info("Run pyvoronoi. Time (sec): {0}. Number of input points: {1} - segments: {2}".format(
            time_after - time_before,
            count_points,
            count_segment
    ))

    logging.info("Count output structures. Vertices: {0}, Edges: {1}, Cells: {2}".format(
        pv.CountVertices(),
        pv.CountEdges(),
        pv.CountCells(),
    ))

    logging.info('Start parsing edges - Evaluating performance for curve computation')
    time_before = time.time()
    count_curved_edges = 0
    for i in xrange(pv.CountEdges()):
        e = pv.GetEdge(i)
        startVertex = pv.GetVertex(e.start)
        endVertex = pv.GetVertex(e.end)
        max_distance = pyvoronoi.Distance([startVertex.X, startVertex.Y], [endVertex.X, endVertex.Y]) / 10
        if startVertex != -1 and endVertex != -1:
            if not e.is_linear:
                points = pv.DiscretizeCurvedEdge(i, max_distance, 1 / factor)
                count_curved_edges += 1
    time_after = time.time()
    logging.info('Done parsing {0} curved edges. Done in {1} sec'.format(count_curved_edges, time_after - time_before))
    del pv

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - Script: %(filename)s - Line: %(lineno)d - %(levelname)s - %(message)s',
                        datefmt='%m-%d %H:%M:%S')

    build_and_solve_voronoi_problem(100, 1000)

