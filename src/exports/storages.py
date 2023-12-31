from django.core.files.storage import default_storage

def save(fpath, file_obj, overwrite=False):
    """
    Save a file to the default storage backend.
    """
    if overwrite is True and default_storage.exists(fpath):
        default_storage.delete(fpath)
    default_storage.save(fpath, file_obj)