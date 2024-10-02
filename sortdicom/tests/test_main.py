"""DICOM tests."""

# ruff: noqa: S101

from __future__ import annotations

# Python imports
import copy
import datetime
import logging
import tempfile
from pathlib import Path

# Module imports
import pydicom
import pytest
from pydicom.uid import UID, ExplicitVRLittleEndian

# Local imports
from sortdicom import sortdicom

logger = logging.getLogger(__name__)


@pytest.fixture()
def dicom() -> pydicom.dataset.Dataset:
    """Create a DICOM from scratch."""
    # Sets dataset values
    ds = pydicom.dataset.Dataset()
    ds.PatientName = "Samwise Gamgee"
    ds.PatientID = "29071954"

    dt = datetime.datetime.now(tz=datetime.UTC)
    ds.ContentDate = dt.strftime("%Y%m%d")
    ds.ContentTime = dt.strftime("%H%M%S.%f")

    # Set file meta information
    file_meta = pydicom.dataset.FileMetaDataset()
    file_meta.MediaStorageSOPClassUID = UID("1.2.840.10008.5.1.4.1.1.2")
    file_meta.MediaStorageSOPInstanceUID = UID("1.2.3")
    file_meta.ImplementationClassUID = UID("1.2.3.4")
    file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

    ds.file_meta = file_meta
    return ds


@pytest.mark.skip()
def list_of_dirs(
        num_dirs: int = 2,
        depth: int = 2,
        current_depth: int = 0,
        dirs: list | None = None,
) -> list:
    """Recursively create a nested directory structure."""
    if dirs is None:
        dirs = [tempfile.TemporaryDirectory()]

    if current_depth >= depth:
        return dirs

    tmp_dirs = []
    for d in dirs:
        tmp_dirs = tmp_dirs + [
            tempfile.TemporaryDirectory(dir=d.name) for _ in range(num_dirs)
        ]

    return dirs + list_of_dirs(
        num_dirs,
        depth,
        current_depth=current_depth+1,
        dirs=tmp_dirs,
    )

def test_get_dicoms(dicom: pydicom.dataset.Dataset) -> None:
    """Test get_dicoms."""
    # Create the directory structure:
    #
    # /
    #   0/
    #           0/
    #                   0.dcm
    #                   1.dcm
    #           1/
    #                   0.dcm
    #                   1.dcm
    #           0.dcm
    #           1.dcm
    #   1/
    #           0/
    #                   0.dcm
    #                   1.dcm
    #           1/
    #                   0.dcm
    #                   1.dcm
    #           0.dcm
    #           1.dcm
    #   0.dcm
    #   1.dcm
    num_dirs = 2
    depth = 2
    dirs = list_of_dirs(num_dirs, depth)

    num_dicoms_per_dir = 2
    dicoms = []
    for d in dirs:
        for i in range(num_dicoms_per_dir):
            dicom_path = Path(d.name) / f"{i}.dcm"
            dicom.save_as(dicom_path, enforce_file_format=True)
            dicoms.append(dicom_path)

    assert len(dirs) == sum([num_dirs ** i for i in range(depth + 1)])
    assert len(dicoms) == len(dirs) * num_dicoms_per_dir

    dcms = sortdicom.get_dicoms(dirs[0].name)
    assert len(dcms) == len(dicoms)


def test_group_dicoms(dicom: pydicom.dataset.Dataset) -> None:
    """Test group_dicoms."""
    num_groups = 10
    group_info = { str(i): i for i in range(1, num_groups + 1) }
    dicoms = []
    for group, num in group_info.items():
        for i in range(num):
            dcm_copy = copy.deepcopy(dicom)
            dcm_copy.SeriesDescription = f"{group}_{i}"
            dicoms.append(dcm_copy)

    grouped_dicoms = sortdicom.group_dicoms(dicoms, split=0)
    assert len(grouped_dicoms) == num_groups

    def nth_triangular_num(n: int) -> int:
        if n == 1:
            return 1
        return n + nth_triangular_num(n - 1)

    grouped_dicoms = sortdicom.group_dicoms(dicoms)
    assert len(grouped_dicoms) == nth_triangular_num(num_groups)
