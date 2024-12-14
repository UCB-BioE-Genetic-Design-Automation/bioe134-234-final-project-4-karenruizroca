def reverse_complement(sequence):
    """
    Calculates the reverse complement of a DNA sequence.
    
    Args:
        sequence (str): A string representing the DNA sequence.

    Returns:
        str: The reverse complement of the DNA sequence.

    Raises:
        ValueError: If the DNA sequence contains invalid characters.
    """
    valid_nucleotides = {'A', 'T', 'C', 'G'}
    if any(char not in valid_nucleotides for char in sequence):
        raise ValueError("DNA sequence contains invalid characters. Allowed characters: A, T, C, G.")

    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return ''.join(complement[base] for base in reversed(sequence))

def find_pam(genome_data, organism_name, gene_name, pam_sequence="TTTV"):
    # Locate the gene in the genome file
    genome = genome_data[organism_name]["genome"]
    gene_info = genome_data[organism_name]["genes"].get(gene_name)
    
    if not gene_info:
        raise ValueError(f"Gene {gene_name} not found in {organism_name}.")

    start, end = gene_info["start"], gene_info["end"]
    target_region = genome[start-50:end+50]  # Search 50 bp upstream and downstream

    # Search for the PAM sequence
    for i in range(len(target_region) - len(pam_sequence)):
        if target_region[i:i + len(pam_sequence)] == pam_sequence:
            return start - 50 + i  # Return PAM index in the full genome

    raise ValueError(f"No PAM sequence {pam_sequence} found near {gene_name}.")

def design_grna(genome_data, organism_name, gene_name, pam_sequence="TTTV", grna_length=20):
    # Find the PAM index
    pam_index = find_pam(genome_data, organism_name, gene_name, pam_sequence)

    # Extract the 20 bp sequence upstream of the PAM
    genome = genome_data[organism_name]["genome"]
    grna_target = genome[pam_index - grna_length:pam_index]

    # Generate the complementary gRNA sequence
    grna_complementary = reverse_complement(grna_target)

    return grna_complementary

if __name__ == "__main__":
    # Example DNA sequence for demonstration
    dna_example = "ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG"

    try:
        # Perform reverse complement
        rc_result = reverse_complement(dna_example)
        print(f"Reverse Complement of '{dna_example}': {rc_result}")

        # Perform translation
        translation_result = translate(dna_example)
        print(f"Translation of '{dna_example}': {translation_result}")
    except Exception as e:
        print(f"Error: {str(e)}")
