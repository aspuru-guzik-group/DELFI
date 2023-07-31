import streamlit as st
import content.scoring_system as scoring_system
import content.run_model as run_model

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ("Scoring System", "Run DELFI on SMILES or CSV", "Score your own SMILES data"))

    if page == "Scoring System":
        scoring_system.render(upload_csv=False)

    elif page == "Run DELFI on SMILES or CSV":  
        run_model.render()

    elif page == "Score your own SMILES data":
        scoring_system.render(upload_csv=True)

if __name__ == "__main__":
    main()
