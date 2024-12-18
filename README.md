
# BioE 134 Final Project: Plant Genome Editing Using CRISPR 

## Project Overview

Our team wanted to create a CRISPR-based knockout construction file for specific organisms and gene sequences. Each member took a different part of the animal kingdom. We divided it into higher plants (like tomatoes, maize), cyanobacteria, fungi, and insects. The construction files would help the scientists looking to perform a gene knock out without having to specify more than the organism name and target gene. Our combined resources of the animal kingdom would aid in picking out a toolkit for the experiment. From there we must each design our own guide RNA and a method to locate the PAM sequence. 


## Scope of Work

As part of the final project for BioE 134, I developed two functions that are foundational for CRISPR knock out in cyanobacteria:

1. **Find PAM Sequence**: This function returns the index of the DNA sequence's PAM index, which is  essential for the creation of a CRISPR construct.
   
2. **Design gRNA**: This function uses the Find PAM function in order to find the target DNA's sequence that will guide the CAS12.

Both functions include input validation and error handling to ensure proper use. The Find PAM sequence raises an error if no PAM sequence is found, while the design gRNA function raises an error for genes not found in the genomic data of organism provided.

---

## Function Descriptions

### 1. Find PAM Sequence (`find_pam`)

- **Description**: This function takes an organism name and desired gene to edit and returns index of PAM sequence near the gene of interest. The function raises a `ValueError` if no PAM sequences are found. Must check which CRISPR toolkit it may use to look for appropriate PAM sequence. 
- **Inputs**: A string representing the name of the organism. A string including the name of the gene of interest. 
- **Output**: An integer for the index of the PAM sequence near the gene. 

**Example**:
```python
pam_sequence("cyanobacteria","geneA")
# Returns: "34"
```

### 2. Design Guide RNA  (`design_grna`)

- **Description**: This function helps build a base pair sequence complementary to the target DNA upstream of the PAM sequence of specified organism and near the gene of interest.
- **Input**: A string representing the DNA sequence.
- **Output**: A string representing the translated protein sequence.

**Example**:
```python
design_grna("cyanobacteria", "geneB")
# Returns: "ACTGTTGGATCGATAAGTC"
```

---

## Error Handling

### Find PAM Sequence
- Raises `ValueError` if no PAM sequence is found for inputted gene

### Design Guide RNA
- Raises `ValueError` if there are not enough base pairs upstream of the PAM sequence

---

## Testing

- **Test File**: `tests/test_find_pam.py`

I tested the find_pam function by designing comprehensive unit tests to validate its behavior under various conditions:

1. Valid Inputs: I verified that the function correctly identifies the PAM sequence near a target gene and accurately returns its location.
2. Edge Cases: I tested scenarios where the target gene or organism is missing from the input data, ensuring the function raises appropriate ValueError exceptions.
3. No PAM Found: I included a test to confirm that the function handles cases where no PAM sequence is found near the specified gene, raising a ValueError with a clear and informative message.
5. Boundary Conditions: I tested genes located at the very start or end of the genome sequence to ensure the function searches for PAM sequences correctly without causing indexing errors.

- **Test File**: `tests/test_design_grna.py
I tested my design_grna in a similar manner. However find_pam is free of errors and if more organism data was added adequately it would be able to find it. Yet design_grna still needs some work. Regardless here are the test cases: 

1. Valid Inputs: I ensured that the function generates a correct gRNA sequence, verifying that it is exactly 20 base pairs long and contains only valid DNA bases (A, T, C, G).
2. Invalid Gene: I tested cases where the target gene is missing or invalid, ensuring the function raises a ValueError with a clear and informative message.
3. Invalid Organism: I verified that the function properly handles scenarios where the organism name is not found in the input data, raising an appropriate ValueError.
4. No PAM Sequence Found: I included a test to confirm that the function correctly handles cases where no PAM sequence is located near the specified gene, raising a ValueError indicating the absence of a PAM site.
5. Boundary Conditions: I tested genes positioned at the very start or end of the genome sequence to ensure the function generates the correct gRNA sequence without causing indexing errors or unexpected behavior.


---

## Usage Instructions

Clone the repository and install the required dependencies listed in `requirements.txt`. The functions can be imported from the `bio_functions.py` module.

**Example**:

```bash
pip install -r requirements.txt
```

Once installed, you can use the functions as follows:

```python
from bio_functions import find_pam, design_grna

# Example Organism and Gene
organism_name = "Synechococcus elongatus UTEX 2973"
gene_name = "nblA"

# Find PAM sequence
pam_index = find_pam(organism_name, gene_name)
print(f"PAM sequence found at index: {pam_index}")

# Design gRNA sequence
grna_sequence = design_grna(organism_name, gene_name)
print(f"Generated gRNA sequence: {grna_sequence}")
```

---

## Conclusion and accomplishments
This is my effort in creating a smoother workflow for genetic engineering experiments involving cyanobacteria. I mention their importance in bio_functions_docs along with some articles for further reading. I worked on two functions that would be essential for the implementation of a computer aided experiment. The ultimate goal would be for the user to be able to provide the organism (of any animal kingdom) and be able to get a list of steps to perform their experiment. As of right now find_pam is able to correctly find PAM sequences near target genes and behaves rather predictably if no valid PAM sequence is found. I have included wrappers for various functions (explicitly disucssed in bio_functions_docs) for when this project progresses to a user-LLM interface ordeal. 
This course has been a lovely way to finish up my education at UC Berkeley. I would like to give a big thank you to Professor Anderson whose lectures were very interesting and was always willing to answer questions. And Aditya for helping me in my projects and DSP accomodations. 

