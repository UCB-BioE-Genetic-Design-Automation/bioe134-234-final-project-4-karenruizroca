import json
from bio_functions import load_fasta_genome

# Paths
fasta_file = "data/synechococcus_elongatus_2973.fasta"
json_file = "wrapper/organism_data.json"

try:
    # Load genome from FASTA
    genome_sequence = load_fasta_genome(fasta_file)
    print("Loaded genome sequence successfully.")

    # Safely load existing JSON
    try:
        with open(json_file, "r") as file:
            content = file.read()
            if not content.strip():
                raise ValueError("The JSON file is empty!")
            organism_data = json.loads(content)
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error loading JSON: {e}")
        exit(1)

    # Update genome sequence
    organism_name = "Synechococcus elongatus UTEX 2973"
    if organism_name in organism_data.get("organisms", {}):
        organism_data["organisms"][organism_name]["genome"]["sequence"] = genome_sequence
        print(f"Updated genome sequence for {organism_name}.")
    else:
        print(f"Error: Organism '{organism_name}' not found in JSON file.")
        exit(1)

    # Save updated JSON
    try:
        with open(json_file, "w") as file:
            json.dump(organism_data, file, indent=4)
        print("Genome sequence updated successfully.")
    except Exception as e:
        print(f"Error saving JSON: {e}")
        exit(1)

except Exception as e:
    print(f"Unexpected error: {e}")
    exit(1)
