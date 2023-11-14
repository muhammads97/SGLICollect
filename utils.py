import os, shutil

def empty_temp():
    """
    Clear the temporary files from ./temp
    """
    for filename in os.listdir("./temp"):
        if filename.endswith("tmp"): continue
        file_path = os.path.join("./temp", filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))