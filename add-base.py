import argparse
import rdflib


# test comment
def find_ontology_base(file_path):
    g = rdflib.Graph()
    g.parse(file_path, format='turtle')
    
    for s in g.subjects(predicate=rdflib.RDF.type, object=rdflib.OWL.Ontology):
        return str(s)
    return None

def add_base_if_missing(file_path):
    base_uri = find_ontology_base(file_path)
    if base_uri is None:
        print("No owl:Ontology found in the RDF file!")
        return

    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Find the line number of the first occurrence of '@prefix'
    prefix_line_number = next((i for i, line in enumerate(lines) if line.startswith("@prefix")), None)

    if prefix_line_number is not None:
        # Check if @base is already in the file before the first @prefix
        if all("@base" not in line for line in lines[:prefix_line_number]):
            lines.insert(prefix_line_number, f"@base <{base_uri}> .\n")
    else:
        # If no @prefix is found, just append at the end (or handle in some other manner)
        lines.append(f"@base <{base_uri}> .\n")

    with open(file_path, 'w') as f:
        f.writelines(lines)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add @base to an RDF Turtle file if it is missing.')
    parser.add_argument('file_path', help='Path to the RDF Turtle file.')

    args = parser.parse_args()

    add_base_if_missing(args.file_path)
