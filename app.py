import streamlit as st
import content.scoring_system as scoring_system
import content.run_model as run_model
import content.understand_scoring_system as understand_scoring_system

def main():
    st.set_page_config(page_title="DELFI", page_icon=":dolphin:")

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ("Scoring System applied to QM8", "Run DELFI on SMILES or CSV", "Analysis of your scores", "Understand the Scoring System"))

    if page == "Scoring System applied to QM8":
        scoring_system.render(upload_csv=False)

    elif page == "Run DELFI on SMILES or CSV":  
        run_model.render()

    elif page == "Analysis of your scores":
        scoring_system.render(upload_csv=True)

    elif page == "Understand the Scoring System":
        understand_scoring_system.render()

if __name__ == "__main__":
    main()
