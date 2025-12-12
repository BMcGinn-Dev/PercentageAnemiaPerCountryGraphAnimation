import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Initialize empty dataframe
clean_anemia_df = pd.DataFrame()

# File path to interpolated data source
file_path = 'DataSources/Interpolated_Data_Anemia.csv'

# Attempt to read in the file
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

# Get unique years from the data
unique_years = sorted(clean_anemia_df["TIME_PERIOD"].unique())

# Calculate global min/max for consistent scaling
global_max = clean_anemia_df["OBS_VALUE"].max()
global_min = clean_anemia_df["OBS_VALUE"].min()

# Create a persistent color mapping for all countries
all_countries = clean_anemia_df["REF_AREA_LABEL"].unique()
color_palette = plt.cm.tab20(np.linspace(0, 1, len(all_countries)))
country_colors = dict(zip(all_countries, color_palette))

# Create figure and axes
fig, ax = plt.subplots(figsize=(14, 8))


def update(frame_number):
    """Update function for each animation frame"""
    ax.clear()

    # Get current year
    current_year = unique_years[frame_number]

    # Filter data for current year & get top 10
    current_year_data = clean_anemia_df[clean_anemia_df["TIME_PERIOD"] == current_year]
    top_10_countries = current_year_data.nlargest(10, "OBS_VALUE").copy()

    # Sort by percentage ascending (for bottom-to-top display)
    top_10_countries = top_10_countries.sort_values(by="OBS_VALUE", ascending=True)

    # Get colors for each country
    colors = [country_colors[country] for country in top_10_countries["REF_AREA_LABEL"]]

    # Create horizontal bar chart
    bars = ax.barh(
        top_10_countries["REF_AREA_LABEL"],
        top_10_countries["OBS_VALUE"],
        color=colors,
        edgecolor='white',
        linewidth=0.7
    )

    # Customize the plot
    ax.set_xlabel('Anemic Percentage (%)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Country', fontsize=13, fontweight='bold')
    ax.set_title(
        f'Top 10 Countries by Anemic Percentage - Year {current_year}',
        fontsize=18,
        fontweight='bold',
        pad=20
    )

    # Set consistent x-axis limits
    ax.set_xlim(max(0, global_min * 0.9), global_max * 1.1)

    # Add value labels on bars
    for i, (country, percentage) in enumerate(zip(
            top_10_countries["REF_AREA_LABEL"],
            top_10_countries["OBS_VALUE"]
    )):
        ax.text(
            percentage + (global_max * 0.01),
            i,
            f'{percentage:.1f}%',
            va='center',
            ha='left',
            fontsize=11,
            fontweight='bold',
            color='black'
        )

    # Add grid
    ax.grid(axis='x', linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)

    plt.tight_layout()


# Create the animation - simple, just cycle through years
anim = animation.FuncAnimation(
    fig,
    update,
    frames=len(unique_years),
    interval=25,  # 200ms per year = 5 years per second
    repeat=True,
    blit=False
)

# Display the animation
plt.show()

# Optional: Save the animation
# anim.save('anemia_animation.mp4', writer='ffmpeg', fps=5, dpi=150)
# anim.save('anemia_animation.gif', writer='pillow', fps=5, dpi=100)