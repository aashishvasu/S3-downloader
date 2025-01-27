# S3-folder-downloader (S3FD)

A multithreaded downloader for S3-compliant object storage, built with Python and [PySimpleGUI](https://www.pysimplegui.org).

## Getting Started

S3FD provides a GUI for downloading entire folders from S3-compliant storage using multiple threads.

### Usage

- Clone the repo or download the [latest release](https://github.com/aashishvasu/S3-downloader/releases/latest)
- Install the [prerequisites](#Prerequisites) (see below)
- Configure your S3 settings in `settings.ini`
- Run the application:
  ```sh
  python main.py
  ```

### Prerequisites

- Python 3.7+
- PySimpleGUI
- boto3

### Installing

Install the prerequisites manually, or using the included `requirements.txt`.

**NOTE: I would recommend [using a virtual environment](https://docs.python.org/3/library/venv.html), but that's obviously optional.**

#### Virtual Environment (optional)

```sh
# Create virtual environment
py -m venv venv 
```

#### Using `requirements.txt`

```sh
pip install -r requirements.txt
```

#### Manually

```sh
# boto
pip install boto3

# PySimpleGui
pip install pysimplegui
```

## Development

- [`main.py`](main.py): Entry point of the application
- [`app.py`](app.py): Core application logic and GUI setup
- [`src/downloader.py`](src/downloader.py): Handles S3 interactions and download logic
- [`src/file_progress.py`](src/file_progress.py): Manages file download progress reporting
- [`src/job.py`](src/job.py): Download state persistence for resuming interrupted downloads
- [`src/settings.py`](src/settings.py): Handles loading and saving of S3 settings
- [`layouts/browser.py`](layouts/browser.py): Layout for file browsing interface
- [`layouts/fileprogress.py`](layouts/fileprogress.py): Layout for file download progress display
- [`layouts/settings.py`](layouts/settings.py): Layout for S3 settings configuration

## Built With

- Python
- PySimpleGUI
- boto3
- [Love](https://www.merriam-webster.com/dictionary/love)

## Versioning

This project uses [Semantic Versioning](http://semver.org/). For the versions
available, see the [tags on this repository](https://github.com/aashishvasu/S3-downloader/tags).

## Contributors

  - [**Aashish Vasudevan**](https://github.com/aashishvasu) - *Repo owner*

## License

This project is licensed under the [LGPL-2.1](LICENSE.md) license - see the [LICENSE.md](LICENSE.md) file for details.