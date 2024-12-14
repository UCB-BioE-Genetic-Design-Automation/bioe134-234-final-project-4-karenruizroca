
# BioE 134 Final Project Submission

## Project Overview

This project provides two core bioinformatics utilities: 

1. **Reverse Complement (revcomp)**: Calculates the reverse complement of a DNA sequence.
2. **Translate**: Translates a DNA sequence into a protein sequence according to the standard genetic code.

These functions are implemented in **Python** and are part of the broader bioinformatics toolset aimed at automating genetic sequence analysis tasks.

---

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

Both functions have been tested with standard, edge, and invalid input cases. A comprehensive suite of tests has been implemented using **pytest**.

- **Test File**: `tests/test_bio_functions.py`

The tests include:
- Valid sequences
- Sequences containing invalid characters
- Sequences with lengths not divisible by three (for the translate function)
- Palindromic sequences (for reverse complement)
- Lowercase input handling

---

## Usage Instructions

Clone the repository and install the required dependencies listed in `requirements.txt`. The functions can be imported from the `bio_functions.py` module.

**Example**:

```bash
pip install -r requirements.txt
```

Once installed, you can use the functions as follows:

```python
from bio_functions import reverse_complement, translate

# Example DNA sequence
dna_sequence = "ATGC"

# Reverse complement
print(reverse_complement(dna_sequence))

# Translate
print(translate("ATGGCC"))
```

---

## Conclusion

These two functions provide foundational operations for working with the Cyanobacteria animal kingdrom in bioinformatics pipelines. They have been tested and documented, ensuring proper error handling and robust functionality.
