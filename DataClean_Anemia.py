import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


# Initializing empty dataframe
clean_anemia_df = pd.DataFrame()

# File path to the data source
file_path = 'DataSources/Clean_Data_Anemia.csv'

# Attempting to read in the file
try:
    clean_anemia_df = pd.read_csv(file_path)
    print("Data Source Found.")
    print('*' * 50)

except FileNotFoundError:
    print("Error: The data source file was not found. Check the path and filename.")
except pd.errors.EmptyDataError:
    print("Error: The file exists but is empty.")
except Exception as e:
    print(f"An unexpected error occurred while reading the file: {e}")

# Print out column names
# print(clean_anemia_df.columns)

# Print out the head of the dataframe
# print(clean_anemia_df.head())

# ____________________________________________________________________________________________________________________
# Beginning Horizontal Bar Chart creation

# Get unique years from the data
unique_years = sorted(clean_anemia_df["TIME_PERIOD"].unique())

# Create figure and axes
fig, ax = plt.subplots(figsize=(12, 8))

# Define colors for bars
bar_colors = plt.cm.Reds(np.linspace(0.4, 0.8, len(unique_years)))

def update(frame):
    # Clear the axes --> This is how it repeats for each year
    ax.clear()

    # Get current year
    current_year = unique_years[frame]

    # Filter data for current year & create new dataframe 'top_10_countries'
    current_year_data = clean_anemia_df[clean_anemia_df["TIME_PERIOD"] == current_year]
    top_10_countries = current_year_data.nlargest(10, "OBS_VALUE")

    # Sort by percentage ascending
    top_10_countries = top_10_countries.sort_values(by="OBS_VALUE", ascending=True)

    # Create horizontal bar chart
    bars = ax.barh(top_10_countries["REF_AREA_LABEL"], top_10_countries["OBS_VALUE"], color=bar_colors)

    # Customize the plot
    ax.set_xlabel('Anemic Percentage (%)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Country', fontsize=12, fontweight='bold')
    ax.set_title(f'Top 10 Countries by Anemic Percentage - Year {current_year}', fontsize=16, fontweight='bold', pad=20)

    # Set consistent x-axis limits (adjust based on data range)
    max_value = top_10_countries["OBS_VALUE"].max()
    ax.set_xlim(5, max_value * 1.1)

    # Add value labels on bars
    for i, (country, percentage) in enumerate(zip(top_10_countries["REF_AREA_LABEL"], top_10_countries["OBS_VALUE"])):
        ax.text(percentage + 0.5, i, f'{percentage:.1f}%', va='center', ha='left', fontsize=10, fontweight='bold', color='black')

    # Add a grid for better readability
    ax.grid(axis='x', linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)

    # Adjust layout to prevent clipping of tick-labels
    plt.tight_layout()

#_____________________________________________________________________________________________________________________
# Create the animation
# interval:  500 milliseconds between frames (500 = .5 second per year)
# repeat: whether to loop the animation
anim = animation.FuncAnimation(
    fig,
    update,
    frames=len(unique_years),
    interval=500,
    repeat=True
)

# Display the animation
plt.show()

# Optional: Save the animation as MP4 (requires ffmpeg)
# anim.save('anemia_animation.mp4', writer='ffmpeg', fps=1, dpi=100)

# Optional: Save as GIF (requires pillow)
# anim.save('anemia_animation.gif', writer='pillow', fps=1)