# TF-IDF MapReduce
This repository contains the implementation of TF-IDF following the Map-Reduce paradigm.

## What is TF-IDF?
Term Frequency - Inverse Document Frequency (TF-IDF) is statistical method to measure how important a term is withing a document relative to large collection of documents.

`Term Frequency` is the number of times a term appears in a document relative to the total number of words in that document.

$tf(t,d) = \frac{{\text{{Number of occurrences of }} t \text{{ in document }} d}}{{\text{{Total number of words in document }} d}}$

`Inverse Document Frequency` is a measure of how unique or rare a term is across a collection of documents.

$\text{idf}(t, d) = \log\left(\frac{{\text{{Number of all documents}}}}{{\text{{Number of document which contain }}t}}\right)$

`TF-IDF` considers both the frequency of the word in the document, and its rarity across the entire collection. TF-IDF calculates how much relevant our word or term is.

$\text{tf-idf}(t, d, D) = \text{tf}(t, d) \times \text{idf}(t, D)$