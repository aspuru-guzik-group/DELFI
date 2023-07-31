import seaborn as sns
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap



bar_color = "#1F0C48"
bar_outline = "#7E317B"
background_color = "#FDF5E6"
colormap = LinearSegmentedColormap.from_list('custom_colormap', list(zip([0, 0.5, 1], ["#1F0C48","#E74A76","#FF9242"])))
plt.rcdefaults()
plt.rcParams.update({
        'figure.facecolor': background_color,
        'figure.edgecolor': background_color,
        'axes.facecolor': background_color,
        'font.family': 'monospace',
        'text.color': bar_color,
        'xtick.color': bar_color,
        'ytick.color': bar_color,
    })

def filter_numeric_columns(df, columns):
    return [column for column in columns if pd.api.types.is_numeric_dtype(df[column])]



def visualize_heatmap(df, columns):
    st.subheader("Heatmap")
    plt.figure(figsize=(10, 6))
    heatmap_df = df[columns].corr()
    sns.heatmap(heatmap_df, annot=True, cmap=colormap, fmt=".2f", linewidths=0.5, vmin=0, vmax=1)
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    st.pyplot(plt)
    st.write("---")


def visualize_histogram(df, columns):
    st.subheader("Histogram")
    for column in columns:
        st.write(f"### {column} Distribution")
        plt.figure(figsize=(8, 6))
        plt.hist(df[column], bins="auto", alpha=0.7, color=bar_color, ec=bar_outline)
        plt.xlabel("Score", color=bar_outline)
        plt.ylabel("Count", color=bar_outline)
        plt.tight_layout()
        st.pyplot(plt)
        st.write("---")

def visualize_filtered_histogram(df, threshold=0):
    st.subheader("Filtered Histogram")
    counts = []
    columns = df.columns[3:]
    for column in columns:
        filtered_data = df[df[column] > threshold][column]
        counts.append(len(filtered_data))

    plt.figure(figsize=(8, 6))
    plt.bar(columns, counts, color=bar_color, edgecolor=bar_outline)
    plt.xlabel("Columns", color=bar_outline)
    plt.ylabel("Count", color=bar_outline)
    plt.xticks(rotation=55, ha='right')  # Rotate the tick labels by 45 degrees
    plt.tight_layout()
    st.pyplot(plt)
    st.write("---")