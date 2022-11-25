import json
import math
import os
import pickle
import subprocess

import boto3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from sklearn.preprocessing import StandardScaler
from tensorflow.python.keras import Model

from doctrina.dataset import Dataset


def save_learning_curve(workdir, history, metrics=('loss',)):
    curve = build_learning_curve(history, metrics)
    curve.to_csv(f'{workdir}/learning_curve.csv')

    plot_learning_curve(curve, metrics)

    chart = f'{workdir}/learning_curve.png'
    plt.savefig(chart)
    image_url = save_public_s3_file(chart, 'image/png')

    return image_url


def load_learning_curve(workdir):
    curve = pd.read_csv(f'{workdir}/learning_curve.csv')
    curve.index = curve['epoch']
    return curve.drop(columns=['epoch'])


def load_input_X(hyperparams: dict):
    path = hyperparams['input_X']

    train_X = pd.read_hdf(f'{path}/train_X.h5', stop=hyperparams['nrows'])
    validate_X = pd.read_hdf(f'{path}/validate_X.h5')

    test = pd.read_hdf(f'{path}/test_X.h5')
    segments = test.iloc[:, 0].map(lambda s: s.split('.')[0])
    test_X = test.iloc[:, 1:]

    return train_X, validate_X, segments, test_X


def load_input_y(hyperparams):
    path = hyperparams['input_y']

    train_y = pd.read_hdf(f'{path}/train_y.h5', stop=hyperparams['nrows'])
    validate_y = pd.read_hdf(f'{path}/validate_y.h5')

    return train_y, validate_y


def train_scaler(train_X, validate_X, test_X):
    scaler = StandardScaler()

    train_X_scaled = pd.DataFrame(
        scaler.fit_transform(train_X),
        columns=train_X.columns
    )

    validate_X_scaled = pd.DataFrame(
        scaler.transform(validate_X),
        columns=validate_X.columns
    )

    test_X_scaled = pd.DataFrame(
        scaler.transform(test_X),
        columns=test_X.columns
    )

    return scaler, train_X_scaled, validate_X_scaled, test_X_scaled


def shuffle(X, y, seed):
    idx = np.arange(X.shape[0])
    np.random.seed(seed)
    np.random.shuffle(idx)
    return X.iloc[idx], y.iloc[idx]


def build_plot_predictions(
        model,
        train_X,
        train_y,
        validate_X,
        validate_y
):
    train_y_hat = model.predict(train_X)
    validate_y_hat = model.predict(validate_X)

    plot_predictions(
        train_y,
        train_y_hat,
        validate_y,
        validate_y_hat
    )


def save_scaler(workdir, scaler):
    params = {
        'mean' : list(scaler.mean_),
        'scale': list(scaler.scale_)
    }

    path = f'{workdir}/scaler_params.json'

    with open(path, 'w') as f:
        f.write(json.dumps(params, indent=True))


def load_scaler(workdir) -> StandardScaler:
    path = f'{workdir}/scaler_params.json'

    with open(path, 'r') as f:
        params = json.loads(f.read())

    scaler = StandardScaler()
    scaler.mean_ = params['mean']
    scaler.scale_ = params['scale']

    return scaler


def build_learning_curve(hist, metrics=('loss',)):
    epochs = len(hist.history[metrics[0]])

    curve = pd.DataFrame(index=range(epochs))
    curve.index.name = 'epoch'

    for metric in metrics:
        curve[f'train_{metric}'] = hist.history[metric]
        curve[f'validate_{metric}'] = hist.history[f'val_{metric}']

    return curve


def plot_learning_curve(curve: pd.DataFrame, metrics=('loss',)):
    fig = plt.figure(figsize=[12, 4])
    fig.patch.set_facecolor('lightgrey')

    ymin = curve.min().min() * 0.8
    ymax = curve.max().max() * 1.2

    rows = math.ceil(len(metrics) / 2)
    cols = min(2, len(metrics))

    for i, metric in enumerate(metrics):
        plt.subplot(rows, cols, i + 1)
        plt.ylim([ymin, ymax])

        plt.title(metric)
        plt.xlabel('Epoch')
        plt.ylabel('Cost')

        plt.plot(curve.index, curve[f'train_{metric}'], label=f'train')
        plt.plot(curve.index, curve[f'validate_{metric}'], label=f'validate')
        plt.legend()


