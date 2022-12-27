from abc import ABC, abstractmethod
import pandas as pd
from datasets import *


#creating abstract interface
class DatasetReader(ABC):
    
    ''' Interface for generic dataset reader. Defines the signature for two methods required for checking the file format and parsing the file '''
    
    
    @abstractmethod 
    def check_format(filename)-> bool:
        '''Takes a file as argument
            returns True if the file format is compatible with the reader, False otherwise''' 
        pass
    
   
    @abstractmethod
    def read(filename) -> Dataset:
        '''Takes a file as argument
            returns a Dataset object enclosing the dataFrame obtained by parsing the file'''
        pass
      
    
    
  
    
class GffReader(DatasetReader):
    ''' a DatasetReader realization that is specific for gff3 format files.
        Defines the inherited abstract methods in accordance to gff3 format specific features. '''
    
    @staticmethod
    def check_format(filename)-> bool:
        ''' static method, takes a file as argument.
            Assumes the file format specifcation are found in the first line of the file.
            Checks the format and returns True if the format == gff3 and False otherwise '''
        
        with open(filename, "r") as gff3_file:
            file_format= gff3_file.readline()
            if "gff-version   3" in file_format:
                return True
            else: return False
            
            

    @staticmethod
    def read(filename) -> Dataset:
        ''' Static method. Takes a file as an input, checks if it is a .gff3 file. Creates a pd.DataFrame object by parsing the file.
            Assumes that all lines starting with "#" are comment lines and skips them.
            returns a GffDataset object containing the DataFrame.'''
    
        # Initialize an empty list for the rows 
        rows = []
        # open GFF3 file
        with open(filename, 'r') as gff3_file:
         
            #check format
            if GffReader.check_format(filename):
                
                #iterate over the lines 
                for line in gff3_file:
                    
                    # Skip comment lines 
                    if line[0]=='#':  continue
                    
                    
                    # Split the line into separate columns 
                    cols = line.strip().split('\t')
                    

                    # Add the feature
                    rows.append(cols)
                    
                # Create DataFrame
                df = pd.DataFrame(rows, columns=["SeqID", "Source", "Type", "Start", "End", "Score", "Strand", "Phase", "Attributes"])
                
                    
                # Cast to category
                df["Start"]= pd.to_numeric(df["End"], errors="ignore").astype("int64")
                df["End"]= pd.to_numeric(df["End"], errors="ignore").astype("int64")
                df["Score"]= pd.to_numeric(df["Score"], errors="coerce").astype("float64")
                
                
                return GffDataset(df)
            else:
                raise ValueError ("Can't parse files other than GFF")

         
data= GffReader.read("data.gff3")


            