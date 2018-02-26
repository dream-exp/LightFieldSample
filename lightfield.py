import cv2
import numpy as np
from glob import glob

src_folder_path = "./src/" # ソース画像がおいてあるディレクトリ指定
x_amount = 17 # 横方向の画像枚数
y_amount = 17 # 縦方向の画像枚数

file_amount = x_amount * y_amount

def import_images(path):
    for i in range(0, file_amount):
        im = cv2.imread(path + str(i) + ".png")
        if i == 0:
            images = np.zeros((y_amount, x_amount, im.shape[0], im.shape[1], 3))
        images[int(i / y_amount), i % x_amount] = im

    return images

def render(view_x, view_y, images, aperture, f_length):
    file_name = "./dst/output_ap" + str(aperture) + "_fl" + str(f_length) +".png"
    aperture = (100 - int(aperture)) / 100
    f_length = int(f_length)
    slice_images = images[int(view_y - y_amount * aperture * 0.5):int(view_y + y_amount * aperture * 0.5), int(view_x - x_amount * aperture * 0.5):int(view_x + x_amount * aperture * 0.5)]

    slice_x_amount = slice_images.shape[0]
    slice_y_amount = slice_images.shape[1]

    image_width = slice_images[0][0].shape[0]
    image_height = slice_images[0][0].shape[1]

    # print(slice_images)

    sum_image = np.zeros((image_width, image_height, 3))
    sum_count = 0

    for x in range(0, slice_x_amount):
        for y in range(0, slice_y_amount):
            # print("x:" + str(x) + ", y:" + str(y))
            
            if f_length < 0:
                minus_flag = True
            else:
                minus_flag = False


            padding = int(abs(f_length) / 10)
            focal_image = np.zeros((slice_images[0, 0].shape[0] + 2 * f_length, slice_images[0, 0].shape[1] + 2 * f_length, 3))
            
            if not minus_flag:
                if x < slice_x_amount/2 and y < slice_y_amount/2: # 左上
                    sum_image[0:image_width - padding, 0:image_height - padding] += slice_images[x][y][padding:image_width, padding:image_height]
                    sum_count += 1
                elif x > slice_x_amount/2 and y < slice_y_amount/2: # 右上
                    sum_image[padding:image_width, 0:image_height - padding] += slice_images[x][y][0:image_width - padding, padding:image_height]
                    sum_count += 1
                elif x < slice_x_amount/2 and y > slice_y_amount/2: # 左下
                    sum_image[0:image_width - padding, padding:image_height] += slice_images[x][y][padding:image_width, 0:image_height - padding]
                    sum_count += 1
                elif x > slice_x_amount/2 and y > slice_y_amount/2: # 右下
                    sum_image[padding:image_width, padding:image_height] += slice_images[x][y][0:image_width - padding, 0:image_height - padding]
                    sum_count += 1
            else:
                if x < slice_x_amount/2 and y < slice_y_amount/2: # 左上
                    sum_image[padding:image_width, padding:image_height] += slice_images[x][y][0:image_width - padding, 0:image_height - padding]
                    sum_count += 1
                elif x > slice_x_amount/2 and y < slice_y_amount/2: # 左上
                    sum_image[0:image_width - padding, padding:image_height] += slice_images[x][y][padding:image_width, 0:image_height - padding]
                    sum_count += 1
                elif x < slice_x_amount/2 and y > slice_y_amount/2: # 左下
                    sum_image[padding:image_width, 0:image_height - padding] += slice_images[x][y][0:image_width - padding, padding:image_height]
                    sum_count += 1
                elif x > slice_x_amount/2 and y > slice_y_amount/2: # 左下
                    sum_image[0:image_width - padding, 0:image_height - padding] += slice_images[x][y][padding:image_width, padding:image_height]
                    sum_count += 1

                # focal_image[x:slice_images[x][y].shape[0] + x, y:slice_images[x][y].shape[1] + y] += slice_images[x][y]
            # print(focal_image[x:slice_images[x][y].shape[0] + x, y:slice_images[x][y].shape[1] + y].shape)
            # elif x > slice_images.shape[0]/2 and y < slice_images.shape[1]/2: #右上
            # elif x < slice_images.shape[0]/2 and y > slice_images.shape[1]/2: # 左下
            # elif x > slice_images.shape[0]/2 and y > slice_images.shape[1]/2: # 右下

    sum_image /= sum_count

    print(sum_count)

    # sum_image = cv2.bilateralFilter(sum_image.astype(np.float32), 100, 1, 1)
    # sum_image = cv2.GaussianBlur(sum_image.astype(np.float32), (11, 11), 0)

    cv2.imwrite(file_name, sum_image)
    print("output " + file_name)


if __name__ == '__main__':
    if src_folder_path[:-1] != '/':
        src_folder_path += '/'

    multi_view_images = import_images(src_folder_path)

    # while True:
    #     aperture = input('input aperture value(0 - 99) >>> ')
    #     f_length = input('input focal length value(Even & 0 - 100) >>> ')

    #     render(9, 9, multi_view_images, aperture, f_length)

    for i in range(0, 101, 10):
        for j in range(-50, 51, 5):
            render(9, 9, multi_view_images, i, j)
