import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

from patient_survival_prediction_model.config.core import config
from patient_survival_prediction_model.pipeline import patient_survival_prediction_pipe
from patient_survival_prediction_model.processing.data_manager import load_dataset, save_pipeline

def run_training() -> None:
    
    """
    Train the model.
    """

    # read training data
    data = load_dataset(file_name = config.app_config.training_data_file)
    
    # divide train and test
    X_train, X_test, y_train, y_test = train_test_split(
        
        data[config.self_model_config.features],     # predictors
        data[config.self_model_config.target],       # target
        test_size = config.self_model_config.test_size,
        random_state=config.self_model_config.random_state,   # set the random seed here for reproducibility
    )

    # Pipeline fitting
    patient_survival_prediction_pipe.fit(X_train, y_train)
    #y_pred = bikeshare_pipe.predict(X_test)

    # Calculate the score/error
    #print("R2 score:", r2_score(y_test, y_pred).round(2))
    #print("Mean squared error:", mean_squared_error(y_test, y_pred))

    # persist trained model
    save_pipeline(pipeline_to_persist = patient_survival_prediction_pipe)
    
if __name__ == "__main__":
    run_training()