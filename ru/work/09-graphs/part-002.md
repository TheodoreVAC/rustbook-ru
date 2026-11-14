## 9.2 What is Graph?

In the previous chapter, we discussed binary trees as a data structure, while this chapter focuses on graphs - a more generalized form of trees. Although trees can be viewed as simplified graphs or carefully selected graphs with certain constraints on their node relationships, graphs have no such limitations. While trees have a root node and a top-to-bottom direction, graphs lack both. Unlike trees, graphs can contain cycles. They consist of points, edges, and point-edge relationships, whereas trees consist of nodes and connections. The figure above illustrates a graph with multiple nodes and connections, which demonstrates the vertical and horizontal relationships between different items. For example, calculus and linear algebra have no direct connection, but they can jointly incubate neural networks, forming a horizontal relationship. Derivatives, on the other hand, contribute to the construction of calculus, which is a part of calculus, and this forms a vertical relationship.

Graphs are versatile data structures that can be used to represent various real-world phenomena, such as flight maps, social network graphs, and course planning graphs. In this chapter, we will learn about the concept and storage format of graphs, and how to implement them in Rust. We will also explore two essential graph search algorithms that can be applied to solve different problems. Research on graphs, their various applications, and algorithms belong to a specialized discipline called graph theory.

### 9.2.1 Vocabularies and Definitions of Graph

A graph is a more general form of a tree and is defined by the following concepts:

- Vertex (or node): an element of the graph that has a name, or key, and may have additional information, or payload.
- Edge: an element that connects two vertices and indicates a relationship between them. An edge can be unidirectional or bidirectional, and may have a weight, which represents a measure such as distance, cost, time, or closeness.
- Weight: a measure of an edge.

A graph can be represented as G = (V, E), where V is the set of vertices and E is the set of edges. The figure below shows an example of a weighted directed graph with a vertex set V = (V 0, V 1, V 2, V 2, V 4, V 5) and an edge set E consisting of various connections and their weights, with a total of 9 edges.

![Figure 9.1: Graph](images/fig-9.1.png)

*Figure 9.1: Graph*

In addition to vertices, edges, and weights, paths are used to represent the order of points. A path is a vertex sequence that represents the order of point connections, such as (v, w, x, y, z). Cyclic graphs, which have cycles, such as V 5−> V 2−> V 3−> V 5, may also exist. If there are no cycles in the graph, it is called an acyclic graph or DAG graph. Many important problems can be represented using DAG graphs.
