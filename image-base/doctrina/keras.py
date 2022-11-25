import json

from tensorflow.python.keras import Sequential
from tensorflow.python.keras import backend as K
from tensorflow.python.keras.models import model_from_json


def load_keras_model(workdir: str) -> Sequential:
    with open(f'{workdir}/keras_model.json', 'r') as f:
        model = model_from_json(f.read())

    model.load_weights(f"{workdir}/keras_weights.h5")

    return model


def save_keras_model(workdir: str, model: Sequential):
    # Saving the model specification
    model_spec = json.dumps(json.loads(model.to_json()), indent=True)
    with open(f'{workdir}/keras_model.json', 'w') as f:
        f.write(model_spec)

    # Saving the learned weights
    model.save_weights(f"{workdir}/keras_weights.h5")


def r2_score(y_true, y_pred):
    SS_res =  K.sum(K.square(y_true - y_pred))
    SS_tot = K.sum(K.square(y_true - K.mean(y_true)))
    return 1 - SS_res/(SS_tot + K.epsilon())


def mean_error(y_true, y_pred):
    return K.mean(y_pred) - K.mean(y_true)