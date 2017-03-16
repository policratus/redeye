"""
Contains classes for feature extraction
"""
from cv2 import cornerHarris, dilate
from sklearn import decomposition
from sklearn.cluster import KMeans
from basic import image_basic


class ExtractFeaturesImage(image_basic.FilterImage):
    """
    Encapsulates methods for extract image features
    """
    def dominant_colors(self, image, number_of_colors=3):
        """
        Return the most relevant colors in image
        """
        if image.mode != 'RGB':
            image = image.convert('RGB')

        cluster = 0

        kmeans = KMeans(number_of_colors)

        image = self.resize(image, 200, 200)

        image_array = self.to_array(image)

        kmeans.fit(
            [
                pixel
                for pixel_line in image_array
                for pixel in pixel_line
            ]
        )

        centers = kmeans.cluster_centers_

        centers = centers.astype(int)

        for color in centers:
            cluster += 1
            print "[DOMINANT COLORS]: Color #{cluster_num} (RGB): {RGB}".format(
                cluster_num=cluster,
                RGB=color
            )

    def simple_mean_image(self, path):
        """
        Generate a mean image taking in some assumptions:
            1. All images analyzed has the same size
            2. All images are normalized (centralized, cropped) on the
                object been analyzed (faces or animals, for instance)
            3. Image with different size than first one read will be discarded
            4. The path parameter must point to a directory with more than one recognizable
                image. Otherwise, will be returned the input image.
        """
        count_images = 1

        files = iter(self.file_list(path))

        first_file = files.next()
        first_image = self.open_image(first_file)
        assumed_size_images = self.image_shape(first_image)

        image_array = self.to_array(first_image, 'float32')

        print 'Assuming that other images has size {0} x {1}'.format(
            assumed_size_images[1],
            assumed_size_images[0]
        )

        while True:
            try:
                next_image = self.to_array(self.open_image(files.next()), 'float32')

                if assumed_size_images == next_image.shape:
                    image_array += next_image
                    count_images += 1
            except StopIteration:
                image_array /= count_images

                self.save(
                    self.array_to_image(
                        self.to_array(image_array, 'uint8')
                    ), path + '/mean_image.png'
                )

                break

    def simple_eigen_images(self, path):
        """
        Creates a plot image of eigen images. Useful on normalized object
        recognition

        Parameters
        ----------
        path: str
            The filesystem path to analyze images
        """
        max_eigen_images = 30
        max_images_to_analyze = 1000

        files = self.file_list(path)

        if files:
            if len(files) > max_eigen_images or \
                    len(files) > max_images_to_analyze:
                print 'Image database is too large. Generating only first {0} eigen images'.format(
                    max_eigen_images
                )

                components = max_eigen_images
            else:
                components = len(files)

            files = iter(files)
            first_file = files.next()

            first_image = self.color_space(self.open_image(first_file), 'greyscale')
            assumed_size_images = self.image_shape(first_image)

            image_array = self.to_array([self.to_array(first_image).flatten()])

            analyzed_images = 0
            while analyzed_images <= max_images_to_analyze:
                try:
                    next_image = self.to_array(
                        self.to_array(
                            self.color_space(
                                self.open_image(files.next()),
                                'greyscale'
                            )
                        )
                    )

                    if assumed_size_images == next_image.shape:
                        image_array = self.append_arrays(
                            (
                                image_array,
                                self.to_array([next_image.flatten()])
                            )
                        )

                    analyzed_images += 1
                except StopIteration:
                    break

            image_array = self.flattened_images_centering(image_array)

            pca = decomposition.PCA(
                n_components=components,
                svd_solver='randomized',
                whiten=True
            )

            pca.fit_transform(image_array)

            self.save_image_gallery(
                path,
                'Eigenimages',
                pca.components_,
                shape=assumed_size_images,
                prefix='eigen_images'
            )
        else:
            print 'No files found to generate eigen images'

    def simple_corner_detection(self, image):
        """
        Detects corners using Harris corner detection
        algorithm

        Parameters
        ----------
        image: PIL Image object
        """
        if image.mode != 'RGB':
            image = self.color_space(
                image,
                'color',
                size=2**16
            )

        if image.mode != 'L':
            gray_image = self.color_space(image, 'greyscale')
        else:
            gray_image = image

        dilate_kernel = self.matrix_of_ns(5, 1)

        dilated_image = dilate(
            cornerHarris(
                self.to_array(
                    gray_image,
                    array_type='float32'
                ),
                blockSize=2,
                ksize=3,
                k=0.04
            ),
            dilate_kernel
        )

        image = self.to_array(image)

        image[
            dilated_image > 0.05 * dilated_image.max()
        ] = [255, 153, 51]

        return self.array_to_image(image)
