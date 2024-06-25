
import os,sys,math
import numpy as np

import large_image
from large_image.cache_util import LruCacheMetaclass, methodcache

import OpenVisus as ov

# ///////////////////////////////////////////////////////////////////////////////////
class OpenVisusTileSource(large_image.tilesource.TileSource, metaclass=LruCacheMetaclass):

	cacheName = 'tilesource'
	name = 'openvisus'
 
	min_tile_pixels =256*256

	extensions = {
	  None: large_image.constants.SourcePriority.LOW,
	  'idx': large_image.constants.SourcePriority.PREFERRED,
	}

	# constructor
	def __init__(self, item=None, *args, **kwargs):

		# doto
		#from large_image.cache_util import cachesClear,cachesInfo
		#cachesClear()
		#cachesInfo()

		print(f"OpenVisusTileSource::__init__({item},args={args}, kwargs={kwargs})")

		if not kwargs.get('encoding'):
				kwargs = kwargs.copy()
				kwargs['encoding'] = 'PNG'

		super().__init__(item, *args, **kwargs)

		from girder.models.file import File
		file = File().load(item['largeImage']['fileId'], force=True)
		print("girder file",file)

		# local file
		try:
			url = str(self._getLargeImagePath()).strip()
			assert(os.path.isfile(url))
		
		# s3 file
		except:

			assetstore=File().getAssetstoreAdapter(file).assetstore

			service    = assetstore['service']
			region     = assetstore['region']
			prefix     = assetstore['prefix']
			bucket     = assetstore['bucket']
			access_key = assetstore['accessKeyId']
			secret_key = assetstore['secret']
			s3Key      = file['s3Key']

			endpoint_url=f"https://{service}/{prefix}" if prefix else f"https://{service}"

			# compose url
			url=f"{endpoint_url}/{bucket}/{s3Key}?"
			if access_key:   url+=f"&access_key={access_key}"
			if secret_key:   url+=f"&secret_key={secret_key}"
			if region:       url+=f"&region={region}"
			if endpoint_url: url+=f"&endpoint_url={endpoint_url}"

			# TODO: caching is always enabled (!)
			url+="&cached=arco"

		print(f"LoadDataset url={url}")
		self.db=ov.LoadDataset(url)
		self.bitmask=self.db.getBitmask().toString()
		self.access=self.db.createAccessForBlockQuery()
		print(self.bitmask)
		self.sizeY,self.sizeX=self.db.shape

		# TODO?
		assert('2' not in self.bitmask) 
		self.levels=1
		self.tileWidth =2**len([it for it in self.bitmask if it=='0'])
		self.tileHeight=2**len([it for it in self.bitmask if it=='1'])
		print(f"pow2 size {self.tileWidth} {self.tileHeight}")

		# i.e. I DO NOT want V....1111 or V....000 otherwise the tile size cannot be constant
		assert(self.bitmask.endswith("01") or self.bitmask.endswith("10"))
		
		# the right part must be 01 or 10 this to keep the tile size constant
		s=self.bitmask
		while (s.endswith("01") or s.endswith("10")):
    
			# do not go too small
			if self.tileWidth*self.tileHeight<=self.min_tile_pixels:
				break
  
			self.tileWidth >>=1
			self.tileHeight>>=1
			self.levels+=1
			s=s[0:-2]
  

		print(f"tile size {self.tileWidth} {self.tileHeight}")
		self.minLevel = 0
		self.maxLevel = self.levels-1
  
		#self.dtype=self.db.getField().dtype
		#self.bandCount=1
  
		# TODO
		# fields? how to support multiple fields?
		# bands?  I think I just return the image
		# frames? could be 3d or with time, I do not think both
		#         if 3d then I need to make sure the Z samples are all on the left, like V22220101010101....
		
	# canRead
	@classmethod
	def canRead(cls, *args, **kwargs):
		return True

	# getMetadata
	def getMetadata(self):
		return super().getMetadata()

	# getTile
	@methodcache()
	def getTile(self, x, y, z, *args, **kwargs):
   
		# I am always returning numpy arrays
		assert(kwargs.get("numpyAllowed","always")=="always")
  
		# todo
		assert(kwargs.get("frame",None) is None)

		max_resolution=len(self.bitmask)-1
		dx=self.tileWidth
		dy=self.tileHeight
		for L in range(self.maxLevel,z,-1):
			dx<<=1
			dy<<=1
			max_resolution-=2
	
		x1 = x*dx
		y1 = y*dy
		x2 = min(x1+dx,self.sizeX)
		y2 = min(y1+dy,self.sizeY)
  
		# mirror y
		y1,y2=self.sizeY-y2,self.sizeY-y1

		print(f"getTile x={x} y={y} z={z} tileWidth={self.tileWidth} tileHeight={self.tileHeight} x1={x1} y1={y1} x2={x2} y2={y2} max_resolution={max_resolution}")
		tile=self.db.read(x=[x1,x2],y=[y1,y2],max_resolution=max_resolution, access=self.access)
		# can be smaller because I am on the boundary
		assert(tile.shape[0]<=self.tileHeight and tile.shape[1]<=self.tileWidth)

		# mirror
		tile=np.flip(tile, axis=0)
	
		return self._outputTile(tile, large_image.constants.TILE_FORMAT_NUMPY, x, y, z, **kwargs)

	@staticmethod
	def getLRUHash(*args, **kwargs):
		return "openvisus-" + super(OpenVisusTileSource, OpenVisusTileSource).getLRUHash(*args, **kwargs)

# //////////////////////////////////////////////////////////////
def open(*args, **kwargs):
	return OpenVisusTileSource(*args, **kwargs)

# //////////////////////////////////////////////////////////////
def canRead(*args, **kwargs):
	return OpenVisusTileSource.canRead(*args, **kwargs)

