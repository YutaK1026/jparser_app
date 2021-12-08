import cv2
import math
import numpy as np


def angle(pt1, pt2, pt0) -> float:
    dx1 = float(pt1[0,0] - pt0[0,0])
    dy1 = float(pt1[0,1] - pt0[0,1])
    dx2 = float(pt2[0,0] - pt0[0,0])
    dy2 = float(pt2[0,1] - pt0[0,1])
    v = math.sqrt((dx1*dx1 + dy1*dy1)*(dx2*dx2 + dy2*dy2) )
    return (dx1*dx2 + dy1*dy2)/ v

def coordinates_control(Colist):
    point_list = [[int(Colist[0]),int(Colist[1])],[int(Colist[2]),int(Colist[3])],[int(Colist[4]),int(Colist[5])],[int(Colist[6]),int(Colist[7])]]
    point_x_list = [point_list[0][0]*point_list[0][1],point_list[1][0]*point_list[1][1],point_list[2][0]*point_list[2][1],point_list[3][0]*point_list[3][1]]
    point_return_list = []
    point_x_list = sorted(point_x_list,reverse=True)
    for i in range(4):
        for j in range(4):
            if point_x_list[i] == point_list[j][0] * point_list[j][1]:
                point_return_list.append(point_list[j][0])
                point_return_list.append(point_list[j][1])
                break  
    point_return_list[0],point_return_list[1],point_return_list[2],point_return_list[3],point_return_list[4],point_return_list[5],point_return_list[6],point_return_list[7] = point_return_list[6],point_return_list[7],point_return_list[4],point_return_list[5],point_return_list[0],point_return_list[1],point_return_list[2],point_return_list[3]
    min_distance = (point_return_list[0]-point_return_list[6])**2 + (point_return_list[1]-point_return_list[7])**2
    max_distance = (point_return_list[0]-point_return_list[2])**2 + (point_return_list[1]-point_return_list[3])**2
    if min_distance > max_distance:
        point_return_list[2],point_return_list[3],point_return_list[6],point_return_list[7] = point_return_list[6],point_return_list[7],point_return_list[2],point_return_list[3]
    return point_return_list
    
def findSquares(bin_image, image, cond_area = 1000):
    contours, _ = cv2.findContours(bin_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for i, cnt in enumerate(contours):
        arclen = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, arclen*0.02, True)
        area = abs(cv2.contourArea(approx))
        if approx.shape[0] == 4 and area > cond_area and cv2.isContourConvex(approx) :
            maxCosine = 0
            for j in range(2, 5):
                cosine = abs(angle(approx[j%4], approx[j-2], approx[j-1]))
                maxCosine = max(maxCosine, cosine)
            if maxCosine < 0.3 :
                rcnt = approx.reshape(-1,2)
                cv2.polylines(image, [rcnt], True, (0,0,255), thickness=2, lineType=cv2.LINE_8)
    return image,rcnt



def coordinates(image):
    image = cv2.resize(image , dsize=(1108, 1478))
    if image is None :
        exit(1)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    rimage,rcnt = findSquares(bw, image)
    s = "".join(map(str, rcnt))
    s = s.replace("]"," ")
    s = s.replace("["," ")
    l = [x.strip() for x in s.split(' ')]
    coordinates_list = []
    for i in range(len(l)):
        S = ''.join(filter(str.isalnum, l[i]))
        coordinates_list.append(S)
    coordinateslist = [a for a in coordinates_list if a != '']
    return coordinateslist

def main(image):
    source_image = cv2.resize(image , dsize=(1108, 1478))
    CooList= coordinates_control(coordinates())
    source_corners = np.array([(int(CooList[0]),int(CooList[1])),(int(CooList[2]),int(CooList[3])),(int(CooList[4]),int(CooList[5])),(int(CooList[6]),int(CooList[7]))])
    width, height = 1074,1512
    target_corners = np.array([(0, 0), (0,height),(width, height), (width, 0)])    
    H, _ = cv2.findHomography(source_corners, target_corners, cv2.RANSAC)
    transformed_image = cv2.warpPerspective(
        source_image, H, (source_image.shape[1], source_image.shape[0]))
    img= cv2.imwrite('Square_Detector.jpg', transformed_image)
    print(CooList)
    c = cv2.waitKey()
    return  img

if __name__ == '__main__':
    main()