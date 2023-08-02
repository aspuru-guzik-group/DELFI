import streamlit as st
import pandas as pd

def update_df(num_rows):
    # (overlap - (deltaEn/2) - (deltaTDM)/3) )*20
    for i in range(len(st.session_state["df"])):
        st.session_state["df"].iloc[i]["Partial Score"] = (st.session_state["df"].iloc[i]['Overlap'] - (st.session_state["df"].iloc[i]['(Delta)En.'] / 2) - (st.session_state["df"].iloc[i]['(Delta)TDM'] / 3))*20

    num_rows = num_rows - len(st.session_state["df"])

    if num_rows > 0:
        new_df = pd.DataFrame({
                'Overlap': [0.0] * num_rows,
                '(Delta)En.': [0.0] * num_rows,
                '(Delta)TDM': [0.0] * num_rows,
                'Partial Score': [0.0] * num_rows,
            }, 
            index=[f'S_{len(st.session_state["df"]) + i + 1}' for i in range(num_rows)]
        )
        st.session_state["df"] = pd.concat([st.session_state["df"], new_df])
    
    elif num_rows < 0:
        st.session_state["df"] = st.session_state["df"][:num_rows]

    

    print(st.session_state["df"])



def render():
    st.title("Partial Score Calculator")

    st.image("img/Fig1.png")

    

    if 'df' not in st.session_state:
        data = {
            'Overlap': [0.0] ,
            '(Delta)En.': [0.0] ,
            '(Delta)TDM': [0.0] ,
            'Partial Score': [0.0] ,
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
