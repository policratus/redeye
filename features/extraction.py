"""
Contains classes for feature extraction
"""
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
        first_image = self.to_array(self.open_image(first_file), 'float32')
        assumed_size_images = first_image.shape

        image_array = first_image

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
                    self.from_array(
                        self.to_array(image_array, 'uint8')
                    ), path + '/mean_image.png'
                )

                break
