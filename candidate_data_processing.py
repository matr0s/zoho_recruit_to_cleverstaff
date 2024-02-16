import pandas as pd
import os
from datetime import datetime

def process_candidates_and_notes(export_data_folder, output_file_name_template):
    # Define file paths
    candidates_file_path = os.path.join(export_data_folder, 'Candidates_001.csv')
    notes_file_path = os.path.join(export_data_folder, 'Notes_001.csv')
    educational_details_file_path = os.path.join(export_data_folder, 'Candidates_Educational_Details.csv')

    # Load the candidates, notes, and educational details data
    candidates_df = pd.read_csv(candidates_file_path)
    notes_df = pd.read_csv(notes_file_path)
    educational_details_df = pd.read_csv(educational_details_file_path)

    # Ensure 'Middle Name' column exists in candidates_df
    if 'Middle Name' not in candidates_df.columns:
        candidates_df['Middle Name'] = ''
    # Ensure 'Gender' column exists in candidates_df with default values if not present
    if 'Gender' not in candidates_df.columns:
        candidates_df['Gender'] = ''  # Default value for 'Gender'


    # Convert and sort notes 'Created Time'
    notes_df['Created Time'] = pd.to_datetime(notes_df['Created Time'], format='%d.%m.%Y %I:%M %p')
    notes_df = notes_df.sort_values(by='Created Time', ascending=False)

    # Format and aggregate notes
    notes_df['Formatted Note'] = notes_df.apply(lambda row: f"<b>Created Time:</b> {row['Created Time']}\n<br><b>Job Opening Name:</b> {row['Job Opening Name']}\n<br><b>Comment:</b> {row['Note Content']}\n<br>-----\n<br>", axis=1)
    aggregated_notes = notes_df.groupby('Parent ID')['Formatted Note'].apply(lambda x: '\n<br>'.join(x)).reset_index()

    # Merge notes with candidates
    merged_df = pd.merge(candidates_df, aggregated_notes, left_on='Candidate Id', right_on='Parent ID', how='left')
    merged_df['Formatted Note'].fillna('', inplace=True)

    # Format and aggregate educational details
    educational_details_df['Formatted Education'] = educational_details_df.apply(lambda row: f"{row['Institute / School']}, {row['Major / Department']}, {row['Degree']}, {row['Duration_From']}, {row['Duration_To']}{', Currently pursuing' if row['Currently pursuing'] else ''}", axis=1)
    aggregated_education = educational_details_df.groupby('Candidate Id')['Formatted Education'].apply(lambda x: '\n<br>'.join(x)).reset_index()

    # Merge educational details with merged_df
    merged_df = pd.merge(merged_df, aggregated_education, on='Candidate Id', how='left')
    merged_df['Formatted Education'].fillna('', inplace=True)

    # Add additional info and education to 'Comment'
    def add_additional_info_to_comment(row):
        additional_info = f"<b>Experience in Years:</b> {row.get('Experience in Years', '')} \n <br> <b>Additional Info:</b> {row.get('Additional Info', '')}  \n <br> <b>Created Time:</b> {row.get('Created Time', '')}  \n <br> <b>Last Activity Time:</b> {row.get('Last Activity Time', '')}  \n <br> <b>Source:</b> {row.get('Source', '')}  \n <br> <b>English level:</b> {row.get('English level', '')}  \n <br> <b>Telegram:</b> {row.get('Telegram', '')}  \n <br> <b>Education:</b> <br> {row.get('Formatted Education', '')}  \n <br> -----  \n <br>"
        return additional_info + row.get('Formatted Note', '')

    
    merged_df['Comment'] = merged_df.apply(add_additional_info_to_comment, axis=1)

    # Handle combined fields
    merged_df['Phone'] = merged_df[['Phone', 'Mobile']].apply(lambda x: ' / '.join(x.dropna().astype(str)), axis=1)
    merged_df['Skype'] = merged_df[['Skype ID', 'Skype']].apply(lambda x: ' / '.join(x.dropna().astype(str)), axis=1)
    merged_df['Salary'] = merged_df[['Desired Salary', 'Expected Salary']].apply(lambda x: ' / '.join(x.dropna().astype(str)), axis=1)

   # Handle potential duplicate 'Currency' columns
    currency_columns = [col for col in merged_df.columns if 'Currency' in col]
    if len(currency_columns) > 1:
        # If there are multiple 'Currency' columns, keep only the desired one and drop the others
        # Adjust this logic based on your specific needs
        merged_df.drop(columns=[col for col in currency_columns if col != 'Currency of salary'], inplace=True)
 

    # Define the final columns mapping and prepare the final DataFrame
    final_columns_mapping = {
        'First Name': 'First Name',
        'Middle Name': 'Middle Name',
        'Last Name': 'Last Name',
        'Desired position': 'Desired Position',
        'Current Job Title': 'Current Position',
        'Current Employer': 'Current Company',
        'Date of Birth': 'Date Of Birth',
        'Gender': 'Gender',
        'Country': 'Country',
        'City': 'City',
        'Candidate Status': 'Status',
        'Phone': 'Phone',
        'Email': 'Email',
        'Skype': 'Skype',
        'Linkedin': 'LinkedIn',
        'Salary': 'Salary',
        'Currency of salary': 'Currency',
        'Skill Set': 'Skills',
        'Comment': 'Comment'
    }
    final_df = merged_df.rename(columns=final_columns_mapping)[list(final_columns_mapping.values())]

    # Export the final DataFrame to an Excel file (.xlsx)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file_name = output_file_name_template.format(timestamp=timestamp)
    final_df.to_excel(output_file_name, index=False)

    print(f"Output file created: {output_file_name}")

if __name__ == "__main__":
    export_data_folder = 'ExportData'
    output_file_name_template = 'final_candidates_with_notes_{timestamp}.xlsx'
    process_candidates_and_notes(export_data_folder, output_file_name_template)
