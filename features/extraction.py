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
