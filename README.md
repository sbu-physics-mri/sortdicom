# Sort Dicom

A very simple script that sorts DICOM files bassed on their series description and time of acquisition.

That is DICOMs with the following series descriptions:

- `ACR_T1` :: Acquired at 12:00:00
- `ACR_T2` :: Acquired at 12:05:00
- `RF_NOISE` :: Acquired at 12:10:00
- `RF_NOISE` :: Acquired at 12:15:00
- `ACR_T2` :: Acquired at 12:20:00

would be grouped into the directory structure:

```
ACR/
    ACR_T1_120000.dcm
    ACR_T2_120500.dcm
    ACR_T2_122000.dcm
RF/
    RF_NOISE_121000.dcm
    RF_NOISE_121500.dcm
```
   
## Installation

```
pip install sortdicom
```

## Usage

```
usage: sortdicom.cmd [-h] [-o OUT] data_path

Sorts DICOMs into directories based on their series description.

positional arguments:
  data_path          Path to the data directory containing DICOM files.

options:
  -h, --help         show this help message and exit
  -o OUT, --out OUT  Path to stored the grouped DICOM files.
```

## License

This project is licensed under the GNU GPL v3 license which can be found [here](LICENSE)

## Contributing

Contributions welcome - please open an issue and/or pull request.
