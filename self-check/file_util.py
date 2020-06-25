### return the reverse sorted (first) filename, given a search string and directory

def select_filename(directory, search_string):
    # print(f'Looking in {directory}')
    file_name=[]
    for path in directory.glob(search_string):
        file_name.append(path)
        # print(f'   Found: {path}')
    for selected in sorted(file_name, reverse=True):
        return selected

