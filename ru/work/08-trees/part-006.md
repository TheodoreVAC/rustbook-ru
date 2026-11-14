## 8.6 Summary

This chapter introduced us to trees, an efficient data structure that enables us to implement a wide range of useful algorithms. Trees find extensive applications in storage, networking, and other domains. Throughout this chapter, we completed the following tasks using trees:

- Parseed and evaluated expressions.
- Implemented binary heaps as priority queues.
- Implemented binary trees, binary search trees, and balanced binary search trees.

In the previous chapters, we learned about several abstract data types used to implement mapping relationships (Maps), including ordered tables, hash tables, binary search trees, and balanced binary search trees. The table below compares the worst-case performance of various operations supported by these data types. While red-black trees are an improvement over AVL trees, their complexity and performance remain similar to AVL trees, with only differences in coefficients. For further information, readers are encouraged to consult relevant resources.

**Table 8.5: Performance of various abstract data types**

| Operation | Ordered table | Hash table | BST | AVL | Red-black tree |
| --- | --- | --- | --- | --- | --- |
| insert | O(n) | O(1) | O(n) | O(log(n)) | O(log(n)) |
| contains | O(log(n)) | O(1) | O(n) | O(log(n)) | O(log(n)) |
| delete | O(n) | O(1) | O(n) | O(log(n)) | O(log(n)) |
