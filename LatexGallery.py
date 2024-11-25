import os
from PIL import Image

"""

"""
class LatexCode:
    def __init__(self, main_folder):
        self.main_folder = main_folder
        self.latex_code = r"""
% Photo Gallery
"""
    def chapter(self, chapter_folder):
        """Generate LaTeX code for a chapter."""

        self.chapter_folder = chapter_folder
        self.latex_code += f"\\section*{{Chapter: {chapter_folder}}}\n"
        print(f"== Chapter: {chapter_folder}")

    def landscape_images(self, landscape_images):
        """Generate LaTeX code for landscape images."""

        print("\tLandscape images: {}".format(len(landscape_images)))
        self.latex_code += r"""
% Landscape Images Grid
\begin{figure}[H]
    \centering
    \begin{tabular}{ccc}
"""
        steps = 18      # Number of images per page
        compteur = 0
        for i, image in enumerate(landscape_images):
            image_path = os.path.join(self.main_folder, self.chapter_folder, image)
            self.latex_code += f"        \\includegraphics[width=0.32\\textwidth]{{{image_path}}}"
            if (i + 1) % 3 == 0:
                self.latex_code += r" \\" + "\n"  # End of row
            else:
                self.latex_code += " &\n"
            if (i + 1) % steps == 0:
                compteur += steps
                self.latex_code += r"""
    \end{tabular}
\end{figure}
\newpage

\begin{figure}[H]
    \centering
    \begin{tabular}{ccc}
"""                        
        self.latex_code += r"""    \end{tabular}
\end{figure}

"""
    def portrait_images(self, portrait_images):
        """Generate LaTeX code for portrait images."""

        steps = 18      # Number of images per page
        compteur = 0
        print("\tPortrait images: {}".format(len(portrait_images)))
        self.latex_code += r"""
% Portrait Images
\begin{figure}[H]
    \centering
"""
        for i, image in enumerate(portrait_images):
            image_path = os.path.join(self.main_folder, self.chapter_folder, image)
            self.latex_code += f"""
    \\begin{{subfigure}}[t]{{0.28\\textwidth}}
        \\centering
        \\includegraphics[width=\\textwidth, height=0.8\\textheight, keepaspectratio]{{{image_path}}}
        \\caption{{Portrait Image {i + 1}}}
    \\end{{subfigure}}
"""
            if i % 3 == 0:
                self.latex_code += r"\hfill" + "\n"
            if (i + 1) % 3 == 0:
                self.latex_code += r"\\ \n"  # New row for every 2 images
            if (i + 1) % steps == 0:
                compteur += steps
                self.latex_code += r"""
\end{figure}

\newpage
\begin{figure}[H]
    \centering
"""
        self.latex_code += r"""
\end{figure}

""" 

    def write_to_file(self, output_file):
        """Write LaTeX code to a file."""
        with open(output_file, "w") as f:
            f.write(self.latex_code)
        print(f"LaTeX file generated: {output_file}")

def generate_latex(main_folder, output_file="photo_gallery.tex"):           
    """Generate LaTeX code for a gallery."""
    return r"""
% Photo Gallery
"""


def is_portrait(image_path):
    """Check if an image is portrait."""
    with Image.open(image_path) as img:
        return img.height > img.width
    
class Gallery:
    def __init__(self, main_folder, output_file="photo_gallery.tex"):
        self.main_folder = main_folder
        self.output_file = output_file

    def generate(self):
        """Generate LaTeX code for a gallery."""
        
        # Get list of image files
        extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.pdf')

        # Begin LaTeX document
        latex_code = LatexCode(self.main_folder)

        steps = 18      # Number of images per page
        # Iterate through subfolders (chapters)
        for chapter_folder in sorted(os.listdir(self.main_folder)):
            chapter_path = os.path.join(self.main_folder, chapter_folder)
            if os.path.isdir(chapter_path):  # Process only directories
                images = [f for f in sorted(os.listdir(chapter_path)) if f.lower().endswith(extensions)]
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