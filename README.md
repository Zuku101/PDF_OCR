<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
  </ol>
</details>

## About The Project

This code snippet will search a given directory for PDF files that are non-searchable and convert them to searchable PDFs (OCR). When you obtain manuscript PDF files from online databases, they may not be in a searchable format. This means you are unable to highlight and search for text within the PDF. This small Python function will recursively search through a directory containing PDF files, determine the PDF files that are non-searchable, and convert them to a searchable format. Optical Character Recognition (OCR) is a method to enable text recognition within images and documents. PDFs contain vector graphics that can contain raster objects (.png, .jpg etc.). The OCR process will first rasterize each page of the PDF file, and then an OCR "layer" is created.

Additionally, this tool supports multiple languages, including Polish, making it versatile for recognizing text in various languages.

This python function wraps the command-line program <a href="https://ocrmypdf.readthedocs.io/en/latest/index.html" target="_blank"><strong>OCRmyPDF</strong></a>.

### Built With

* Python version: 3.10

## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

* Install <a href="https://ocrmypdf.readthedocs.io/en/latest/installation.html" target="_blank"><strong>OCRmyPDF</strong></a>

### Installation

1. In a terminal, clone the repo by running:
    ```sh
    git clone 
    ```

2. Change into the project directory (update path to reflect where you stored this project directory):
    ```sh
    cd /home/user/pdf_ocr
    ```

3. Install the required Python packages:
    ```sh
    python3 -m pip install -r requirements.txt
    ```

## Usage

1. In a terminal, move into the project directory
     ```sh
     cd /home/user/ocr-pdf
     ```

2. Run the following to execute the epoch script:
    ```sh
    python main.py -i "full/path/to/PDF/storage/diectory"
    ```

  * **-i:** full directory path to the PDF storage directory
