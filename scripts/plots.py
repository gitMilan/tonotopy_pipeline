
import numpy as np
import nibabel as nb
import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('SVG')


def tonotopy_plot(nii_file_path, start, stop, save_path):
    """ Creates a tonotopic plot from a nii_file. """
    # start, stop = start, stop
    nii_loaded = nb.load(nii_file_path)
    nii_fdata = nii_loaded.get_fdata()

    def average_slices(start, stop, niidata):
        """ Averages multiple nii file slices. """
        slices = []
        for x in range(start, stop + 1):
            slices.append(niidata[:, :, x])

        return np.mean(slices, axis=0)

    def transform_matrix(matrix):
        """ Transforms the matrix. """
        rotated = np.rot90(matrix)
        flipped = np.fliplr(rotated)
        return flipped

    aver = average_slices(start, stop, nii_fdata)
    transformed = transform_matrix(aver)
    transformed[transformed == 0.0] = np.nan

    def plot(map, save_path):
        """ Plot a nii matrix. """
        ticks = np.linspace(np.nanmin(map),
                            np.nanmax(map), 6, endpoint=True)
        fig, ax = plt.subplots()

        plt.xticks([])
        plt.yticks([])
        cax = ax.imshow(map, cmap='jet_r')
        cbar = fig.colorbar(cax, ticks=ticks, orientation='horizontal', aspect=70)
        x_axis = ['1/4', '1/2', '1', '2', '4', '8']
        cbar.ax.set_xticklabels(x_axis)
        cbar.ax.set_title('kHZ')

        plt.ylim([70, 25])
        # output_dir = config.path_to_files["output_dir"]
        save_name = os.path.join(save_path)
        plt.savefig(save_name)

    plot(transformed, save_path)

    # return transformed