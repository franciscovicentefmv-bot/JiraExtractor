import zipfile
import os

def create_zip(files):
    zip_path = "exports/result.zip"
    os.makedirs("exports", exist_ok=True)

    with zipfile.ZipFile(zip_path, 'w') as z:
        for f in files:
            z.write(f, arcname=os.path.basename(f))

    return zip_path
