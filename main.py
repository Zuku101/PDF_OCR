import os
import glob
import pandas as pd
import re
import argparse
import subprocess
from pdfminer.pdftypes import resolve1
from pdfminer.pdfpage import PDFPage

PDF_STORAGE_BASE_PATH = '/home/User/PDF/STORAGE/BASE/PATH'

def sorted_nicely(data, reverse = False):
	convert = lambda text: int(text) if text.isdigit() else text
	alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
	
	return sorted(data, key = alphanum_key, reverse=reverse)

def get_pdf_searchable_pages(fname):
    searchable_pages = []
    non_searchable_pages = []
    page_num = 0
    with open(fname, 'rb') as infile:
        for page in PDFPage.get_pages(infile):
            page_num += 1
            resources = resolve1(page.resources)
            
            if 'Font' in resources:
                searchable_pages.append(page_num)
            else:
                xobjects = resources.get('XObject')
                if xobjects:
                    xobjects = resolve1(xobjects)
                    if any(resolve1(xobject).get('Subtype') == '/Image' for xobject in xobjects.values()):
                        searchable_pages.append(page_num)
                    else:
                        non_searchable_pages.append(page_num)
                else:
                    non_searchable_pages.append(page_num)

    return searchable_pages, non_searchable_pages

def run_command(cmdLineArguments):
	process = subprocess.Popen(cmdLineArguments, stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)
	stdout = process.communicate()[0]
	p_status = process.wait()

debug=False

if debug:
	class Namespace:
		def __init__(self, **kwargs):
			self.__dict__.update(kwargs)
	
	args = Namespace(pdf_storage_path=PDF_STORAGE_BASE_PATH)

def main(args):
    file_info = {'title':[], 'path':[], 'searchable':[]}
    cnt = 1
    num_files = len(glob.glob(os.path.join(args.pdf_storage_path, '**', '*.pdf'), recursive=True))
    for ifile in glob.glob(os.path.join(args.pdf_storage_path, '**', '*.pdf'), recursive=True):
        try:
            searchable, nonsearch = get_pdf_searchable_pages(ifile)
            file_info['title'].append(os.path.basename(ifile).split('.pdf')[0].strip())
            file_info['path'].append(ifile)
            file_info['searchable'].append(True if len(searchable) > len(nonsearch) else False)
        except Exception as e:
            print(e)
            file_info['title'].append(os.path.basename(ifile).split('.pdf')[0].strip())
            file_info['path'].append(ifile)
            file_info['searchable'].append(True)

        print(f"Finished scanning {cnt} of {num_files} files: {os.path.basename(ifile)}")
        cnt += 1

    file_info = pd.DataFrame(file_info)

    print(f"\nFound {file_info[file_info['searchable']==False].shape[0]} PDF files to convert...\n")

    cnt = 1
    for index, row in file_info[file_info['searchable']==False].iterrows():
        print(f"Starting conversion {cnt} of {len(file_info[file_info['searchable']==False])}: {os.path.basename(row['path'])}")

        log_file_path = f"log_{os.path.basename(row['path'])}.txt"
        ocr_cmd = [
            'ocrmypdf',
            '--verbose',
            '--language', 'pol',
            f"'{row['path']}'",
            f"'{row['path']}'"
        ] + [f" > {log_file_path} 2>&1"]
        run_command(' '.join(ocr_cmd))

        print(f"Finished converting {os.path.basename(row['path'])}")
        cnt += 1

    print('Finished converting all PDF files in directory.')

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--pdf_storage_path', help='Path to where script stores PDF files.', required=True)
	args = parser.parse_args()

	main(args)
	