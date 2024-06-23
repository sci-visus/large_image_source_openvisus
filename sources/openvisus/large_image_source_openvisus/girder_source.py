from girder_large_image.girder_tilesource import GirderTileSource

from . import OpenVisusTileSource

# //////////////////////////////////////////////////////////////////////////////////
class OpenVisusGirderTileSource(OpenVisusTileSource, GirderTileSource):

    cacheName = 'tilesource'
    name = 'openvisus'

    @staticmethod
    def getLRUHash(*args, **kwargs):
        return "openvisus-" + super(OpenVisusGirderTileSource, OpenVisusGirderTileSource).getLRUHash(*args, **kwargs)