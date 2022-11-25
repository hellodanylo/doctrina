from typing import Optional

import seaborn as sns
from matplotlib import pyplot as plt
from tensorflow.python.keras import Sequential

from doctrina.dataset import Dataset
from doctrina.keras import load_keras_model
from doctrina.learning_curve import LearningCurve
from doctrina.task import load_task


class TrainingReport:
    def __init__(self):
        self.workdir: Optional[str] = None
        self.task: Optional[dict] = None
        self.dataset: Optional[Dataset] = None
        self.model: Optional[Sequential] = None
        self.learning_curve: Optional[LearningCurve] = None

    @staticmethod
    def from_workdir(workdir) -> 'TrainingReport':
        report = TrainingReport()
        report.workdir = workdir
        report.task = load_task(workdir)
        report.model = load_keras_model(workdir)
        report.learning_curve = LearningCurve.from_workdir(workdir)
        return report

    def plot_params_histograms(self):
        weights = self.model.get_weights()
        layers = int(len(weights) / 2)
        ncols = 2
        nrows = layers

        plt.figure(figsize=[15, nrows * 4], dpi=300)

        for l in range(layers):
            layer_biases = weights[l * 2 + 1]
            layer_weights = weights[l * 2].reshape(-1)
            weights_mean = layer_weights.mean()
            weights_std = layer_weights.std()
            biases_mean = layer_biases.mean()
            biases_std = layer_biases.std()

            plt.subplot(nrows, ncols, l * 2 + 1)
            plt.title(f'L{l + 1} Weights: n = {layer_weights.shape[0]}, mean = {weights_mean}, std = {weights_std}')
            sns.distplot(
                layer_weights,
                hist=False,
                kde=True,
                norm_hist=True,
                rug=True,
                rug_kws={'color': 'orange'}
            )

            plt.subplot(nrows, ncols, l * 2 + 2)
            plt.title(f'L{l + 1} Biases: n = {layer_biases.shape[0]}, mean = {biases_mean}, std = {biases_std}')
            sns.distplot(
                layer_biases,
                hist=False,
                kde=True,
                norm_hist=True,
                rug=True,
                rug_kws={'color': 'orange'}
            )