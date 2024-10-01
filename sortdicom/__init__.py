"""Main script."""

# Python imports
import argparse

# Local imports
from sortdicom import sortdicom


def parseargs() -> object:
    """Pass the CLI args."""
    parser = argparse.ArgumentParser(
        description="Sorts DICOMs into directories based on their series description.",
     )

    parser.add_argument(
        "data_path",
        type=str,
        help="Path to the data directory containing DICOM files.",
    )

    parser.add_argument(
        "-o",
        "--out",
        default="sorted",
        type=str,
        help="Path to stored the grouped DICOM files.",
    )

    return parser.parse_args()


def main() -> bool:
    """Sort DICOM images based on series description."""
    args = parseargs()

    dcms = sortdicom.get_dicoms(args.data_path)
    grouped_dcms = sortdicom.group_dicoms(dcms)
    return sortdicom.save_dicoms(grouped_dcms, args.out)
