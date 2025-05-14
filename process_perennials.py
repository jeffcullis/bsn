import csv
import argparse
from plant_names import PlantNames
from plant_wiki import PlantWiki

# Input file containing scientific names of perennials
PERENNIALS_LIST_FILE = "./data/perennials.txt"
# Output file to store common names
PERENNIALS_INFO_FILE = "./data/perennials_info.csv"

plant_names = PlantNames()
plant_wiki = PlantWiki()

def guess_scientific_name(full_name):
    name_words = full_name.strip().split()
    name_options = []
    if len(name_words) > 0:
        name_options.append(name_words[0])
    
    if len(name_words) > 1:
        name_options.append(' '.join(name_words[:2]))

    if len(name_words) > 2:
        if name_words[1].lower() == 'x':
            name_options.append(' '.join([name_words[0], name_words[2]]))
            name_options.append(' '.join(name_words[:3]))

    print(name_options)
    # Reverse name options order to try the longest (most specific) name first
    for name in reversed(name_options):
        pn_name = plant_names.get_common_name(name)
        pw_desc, pw_img = plant_wiki.get_wiki_data(name)
        if pn_name or pw_desc:
            return name
    
    if len(name_options) > 0:
        return name_options[0]
    else:
        return ''

def main():
    parser = argparse.ArgumentParser(
        description="Process perennial plant names and map to common names."
    )
    parser.add_argument(
        "-i", "--input_perennials",
        type=str,
        default=PERENNIALS_LIST_FILE,
        help="Path to the input text file containing perennial scientific names (one per line)."
    )
    parser.add_argument(
        "-o", "--output_csv",
        type=str,
        default=PERENNIALS_INFO_FILE,
        help="Path to the output CSV file with common names and info from wikipedia."
    )
    args = parser.parse_args()

    print(f"Input file: {args.input_perennials}")
    print(f"Output file: {args.output_csv}")

    perennials_list = []
    # Read the list of perennials from the input file
    with open(args.input_perennials, 'r') as list_file:
        perennials_list = list_file.readlines()

    # Specify CSV column order
    fieldnames = ["full_name", "scientific_name", "common_name", "description", "image_url"]

    with open(args.output_csv, "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for perennial_line in perennials_list:
            full_name = perennial_line.strip()
            scientific_name = guess_scientific_name(full_name)
            common_name = plant_names.get_common_name(scientific_name)
            description, image_url = plant_wiki.get_wiki_data(scientific_name)
            row = {"full_name": full_name, "scientific_name": scientific_name
                   , "common_name": common_name, "description": description, "image_url": image_url}
            # Write the row to the CSV file
            writer.writerow(row)

if __name__ == "__main__":
    main()


