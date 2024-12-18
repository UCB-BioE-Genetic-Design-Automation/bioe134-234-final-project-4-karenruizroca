import pytest
from bio_functions import generate_construction_file, GENOME_DATA, find_pam, design_grna

# Test constants
ORGANISM_NAME = "Synechococcus elongatus UTEX 2973"
VALID_GENE = "nblA"
INVALID_GENE = "invalid_gene"
INVALID_ORGANISM = "Unknown Organism"

def test_valid_construction_file():
    """
    Test that generate_construction_file returns a correct construction file for valid inputs.
    """
    result = generate_construction_file(ORGANISM_NAME, VALID_GENE)
    
    # Validate keys in the construction file
    assert "construction_file" in result
    assert "metadata" in result["construction_file"]
    assert "organism" in result["construction_file"]["metadata"]


def test_missing_gene():
    """
    Test that generate_construction_file raises ValueError for a missing gene.
    """
    with pytest.raises(ValueError, match=f"Gene '{INVALID_GENE}' not found"):
        generate_construction_file(ORGANISM_NAME, INVALID_GENE)

def test_missing_organism():
    """
    Test that generate_construction_file raises ValueError for a missing organism.
    """
    with pytest.raises(ValueError, match=f"Organism '{INVALID_ORGANISM}' not found"):
        generate_construction_file(INVALID_ORGANISM, VALID_GENE)

def test_pam_sequence_matches_toolkit():
    """
    Test that the forward oligo in the construction file is derived correctly using the PAM sequence.
    """
    result = generate_construction_file(ORGANISM_NAME, VALID_GENE)
    
    # Derive gRNA sequence
    grna_sequence = design_grna(ORGANISM_NAME, VALID_GENE)
    
    # Check that forward oligo matches the expected gRNA
    forward_oligo = result["construction_file"]["steps"][0]["inputs"]["forward_oligo"]
    assert forward_oligo == grna_sequence, "Forward oligo does not match the gRNA sequence derived from the PAM."


def test_gRNA_sequence_validity():
    """
    Test that the gRNA sequence matches the forward oligo in the construction file.
    """
    result = generate_construction_file(ORGANISM_NAME, VALID_GENE)
    
    # Derive the expected gRNA sequence
    expected_grna_sequence = design_grna(ORGANISM_NAME, VALID_GENE)
    
    # Forward oligo should match the expected gRNA sequence
    forward_oligo = result["construction_file"]["steps"][0]["inputs"]["forward_oligo"]
    assert forward_oligo == expected_grna_sequence, "Forward oligo does not match the expected gRNA sequence."

