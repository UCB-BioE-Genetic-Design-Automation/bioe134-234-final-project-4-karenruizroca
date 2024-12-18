import pytest
from bio_functions import design_grna, find_pam

# Mock Data for Testing
ORGANISM_NAME = "Synechococcus elongatus UTEX 2973"
VALID_GENE = "nblA"
INVALID_GENE = "invalid_gene"
TOOLKIT_PAM_SEQUENCE = "YTN"

# Test 1: Valid inputs return a correct gRNA sequence
def test_design_grna_valid():
    """
    Test that the design_grna function returns the correct gRNA sequence for valid inputs.
    """
    grna = design_grna(ORGANISM_NAME, VALID_GENE)
    assert isinstance(grna, str), "gRNA should be a string."
    assert len(grna) == 20, "gRNA should be 20 bp in length."
    # Verify that gRNA is a valid DNA sequence
    assert all(base in "ATCG" for base in grna), "gRNA contains invalid DNA bases."

# Test 2: Invalid gene raises an error
def test_design_grna_invalid_gene():
    """
    Test that the design_grna function raises a ValueError for an invalid gene.
    """
    with pytest.raises(ValueError, match=f"Gene '{INVALID_GENE}' not found in '{ORGANISM_NAME}'."):
        design_grna(ORGANISM_NAME, INVALID_GENE)

# Test 3: Invalid organism raises an error
def test_design_grna_invalid_organism():
    """
    Test that the design_grna function raises a ValueError for an invalid organism.
    """
    invalid_organism = "Unknown Organism"
    with pytest.raises(ValueError, match=f"Organism '{invalid_organism}' not found in JSON."):
        design_grna(invalid_organism, VALID_GENE)

# Test 4: No PAM sequence near the gene
def test_design_grna_no_pam():
    """
    Test that the design_grna function raises an error if no PAM sequence is found.
    """
    # Mock a gene without a PAM sequence nearby
    no_pam_gene = "gene_without_pam"
    with pytest.raises(ValueError, match=f"No PAM sequence {TOOLKIT_PAM_SEQUENCE} found near '{no_pam_gene}'"):
        design_grna(ORGANISM_NAME, no_pam_gene)

# Test 5: Boundary condition - gRNA at the start of the genome
def test_design_grna_boundary_start():
    """
    Test that the design_grna function correctly handles genes near the start of the genome.
    """
    boundary_gene = "start_gene"
    grna = design_grna(ORGANISM_NAME, boundary_gene)
    assert isinstance(grna, str), "gRNA should be a string."
    assert len(grna) == 20, "gRNA should be 20 bp in length."

# Test 6: Boundary condition - gRNA at the end of the genome
def test_design_grna_boundary_end():
    """
    Test that the design_grna function correctly handles genes near the end of the genome.
    """
    boundary_gene = "end_gene"
    grna = design_grna(ORGANISM_NAME, boundary_gene)
    assert isinstance(grna, str), "gRNA should be a string."
    assert len(grna) == 20, "gRNA should be 20 bp in length."
