"""Sort Dicom files from MRI QA visit."""

from __future__ import annotations

# Python imports
import contextlib
import logging
from collections import defaultdict
from pathlib import Path

# Module imports
import pydicom

logger = logging.getLogger(__name__)

def get_dicoms(rdir: Path | str) -> list[pydicom.dataset.Dataset]:
    """Get a list of dicoms.

    Args:
        rdir : Root directory containing DICOM images.

    Returns:
        dicoms : List of DICOM images.

    """
    rdir = rdir if isinstance(rdir, Path) else Path(rdir)
    dcms = []
    for item in [f for f in rdir.iterdir() if f.is_file()]:
        with contextlib.suppress(pydicom.errors.InvalidDicomError):
            dcm = pydicom.dcmread(item)
            dcms.append(dcm)
    if not len(dcms):
        logger.warning("No DICOM images found in '%s'", rdir)
    return dcms


def group_dicoms(
        dcms: list[pydicom.dataset.Dataset],
) -> dict[list[pydicom.dataset.Dataset]]:
    """Group related DICOMS together.

    Looks at the first item when the DICOM series description is
        split with "_" and uses that as the group.

    Args:
        dcms : List of DICOM images.

    Returns:
        grouped_dcms : Dictionary of the format group : list_of_dicoms

    """
    grouped_dcms = defaultdict(list)
    for dcm in dcms:
        group = dcm.SeriesDescription.split("_")[0]
        grouped_dcms[group].append(dcm)
    return grouped_dcms


def save_dicoms(
        grouped_dcms: dict[list[pydicom.dataset.Dataset]],
        out_dir: Path | str = ".",
) -> bool:
    """Save group dicoms to the relavent group directory.

    Args:
        grouped_dcms : DICOMs grouped together by dict key.
        out_dir : The out directory to save the grouped DICOMS under.
                Defaults to ".".

    Returns:
        return value : True if sucessful, False otherwise.

    """
    out_dir = out_dir if isinstance(out_dir, Path) else Path(out_dir)

    for group, dcms in grouped_dcms.items():
        group_dir = out_dir / group
        group_dir.mkdir(exist_ok=True, parents=True)
        for dcm in dcms:
            out_file = (
                group_dir
                / f"{dcm.SeriesDescription}_{dcm.ContentTime}.dcm"
            )
            with out_file.open("wb") as outfile:
                dcm.save_as(outfile)
    return True
