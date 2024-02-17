import csv
import os

# Step 1 & 2: Open the original CSV file in read mode and read it
with open('terrain_coinafrique.csv', 'r') as inp, open('temp.csv', 'w', newline='') as out:
    # Step 3 & 4: Open a new CSV file in write mode
    writer = csv.writer(out)
    # Step 5: Iterate over each row in the original CSV file
    for row in csv.reader(inp):
        # Step 6: If the row is not empty and does not contain empty boxes, write it into the new CSV file
        if row and all(field.strip() for field in row):
            writer.writerow(row)

# Step 7: Close both files (automatically done by 'with' statement)

