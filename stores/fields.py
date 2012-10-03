class Point(object):

    def __init__(self, x, y=None):
        """
        The Point object may be initialized with either a tuple, or individual
        parameters.

        For Example:
        >>> p = Point((5, 23)) # 2D point, passed in as a tuple
        """
        if isinstance(x, (tuple, list)):
            # Here a tuple or list was passed in under the `x` parameter.
            ndim = len(x)
            coords = x
        elif isinstance(x, (int, long, float)) and isinstance(y, (int, long, float)):
            # Here X, Y, and (optionally) Z were passed in individually, as parameters.
            ndim = 2
            coords = [x, y]
        else:
            raise TypeError('Invalid parameters given for Point initialization.')

        if ndim != 2:
            raise TypeError('Invalid point dimension: %s' % str(ndim))

        self.x = coords[0]
        self.y = coords[1]
        self.ndim = ndim

    def __iter__(self):
        """
        Allows iteration over coordinates of this Point.
        """
        for coord in self.coords:
            yield coord

    def __len__(self):
        """
        Returns the number of dimensions for this Point.
        """
        return self.ndim

    def __repr__(self):
        return unicode(self)

    def __unicode__(self):
        return "Point(%s, %s)" % self.coords

    @property
    def coords(self):
        """
        Returns a tuple of the point.
        """
        return (self.x, self.y)

    @coords.setter
    def coords(self, value):
        """
        Sets the coordinates of the point with the given tuple.
        """
        self.x, self.y = value
