import numpy as np
import numpy.linalg as la
import matplotlib.image as mpimg


def compress_image(filename : str, rgb_ranks : tuple[int, int, int] = (1, 1, 1)) -> None:
    """note this code keeps the transparency layer"""
    #reads image
    image = mpimg.imread(filename) \
                 .astype(np.float64) #converts all points to floats
    # converts image
    image = image if image.max <= 1 else image/255 
    # saves transparence layer
    transparent_layer = image[:, :, 3]
    #cuts out the transparent_layer
    image = image[..., :3] 

    # seprates all rgb channels
    rgb = (
        image[:, :, 0], 
        image[:, :, 1], 
        image[:, :, 2]
    ) 
    #runs svd on all rgb channels
    svdRgb = map(la.svd, rgb) 

    # recomputes the rgb channels with the given rank
    svdRgbApprox = tuple(
        map(
            lambda x : x[0][0][:, :x[1]] * x[0][1][:x[1]] @ x[0][2][:x[1]], #reconstruction for the given rank
            zip(svdRgb, rgb_ranks)
        )
    ) 
    #stacks all channels back together
    compressed_image = np.dstack((*svdRgbApprox, transparent_layer))

    #saves the image with the ranks in the file name 
    mpimg.imsave(
        f'{filename[:-4]}_rank_r_{rgb_ranks[0]}_g_{rgb_ranks[1]}_b_{rgb_ranks[2]}.png', 
        np.clip(compressed_image, 0., 1.)
    )

'''ive not only compressed the image but the code too'''
def compressImage(f,r):mpimg.imsave(f'{f[:-4]}Rr{r[0]}g{r[1]}b{r[2]}.png',np.clip((np.dstack(list(map(lambda x:x[0][0][:,:x[1]]*x[0][1][:x[1]]@x[0][2][:x[1]],zip(map(la.svd,[mpimg.imread(f).astype(np.float64)[...,:3][:,:,i] if mpimg.imread(f).astype(np.float64).max > 1 else mpimg.imread(f).astype(np.float64)[...,:3][:,:,i]/255 for i in range(3)]),r))))),0.,1.))
"""          fileanme^ |        |    image name^   limts the values between [0, 1]^       |      |    |       |     combines each rank to the matricie in a tuple^    |      |          |                   |          |      |          converts all values between [0, 1] ^                                                                |             |    |         |
                   rank^        |             compresses all rgb channels in to a 3d array^      |    |       |                   maps the svd decomp for each channel^      |          |                   |          |      |                                           this for loop creates a list with all rgb values in there on matrix^             |    |         |
                 saves the image^                converts to list as dstack doesnt like genertors^    |       |                                                    svd decomp^          |                   |          |      |                                                                                              this is 3 for the 3 rgb values^    |         |
                                                                        maps all values witht the rank^       |                                                          reads the image^                   |          |      |                                                                              the ranks that the rgb matricie will be zipped with^         |                                                                                 
                                                         creates the new approximate array with the given rank^                                                                converts all values to floats^          |      |                                                                                                the min and max value for the clip function^                                                                                
                                                                                                                                                                                                 selects all rgb values^      |                                                                                                                                                                                                                             
                                                                                                                                                                                selects the ith element of all row and columns^""" 