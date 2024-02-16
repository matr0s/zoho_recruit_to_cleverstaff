# ZOHO RECRUIT Candidate Data Processing Script

This Python script processes and combines data from multiple CSV files related to candidates, their notes, and educational details, and exports the consolidated data into an Excel file. It's specifically designed to prepare candidate data for import from ZOHO Recruit into systems like Cleverstaff, with customized formatting including HTML tags for line breaks.

## Features

- Reads candidate, notes, and educational details from CSV files.
- Aggregates notes and educational details per candidate.
- Formats text content with HTML `<br>` tags for compatibility with various systems.
- Handles potential duplicate 'Currency' columns after merging data.
- Exports the final consolidated data into an Excel file with a timestamp in the filename.

## Requirements

- Python 3
- pandas library
- openpyxl library (for writing to Excel files)

## Usage

1. Place your CSV files (`Candidates_001.csv`, `Notes_001.csv`, `Candidates_Educational_Details.csv`) in a ExportData directory.
2. Update the `export_data_folder` variable (if necessary) in the script to point to the directory containing your CSV files.
3. Run the script:

```
python3 candidate_data_processing.py
```

4. Check the script's output directory for the generated Excel file.

## Customization

You can customize the script by modifying the column mappings and formatting in the process_candidates_and_notes function to match your specific data structure and requirements.

## Contributing

Feel free to fork this repository and submit pull requests with any enhancements or fixes.

## License

This project is open-source and available under the MIT License.

## Contact

For any questions or suggestions, please open an issue in this repository.

Make sure to replace `candidate_data_processing.py` with the actual filename of your script if it's different. Also, review and adjust any specific details to ensure they accurately describe your project and how to use the script.
