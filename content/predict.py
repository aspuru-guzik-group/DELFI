import streamlit as st
import pandas as pd
import numpy as np
import torch
import deepchem as dc
from deepchem.models import GATModel
from rdkit.Chem import AllChem
from rdkit import Chem
import rdkit, rdkit.Chem
import os

functionals_dictionary = {
    "SPW92": 0,
    "B97D": 1,
    "MPW91": 2,
    "PBE": 3,
    "BLYP": 4,
    "N12": 5,
    "B97MV": 6,
    "mBEEF": 7,
    "M06L": 8,
    "revM06L": 9,
    "MN15L": 10,
    "revTPSS": 11,
    "TPSS": 12,
    "wB97XD": 13,
    "CAMB3LYP": 14,
    "wB97XV": 15,
    "LRCwPBE": 16,
    "LRCwPBEh": 17,
    "MPW1K": 18,
    "PBE0": 19,
    "HSEHJS": 20,
    "rcamB3LYP": 21,
    "BHHLYP": 22,
    "PBE50": 23,
    "BMK": 24,
    "M06SX": 25,
    "M062X": 26,
    "wB97MV": 27,
    "wM05D": 28,
    "MN15": 29,
    "PW6B95": 30,
    "SCAN0": 31,
    "M11": 32,
    "revTPSSh": 33,
    "TPSSh": 34,
    "B3LYP": 35,
    "HFLYP": 36,
    "SOGGA11X": 37,
}

def collect_smiles(smiles_list):
    errors = []
    smiles = []
    for i, test in enumerate(smiles_list):
        mol = Chem.MolFromSmiles(test)
        if mol is None:
            errors.append(i)
        else:
            smiles.append(test)
    if errors:
        error_indices = [str(i).replace(',', '') for i in errors]
        df_merged = pd.DataFrame(error_indices, columns=["SMILE Error Row"])
        st.write("SMILE Errors:")
        st.dataframe(df_merged)
    return smiles

def featurize_smiles(smiles):
    featurizer = dc.feat.MolGraphConvFeaturizer(use_edges=True)##True
    X = featurizer.featurize(smiles)
    data = dc.data.NumpyDataset(X=X)
    return data

def load_model(model_name):
    recommender_state = torch.load(model_name, map_location=torch.device('cpu'))
    activation = torch.nn.Sigmoid()
    recommender = GATModel(
        mode='regression',
        n_tasks=38,
        batch_size=128,
        n_layers=2,
        graph_attention_layers=[128, 128],
        learning_rate=0.001,
        activation=activation,
        dropout=0.1,
        predictor_dropout=0.2
    )
    recommender.model.load_state_dict(recommender_state)
    return recommender

def predict(data, model):
    model.model.eval()
    predictions = model.predict(data)
    for i in range(len(predictions)):
        for j in range(len(predictions[i])):
            if predictions[i][j] < 0:
                predictions[i][j] = 0
    predictions = predictions * 100
    return predictions

def save_predictions(predictions, output):
    np.save(output, predictions)

def main(smiles_input):
    filtered_smiles = collect_smiles(smiles_input)
    data = featurize_smiles(filtered_smiles)
    model = load_model(os.path.join(os.path.dirname(__file__), os.pardir, 'models', 'functional_recommender.pt'))
    predictions = predict(data, model)

    predictions_table = pd.concat([pd.DataFrame(filtered_smiles, columns=['SMILES']), pd.DataFrame(predictions, columns=functionals_dictionary.keys())], axis=1)

    return predictions_table


if __name__ == '__main__':
    with open(os.path.join(os.path.dirname(__file__), os.pardir, 'data_files', 'scores_without_NaN.csv'), "r") as f:
        save_predictions(main(pd.read_csv(f)['SMILES']), "predictions.npy")
