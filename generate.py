import os
from dotenv import load_dotenv
from LatexGallery import Gallery


if __name__ == "__main__":
    load_dotenv()

    main_folder = os.getenv('MAIN_FOLDER')
    work_folder = os.getenv('WORK_FOLDER')    
    output = os.getenv('OUTPUT_FILE')    

    gallery = Gallery(main_folder, work_folder,output)
    gallery.generate()  # Generate LaTeX code       