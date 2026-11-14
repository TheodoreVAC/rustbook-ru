## 9.4 The Graph Abstract Data Type

The graph abstract data type can be defined based on the basic definition of a graph. At the core of the graph are vertices and edges, and operations are defined around them. The following operations are defined for a graph:

- new(): Creates a new empty graph with no parameters and returns an empty graph.
- add_vertex(v): Adds a vertex with parameter v to the graph and has no return value.
- add_edge(fv,tv,w): Adds a weighted directed edge with parameters fv, tv, and w to the graph and has no return value.
- get_vertex(vk): Finds the vertex with key vk in the graph, requires parameter vk, and returns the vertex.
- get_vertices(): Returns a list of all vertices in the graph without parameters.
- vert_nums(): Returns the number of vertices in the graph without parameters.
- edge_nums(): Returns the number of edges in the graph without parameters.
- contains(vk): Checks whether the vertex is in the graph with parameter vk and returns a Boolean value.
- is_empty(): Checks whether the graph is empty without parameters and returns a Boolean value.

Assuming g is a newly created empty graph, the table below shows the results of various graph operations. [] stores vertices, and () stores edges, where the first two values are points and the third value is the edge weight, such as (1, 5, 2), which means that the edge weight between point 1 and point 5 is 2.

**Table 9.1: Operations on Graph**

| Operation | Graph value | Return value |
| --- | --- | --- |
| g.is_empty() | [] | true |
| g.add_vertex(1) | [1] |  |
| g.add_vertex(5) | [1,5] |  |
| g.add_edge(1,5,2) | [1,5,(1,5,2)] |  |
| g.get_vertex(5) | [1,5,(1,5,2)] | 5 |
| g.get_vertex(4) | [1,5,(1,5,2)] | None |
| g.edge_nums() | [1,5,(1,5,2)] | 1 |
| g.vert_nums() | [1,5,(1,5,2)] | 2 |
| g.contains(1) | [1,5,(1,5,2)] | true |
| g.get_verteces() | [1,5,(1,5,2)] | [1,5] |
| g.add_vertex(7) | [1,5,7,(1,5,2)] |  |
| g.add_vertex(9) | [1,5,7,9,(1,5,2)] |  |
| g.add_edge(7,9,8) | [1,5,7,9,(1,5,2),(7,9,8)] |  |
| g.contains(3) | [1,5,7,9,(1,5,2),(7,9,8)] | false |
| g.vert_nums() | [1,5,7,9,(1,5,2),(7,9,8)] | 4 |
| g.edge_nums() | [1,5,7,9,(1,5,2),(7,9,8)] | 2 |
