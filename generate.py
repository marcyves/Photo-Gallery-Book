import os
from dotenv import load_dotenv
from LatexGallery import Gallery


if __name__ == "__main__":
    load_dotenv()

    folder = os.getenv('MAIN_FOLDER')
    output = os.getenv('OUTPUT_FILE')    

    gallery = Gallery(folder,output)
    gallery.generate()  # Generate LaTeX code       