def plot_layer_weights(weights: np.ndarray):
    windows = [1, 5, 10, 25]

    fig = plt.figure(figsize=[12, 8])
    fig.patch.set_facecolor('lightgrey')

    for i, w in enumerate(windows):
        plt.subplot(math.ceil(len(windows) / 2), 2, i + 1)
        plt.xlabel('Feature')
        plt.ylabel('Average Weight')
        plt.title(f'Bin Size = {w}')
        a = pd.Series(weights).groupby(lambda t: int(t / w)).mean()
        a.index = a.index * w
        a.plot()

    plt.tight_layout()


def plot_predictions(
        train_y,
        train_y_hat,
        validate_y,
        validate_y_hat
):
    full_y = np.concatenate([train_y, validate_y]).reshape(-1)
    full_y_hat = np.concatenate([train_y_hat, validate_y_hat]).reshape(-1)

    fig, ax = plt.subplots(figsize=[12, 8])
    plt.xlabel('Time')
    plt.ylabel('Time to Failure')

    plt.plot(full_y_hat, label='predicted')
    plt.plot(full_y, label='actual')

    validate_n = validate_y.shape[0]
    full_n = full_y.shape[0]

    ax.axvspan(full_n - validate_n, full_n, alpha=0.2, color='green')

    plt.legend()


def save_predictions(workdir: str, model: Model, dataset: Dataset):
    train_y_hat = pd.Series(model.predict(dataset.train_X).reshape(-1))
    validate_y_hat = pd.Series(model.predict(dataset.validate_X).reshape(-1))
    test_y_hat = pd.Series(model.predict(dataset.test_X).reshape(-1))

    train_y_hat.to_hdf(f'{workdir}/predictions.h5', 'train_y_hat')
    validate_y_hat.to_hdf(f'{workdir}/predictions.h5', 'validate_y_hat')
    test_y_hat.to_hdf(f'{workdir}/predictions.h5', 'test_y_hat')


def load_predictions(workdir: str):
    train_y_hat = pd.read_hdf(f'{workdir}/predictions.h5', 'train_y_hat')
    validate_y_hat = pd.read_hdf(f'{workdir}/predictions.h5', 'validate_y_hat')
    test_y_hat = pd.read_hdf(f'{workdir}/predictions.h5', 'test_y_hat')

    return train_y_hat, validate_y_hat, test_y_hat


def save_notebook(workdir: str, task: dict):
    notebook_output = f'{workdir}/notebook.html'

    subprocess.run(' '.join([
        f'ML_JOB_WORKDIR={workdir}',
        'bash',
        '-c',
        "'",
        ' '.join([
            'jupyter',
            'nbconvert',
            '--ExecutePreprocessor.timeout=600',
            '--execute',
            task['notebook'],
            '--output',
            notebook_output
        ]),
        "'"
    ]), shell=True)

    notebook_url = save_public_s3_file(
        path=notebook_output,
        content_type='text/html'
    )

    return notebook_url


def report_notebook(notebook_url):
    return {
        "fallback": "Notebook",
        "actions" : [
            {
                "type": "button",
                "text": "View Notebook",
                "url" : notebook_url
            }
        ]
    }


def send_slack(message, attachments):
    slack_url = os.getenv('SLACK_URL')

    body = {
        'text'       : f'`{message}`',
        "attachments": attachments
    }

    print(json.dumps(body, indent=True))
    requests.post(slack_url, json=body)


def save_public_s3(path: str, body: bytes, content_type: str):
    bucket_name = os.getenv('PUBLIC_S3_BUCKET')

    remote_path = path if path[0] != '/' else path[1:]

    s3 = boto3.client('s3')
    s3.put_object(
        Body=body,
        Bucket=bucket_name,
        Key=remote_path,
        ACL='public-read',
        ContentType=content_type
    )

    return to_public_s3_url(path)


def save_public_s3_file(path, content_type):
    bucket_name = os.getenv('PUBLIC_S3_BUCKET')

    local_path = path
    remote_path = path if path[0] != '/' else path[1:]

    s3 = boto3.client('s3')
    s3.upload_file(
        local_path,
        bucket_name,
        remote_path,
        ExtraArgs={
            'ACL'        : 'public-read',
            'ContentType': content_type
        }
    )

    return to_public_s3_url(path)


def to_public_s3_url(path):
    if path[0] == '/':
        path = path[1:]

    bucket_name = os.getenv('PUBLIC_S3_BUCKET')
    return f'https://s3-us-west-1.amazonaws.com/{bucket_name}/{path}'


def save_pickle(model, name):
    with open(name + '.pickle', 'wb') as f:
        f.write(pickle.dumps(model))
