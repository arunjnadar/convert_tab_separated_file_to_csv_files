import os
import numpy as np
import pandas as pd
from dateutil import parser

class ConvertTabSeparatedToCSVFile:
    """A class that converts tab separated files into CSV Files"""

    def convert_tab_separated_to_csv_file(self, tag_prefix, input_file_location_and_name, output_folder):
        """Function that converts tab separated file"""

        # Read file content
        file_content_df = pd.read_table(input_file_location_and_name, index_col='Timestamp')

        # Get the index of data frame
        df_timestamps = file_content_df.index

        # get start time and end time from df_timestamps
        start_time = parser.parse(df_timestamps[0])
        end_time = parser.parse(df_timestamps[-1])
        formatted_start_time = "{0}{1}{2}{3}{4}{5}".format(start_time.year,f"{start_time:%m}",f"{start_time:%d}",start_time.hour, start_time.minute,start_time.second)
        formatted_end_time = "{0}{1}{2}{3}{4}{5}".format(end_time.year,f'{end_time:%m}',f'{end_time:%d}',end_time.hour, end_time.minute,end_time.second)

        # get the data frame columns
        df_columns = file_content_df.columns

        for df_column in df_columns:
            # Get values from data frame for this particular column
            df_column_values = file_content_df[df_column]

            # list to hold the values that should be added to file
            list_to_hold_values = []

            # File name to store values
            df_column_file_name = df_column + "_ST_" + formatted_start_time + "_ET_" + formatted_end_time + ".csv"

            # file location and name to store values
            file_location_and_name_to_store_values = os.path.join(output_folder, df_column_file_name)

            # Iterate through df_timestamps and df_column_values
            for time_stamp, df_value in zip(df_timestamps, df_column_values):
                
                # Remove comma from df value
                df_value_without_comma = str(df_value).replace(',', '')

                #print ("{0},{1},{2}".format(df_column, time_stamp, df_value_without_comma))

                # Variable to hold values that should be added to list
                values_to_be_added_to_list = "{0}{1},{2},{3}\n".format(tag_prefix, df_column,time_stamp,df_value_without_comma)

                # add the values to list list_to_hold_values
                list_to_hold_values.append(values_to_be_added_to_list)

            #print (list_to_hold_values)

            print ("Creating file {0}...".format(df_column_file_name))

            # Create a file object
            with open(file_location_and_name_to_store_values, 'w') as f_obj:
                for line_in_list in list_to_hold_values:
                    f_obj.write(line_in_list)
    
    # Function to rename file
    def rename_file(self, old_file_location_and_name, folder_location_and_name):
        """Function to rename file"""
        
        # Get the folder path and file name
        folder_path, file_name = os.path.split(old_file_location_and_name)

        # Get the base name and file extension
        file_name_without_extension, file_extension = os.path.splitext(file_name)

        # New file name
        new_file_name = file_name_without_extension + ".DONE"
        new_file_location_and_name = os.path.join(folder_location_and_name, new_file_name)
        
        # Rename the file to extension .Done
        os.replace(old_file_location_and_name, new_file_location_and_name)

    # Main function
    def main(self):
        """Function that does the main work"""
        # Clear the screen
        if(os.name == 'posix'):
            os.system('clear')
        # else screen will be cleared for windows
        else:
            os.system('cls')

        # variable to store the tag prefix
        tag_prefix = "jana_"

        # Specify the input file extension
        input_file_extension = '.txt'

        # Get current working directory
        current_working_directory = os.getcwd()

        # Name of folder that contains the input files
        input_files_folder_name = 'input_files'
        
        # Input files location and name
        input_files_folder_location_and_name = os.path.join(current_working_directory, input_files_folder_name)

        # Name of folder to store the output files
        output_files_folder_name = 'output_files'
        output_files_folder_location_and_name = os.path.join(current_working_directory, output_files_folder_name)

        # check if output folder exists and if not then create it
        output_folder_exists = os.path.isdir(output_files_folder_location_and_name)
        if (not output_folder_exists):
            try:
                os.mkdir(output_files_folder_location_and_name)
            except OSError:
                print ("Could not create folder {0}. Please check.".format(output_files_folder_location_and_name))

        # Output files location and name
        list_of_files = os.listdir(input_files_folder_location_and_name)

        # List to hold files that has the extension specified in variable input_file_extension
        list_of_files_that_has_specified_extension = []

        for file_in_folder in list_of_files:
            
            if (file_in_folder.endswith(input_file_extension)):

                # Add it to list variable list_of_files_that_has_specified_extension
                list_of_files_that_has_specified_extension.append(file_in_folder)
        
        # Check if the list list_of_files_that_has_specified_extension contains any file
        if (len(list_of_files_that_has_specified_extension) > 0):
            # Iterate through the list
            for file_in_list in list_of_files_that_has_specified_extension:

                # Create the path that contains the file
                file_location_and_name = os.path.join(input_files_folder_location_and_name, file_in_folder)

                # call function convert_tab_separated_to_csv_file to read the tab separated file
                self.convert_tab_separated_to_csv_file(tag_prefix=tag_prefix, input_file_location_and_name=file_location_and_name, output_folder=output_files_folder_location_and_name)

                # rename file to .Done in output_files folder by calling function rename_file
                self.rename_file(old_file_location_and_name=file_location_and_name, folder_location_and_name=input_files_folder_location_and_name)
        else:
            print ("Found no file that has extension {0} in folder {1}. Please check.".format(input_file_extension, input_files_folder_location_and_name))
            

# Make an instance of class ConvertTabSeparatedToCSVFile
ctstcsvf_instance = ConvertTabSeparatedToCSVFile()
ctstcsvf_instance.main()