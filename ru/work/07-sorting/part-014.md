## 7.14 Summary

In this chapter, we learned about ten different types of sorting algorithms. Bubble sort, selection sort, and insertion sort are O(n2) algorithms, while most other sorting algorithms have a complexity of O(nlog2(n)). Selection sort is an improvement on bubble sort, shell sort improves on insertion sort, heap sort improves on selection sort, and quicksort and merge sort both use the divide-and-conquer approach. All of these sorts are based on comparison, but there are also non-comparison sorts that rely solely on numerical patterns for sorting, such as bucket sort, counting sort, and radix sort. These sorts have a complexity of approximately O(n) and are suitable for sorting small amounts of data. Counting sort is a special case of bucket sort, and radix sort is a multi-round bucket sort that can degrade into counting sort. In addition to the basic sorting algorithms, we also learned about improved versions of some algorithms, particularly the TimSort algorithm, which is an efficient and stable hybrid sorting algorithm. Its improved version is already the default sorting algorithm for many languages and platforms. The table below summarizes the various sorting algorithms, which readers can compare and understand on their own to deepen their understanding.

**Table 7.1: Time and space complexity of various sorting algorithms**

| No | Algorithm | Time-worst | Time-best | Time-average | Space | Stability |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Bubble sort | O(n2) | O(n) | O(n2) | O(1) | stable |
| 2 | Quick sort | O(n2) | O(nlog(n)) | O(nlog(n)) | O(nlog(n)) | unstable |
| 3 | Selection sort | O(n2) | O(n2) | O(n2) | O(1) | unstable |
| 4 | Heap sort | O(nlog(n)) | O(nlog(n)) | O(nlog(n)) | O(1) | unstable |
| 5 | Insertion sort | O(n2) | O(n) | O(n2) | O(1) | stable |
| 6 | Shell sort | O(n2) | O(n) | O(n1.3) | O(1) | unstable |
| 7 | Merge sort | O(nlog(n)) | O(nlog(n)) | O(nlog(n)) | O(n) | stable |
| 8 | Counting sort | O(n + k) | O(n + k) | O(n + k) | O(n + k) | stable |
| 9 | Bucket sort | O(n2) | O(n) | O(n + k) | O(n + k) | stable |
| 10 | Radix sort | O(nk) | O(nk) | O(nk) | O(n + k) | stable |
| 11 | Tim sort | O(nlog(n)) | O(n) | O(nlong(n)) | O(n) | stable |
