import cv2
import numpy as np

input_image_file_format = 'data/L/{:03d}.png'
template_image_file = 'data/templates/ayat_marker.png'
ayah_per_page_file = open('data/ayah_per_page.txt')
ayah_per_page = [int(x) for x in ayah_per_page_file.read().split(', ')]
print len(ayah_per_page)

def process_page(page):
    input_image_file = input_image_file_format.format(page)
    # print input_image_file
    template_image = cv2.imread(template_image_file, 0)
    input_image_bgr = cv2.imread(input_image_file)
    input_image_gray = cv2.cvtColor(input_image_bgr, cv2.COLOR_BGR2GRAY)
    input_image_edge = cv2.Canny(input_image_gray, 100, 200)
    template_image_edge = cv2.Canny(template_image, 100, 200)
    cv2.imshow('template', template_image_edge)
    cv2.imshow('input', input_image_edge)
    res = cv2.matchTemplate(input_image_edge, template_image_edge, cv2.TM_CCOEFF_NORMED)
    # cv2.namedWindow('res', cv2.WINDOW_NORMAL)
    # cv2.imshow('res', res)

    tH, tW = template_image.shape
    threshold = 0.2
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
    for page in range(3, 605):
        error_detected = process_page(page)
        if error_detected:
            break
        else:
            print("processed", page)

if __name__ == '__main__':
    main()