import datetime
import os
import pathlib
from PIL import Image

"""

"""
class LatexCode:
    def __init__(self, folder):
        self.folder = folder
        self.latex_code = r"""
% Photo Gallery
"""
    def chapter(self, chapter_folder):
        """Generate LaTeX code for a chapter."""

        self.chapter_folder = chapter_folder
        self.latex_code += f"\\chapter{{Chapter: {chapter_folder}}}\n"
        print(f"== Chapter: {chapter_folder}")

    def generate_images(self, images, rows=5, columns=3):
        """Generate LaTeX code for image grid"""

        # Number of images per page
        steps = rows * columns
        format_string = "c" * columns
        width = round((1 / columns) * 0.96, 2)
        print("\tCreating grid ({},{}) for {} images".format(rows, columns, len(images)))

#\begin{figure}[H]   
#    \centering

        self.latex_code += r"""
    \begin{tabular}{""" + format_string + r"""}
"""
        compteur = 0
        for i, image in enumerate(images):
            image_path = os.path.join(self.folder, self.chapter_folder, image)
            self.latex_code += f"        \\includegraphics[width="+ str(width) + f"\\textwidth]{{{image_path}}}"
            if (i + 1) % columns == 0:
                self.latex_code += r" \\" + "\n"  # End of row
            else:
                self.latex_code += " &\n"
            if (i + 1) % steps == 0:
                compteur += steps
                self.latex_code += r"""
    \end{tabular}
    \begin{tabular}{ccc}
"""                        
# \end{figure}
# \newpage

# \begin{figure}[H]
#     \centering

        self.latex_code += r"""    \end{tabular}

"""
#\end{figure}

    def landscape_images(self, landscape_images):
        """Generate LaTeX code for landscape images."""
        self.generate_images(landscape_images, rows=5, columns=3)

    def portrait_images(self, portrait_images):
        """Generate LaTeX code for portrait images."""
        self.generate_images(portrait_images, rows=3, columns=4)


    def write_to_file(self, output_file):
        """Write LaTeX code to a file."""
        with open(output_file, "w") as f:
            f.write(self.latex_code)
        print(f"LaTeX file generated: {output_file}")

def is_portrait(image_path):
    """Check if an image is portrait."""
    with Image.open(image_path) as img:
        return img.height > img.width
    
class Gallery:
    def __init__(self, main_folder, work_folder, output_file="photo_gallery.tex"):
        self.main_folder = main_folder
        self.work_folder = work_folder
        self.output_file = output_file

        # Get list of image files
        self.extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.pdf')

        self.prepare()

    def prepare(self):
        """Prepare the gallery by resizing images."""
        # check if working folder exists
        if not os.path.exists(self.work_folder):
            print("Creating working folder...", self.work_folder)
            os.makedirs(self.work_folder)  

            # Resize images
            for chapter_folder in sorted(os.listdir(self.main_folder)):
                chapter_path = os.path.join(self.main_folder, chapter_folder)
                if os.path.isdir(chapter_path):  # Process only directories
                    # check if image folder exists in working folder
                    working_chapter_path = os.path.join(self.work_folder, chapter_folder)
                    if not os.path.exists(working_chapter_path):
                        print("Creating chapter folder...", working_chapter_path)
                        os.makedirs(working_chapter_path)  

                    images = [f for f in sorted(os.listdir(chapter_path)) if f.lower().endswith(self.extensions)]
                    if not images:
                        continue  # Skip empty folders
                    for image in images:
                        image_path = os.path.join(chapter_path, image)

                        creation_time = os.stat(image_path).st_birthtime
                        creation_datetime = datetime.datetime.fromtimestamp(creation_time)            
                        formatted_time = creation_datetime.strftime('%Y-%m-%d_%H-%M-%S')
                        directory, original_name = os.path.split(image_path)
                        file_name, file_ext = os.path.splitext(original_name)
                        new_name = f"{formatted_time}{file_ext}"

                        image_path_new = os.path.join(self.work_folder, chapter_folder, new_name)
                        self.resize_image(image_path, image_path_new)
        else:
            print("Working folder already exists...", self.work_folder)

    def resize_image(self, image_path, image_path_new):
        """Resize an image."""

        with Image.open(image_path) as img:
            # Size of the image in pixels (size of original image) 
            width, height = img.size

            if width > height:
                new_width = 1000
                new_height = int(height * new_width / width)
            else:
                new_height = 1000
                new_width = int(width * new_height / height)

            newsize = (new_width, new_height)
            img.resize(newsize).save(image_path_new)

    def generate(self):
        """Generate LaTeX code for a gallery."""
        
        # Begin LaTeX document
        latex_code = LatexCode(self.work_folder)

        steps = 18      # Number of images per page
        # Iterate through subfolders (chapters)
        for chapter_folder in sorted(os.listdir(self.work_folder)):
            chapter_path = os.path.join(self.work_folder, chapter_folder)
            if os.path.isdir(chapter_path):  # Process only directories
                images = [f for f in sorted(os.listdir(chapter_path)) if f.lower().endswith(self.extensions)]
                if not images:
                    continue  # Skip empty folders

                # Separate images into portrait and landscape categories
                portrait_images = []
                landscape_images = []
                for image in images:
                    image_path = os.path.join(chapter_path, image)
                    if is_portrait(image_path):
                        portrait_images.append(image)
                    else:
                        landscape_images.append(image)
                # Add chapter title
                latex_code.chapter(chapter_folder)
                print(f"== Number of images: {len(images)}")

                # Add landscape images in a grid (3x3 layout)
                if landscape_images:
                    latex_code.landscape_images(landscape_images)
                # Add portrait images
                if portrait_images:
                    latex_code.portrait_images(portrait_images)
        # Write to output file
        latex_code.write_to_file(self.output_file)