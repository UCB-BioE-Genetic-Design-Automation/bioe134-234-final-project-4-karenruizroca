# ===========================
#  IMPORTS
# ===========================
from Bio import SeqIO
import os
import json
from copy import deepcopy


# ===========================
#  GLOBAL VARIABLES
# ===========================
# Load the organisms' data JSON file
with open("wrapper/organism_data.json", "r") as file:
    GENOME_DATA = json.load(file)

# ===========================
#  HELPER FUNCTIONS
# ===========================

def generate_construction_file(organism_name, gene_name):
    """
    Generates and prints a CRISPR gene knockout construction file.

    Args:
        organism_name (str): Name of the organism.
        gene_name (str): Target gene name.

    Returns:
        dict: A populated construction file instance.
    """
    # Verify the template file exists
    template_path = "wrapper/construction_file_format.json"
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template file '{template_path}' not found.")

    # Retrieve organism toolkit and gene details
    organism = GENOME_DATA["organisms"].get(organism_name)
    if not organism:
        raise ValueError(f"Organism '{organism_name}' not found.")

    gene = organism["genes"].get(gene_name)
    if not gene:
        raise ValueError(f"Gene '{gene_name}' not found in '{organism_name}'.")

    toolkit = organism["toolkit"]
    crispr_system = toolkit["crispr_systems"][0]

    # Generate forward and reverse oligos dynamically
    forward_oligo = design_grna(organism_name, gene_name)
    reverse_oligo = reverse_complement(forward_oligo)

    # Read the template JSON file
    with open(template_path, "r") as template_file:
        template = json.load(template_file)

    # Prepare dynamic values for placeholders
    placeholders = {
        "experiment_name": f"{gene_name}_knockout_{organism_name.replace(' ', '_')}",
        "forward_oligo": forward_oligo,
        "reverse_oligo": reverse_oligo,
        "template_dna": f"genomic_DNA_{organism_name}",
        "pcr_output": f"PCR_product_{gene_name}",
        "input_dna": f"PCR_product_{gene_name}",
        "restriction_enzyme": f"{crispr_system}_restriction_enzyme",
        "fragment_selection": f"selected_fragment_{gene_name}",
        "digest_output": f"Digested_{gene_name}",
        "input_dnas": [f"Digested_{gene_name}", "Vector_backbone"],  # List instead of string
        "ligation_output": f"Ligation_product_{gene_name}",
        "strain_name": organism_name,
        "antibiotic": "Spec",  # Example antibiotic
        "final_construct": f"Final_construct_{gene_name}",
        "enzyme_list": [f"{crispr_system}_restriction_enzyme"],  # List for enzymes
        "additional_notes": f"Knockout construct for {gene_name}"
    }
    # Replace placeholders in the JSON template
    def replace_placeholders(obj, placeholders):
        if isinstance(obj, dict):
            return {k: replace_placeholders(v, placeholders) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [replace_placeholders(item, placeholders) for item in obj]
        elif isinstance(obj, str):
            try:
                return obj.format(**placeholders)
            except KeyError as e:
                raise KeyError(f"Missing placeholder key: {e}")  # Debug missing placeholders
        return obj


    populated_file = replace_placeholders(template, placeholders)
    print("DEBUG: Fully populated construction file:", json.dumps(populated_file, indent=4))


    # DEBUG: Print the dynamically populated steps for inspection
    print("DEBUG: Populated Construction File:", json.dumps(populated_file, indent=4))

    # Print the steps in a user-friendly format
    print("\nGenerated Construction Steps:")
    for step in populated_file["construction_file"]["steps"]:
        step_type = step["step_type"].lower()
        inputs = step["inputs"]
        outputs = step["outputs"]

        if step_type == "pcr":
            print(f"pcr {inputs['forward_oligo']} {inputs['reverse_oligo']} {inputs['template']} {outputs['product']}")
        elif step_type == "digest":
            print(f"digest {inputs['dna']} {inputs['enzymes'][0]} 1 {outputs['product']}")
        elif step_type == "ligate":
            print(f"ligate {inputs['dnas']} {outputs['product']}")
        elif step_type == "transform":
            print(f"transform {inputs['dna']} {inputs['strain']} {inputs['antibiotics'][0]} {outputs['product']}")

    return populated_file



def get_genome_sequence(organism_name):
    """
    Loads the genome sequence for a specific organism from its FASTA file.

    Args:
        organism_name (str): The name of the organism.

    Returns:
        str: The genome sequence.
    """

    # Retrieve organism data
    organism = GENOME_DATA["organisms"].get(organism_name)
    if not organism:
        raise ValueError(f"Organism '{organism_name}' not found in JSON.")

    # Get the FASTA file path
    fasta_file = organism["genome"].get("sequence")
    print(f"DEBUG: FASTA file path retrieved: {fasta_file}")  # Add this line

    if not fasta_file:
        raise ValueError(f"FASTA file path not found for '{organism_name}'.")

    # Load and return the genome sequence from the FASTA file
    with open(fasta_file, "r") as file:
        record = next(SeqIO.parse(file, "fasta"))
        return str(record.seq)

def reverse_complement(sequence):
    """
    Computes the reverse complement of a DNA sequence.

    Args:
        sequence (str): The DNA sequence.

    Returns:
        str: The reverse complement of the input DNA sequence.
    """
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return ''.join(complement[base] for base in reversed(sequence))

def get_toolkit_for_organism(organism_name):
    """
    Retrieve the genetic engineering toolkit available for the specified organism.
    
    Args: organism_name (str): The name of the organism.
        
    Returns: dict: A dictionary containing the toolkit details for the organism, including CRISPR systems and PAM sequences.
    """
    # Retrieve the organism's data
    organism = GENOME_DATA["organisms"].get(organism_name)
    if not organism:
        raise ValueError(f"No toolkit found for organism {organism_name}.")

    # Return the toolkit
    toolkit = organism.get("toolkit")
    if not toolkit:
        raise ValueError(f"Toolkit not defined for {organism_name}.")

    return toolkit


def get_gene_region(organism_name, gene_name):
    """
    Extracts the genome region surrounding a specified gene.

    Args:
        organism_name (str): Name of the organism.
        gene_name (str): Name of the gene.

    Returns:
        str: The extracted genome region, including 50 base pairs flanking the gene.
    """
    # Fixed flanking base pairs
    flanking_bp = 50

    # Retrieve the organism's data
    organism = GENOME_DATA["organisms"].get(organism_name)
    if not organism:
        raise ValueError(f"Organism {organism_name} not found.")

    genome = organism["genome"]["sequence"]
    gene = organism["genes"].get(gene_name)
    if not gene:
        raise ValueError(f"Gene {gene_name} not found in {organism_name}.")

    # Extract the region with flanking base pairs
    start, end = gene["start"], gene["end"]
    return genome[max(0, start - flanking_bp):min(len(genome), end + flanking_bp)]

# ===========================
#  MAIN FUNCTIONS
# ===========================

def find_pam(organism_name, gene_name):
    """
    Finds the PAM sequence for the CRISPR system of the specified organism near a target gene.

    Args:
        organism_name (str): Name of the organism.
        gene_name (str): Name of the gene near which to search for the PAM sequence.

    Returns:
        int: The index of the PAM sequence in the full genome.
    """
    # Load genome sequence
    genome_sequence = get_genome_sequence(organism_name)
    
    # Retrieve organism and gene data
    organism = GENOME_DATA["organisms"].get(organism_name)
    gene = organism["genes"].get(gene_name)
    if not gene:
        raise ValueError(f"Gene '{gene_name}' not found in '{organism_name}'.")

    strand = gene.get("strand", "+")  # Default to forward strand

    # Extract region around the gene
    start, end = gene["start"], gene["end"]
    flanking_bp = 50
    target_region = genome_sequence[max(0, start - flanking_bp):min(len(genome_sequence), end + flanking_bp)]

    # Reverse complement if on the reverse strand
    if strand == "-":
        target_region = reverse_complement(target_region)

    # Search for the PAM sequence
    pam_sequence = organism["toolkit"].get("pam_sequence")
    print(f"DEBUG: Searching for PAM '{pam_sequence}' in target region...")
    for i in range(len(target_region) - len(pam_sequence) + 1):
        if all(
            base == ref or ref == "N" or (ref == "Y" and base in "CT")
            for base, ref in zip(target_region[i:i + len(pam_sequence)], pam_sequence)
        ):
            print(f"DEBUG: PAM found at index {i}")
            return max(0, start - flanking_bp + i)

    print("DEBUG: No valid PAM sequence found.")
    raise ValueError(f"No PAM sequence {pam_sequence} found near '{gene_name}' in '{organism_name}'.")


def design_grna(organism_name, gene_name):
    """
    Designs a gRNA sequence for the specified gene in the given organism.

    Args:
        organism_name (str): Name of the organism.
        gene_name (str): Name of the gene for which the gRNA is being designed.

    Returns:
        str: The complementary gRNA sequence.
    """
    # Fixed gRNA length of 20 bp
    grna_length = 20

    # Locate the PAM using the find_pam function
    pam_index = find_pam(organism_name, gene_name)

    # Extract genome sequence using the helper function
    genome_sequence = get_genome_sequence(organism_name)

    # Extract the sequence upstream of the PAM
    grna_target = genome_sequence[max(0, pam_index - grna_length):pam_index]

    # Validate the gRNA target length
    if len(grna_target) != grna_length:
        raise ValueError(f"Unable to extract {grna_length}-bp sequence upstream of the PAM.")

    # Generate the complementary gRNA sequence
    return reverse_complement(grna_target)


# ===========================
#  TEST FUNCTIONS (OPTIONAL)
# ===========================

if __name__ == "__main__":
    # Example usage for testing
    organism = "Synechococcus elongatus UTEX 2973"
    gene = "nblA"
    
    try:
        print("Testing find_pam:")
        pam_index = find_pam(organism, gene)
        print(f"PAM Index: {pam_index}")
        
        print("\nTesting design_grna:")
        grna = design_grna(organism, gene)
        print(f"Designed gRNA: {grna}")
        
    except ValueError as e:
        print(e)