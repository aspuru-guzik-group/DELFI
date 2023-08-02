import streamlit as st
import pandas as pd

def calculate_partial_score(df):
    # (overlap - (deltaEn/2) - (deltaTDM)/3) * 20
    df["Partial Score"] = (df['Overlap'] - (df['(Delta)En.'] / 2) - (df['(Delta)TDM'] / 3)) * 20
    return df

def update_df(num_rows):
    df_copy = st.session_state["df"].copy()

    df_copy = calculate_partial_score(df_copy)

    num_rows = num_rows - len(df_copy)

    if num_rows > 0:
        new_df = pd.DataFrame({
            'Overlap': [0.0] * num_rows,
            '(Delta)En.': [0.0] * num_rows,
            '(Delta)TDM': [0.0] * num_rows,
        },
            index=[f'S_{len(df_copy) + i + 1}' for i in range(num_rows)]
        )
        df_copy = pd.concat([df_copy, new_df])

    elif num_rows < 0:
        df_copy = df_copy[:num_rows]

    st.session_state["df"] = df_copy

def render():
    st.title("Partial Score Calculator")
    st.image("img/Fig1.png")

    if 'df' not in st.session_state:
        data = {
            'Overlap': [0.0],
            '(Delta)En.': [0.0],
            '(Delta)TDM': [0.0],
            "Partial Score": None
        }

        st.session_state["df"] = pd.DataFrame(data, index=['S_1'])

    num_rows = st.number_input("Number of Rows", min_value=1, value=len(st.session_state['df']), step=1)

    row1, row2, row3 = st.empty(), st.empty(), st.empty()

    with row3:
        if st.button("Update"):
            update_df(num_rows)

    with row2:
        st.write("Total Score: ", st.session_state["df"]["Partial Score"].sum())
    
    with row1:
        st.session_state["df"] = st.data_editor(st.session_state["df"])

if __name__ == "__main__":
    render()
