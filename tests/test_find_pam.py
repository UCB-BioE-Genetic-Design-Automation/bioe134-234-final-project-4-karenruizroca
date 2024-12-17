import pytest
from bio_functions import find_pam, get_genome_sequence
import json
import os

# Load JSON file
JSON_FILE = "wrapper/organism_data.json"
with open(JSON_FILE, "r") as file:
    organism_data = json.load(file)

# Test data
ORGANISM_NAME = "Synechococcus elongatus UTEX 2973"
GENE_NAME = "nblA"
GENOME_FILE = organism_data["organisms"][ORGANISM_NAME]["genome"]["sequence"]

@pytest.fixture
def genome_sequence():
    """
    Load the genome sequence from the FASTA file for testing.
    """
    return get_genome_sequence(ORGANISM_NAME)

def test_valid_pam_index(genome_sequence):
    """
    Test that find_pam locates a valid PAM sequence near the nblA gene.
    """
    pam_index = find_pam(ORGANISM_NAME, GENE_NAME)
    assert isinstance(pam_index, int), "PAM index should be an integer"
    assert pam_index > 0, "PAM index should be positive"
    print(f"Valid PAM index found: {pam_index}")

def test_missing_gene():
    """
    Test that find_pam raises ValueError for a missing gene.
    """
    with pytest.raises(ValueError, match="Gene 'invalid_gene' not found"):
        find_pam(ORGANISM_NAME, "invalid_gene")

def test_missing_organism():
    """
    Test that find_pam raises ValueError for a missing organism.
    """
    with pytest.raises(ValueError, match="Organism 'invalid_organism' not found"):
        find_pam("invalid_organism", GENE_NAME)

def test_no_pam_found(monkeypatch):
    """
    Test behavior when no PAM sequence is found near a gene.
    """
    # Use monkeypatch to mock get_genome_sequence with a target region lacking the PAM sequence
    def mock_get_genome_sequence(organism_name):
        return "ATCGATCGATCGATCGATCG"  # Mock genome with no valid PAM (YTN)

    monkeypatch.setattr("bio_functions.get_genome_sequence", mock_get_genome_sequence)

    with pytest.raises(ValueError, match="No PAM sequence .* found"):
        find_pam(ORGANISM_NAME, GENE_NAME)


def test_boundary_conditions(monkeypatch, genome_sequence):
    """
    Test that find_pam handles genes near the start or end of the genome.
    """
    # Add a mock gene to test edge boundary conditions
    mock_organism_data = organism_data.copy()
    mock_organism_data["organisms"][ORGANISM_NAME]["genes"]["mock_gene"] = {
        "start": 1,
        "end": 10,
        "strand": "+",
        "description": "Mock gene at genome start."
    }

    # Monkeypatch GENOME_DATA globally for this test
    monkeypatch.setattr("bio_functions.GENOME_DATA", mock_organism_data)

    # Now run find_pam and assert the behavior
    pam_index = find_pam(ORGANISM_NAME, "mock_gene")
    assert isinstance(pam_index, int)
    print(f"Boundary PAM index: {pam_index}")


if __name__ == "__main__":
    pytest.main()
