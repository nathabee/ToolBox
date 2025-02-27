 

# copy drag drop in wordpress in the library...


# make a first SQL script file to update   caption und description : 
# after execution of this file in : <sql_file>
# will be executed from mysql or phpmyadmin ( http://localhost/phpmyadmin/)  (login user from database of wp_beegarten db for example)


# make a second SQL script file to update  alternative name using entries in the database  :
 
#INSERT INTO wp_postmeta (post_id, meta_key, meta_value) SELECT post_id, '_wp_attachment_image_alt',  SUBSTRING_INDEX(SUBSTRING_INDEX(meta_value, '/', -1), '-', 1)
#FROM wp_postmeta WHERE meta_key = '_wp_attached_file'   AND meta_value LIKE '2024/05/%.jpg'; 



import os
import csv
import shutil

def rename_and_copy_images(csv_file, image_dir, output_dir, sql_file):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Recursively search for image files in all subdirectories
    image_files = []
    for root, dirs, files in os.walk(image_dir):
        for file in files:
            if file.endswith('.jpg'):
                image_files.append(os.path.join(root, file))

    if not image_files:
        print(f"No image files found in {image_dir}")
        return

    # Read the CSV file
    sql_statements = []
    with open(csv_file, 'r', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        next(csvreader)  # Skip header row
        for row in csvreader:
            date, scientific_name, name = row[1], row[2], row[3]
            found_match = False
            for image_file in image_files:
                if os.path.basename(image_file).startswith(date[:20]):  # Check if filename matches the date
                    found_match = True
                    # Rename the file based on the scientific name
                    image_prefix = ''.join([word.capitalize() for word in scientific_name.split()])
                    new_image_name = f"{image_prefix}-{os.path.basename(image_file).split('-')[-1]}"
                    new_image_path = os.path.join(output_dir, new_image_name)
                    try:
                        shutil.copy(image_file, new_image_path)
                        print(f"Successfully copied {os.path.basename(image_file)} to {new_image_path}")
                        
                        # Prepare SQL update statements
                        sql_statements.append(f"""
                        UPDATE wp_posts
                        SET post_content = "{scientific_name}, scientific name for {name}",
                            post_excerpt = "{name}"
                        WHERE post_title = "{os.path.splitext(new_image_name)[0]}";
                        """)
                    except Exception as e:
                        print(f"Error copying {os.path.basename(image_file)}: {str(e)}")
            if not found_match:
                print(f"No matching filename found for date {date}")

    # Write SQL statements to the file
    with open(sql_file, 'w', encoding='utf-8') as sqlfile:
        sqlfile.write('\n'.join(sql_statements))
        print(f"SQL script written to {sql_file}")

if __name__ == "__main__":
    csv_file = '/home/nathalie/Downloads/bilder/naturgarten/flora_incognita_2024-05-20T20_09_25.csv'  # Path to the CSV file
    image_dir = '/home/nathalie/Downloads/bilder/naturgarten'  # Directory containing image files
    output_dir = os.path.join(image_dir, "tmp2")  # Output directory for renamed and copied images
    sql_file = '/home/nathalie/Downloads/bilder/naturgarten/update_posts.sql'  # Path to the SQL script file
    rename_and_copy_images(csv_file, image_dir, output_dir, sql_file)
 

 