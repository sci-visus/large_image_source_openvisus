import os,sys
from pprint import pprint
import large_image
import large_image_source_openvisus

def SaveImage(filename, img):
  with open(filename,"wb") as f: 
    f.write(img)
  print(f"Saved image {filename}")

# ///////////////////////////////////////////////////////////////////////////////
if __name__ == '__main__' :
  source = large_image.open(sys.argv[1])
  metadata = source.getMetadata()
  pprint(metadata)

  # x,y
  # z is our resolution [0,levels-1]
  # frame could be like the time or the real z
  # bandCount
  
  img, mime_type = source.getRegion(
  # region=dict(left=0, top=50000, right=29280, bottom=50000+2048),
    output=dict(maxWidth=4096), 
    encoding='PNG')
  
  SaveImage(sys.argv[2],img)

