import io
import math
from typing import Optional

import matplotlib.pyplot as plt
import mlflow
import pandas as pd
from matplotlib.figure import Figure
from tensorflow.python.keras import Sequential

from doctrina.util import save_public_s3
from doctrina.dataset import Dataset, SegmentDataset


class LearningCurve:
    def __init__(self):
        self.learning_scores: Optional[pd.DataFrame] = None
        self.final_scores: Optional[pd.DataFrame] = None

    @staticmethod
    def from_history(dataset: Dataset, model: Sequential, history):
        epochs = history.epoch
        scores = history.history

        loss = model.loss
        metrics = [m.name for m in model.metrics]

        columns = pd.MultiIndex.from_product([
            [loss] + metrics,
            ['train', 'validate'],
        ])

        learning_scores = pd.DataFrame(columns=columns, index=epochs)
        learning_scores.index.name = 'epoch'

        learning_scores.loc[:, (loss, 'train')] = scores['loss']
        learning_scores.loc[:, (loss, 'validate')] = scores['val_loss']

        for metric in metrics:
            learning_scores.loc[:, (metric, 'train')] = scores[metric]
            learning_scores.loc[:, (metric, 'validate')] = scores[f'val_{metric}']

        train_X = dataset.train_X
        train_y = dataset.train_y
        validate_X = dataset.validate_X
        validate_y = dataset.validate_y

        train_scores = model.evaluate(
            train_X,
            train_y,
            batch_size=train_X.shape[0]
        )
        validate_scores = model.evaluate(
            validate_X,
            validate_y,
            batch_size=validate_X.shape[0]
        )

        if not isinstance(train_scores, list):
            train_scores = [train_scores]

        if not isinstance(validate_scores, list):
            validate_scores = [validate_scores]

        final_scores = pd.DataFrame(columns=columns)
        final_scores.loc[:, ([loss] + metrics, 'train')] = [train_scores]
        final_scores.loc[:, ([loss] + metrics, 'validate')] = [validate_scores]

        curve = LearningCurve()
        curve.learning_scores = learning_scores
        curve.final_scores = final_scores

        return curve


    @staticmethod
    def from_history_with_segments(
            dataset: SegmentDataset,
            model: Sequential,
            history,
            reconstruction=False
    ):

        epochs = history.epoch
        scores = history.history

        loss = model.loss
        metrics = [m.name for m in model.metrics]

        curve_columns = pd.MultiIndex.from_product([
            [loss] + metrics,
            ['train', 'validate'],
        ])

        learning_scores = pd.DataFrame(columns=curve_columns, index=epochs)
        learning_scores.index.name = 'epoch'

        learning_scores.loc[:, (loss, 'train')] = scores['loss']
        learning_scores.loc[:, (loss, 'validate')] = scores['val_loss']

        for metric in metrics:
            learning_scores.loc[:, (metric, 'train')] = scores[metric]
            learning_scores.loc[:, (metric, 'validate')] = scores[f'val_{metric}']

        learning_scores = learning_scores.dropna(axis=1)

        final_columns = pd.MultiIndex.from_product([
            [loss] + metrics,
            dataset.segments.keys(),
        ])

        final_scores = pd.DataFrame(columns=final_columns)
        for name, segment in dataset.segments.items():
            if reconstruction:
                x = y = segment['x']

            else:
                x = segment['x']
                y = segment['y']

            scores = model.evaluate(x, y, batch_size=x.shape[0])

            if not isinstance(scores, list):
                scores = [scores]

            final_scores.loc[:, ([loss] + metrics, name)] = [scores]

        curve = LearningCurve()
        curve.learning_scores = learning_scores
        curve.final_scores = final_scores

        return curve

    @staticmethod
    def from_workdir(workdir):
        path = f'{workdir}/learning_curve.h5'

        curve = LearningCurve()
        curve.learning_scores = pd.read_hdf(path, 'learning_scores')
        curve.final_scores = pd.read_hdf(path, 'final_scores')

        return curve

    def to_mlflow(self):
        metrics = {'/'.join(k): v for k, v in self.final_scores.iloc[0].to_dict().items()}
        mlflow.log_metrics(metrics)

    def to_workdir(self, workdir):
        path = f'{workdir}/learning_curve.h5'

        self.learning_scores.to_hdf(path, 'learning_scores')
        self.final_scores.to_hdf(path, 'final_scores')

    def to_slack(self, workdir):

        loss = self.final_scores.columns[0][0]

        train_loss = round(self.final_scores[(loss, 'train')].iloc[0], 2)
        validate_loss = round(self.final_scores[(loss, 'validate')].iloc[0], 2)

        return {
            "fallback" : "Learning Curve",
            "title"    : "Learning Curve",
            "image_url": save_public_s3(
                f'{workdir}/learning_curve.png',
                self.render_plot(),
                content_type='image/png'
            ),
            "fields"   : [
                {
                    "title": "Metric",
                    "value": loss,
                    "short": False,
                },
                {
                    "title": f"Train",
                    "value": train_loss,
                    "short": True,
                },
                {
                    "title": f"Validate",
                    "value": validate_loss,
                    "short": True,
                },
            ],
        }

    def to_short_df(self, n=5):
        if self.learning_scores.shape[0] <= n:
            return self.learning_scores

        return self.learning_scores[::int(self.learning_scores.shape[0] / n)]

    def plot(self, metrics=None) -> Figure:
        curve = self.learning_scores

        if metrics is None:
            metrics = curve.columns.levels[0]

        cols = max(1, min(2, len(metrics)))
        rows = math.ceil(len(metrics) / cols)

        fig = plt.figure(figsize=[6 * cols, 4 * rows], dpi=250)
        fig.patch.set_facecolor('lightgrey')

        for i, metric in enumerate(metrics):
            plt.subplot(rows, cols, i + 1)

            ymin = curve[metric].min().min() * 0.8
            ymax = curve[metric].max().max() * 1.2
            plt.ylim([ymin, ymax])

            plt.title(metric)
            plt.xlabel('Epoch')
            plt.ylabel('Cost')

            plt.plot(curve.index, curve[metric]['train'], label='train')
            plt.plot(curve.index, curve[metric]['validate'], label='validate')
            plt.legend()

        plt.tight_layout()
        return fig

    def save_png(self, workdir) -> str:
        self.plot()

        path = f'{workdir}/learning_curve.png'
        plt.savefig(path)

        return path

    def render_plot(self) -> bytes:
        self.plot()

        bs = io.BytesIO()
        plt.savefig(bs, format='png')

        bs.seek(0)
        return bs.read()
