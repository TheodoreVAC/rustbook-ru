## 7.2 What is Sorting?

Sorting involves arranging elements in a specific order in a collection. For example, playing cards are shuffled and arranged by suit or order to play effectively, and words can be sorted alphabetically or by length. Similarly, Chinese cities can be sorted by population, ethnicity, or region. Orderliness is a crucial skill for humans as it enables smooth progress in various areas. Sorting is an important field in computer science, and many pioneers have contributed to the development of sorting algorithms. Various algorithms, including sequential search and binary search, benefit from sorting datasets. Sorting algorithm efficiency is dependent on the number of items being processed, and complex sorting methods are too expensive for small collections while simple algorithms are not suitable for large datasets. In this chapter, we will explore different sorting algorithms and compare their performance. Comparison is the core operation in sorting, as it determines sequence, order, and orderliness. Comparison involves looking at which element is larger or smaller based on a criterion, which can be simple (numerical size) or abstract (health index). If the comparison shows that the order is incorrect, data positions need to be exchanged. However, exchanging data positions is an expensive operation in computer science, and the total number of exchanges is crucial for evaluating the efficiency of algorithms. In this chapter, we will analyze various sorting algorithms using the Big O analysis method, which is the most intuitive indicator for evaluating their efficiency. Apart from efficiency, sorting also has the issue of stability. For instance, in a list like [1,4,9,8,5,5,2,3,7,6], there are two 5s, and different sorts may swap the order of the two 5s. Although they are adjacent in the end, the original order relationship has been destroyed. For numeric data, this may not matter, but for data structures containing keys like personal information, rash sorting may change the order, which is not desirable.

```text
person {
                   person {
    amount: 5,
                       amount: 5,
    name: Shieber,
                       name: Kew,
    phone: 133xx,
                       phone: 133xx,
    age: 20,
                       age: 24,
}
                   }
```

To ensure that the order of the elements in a sorted collection remains stable, it is important to consider stability when evaluating sorting algorithms. Stability refers to whether the relative order of equal elements in the original collection is maintained in the sorted collection. For example, if the amount: 5 appears twice in a collection and sorting changes the order of the two occurrences, this can cause issues for algorithms that rely on the stability of the sequence, such as deduction operations. There are numerous sorting algorithms available for collections, but there are ten basic types of sorting algorithms that serve as the foundation for most of them. These include bubble sort, quick sort, selection sort, heap sort, insertion sort, shell sort, merge sort, counting sort, bucket sort, and radix sort. Many improved algorithms have been derived from these ten basic algorithms. In this article, we will explain several of these improved algorithms, including new bubble sort, cocktail sort, comb sort, binary insertion sort, flash sort, and Tim sort.
