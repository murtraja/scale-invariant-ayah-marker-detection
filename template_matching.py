import cv2
import numpy as np
import math

input_image_file_format = 'data/L/{:03d}.png'
template_image_file = 'data/templates/ayat_marker.png'
template_image_mask_file = 'data/templates/binary_mask.png'
ayah_per_page_file = open('data/ayah_per_page.txt')
ayah_per_page = [int(x) for x in ayah_per_page_file.read().split(', ')]
print len(ayah_per_page)

def matchTemplate(img, tl_unmasked, tlmask):
    iH, iW = img.shape
    res = np.zeros((iH, iW))
    tl = tl_unmasked.copy()
    masked_indices = np.argwhere(tlmask == 255)
    tl_size = len(list(masked_indices))
    tl[masked_indices] = 0
    
    tldash = tl.copy()
    tldash = tldash.astype(np.float64)
    tH, tW = tl.shape
    sum_template = float(np.sum(tl))
    tldash[masked_indices] = tl[masked_indices] - sum_template/tl_size

    sum_template_squares = np.sum(tldash**2)
    for i in range(iH-tH):
        for j in range(iW-tW):
            img_patch = img[i:i+tH, j:j+tW].copy()
            img_patch[masked_indices] = 0
            img_patch_dash = img_patch.astype(np.float64)
            sum_img = np.sum(img_patch)
            numerator = 0.0
            img_patch_dash[masked_indices] = img_patch[masked_indices] - sum_img/(tl_size)
            numerator = np.sum(img_patch_dash*tldash)
            # for ii in range(tH):
            #     for jj in range(tW):
            #         img_patch_dash[ii,jj] = img_patch[ii,jj] - sum_img/(tH*tW)
            #         numerator += img_patch_dash[ii,jj]*tldash[ii,jj]
            sum_img_squares = np.sum(img_patch_dash**2)
            denominator = sum_img_squares*sum_template_squares
            denominator = math.sqrt(denominator)
            if denominator == 0:
                numerator = 0
                denominator = 1
            val = numerator/denominator
            if val < 0:
                val = 0
            res[i,j] = numerator/denominator
    return res



def process_page(page):
    input_image_file = input_image_file_format.format(page)
    # print input_image_file
    template_image = cv2.imread(template_image_file, 0)
    template_image_mask = cv2.imread(template_image_mask_file, 0)
    input_image_bgr = cv2.imread(input_image_file)
    input_image_gray = cv2.cvtColor(input_image_bgr, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('template', template_image_mask)
    # cv2.imshow('input', input_image_edge)
    res = matchTemplate(input_image_gray, template_image, template_image_mask)
    cv2.namedWindow('res', cv2.WINDOW_NORMAL)
    cv2.imshow('res', res)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # return
    tH, tW = template_image.shape
    threshold = 0.72
    loc = np.where( res >= threshold)
    # print("loc shape", loc)
    actual_pts = []
    located_points = zip(*loc[::-1])
    print ("length of located points", len(located_points))
    actual_pts.append(located_points[0])
    # distance_min = 10000
    for pt in located_points[1:]:
        a = pt[0]
        b = pt[1]
        distance = min([(a-x)**2+(b-y)**2 for (x,y) in actual_pts])
        
        # print("distance", distance)
        if distance < 100:
            # print("skipping", pt)
            continue
        actual_pts.append(pt)
        # print("appending", pt)
    # print("minimum distance", distance_min)
    if len(actual_pts) != ayah_per_page[page-1]:
        print("page", page, "incorrect ayahs detected", len(actual_pts), actual_pts, ayah_per_page[page-1])
        
        for pt in actual_pts:
            print pt
            cv2.rectangle(input_image_bgr, pt, (pt[0] + tW, pt[1] + tH), (0,0,255), 2)

        cv2.namedWindow('inp', cv2.WINDOW_NORMAL)
        cv2.imshow('inp', input_image_bgr)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return True

def main():
    for page in range(21, 22):
        error_detected = process_page(page)
        if error_detected:
            break
        else:
            print("processed", page)

if __name__ == '__main__':
    main()