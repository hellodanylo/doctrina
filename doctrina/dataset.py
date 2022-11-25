import typing
from collections import OrderedDict
from typing import Optional

import pandas as pd


class Dataset:
    @classmethod
    def concat(cls, aa, bb):
        out = cls()

        for a in aa.__dict__:
            out.__dict__[a] = aa.__dict__[a]

        for b in bb.__dict__:
            out.__dict__[b] = bb.__dict__[b]

        return out

    @classmethod
    def from_h5_workdir(cls, workdir):
        """
        :param workdir:
        :return:
        """
        dataset = cls()
        for a in dataset.__dict__:
            dataset.__dict__[a] = pd.read_hdf(f"{workdir}/dataset.h5", a)
        return dataset

    @classmethod
    def from_pq_workdir(cls, workdir):
        """
        :param workdir:
        :return:
        """
        dataset = cls()
        for a in dataset.__dict__:
            dataset.__dict__[a] = pd.read_parquet(f"{workdir}/{a}.parquet")
        return dataset

    def to_h5_workdir(self, workdir):
        """
        :param workdir:
        """
        for a in self.__dict__:
            self.__dict__[a].to_hdf(f"{workdir}/dataset.h5", a)

    def to_pq_workdir(self, workdir):
        """
        :param workdir:
        """
        for a in self.__dict__:
            self.__dict__[a].to_parquet(f"{workdir}/{a}.parquet")


class Segment:
    def __init__(self, segment_name):
        self.segment_name = segment_name
        self.frames = {}

    def __getitem__(self, item):
        return self.frames[item]

    def __setitem__(self, key, value):
        self.frames[key] = value

    def to_pq_workdir(self, workdir):
        for name, frame in self.frames.items():
            filename = f"{self.segment_name}_{name}.parquet"
            self.frames[name].to_parquet(f"{workdir}/{filename}")

    @classmethod
    def from_pq_workdir(cls, workdir, segment_name, frame_names):
        """
        :param workdir:
        :return:
        """
        segment = cls(segment_name)

        for frame_name in frame_names:
            filename = f"{segment_name}_{frame_name}.parquet"
            segment.frames[frame_name] = pd.read_parquet(f"{workdir}/{filename}")

        return segment


class RegressionSegment(Segment):
    @classmethod
    def from_pq_workdir(cls, workdir, segment_name, **kwargs):
        frame_names = ["x", "y"]
        return Segment.from_pq_workdir(workdir, segment_name, frame_names)


class FeatureSegment(Segment):
    @classmethod
    def from_pq_workdir(cls, workdir, segment_name, **kwargs) -> 'FeatureSegment':
        frame_names = ["x"]
        return super(FeatureSegment, cls).from_pq_workdir(workdir, segment_name, frame_names)

    def as_reconstruction(self) -> RegressionSegment:
        segment = RegressionSegment(self.segment_name)
        segment['x'] = self['x']
        segment['y'] = self['x']
        return segment


class TargetSegment(Segment):
    @classmethod
    def from_pq_workdir(cls, workdir, segment_name, **kwargs):
        frame_names = ["y"]
        return Segment.from_pq_workdir(workdir, segment_name, frame_names)


class DenoisingSegment(Segment):
    @classmethod
    def from_pq_workdir(cls, workdir, segment_name, **kwargs) -> 'DenoisingSegment':
        frame_names = ['clean_x', 'noisy_x']
        return super(DenoisingSegment, cls).from_pq_workdir(workdir, segment_name, frame_names)

    def to_regression_segment(self) -> RegressionSegment:
        segment = RegressionSegment(self.segment_name)
        segment['x'] = self['noisy_x']
        segment['y'] = self['clean_x']
        return segment


class ReconstructionSegment(Segment):
    @classmethod
    def from_pq_workdir(cls, workdir, segment_name, **kwargs) -> 'ReconstructionSegment':
        return super(ReconstructionSegment, cls).from_pq_workdir(workdir, segment_name, ['x'])

    def to_regression_segment(self) -> RegressionSegment:
        segment = RegressionSegment(self.segment_name)
        segment['x'] = self['x']
        segment['y'] = self['x']
        return segment


class SegmentDataset:
    def __init__(self):
        self.segments: typing.OrderedDict[str, Segment] = OrderedDict()

    def __getitem__(self, item):
        return self.segments[item]

    def __setitem__(self, key, value):
        self.segments[key] = value

    def __iter__(self):
        return self.segments.values().__iter__()

    def to_pq_workdir(self, workdir):
        for segment in self.segments.values():
            segment.to_pq_workdir(workdir)

    @classmethod
    def from_pq_workdir(cls, workdir, segment_names, frame_names):
        dataset = cls()

        for name in segment_names:
            dataset[name] = Segment.from_pq_workdir(workdir, name, frame_names)

        return dataset


class RegressionDataset(Dataset):
    def __init__(self):
        self.train_X: Optional[pd.DataFrame] = None
        self.train_y: Optional[pd.DataFrame] = None
        self.validate_X: Optional[pd.DataFrame] = None
        self.validate_y: Optional[pd.DataFrame] = None
        self.test_X: Optional[pd.DataFrame] = None
        self.test_y: Optional[pd.DataFrame] = None


class FeaturesDataset(Dataset):
    def __init__(self):
        self.train_X: Optional[pd.DataFrame] = None
        self.validate_X: Optional[pd.DataFrame] = None
        self.test_X: Optional[pd.DataFrame] = None


class TargetDataset(Dataset):
    def __init__(self):
        self.train_y: Optional[pd.DataFrame] = None
        self.validate_y: Optional[pd.DataFrame] = None
        self.test_y: Optional[pd.DataFrame] = None


class MetaDataset(Dataset):
    def __init__(self):
        self.train_meta = Optional[pd.DataFrame]
        self.validate_meta = Optional[pd.DataFrame]
        self.test_meta = Optional[pd.DataFrame]


class ReconstructionDataset(FeaturesDataset):
    def to_regression_dataset(self):
        lookup = {
            'train_y': 'train_X',
            'validate_y': 'validate_X',
            'test_y': 'test_X',
            'train_X': 'train_X',
            'validate_X': 'validate_X',
            'test_X': 'test_X',
        }

        dataset = RegressionDataset()
        for there, here in lookup.items():
            dataset.__dict__[there] = self.__dict__[here]

        return dataset


class DenoisingDataset(Dataset):
    def __init__(self):
        self.train_clean_x: Optional[pd.DataFrame] = None
        self.validate_clean_x: Optional[pd.DataFrame] = None
        self.test_clean_x: Optional[pd.DataFrame] = None
        self.train_noisy_x: Optional[pd.DataFrame] = None
        self.validate_noisy_x: Optional[pd.DataFrame] = None
        self.test_noisy_x: Optional[pd.DataFrame] = None

    def to_regression_dataset(self):
        lookup = {
            'train_y': 'train_clean_x',
            'validate_y': 'validate_clean_x',
            'test_y': 'test_clean_x',
            'train_x': 'train_noisy_x',
            'validate_x': 'validate_noisy_x',
            'test_x': 'test_noisy_x',
        }

        dataset = RegressionDataset()
        for there, here in lookup.items():
            dataset.__dict__[there] = self.__dict__[here]

        return dataset
