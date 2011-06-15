# This module distorts images
from PIL import Image, ImageOps

def distort(filename2,bbox,fsz,akshar):
	#temp_image=Image.open(filename2)
	#distort1 = ImageOps.mirror(temp_image)
	filename=filename2.split('.tif')[0]+"_1"+".tif"
	#distort1.save(filename,"TIFF")
	#distort2=Image.open(filename2)
	

	del_X=bbox[2]-bbox[0]
	strip=[bbox[0]+del_X*.2,bbox[0]+del_X*.4,bbox[0]+del_X*.7]
	for values in range(0,3):
		distort2=Image.open(filename2)
		for y in range(bbox[1],bbox[3]):
			for x in range(strip[values],strip[values]+4):
				distort2.putpixel((x,y),255)
		filename=filename2.split('.tif')[0]+"_"+str(values)+".tif"
		distort2.save(filename,"TIFF")
		line=akshar+" "+str(bbox[0])+" "+str(bbox[1])+" "+str(bbox[2])+" "+str(bbox[3]) # this is the line to be added to the box file
		boxfile=filename.split('.tif')[0]+"box"
		f=open(boxfile,"w") #open new file
		f.write(line+'\n')
		f.close()
        	
	
	
	
