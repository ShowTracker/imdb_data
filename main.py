import pandas as pd
import time

# Passing the TSV file to
# read_csv() function
# with tab separator
# This function will
# read data from file
imdb_data = pd.read_csv('files/data.tsv', sep='\t')

# Retrieve the genres column as a Series
# genres_series = imdb_data["genres"]
#
# # Convert the Series to a list
# unique_genres = set()
#
# # Iterate over each row in the genres Series
# for genres in genres_series:
#     if pd.notna(genres):
#         genres_list = genres.split(",")
#         unique_genres.update(genres_list)
#
# # Convert the set back to a sorted list
# genres_array = sorted(list(unique_genres))
#
# print(genres_array)
#
# # SQL script template to insert genres into the table
# sql_script = "INSERT INTO genres (name) VALUES\n"
#
# # Generate the values part of the SQL script
# values = []
# for genre in genres_array:
#     values.append(f"('{genre}')")
#
# # Join the values with commas and add them to the SQL script
# sql_script += ",\n".join(values)
#
# # Specify the file path to save the SQL script
# file_path = "insert_genres.sql"
#
# # Save the SQL script to a file
# with open(file_path, "w") as file:
#     file.write(sql_script)
#
# print(f"SQL script saved to {file_path}")

# filtered_df = imdb_data[imdb_data["titleType"].isin(["movie", "tvSeries"])]
#
# # Convert the adult column from 0 and 1 to False and True
# filtered_df["isAdult"] = filtered_df["isAdult"].astype(bool)
#
# # Select the desired columns
# selected_columns = ["primaryTitle", "titleType", "runtimeMinutes", "startYear", "endYear", "isAdult"]
# media_info_df = filtered_df[selected_columns]
# media_info_array = media_info_df.values.tolist()
# # print(len(media_info_array))
#
# start_time = time.time()
# # Generate the SQL script to insert values
# sql_script = "INSERT INTO media (title, titleType, duration, isAdult, year, endYear) VALUES\n"
# for i in media_info_array[800001:893396]:
#     title = str(i[0]).replace("'", "''")
#     title_type = i[1]
#     duration = i[2]
#     is_adult = i[5]
#     year = i[3]
#     end_year = i[4]
#
#     sql_values = f"('{title}', '{title_type}', '{duration}', {is_adult}, '{year}', '{end_year}')"
#     sql_script += f"{sql_values},\n"
#
#     # print(sql_script)
#
# # Remove the trailing comma and new line
# sql_script = sql_script.rstrip(",\n")
#
# # Save the SQL script to a file
# file_path = "import_media08.sql"
# with open(file_path, "w", encoding="utf-8") as file:
#     file.write(sql_script)
#
# print(f"SQL script saved to {file_path}")
# end_time = time.time()
# execution_time = end_time - start_time
#
# print(f"Execution time: {execution_time} seconds")


# Select the desired columns
# selected_columns = ["titleType", "primaryTitle", "isAdult", "startYear", "endYear", "runtimeMinutes"]
# media_info_df = filtered_df[selected_columns]
#
# # Convert the DataFrame to a list of lists
# media_info_array = media_info_df.values.tolist()
#
# print(media_info_array)
genres = ['Action', 'Adult', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama',
          'Family', 'Fantasy', 'Film-Noir', 'Game-Show', 'History', 'Horror', 'Music', 'Musical', 'Mystery',
          'News', 'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Talk-Show', 'Thriller', 'War', 'Western', '\\N']


filtered_df = imdb_data[imdb_data["titleType"].isin(["movie", "tvSeries"])]

# Convert the adult column from 0 and 1 to False and True
filtered_df["isAdult"] = filtered_df["isAdult"].astype(bool)
cut = [0, 1001]
# Select the desired columns from media table
media_columns = ["tconst", "primaryTitle", "titleType", "runtimeMinutes", "isAdult", "startYear", "endYear"]
me = filtered_df[media_columns]
media_df = me[0:100]

# Select the desired columns from genres table
genres_columns = ["tconst", "genres"]
ge = filtered_df[genres_columns]
genres_df = ge[0:100]

# Generate the SQL script to insert connections
sql_script = "INSERT INTO genre_media (genre_id, media_id) VALUES\n"
genre_map = {genre: index + 1 for index, genre in enumerate(genres)}

for _, row in genres_df.iterrows():
    tconst = row["tconst"]
    genres = row["genres"]

    # Split the genres into a list
    genre_list = genres.split(",")

    # Get the media ID for the current tconst value
    media_id = media_df[media_df["tconst"] == tconst].index[0] + 1

    # Generate the SQL values for each genre and media ID
    for genre in genre_list:
        genre_id = genre_map.get(genre.strip(), "\\N")
        sql_values = f"({genre_id}, {media_id})"
        sql_script += f"{sql_values},\n"

# Remove the trailing comma and new line
sql_script = sql_script.rstrip(",\n")

# Save the SQL script to a file
file_path = "connect_tables.sql"
with open(file_path, "w") as file:
    file.write(sql_script)

print(f"SQL script saved to {file_path}")
