import matplotlib.animation
import os


def createPath(final, fileName, fileType):
    parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    if final == False:
        movie_folder_path = os.path.join(parent_dir, 'testMovies')
    else:
        movie_folder_path = os.path.join(parent_dir, 'Movies')

    movie_file_path = os.path.join(movie_folder_path, fileName+fileType)

    open(movie_file_path, 'w')

    return movie_file_path

def writer(animationFile, fileType = '.mp4', final = False, fileName = 'movieDefault'):
    
    writer = matplotlib.animation.FFMpegWriter(fps=24)

    movie_file_path = createPath(final, fileName, fileType)

    animationFile.save(movie_file_path, writer=writer)
