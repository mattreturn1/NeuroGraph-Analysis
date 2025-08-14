# Brain Network Analysis Using Graph-Based Methods

## Introduction

In recent years, representing the brain as a network and analyzing it through **machine learning** and **graph analytics** has emerged as a powerful approach for studying its structure and function. Unlike traditional examination methods, this graph-based representation preserves both **structural** and **positional** information, offering unique insights into how different brain regions interact and influence each other.

Such methods have proven particularly valuable in investigating **neurodegenerative and neurodevelopmental disorders** like **Parkinson’s disease** and **Autism**. These conditions often lead to measurable alterations in brain network topology, which can be quantified through specific **graph metrics** — for example, *closeness centrality*, *node degree*, and *clustering coefficient*.

This project aims to evaluate whether graph metrics learned in the *Learning from Networks* course can help **distinguish brain networks** of individuals with Parkinson’s disease or Autism from those of healthy controls.  

We use data from the publicly available dataset **A Collection of Brain Network Datasets** [2], focusing specifically on:
- **Autism Brain Imaging Data Exchange (ABIDE)**
- **Parkinson’s Progression Markers Initiative (PPMI)**  

Brain networks are constructed from **correlation matrices** generated using the *Automated Anatomical Labeling* (**AAL**) parcellation algorithm [3], which divides the brain into **116 distinct regions**. Pearson’s correlation coefficient [4] is used to measure the connectivity between these regions, resulting in a **116×116 adjacency matrix** (13,456 undirected edges).  

These datasets cover thousands of subjects with diverse **age** and **sex** distributions, enabling a broad exploration of demographic effects on brain network structures.

## Installation of the dependencies

1. Clone the repository:

```bash
git clone https://github.com/mattreturn1/Graph_Based-Brain-Networks
```

2. Download the library required

```bash
pip install -r requirements.txt
```

3. The repository contains the already filtered folders.  
   If you want to test the `folders_organizer.py`, you need to download `abide.zip` and `ppmi_v2.zip` from the following link:

[https://auckland.figshare.com/articles/dataset/NeurIPS_2022_Datasets/21397377](https://auckland.figshare.com/articles/dataset/NeurIPS_2022_Datasets/21397377)

Then extract the contents of the `abide.zip` folder and rename the extracted folder to `abide`.  
Similarly, extract the contents of the `ppmi_v2.zip` folder and rename the extracted folder to `ppmi`.  
Move both renamed folders to the root folder of the project.

### Dataset
This project uses the dataset:

Xu, Jiaxing; Yang, Yunhan; Huang, David; Gururajapathy, Sophi; Ke, Yiping; Qiao, Miao; et al. (2023).  
A Collection of Brain Network Datasets. The University of Auckland. Dataset.  
https://doi.org/10.17608/k6.auckland.21397377.v7  

Licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
