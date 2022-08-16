from point_and_shoot import point, shoot
from superimpose import superimpose

def main():
    location = (0, 0)
    point.point(location)
    image = shoot.take_picture()
    shapefile = 0
    filtered_image = superimpose.filter_image(image, shapefile)
        
    


if __name__ == "__main__":
    main()
