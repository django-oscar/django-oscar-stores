# SRID that ist used for distance calculations. If a geodetic coordinate
# system is used to calculate distances in kilometers, miles, etc. this
# SRID will be used to transform the geometries into a geographic
# coordinate system. There are many different SRIDs that can be used. I
# recommend taking a look at http://spatialreference.org/ to find the one
# that is most suitable for you.
# We use Autstralian Albers here (http://spatialreference.org/ref/epsg/3577/)
STORES_GEOGRAPHIC_SRID = 3577
STORES_GEODETIC_SRID = 4326

STORES_SETTINGS = dict(
    [(k, v) for k, v in locals().items() if k.startswith('STORES_')]
)
