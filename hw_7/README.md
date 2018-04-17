hw_7 README

Based on hw_2/hw_3 grading, the full solution is now kept in the Jupyter notebook 'hw7_notebook.ipynb'.  
Images for panoramic stitching are kept in the adjacent 'images' directory.

Problem 1:

There are no output files; results are plotted during each step of 'cleaning up' the image before labeling the coin regions.  Skimage has tools to measure labeled regions, and the final plot shows these measurements (area, eccentricity, and the semi-major/minor axes for fun) overlaying the original image.

Problem 2:

The notebook loads three images I took in Zermatt, Switzerland and the stitching process provided by the 
skimage creators (I call them Stefan & friends) works just as well in combining them as it does with the example images.
I've also included three images from Big Sur, which often do not get merged correctly, as matching between the leftmost 
and center images tends to fail (adjusting the number of feature matching keypoints when calling ORB sometimes helps).

In case there's trouble in sharing this notebook, I've included my stitched panoramic image 'Zermatt_stitched.png'.  The 
final block of code in the notebook will save the result as 'pano-advanced-output.png', as in the tutorial.
