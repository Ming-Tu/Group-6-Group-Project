import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

class DataManager:
    def __init__(self, tabdb_path, playdb_path, requestdb_path):
        """
        Initializes the DataManager with paths to the CSV files.
        
        Args:
            tabdb_path (str): Path to the tabdb CSV file.
            playdb_path (str): Path to the playdb CSV file.
            requestdb_path (str): Path to the requestdb CSV file.
        """
        self.tabdb_path = tabdb_path
        self.playdb_path = playdb_path
        self.requestdb_path = requestdb_path
        
        self.tabdb = None
        self.playdb = None
        self.requestdb = None
    
    def load_data(self):
        """
        Loads data from the provided CSV files into Pandas DataFrames.
        Performs basic validation to ensure the data is correct.
        """
        try:
            # Load tabdb.csv
            self.tabdb = pd.read_csv(self.tabdb_path)
            self._validate_tabdb()
            print("tabdb.csv loaded successfully.")
            
            # Load playdb.csv
            self.playdb = pd.read_csv(self.playdb_path)
            self._validate_playdb()
            print("playdb.csv loaded successfully.")
            
            # Load requestdb.csv
            self.requestdb = pd.read_csv(self.requestdb_path)
            self._validate_requestdb()
            print("requestdb.csv loaded successfully.")
            
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except pd.errors.EmptyDataError:
            print("Error: One or more files are empty.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def _validate_tabdb(self):
        """
        Validates the tabdb DataFrame to ensure it contains the required columns and correct data types.
        """
        required_columns = ["song", "artist", "year", "type", "gender", "duration", "language", "tabber", "source", "date", "difficulty", "special books"]
        
        # Check if all required columns are present
        for column in required_columns:
            if column not in self.tabdb.columns:
                raise ValueError(f"Missing required column in tabdb.csv: {column}")
        
        # Validate data types
        if not np.issubdtype(self.tabdb["year"].dtype, np.number):
            raise ValueError("Column 'year' must be numeric in tabdb.csv.")
        if not np.issubdtype(self.tabdb["difficulty"].dtype, np.number):
            raise ValueError("Column 'difficulty' must be numeric in tabdb.csv.")
        
        # Handle missing values
        self.tabdb.fillna("Unknown", inplace=True)

    def _validate_playdb(self):
        """
        Validates the playdb DataFrame to ensure it contains the required columns.
        """
        required_columns = ["song", "artist"]
        
        # Check if all required columns are present
        for column in required_columns:
            if column not in self.playdb.columns:
                raise ValueError(f"Missing required column in playdb.csv: {column}")
        
        # Handle missing values
        self.playdb.fillna("", inplace=True)

    def _validate_requestdb(self):
        """
        Validates the requestdb DataFrame to ensure it contains the required columns.
        """
        required_columns = ["song", "artist"]
        
        # Check if all required columns are present
        for column in required_columns:
            if column not in self.requestdb.columns:
                raise ValueError(f"Missing required column in requestdb.csv: {column}")
        
        # Handle missing values
        self.requestdb.fillna("", inplace=True)

class QueryManager:
    def __init__(self, data_manager):
        """
        Initializes the QueryManager with a reference to the DataManager.
        
        Args:
            data_manager (DataManager): An instance of DataManager containing the loaded data.
        """
        self.data_manager = data_manager
    
    def filter_tabdb(self, **filters):
        """
        Filters the tabdb DataFrame based on the provided criteria.
        
        Args:
            **filters: Arbitrary keyword arguments representing columns and their desired values to filter by.
        
        Returns:
            DataFrame: A filtered Pandas DataFrame.
        """
        df = self.data_manager.tabdb
        if df is None:
            raise ValueError("Data has not been loaded. Please load the data using DataManager first.")
        
        for column, value in filters.items():
            if column in df.columns:
                df = df[df[column] == value]
            else:
                raise ValueError(f"Column '{column}' does not exist in tabdb.")
        
        return df
    
    def filter_by_date_range(self, start_date, end_date):
        """
        Filters the tabdb DataFrame by a range of dates.
        
        Args:
            start_date (str): The start date in 'YYYY-MM-DD' format.
            end_date (str): The end date in 'YYYY-MM-DD' format.
        
        Returns:
            DataFrame: A filtered Pandas DataFrame with rows that fall within the specified date range.
        """
        df = self.data_manager.tabdb
        if df is None:
            raise ValueError("Data has not been loaded. Please load the data using DataManager first.")
        
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        mask = (df['date'] >= start_date) & (df['date'] <= end_date)
        return df.loc[mask]
    
    def filter_playdb_by_song(self, song_title):
        """
        Filters the playdb DataFrame for a specific song title.
        
        Args:
            song_title (str): The title of the song to filter by.
        
        Returns:
            DataFrame: A filtered Pandas DataFrame containing only rows that match the song title.
        """
        df = self.data_manager.playdb
        if df is None:
            raise ValueError("Data has not been loaded. Please load the data using DataManager first.")
        
        return df[df['song'] == song_title]
    
    def filter_requestdb_by_artist(self, artist_name):
        """
        Filters the requestdb DataFrame for a specific artist name.
        
        Args:
            artist_name (str): The name of the artist to filter by.
        
        Returns:
            DataFrame: A filtered Pandas DataFrame containing only rows that match the artist name.
        """
        df = self.data_manager.requestdb
        if df is None:
            raise ValueError("Data has not been loaded. Please load the data using DataManager first.")
        
        return df[df['artist'] == artist_name]

    def count_song_plays(self, song_title):
        """
        Counts the number of times a song was played based on the playdb DataFrame.
        
        Args:
            song_title (str): The title of the song to count.
        
        Returns:
            int: The count of times the song was played.
        """
        df = self.data_manager.playdb
        if df is None:
            raise ValueError("Data has not been loaded. Please load the data using DataManager first.")
        
        return df[song_title].count()

class PlotManager:
    def __init__(self, data_manager):
        """
        Initializes the PlotManager with a reference to the DataManager.
        
        Args:
            data_manager (DataManager): An instance of DataManager containing the loaded data.
        """
        self.data_manager = data_manager
    
    def plot_difficulty_histogram(self):
        """
        Generates a histogram of the songs by difficulty level.
        """
        df = self.data_manager.tabdb
        if df is None:
            raise ValueError("Data has not been loaded. Please load the data using DataManager first.")
        
        df['difficulty'].plot(kind='hist', bins=5, edgecolor='black', title='Histogram of Songs by Difficulty Level')
        plt.xlabel('Difficulty Level')
        plt.ylabel('Frequency')
        plt.show()
    
    def plot_duration_histogram(self):
        """
        Generates a histogram of the songs by duration.
        """
        df = self.data_manager.tabdb
        if df is None:
            raise ValueError("Data has not been loaded. Please load the data using DataManager first.")
        
        df['duration'].plot(kind='hist', bins=10, edgecolor='black', title='Histogram of Songs by Duration')
        plt.xlabel('Duration (minutes)')
        plt.ylabel('Frequency')
        plt.show()
    
    def plot_language_bar_chart(self):
        """
        Generates a bar chart of the songs by language.
        """
        df = self.data_manager.tabdb
        if df is None:
            raise ValueError("Data has not been loaded. Please load the data using DataManager first.")
        
        df['language'].value_counts().plot(kind='bar', title='Bar Chart of Songs by Language')
        plt.xlabel('Language')
        plt.ylabel('Number of Songs')
        plt.show()
    
    def plot_source_bar_chart(self):
        """
        Generates a bar chart of the songs by source.
        """
        df = self.data_manager.tabdb
        if df is None:
            raise ValueError("Data has not been loaded. Please load the data using DataManager first.")
        
        df['source'].value_counts().plot(kind='bar', title='Bar Chart of Songs by Source')
        plt.xlabel('Source')
        plt.ylabel('Number of Songs')
        plt.show()
    
    def plot_bar_chart_by_decade(self):
        """
        Generates a bar chart of the songs by decade.
        """
        df = self.data_manager.tabdb
        if df is None:
            raise ValueError("Data has not been loaded. Please load the data using DataManager first.")
        
        df['year'] = pd.to_numeric(df['year'], errors='coerce')
        df['decade'] = (df['year'] // 10) * 10
        df['decade'].value_counts().sort_index().plot(kind='bar', title='Bar Chart of Songs by Decade')
        plt.xlabel('Decade')
        plt.ylabel('Number of Songs')
        plt.show()
    
    def plot_cumulative_line_chart(self):
        """
        Generates a cumulative line chart of the number of songs played each Tuesday.
        """
        df = self.data_manager.playdb
        if df is None:
            raise ValueError("Data has not been loaded. Please load the data using DataManager first.")
        
        cumulative_play_count = df.drop(columns=['song', 'artist']).count(axis=0).cumsum()
        cumulative_play_count.plot(kind='line', title='Cumulative Line Chart of Songs Played Each Tuesday')
        plt.xlabel('Date')
        plt.ylabel('Cumulative Songs Played')
        plt.show()
    
    def plot_pie_chart_by_gender(self):
        """
        Generates a pie chart of the songs by gender of the lead vocalist.
        """
        df = self.data_manager.tabdb
        if df is None:
            raise ValueError("Data has not been loaded. Please load the data using DataManager first.")
        
        df['gender'].value_counts().plot(kind='pie', autopct='%1.1f%%', title='Pie Chart of Songs by Gender')
        plt.ylabel('')
        plt.show()

class UserInterface:
    def __init__(self, data_manager, query_manager, plot_manager):
        """
        Initializes the UserInterface with references to DataManager, QueryManager, and PlotManager.
        
        Args:
            data_manager (DataManager): An instance of DataManager.
            query_manager (QueryManager): An instance of QueryManager.
            plot_manager (PlotManager): An instance of PlotManager.
        """
        self.data_manager = data_manager
        self.query_manager = query_manager
        self.plot_manager = plot_manager
        self.root = tk.Tk()
        self.root.title("Ukulele Tuesday Data Analysis")
        
        self.create_widgets()
        self.root.mainloop()
    
    def create_widgets(self):
        """
        Create the UI widgets for user interaction.
        """
        load_button = tk.Button(self.root, text="Load Data", command=self.load_data)
        load_button.pack(pady=5)
        
        filter_button = tk.Button(self.root, text="Filter Data", command=self.filter_data)
        filter_button.pack(pady=5)
        
        plot_button = tk.Button(self.root, text="Plot Data", command=self.plot_data)
        plot_button.pack(pady=5)
    
    def load_data(self):
        """
        Load data using the DataManager.
        """
        try:
            self.data_manager.load_data()
            messagebox.showinfo("Info", "Data loaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def filter_data(self):
        """
        Filter data based on user input.
        """
        try:
            column = simpledialog.askstring("Input", "Enter the column to filter by (e.g., 'artist'): ")
            value = simpledialog.askstring("Input", f"Enter the value to filter '{column}' by: ")
            if column and value:
                filtered_df = self.query_manager.filter_tabdb(**{column: value})
                self.display_dataframe(filtered_df)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def plot_data(self):
        """
        Generate plots based on user selection.
        """
        try:
            plot_options = [
                "Difficulty Histogram",
                "Duration Histogram",
                "Language Bar Chart",
                "Source Bar Chart",
                "Decade Bar Chart",
                "Cumulative Line Chart",
                "Gender Pie Chart"
            ]
            selected_plot = simpledialog.askstring("Input", f"Enter plot type: {', '.join(plot_options)}")
            if selected_plot == "Difficulty Histogram":
                self.plot_manager.plot_difficulty_histogram()
            elif selected_plot == "Duration Histogram":
                self.plot_manager.plot_duration_histogram()
            elif selected_plot == "Language Bar Chart":
                self.plot_manager.plot_language_bar_chart()
            elif selected_plot == "Source Bar Chart":
                self.plot_manager.plot_source_bar_chart()
            elif selected_plot == "Decade Bar Chart":
                self.plot_manager.plot_bar_chart_by_decade()
            elif selected_plot == "Cumulative Line Chart":
                self.plot_manager.plot_cumulative_line_chart()
            elif selected_plot == "Gender Pie Chart":
                self.plot_manager.plot_pie_chart_by_gender()
            else:
                messagebox.showwarning("Warning", "Invalid plot type selected.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def display_dataframe(self, df):
        """
        Display the filtered DataFrame in a new window.
        
        Args:
            df (DataFrame): The DataFrame to be displayed.
        """
        if df is not None and not df.empty:
            window = tk.Toplevel(self.root)
            window.title("Filtered Data")
            frame = ttk.Frame(window)
            frame.pack(fill=tk.BOTH, expand=True)
            tree = ttk.Treeview(frame)
            tree.pack(fill=tk.BOTH, expand=True)
            
            tree["columns"] = list(df.columns)
            for column in df.columns:
                tree.heading(column, text=column)
                tree.column(column, anchor="w")
            
            for _, row in df.iterrows():
                tree.insert("", "end", values=list(row))
        else:
            messagebox.showinfo("Info", "No data available for the selected filter.")

# Example usage
data_manager = DataManager('tabdb.csv', 'playdb.csv', 'requestdb.csv')
query_manager = QueryManager(data_manager)
plot_manager = PlotManager(data_manager)
user_interface = UserInterface(data_manager, query_manager, plot_manager)
