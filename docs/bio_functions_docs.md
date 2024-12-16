## Why Cyanobacteria?

My goal is to create a preciese genetic tools to help engineer cyanobacteria. Tools to create guide RNA are not as expansively robust as that for E. coli for example. It may be beneficial to try to integrate cyanobacteria into a more facilitated work flow as they could aid in both environmental and healthcare settings. Such as: having the ability to fix atmospheric carbon with the help of the sun and water (1). They can do so by undergoing carbon fixation and are able to create ethylene (2) and vitamins (3). 

In order to create a workflow that is easy for scientists and data engineers to collaborate, I would like to aid in the generation of Construction Files. This would essentially be provided by an LLM, when in natural language, the promptee asserts the organism they would like to modify along with the target gene. 

For CRISPR constructs, we first must secure two aims. 

1. Find the PAM sequence. This is where CRISPR CAS 9 / 12 proteins will begin to cleave. This is different for each cas system, and each organism uses a different cas system  
2. Create a guide RNA. This will be able to be done after the PAM sequence is found as the gRNA sequence is upstream of it. 

These functions are implemented in **Python** and are part of the broader bioinformatics toolset aimed at automating genetic sequence analysis tasks.

# Genome Data JSON Documentation

## Organism Data JSON File 
This JSON file stores genome sequences and gene annotations for organisms. It also includes CRISPR toolkit details, such as supported systems and PAM sequences.

## Key Design Decisions
1. **Organisms Grouping**:
   - Each organism is a key under the `organisms` object.
   - This structure allows easy addition of new organisms.

2. **Genome Data**:
   - The `genome` object contains the sequence and a flag (`is_circular`) to indicate whether the genome is circular.

3. **Gene Annotations**:
   - Gene details include `start`, `end`, `strand`, and a `description`.
   - A `_notes` field is added for additional gene-specific comments.

4. **CRISPR Toolkit**:
   - Each organism includes a `toolkit` with supported CRISPR systems and their associated PAM sequences.
   - `notes` in the toolkit clarify details about the PAM sequence.








## Relevant Articles  
1. Cpf1 Is A Versatile Tool for CRISPR Genome Editing Across Diverse Species of Cyanobacteria -> https://www.nature.com/articles/srep39681 
2. Sustained photosynthetic conversion of CO2 to ethylene in recombinant cyanobacterium Synechocystis 6803 -> https://pubs.rsc.org/en/content/articlelanding/2012/ee/c2ee22555g
3. Vitamin B12 excretion by cultures of the marine cyanobacteria Crocosphaera and Synechococcus -> https://aslopubs.onlinelibrary.wiley.com/doi/10.4319/lo.2010.55.5.1959