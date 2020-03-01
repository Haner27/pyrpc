from handlers import RegisterService
from thrifts.image_service import ImageService


class ImageServiceHandler(metaclass=RegisterService):
    REGISTER_NAME = 'Image'
    SERVICE = ImageService

    def __init__(self):
        self.images = []

    def SaveImage(self, image: ImageService.Image):
        self.images.append(image)

    def GetImages(self) -> [ImageService.Image]:
        return self.images

    def GetImageById(self, id: int) -> ImageService.Image or None:
        for image in self.images:
            if id == image.id:
                return image
        return None
