hw_8 README

As in hw_7, the full solution is now kept in the Jupyter notebook 'hw8_notebook.ipynb'.  A separate, identical, script (without the markdown cells) is kepts under hw8_fortravis.py.  This file is for Travis CI.

Problem 1:

The web app should produce results very similar to the example images shown in the homework description.  When first opened, a database is created for the user in the 'uploads' directory.  The 'home' (index) page displays all unique collection names the user has in the database.  
The 'upload' page allows the user to upload a .bib file with a collection name.  If the collection name is not entered, this field is saved as an empty string in the directory.  Finally, the 'query' page allows the user to search the database using SQL command strings.  All pages on the app are rendered from .html files kept in the 'templates' directory; 'base_template.html' gives each page a common heading of links to the other pages.

Problem 2:

A .travis.yml file is kept in the python-ay250-homeworks directory, which should have Travis CI run the hw8_fortravis.py script and give code coverage results.
