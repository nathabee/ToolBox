#conda activate leetcode
#pip install pandas mysql-connector-python
import os
import pandas as pd
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Database connection parameters
db_config = {
    'user': 'beeuser',
    'password': 'bee147',
    'host': 'localhost',
    'database': 'wp_beegarten'
}

# WordPress uploads directory
# sudo chmod 777 /var/www/html/wordpress/wp-content/uploads
wp_uploads_dir = '/var/www/html/wordpress/wp-content/uploads'

# Path to the CSV file
csv_file_path = '/home/nathalie/Downloads/bilder/naturgarten/flora_incognita_2024-05-20T20_09_25.csv'
image_base_path = '/home/nathalie/Downloads/bilder/naturgarten'
   

# Read the CSV file
df = pd.read_csv(csv_file_path, sep=',')

# Function to get the first image file in a directory
def get_first_image_file(directory):
    for filename in os.listdir(directory):
        if filename.endswith((".jpg", ".jpeg", ".png", ".gif")):
            return filename
    return None

# Function to generate a GUID
def generate_guid(date, filename):
    return f"http://localhost/wp-content/uploads/{date}/{filename}"

# Function to get the upload directory and create it if it doesn't exist
def get_upload_dir(date):
    upload_dir = os.path.join(wp_uploads_dir, date)
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    return upload_dir


# Connect to the database
try:
    connection = mysql.connector.connect(**db_config)
    if connection.is_connected():
        cursor = connection.cursor()

        for index, row in df.iterrows():
            date = row['date']
            scientific_name = row['scientific name']
            name = row['name']
            # Extract image metadata from CSV
            alt_text =  row['scientific name']
            caption =  row['name']
            description = row['scientific name']

            directory_path = os.path.join(image_base_path, date)
            filename = get_first_image_file(directory_path)
            if filename is None:
                print(f"No image found in {directory_path}, skipping.")
                continue

            upload_dir = get_upload_dir(date)
            upload_file_path = os.path.join(upload_dir, filename)

            # Copy the image to the WordPress uploads directory
            source_file_path = os.path.join(directory_path, filename)
            if os.path.exists(source_file_path):
                os.system(f"cp {source_file_path} {upload_file_path}")
            else:
                print(f"Image {source_file_path} not found, skipping.")
                continue

            # Insert into wp_posts
            post_date = datetime.strptime(date, '%Y-%m-%dT%H_%M_%SZ').strftime('%Y-%m-%d %H:%M:%S')
            post_name = os.path.splitext(filename)[0]
            guid = generate_guid(date, filename)

            insert_post_query = """
            INSERT INTO wp_posts (
                post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt, post_status, 
                comment_status, ping_status, post_password, post_name, to_ping, pinged, post_modified, 
                post_modified_gmt, post_content_filtered, post_parent, guid, menu_order, post_type, 
                post_mime_type, comment_count
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            post_data = (
                1, post_date, post_date, '', filename, '', 'inherit', 'closed', 'closed', '', post_name, '', '', 
                post_date, post_date, '', 0, guid, 0, 'attachment', 'image/jpeg', 0
            )
            cursor.execute(insert_post_query, post_data)
            attachment_id = cursor.lastrowid

            # Insert into wp_postmeta
            insert_postmeta_query = """
            INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
            VALUES (%s, %s, %s)
            """
            postmeta_data = [
                (attachment_id, '_wp_attached_file', f"{date}/{filename}"),
                (attachment_id, '_wp_attachment_metadata', '{"width":0,"height":0,"file":"' + f"{date}/{filename}" + '"}'), 
                (attachment_id, '_wp_attachment_caption', {caption}),
                (attachment_id, '_wp_attachment_description', {description}),
                (attachment_id, '_wp_attachment_image_alt', {alt_text})
            ]

            cursor.executemany(insert_postmeta_query, postmeta_data)
        
        # Commit the transaction
        connection.commit()
        print(f"Images inserted successfully.")

except Error as e:
    print(f"Error: {e}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed.")