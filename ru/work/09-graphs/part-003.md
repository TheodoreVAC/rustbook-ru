## 9.3 Graph Storage Format

To store a non-linear graph in a linear storage device like computer memory, there are two commonly used methods: adjacency matrix and adjacency list. The adjacency matrix stores the nodes, edges, and weights of the graph in a two-dimensional matrix, which requires N 2 space for a graph with N nodes. However, this method may result in a large waste of space when the graph is sparse. In contrast, the adjacency list is similar to a hash table and saves all the edges related to each vertex by opening a chain for each vertex. Its storage space depends on the number of edges and is generally much smaller than N 2. Therefore, computers use adjacency lists to store graph data structures.

### 9.3.1 Adjacency Matrix

An adjacency matrix is a straightforward way to store a graph. In this method, the vertices of the graph are represented by the rows and columns of a two-dimensional matrix. The value stored at the intersection of row v and column w indicates the presence of an edge between vertex v and vertex w, with the value indicating the weight of the edge. When two vertices have an edge between them, they are called adjacent. The graph shown in (9.1) can be stored using an adjacency matrix.

![Figure 9.2: Adjacency matrix](images/fig-9.2.png)

*Figure 9.2: Adjacency matrix*

Although the adjacency matrix is easy to understand and analyze for small graphs, it suffers from the drawback of being very sparse. Most of the cells in the matrix are empty, leading to a significant waste of space. For a graph with N vertices, an adjacency matrix requires N 2 storage. Therefore, the adjacency matrix is not an efficient method to store large graphs.

### 9.3.2 Adjacency List

![Figure 9.3: Adjacency list](images/fig-9.3.png)

*Figure 9.3: Adjacency list*

An efficient way to save graphs is by using an adjacency list, as shown in the figure above. In this approach, an array stores all the vertices in the graph, and each vertex maintains a linked list that connects it to other vertices. By accessing the linked lists of various vertices, it is possible to know how many points it is connected to, which is similar to the chaining method used by HashMap to solve collisions. The adjacency list stores the linked points in a structure similar to HashMap because edges have weights, while arrays can only save vertices. Graphs implemented with adjacency lists are compact and have no memory waste. This structure is also very convenient for storage. The importance of basic data structures is evident here, and the HashMap implemented in previous chapters is useful for implementing adjacency lists.
