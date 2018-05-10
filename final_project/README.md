final_project README

My version of the sparse coding algorithm (see first markdown cell) is contained in 'finalproject_notebook.ipynb'.  Some parts of the algorithm (namely the gradient descent process used to minimize the vector of weights at each step) require the use of for loops.  In order to speed up this process, in-line 'Cython magic' was used in the cell defining the functions.

Unfortunately, I did not find a combination of batch size and basis function learning rate that reproduces the desired result in a timely fashion.  For reference, the original paper uses a batch size of 100 image presentations, updating the basis functions after each batch with a learning rate of eta ~ 6.0.  This required on the order of 1000 batches before a stable solution was reached, and my code does not run that quickly.

This still provides a good framework for training these artificial neurons on images, and it lets you watch the neurons' receptive fields evolve over time.  Some other ways to speed up the code: some parts with for loops can be vectorized; for example, a vector of training image patches and an array of weight vectors could be sent off to the energy/cost minimization step rather than one weight vector at a time.  This step could also be parallelized, as all the iterations in each batch are independent (I tried this, but multi-threading on my CPU didn't seem to help; I think GPU parallelization is good for optimization algorithms?).  Also, a few steps can be written more succintly with the appropriate numpy operations.

The images used for training are in the 'IMAGES.mat' file; these are the same used by Olshausen, after the preprocessing described in the 1996 paper.
