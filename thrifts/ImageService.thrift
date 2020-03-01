namespace py image_service

const string CONTENT_TYPE_JPEG = 'image/jpeg'
const string CONTENT_TYPE_PNG = 'image/png'
const string CONTENT_TYPE_GIF = 'image/gif'

enum ImageTypes{
    JPEG=1
    PNG=2
    GIF=3
}

struct Image {
    1: i32 id
    2: string filename
    3: i32 width
    4: i32 height
    5: string url
    6: optional string content_type
    7: string md5
}

exception InvaildOperation {
    1: i32 code
    2: string msg
}

service ImageService {
    oneway void SaveImage(1: Image image)
    list<Image> GetImages()
    Image GetImageById(1: i32 id)
}