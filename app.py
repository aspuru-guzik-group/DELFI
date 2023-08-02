import streamlit as st
import content.scoring_system as scoring_system
import content.run_model as run_model
import content.understand_scoring_system as understand_scoring_system

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ("Scoring System", "Run DELFI on SMILES or CSV", "Score your own SMILES data", "Understand the Scoring System"))

    if page == "Scoring System":
        scoring_system.render(upload_csv=False)

    elif page == "Run DELFI on SMILES or CSV":  
        run_model.render()

    elif page == "Score your own SMILES data":
        scoring_system.render(upload_csv=True)

    elif page == "Understand the Scoring System":
        understand_scoring_system.render()

if __name__ == "__main__":
    main()
