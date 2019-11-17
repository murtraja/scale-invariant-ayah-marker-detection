import cv2
import numpy as np
template = cv2.imread('data/templates/ayat_marker_mask.png')
template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
mask = np.logical_and.reduce((template[:,:,0] == 0, template[:,:,1] == 0, template[:,:,2] == 255))
template_gray[:,:] = 0
template_gray[mask] = 255

cv2.imshow('d', template_gray)
cv2.imwrite('binary_mask.png', template_gray)
cv2.waitKey(0)
cv2.destroyAllWindows()