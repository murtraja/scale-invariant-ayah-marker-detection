import cv2
import numpy as np
from correct_ayah import ayah_per_page
from match_template_helper import process_result_points

input_image_file_format = 'data/L/{:03d}.png'
template_image_file = 'data/templates/ayat_marker.png'
output_image_file_format = 'data/output/images/{:03d}.png'
output_coords_file_format = 'data/output/coords/{:03d}.txt'

# img_bgr = cv2.imread("data/L/021.png")
# img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

# tl = cv2.imread('data/templates/ayat_marker_compact.png', 0)
# tH, tW = tl.shape

def resize_image(img, r):
    new_h = int(img.shape[0]*r)
    new_w = int(img.shape[1]*r)
    resized_image = cv2.resize(img, (new_w, new_h))
    return resized_image

# r = 0.95
# img = resize_image(img_gray, r)
# res = cv2.matchTemplate(img, tl, cv2.TM_CCOEFF_NORMED)
# points = process_result(res, 0.5)
# for pt in points:
#     print pt
#     cv2.rectangle(img, pt, (pt[0] + tW, pt[1] + tH), (0,0,255), 2)
# cv2.imshow('i', img)
# print len(points)
# print ayah_per_page[20]

# cv2.waitKey(0)
# cv2.destroyAllWindows()





















def process_page(page):
    
    template_image = cv2.imread(template_image_file, 0)
    tH, tW = template_image.shape

    input_image_file = input_image_file_format.format(page)
    input_image_bgr = cv2.imread(input_image_file)
    input_image_gray = cv2.cvtColor(input_image_bgr, cv2.COLOR_BGR2GRAY)
    
    r_max = 1.2
    r_delta = 0.05
    r_min = 0.8
    threshold = 0.5
    actual_pts = []
    for r in np.arange(r_max, r_min, -r_delta):
        print ("page {}, r {}".format(page, r))
        img = resize_image(input_image_gray, r)
        res = cv2.matchTemplate(img, template_image, cv2.TM_CCOEFF_NORMED)
        loc_unnormalized = np.where( res >= threshold)
        loc = []
        for i in [0, 1]:
            loc.append(np.round(loc_unnormalized[i]/r).astype(np.int64))
        # loc = np.round(loc*float(r)).astype(np.int64)
        located_points = zip(*loc[::-1])
        if len(located_points) > 0:
            actual_pts = process_result_points(located_points, actual_pts)

        
        # display_img = input_image_bgr.copy()
        # for pt in actual_pts:
        #     cv2.rectangle(display_img, pt, (pt[0] + tW, pt[1] + tH), (0,0,255), 2)
        # cv2.namedWindow('i', cv2.WINDOW_NORMAL)
        # cv2.imshow('i', display_img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        
        if len(actual_pts) == ayah_per_page[page-1]:
            # output useful information here
            print ("page", page, "processed in r", r)
            for pt in actual_pts:
                cv2.rectangle(input_image_bgr, pt, (pt[0] + tW, pt[1] + tH), (0,0,255), 2)
            cv2.imwrite(output_image_file_format.format(page), input_image_bgr)
            points_txt = "\n".join([str(x)+' '+str(y) for (x,y) in actual_pts])
            print points_txt
            with open(output_coords_file_format.format(page), 'w') as f:
                f.write(points_txt)
            return;
    # even after downsampling, still not able to find
    found = len(actual_pts)
    required = ayah_per_page[page-1]
    print("required markers {} but found {}".format(required, found))
    return True

# 18, 21, 455, 591
def main():
    for page in range(1, 605):
        error_detected = process_page(page)
        if error_detected:
            break
        else:
            print("processed", page)

if __name__ == '__main__':
    main()