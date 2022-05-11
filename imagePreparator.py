from PIL import Image

class ImagePreparator():
    def cutImage(self, imagePath):
        with Image.open(imagePath) as im:
            box = (250, 0, 1695, 1040)
            im_croped =  im.crop(box)
            im_croped.save('screenshot.png')