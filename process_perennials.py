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

def main():
    parser = argparse.ArgumentParser(
        description="Process perennial plant names and map to common names."
    )
    parser.add_argument(
        "-i", "--input_perennials",
        type=str,
        required=True,
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

    with open(args.input_perennials, 'r') as list_file:
        perennials_list = list_file.readlines()

    # Specify CSV column order
    fieldnames = ["full_name", "scientific_name", "common_name", "description", "image_url"]

    with open(args.output_csv, "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for perennial_name in perennials_list:
            scientific_name = " ".join(line.strip().split()[:2])
            common_name = plant_names.get_common_name(scientific_name)
            description, image_url = plant_wiki.get_info(scientific_name)
            row = {"full_name": perennial_name, "scientific_name": scientific_name
                   , "common_name": common_name, "description": description, "image_url": image_url}
            # Write the row to the CSV file
            writer.writerow(row)

if __name__ == "__main__":
    main()



with open(PERENNIALS_INFO_FILE, 'w') as info_file:
    for line in perennials_list:
        # Take the first two words as the scientific name
        scientific_name = " ".join(line.strip().split()[:2])
        print(f"Processing: {scientific_name}")
        common_name = plant_names.get_common_name(scientific_name)
        if common_name:
            description, image_url = plant_wiki.get_info(scientific_name)
            info_file.write(f"{scientific_name}\t{common_name}\t{description}\t{image_url}\n")
        else:
            print(f"No common name found for {scientific_name}")

