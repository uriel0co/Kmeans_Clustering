from point import Point


class Cluster:
    def __init__(self, cluster_id, initial_point):
        self.id = cluster_id
        self._centroid = Point(str(cluster_id) + '_center')
        #  IMPORTANT NOTE: data type of _points changed from dict to list because of name issues
        self._points = [initial_point]  # List of Point object
        self.compute_centroid()

    def compute_centroid(self):
        """
        Function to recompute new centroid of current points
        :return: Boolean value showing if centroid changed
        """
        if not self._points:
            print("Can't compute center without points")
            return

        def mean(values):
            # this function calculates the average of the values in the list
            mean_of_values = sum(values) / len(values)
            return mean_of_values


        def median(values):
            # this function calculates the median of the list
            values = sorted(values)
            length = len(values)
            index = int(length / 2)
            if length % 2 == 0:
                return mean([values[index], values[index - 1]])
            else:
                return values[index]


        # Saving old state
        old_centroid = tuple(self._centroid.coordinates)

        # We set new center as vector of zeroes. Length of the vector depends on number of coordinates
        number_of_coordinates = len(self._points[0].coordinates)
        new_coordinates = {}
        for i in range(number_of_coordinates):
            new_coordinates[i] = []

        # Now go through each point and add it's coordinates to the center
        for point in self._points:
            for coordinate_index, coordinate_value in enumerate(point.coordinates):
                new_coordinates[coordinate_index].append(coordinate_value)
        list_of_coordinates = []
        for coordinate_index in new_coordinates:
            list_of_coordinates += [median(new_coordinates[coordinate_index])]

        # Divide to find mean

        self._centroid.set_coordinates(list_of_coordinates)

        is_changed = (old_centroid != tuple(self._centroid.coordinates))
        return is_changed



    def add_point(self, point):
        """
        Add point to the cluster
        :param point: Point to add
        """
        self._points.append(point)

    def remove_point(self, point=None):
        """
        Remove given point from the cluster. If point isn't provided then cluster is cleared.
        :param point: Point to remove or nothing
        """
        if not point:
            self._points = []
        elif point not in self._points:
            print('Point with name {} does not belong to cluster {}'.format(point.name, self.id))
        else:
            self._points.remove(point)

    def print(self):
        print('############################################')
        print('Cluster:', self.id)
        print('Number of points:', len(self._points))
        print('Centroid:', self._centroid.coordinates)
        print('Points:', ' '.join(sorted([x.name for x in self._points])))

    def compute_loss(self):
        distances = [self._centroid.distance_to(point.coordinates) for point in self._points]
        return sum(distances)

    def compute_SSE(self):
        errors = [self._centroid.distance_to(point.coordinates)**2 for point in self._points]
        return sum(errors)

    @property
    def centroid(self):
        return self._centroid.coordinates

    @property
    def number_of_points(self):
        return len(self._points)
