import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
#image to be modified has to be in the same directory as photoedit.py

def change_brightness(image, value):
    img = image.copy()
    img += value
    for r in range(len(img)):
        for c in range(len(img[0])):
            for i in range(3):
                if img[r][c][i]>255:
                    img[r][c][i] = 255
                if img[r][c][i] < 0:
                    img[r][c][i] = 0
                
    return img
  
def change_contrast(image, value):
    img = image.copy()
    F = (259*(value + 255))/(255*(259-value))
    for r in range(len(img)):
        for c in range(len(img[0])):
            for i in range(3):
                img[r][c][i] = F * (image[r][c][i] - 128) + 128
                if img[r][c][i]>255:
                    img[r][c][i] = 255
                if img[r][c][i] < 0:
                    img[r][c][i] = 0
    return img

def grayscale(image):
    img = image.copy() 
    for r in range(len(img)):
        for c in range(len(img[0])):
            for i in range(3):
                img[r][c][i] = 0.3*image[r][c][0] + 0.59*image[r][c][1] + 0.11*image[r][c][2]
                if img[r][c][i]>255:
                    img[r][c][i] = 255
                if img[r][c][i] < 0:
                    img[r][c][i] = 0
    return img

def blur_effect(image):
    K = [[0.0625, 0.125, 0.0625],
         [0.125, 0.25, 0.125],
         [0.0625, 0.125, 0.0625]]
    img = image.copy()
    for r in range(1, len(img)-1): #iterate thru rows of img
        for c in range(1, len(img[0])-1):
            for i in range(3):
                img[r][c][i] = (image[r-1][c-1][i] * K[0][0] + image[r-1][c][i] * K[0][1] + image[r-1][c+1][i] * K[0][2] 
                + image[r][c-1][i] * K[1][0] + image[r][c][i] * K[1][1] + image[r][c+1][i] * K[1][2]
                + image[r+1][c-1][i] * K[2][0] + image[r+1][c][i] * K[2][1] + image[r+1][c+1][i] * K[2][2])
    return img
            
        
               

def edge_detection(image):
    K = [[-1, -1, -1],
         [-1, 8, -1],
         [-1, -1, -1]]
    img = image.copy()
    for r in range(1, len(img) -1): #iterate thru rows of img
        for c in range(1, len(img[0]) -1):
            for i in range(3):
                img[r][c][i] = (image[r-1][c-1][i] * K[0][0] + image[r-1][c][i] * K[0][1] + image[r-1][c+1][i] * K[0][2] 
                + image[r][c-1][i] * K[1][0] + image[r][c][i] * K[1][1] + image[r][c+1][i] * K[1][2]
                + image[r+1][c-1][i] * K[2][0] + image[r+1][c][i] * K[2][1] + image[r+1][c+1][i] * K[2][2]) + 128

    for r in range(len(img)):
        for c in range(len(img[0])):
            for i in range(3):
                if img[r][c][i]>255:
                    img[r][c][i] = 255
                if img[r][c][i] < 0:
                    img[r][c][i] = 0
    return img

def embossed(image):
    K = [[-1, -1, 0],
         [-1, 0, 1],
         [0, 1, 1]]
    img = image.copy()
    for r in range(1, len(img) -1): #iterate thru rows of img
        for c in range(1, len(img[0]) -1):
            for i in range(3):
                img[r][c][i] = (image[r-1][c-1][i] * K[0][0] + image[r-1][c][i] * K[0][1] + image[r-1][c+1][i] * K[0][2] 
                + image[r][c-1][i] * K[1][0] + image[r][c][i] * K[1][1] + image[r][c+1][i] * K[1][2]
                + image[r+1][c-1][i] * K[2][0] + image[r+1][c][i] * K[2][1] + image[r+1][c+1][i] * K[2][2]) + 128

    for r in range(len(img)):
        for c in range(len(img[0])):
            for i in range(3):
                if img[r][c][i]>255:
                    img[r][c][i] = 255
                if img[r][c][i] < 0:
                    img[r][c][i] = 0
    return img

def rectangle_select(image, x, y):
    mask = np.full((len(image), len(image[0])), 0)
    for r in range(x[0], y[0]+1):
        for c in range(x[1], y[1]+1):
            mask[r][c] = 1
    return mask
            

def magic_wand_select(image, x, thres):
    mask = np.full((len(image), len(image[0])), 0)
    mask[x[0]][x[1]] = 1
    
    stack = [x]
                
    while stack:
        v = stack.pop()
        # check the top
        if 0 <= v[0]-1 <= len(image)-1 and 0 <= v[1] <= len(image[0])-1:
            avg_r = (image[x[0]][x[1]][0] + image[v[0]-1][v[1]][0])/2
            diff_r = image[x[0]][x[1]][0] - image[v[0]-1][v[1]][0]
            diff_g = image[x[0]][x[1]][1] - image[v[0]-1][v[1]][1]
            diff_b = image[x[0]][x[1]][2] - image[v[0]-1][v[1]][2]
            
            dist_top = math.sqrt(((2+ (avg_r /256))*(diff_r)**2) + 4*(diff_g)**2 + (2+(255-avg_r)/256)*(diff_b)**2)
            
            if dist_top <= thres and mask[v[0]-1][v[1]] == 0:
                
                stack.append((v[0]-1, v[1]))
                mask[v[0]-1][v[1]] = 1
                
        #check the left
        if 0 <= v[0] <= len(image)-1 and 0 <= v[1]-1 <= len(image[0]) -1:
            avg_r = (image[x[0]][x[1]][0] + image[v[0]][v[1]-1][0])/2
            diff_r = image[x[0]][x[1]][0] - image[v[0]][v[1]-1][0]
            diff_g = image[x[0]][x[1]][1] - image[v[0]][v[1]-1][1]
            diff_b = image[x[0]][x[1]][2] - image[v[0]][v[1]-1][2]
            
            dist_left = math.sqrt(((2+ (avg_r /256))*(diff_r)**2) + 4*(diff_g)**2 + (2+(255-avg_r)/256)*(diff_b)**2)
            
            if dist_left <= thres and mask[v[0]][v[1]-1] == 0:
                stack.append((v[0], v[1]-1))
                mask[v[0]][v[1]-1] = 1
                
        #check the right
        if 0 <= v[0] <= len(image)-1 and 0 <= v[1]+1 <= len(image[0]) -1:
            avg_r = (image[x[0]][x[1]][0] + image[v[0]][v[1]+1][0])/2
            diff_r = image[x[0]][x[1]][0] - image[v[0]][v[1]+1][0]
            diff_g = image[x[0]][x[1]][1] - image[v[0]][v[1]+1][1]
            diff_b = image[x[0]][x[1]][2] - image[v[0]][v[1]+1][2]
            
            dist_right = math.sqrt(((2+ (avg_r /256))*(diff_r)**2) + 4*(diff_g)**2 + (2+(255-avg_r)/256)*(diff_b)**2)
            
            if dist_right <= thres and mask[v[0]][v[1]+1] == 0:
                stack.append((v[0], v[1]+1))
                mask[v[0]][v[1]+1] = 1
            
        #check the bottom
        if 0 <= v[0]+1 <= len(image) -1 and 0 <= v[1] <= len(image[0]) -1:
            avg_r = (image[x[0]][x[1]][0] + image[v[0]+1][v[1]][0])/2
            diff_r = image[x[0]][x[1]][0] - image[v[0]+1][v[1]][0]
            diff_g = image[x[0]][x[1]][1] - image[v[0]+1][v[1]][1]
            diff_b = image[x[0]][x[1]][2] - image[v[0]+1][v[1]][2]
            
            dist_bottom = math.sqrt(((2+ (avg_r /256))*(diff_r)**2) + 4*(diff_g)**2 + (2+(255-avg_r)/256)*(diff_b)**2)
            
            if dist_bottom <= thres and mask[v[0]+1][v[1]] == 0:
                stack.append((v[0]+1, v[1]))
                mask[v[0]+1][v[1]] = 1    
            
    return mask

def compute_edge(mask):           
    rsize, csize = len(mask), len(mask[0]) 
    edge = np.zeros((rsize,csize))
    if np.all((mask == 1)): return edge        
    for r in range(rsize):
        for c in range(csize):
            if mask[r][c]!=0:
                if r==0 or c==0 or r==len(mask)-1 or c==len(mask[0])-1:
                    edge[r][c]=1
                    continue
                
                is_edge = False                
                for var in [(-1,0),(0,-1),(0,1),(1,0)]:
                    r_temp = r+var[0]
                    c_temp = c+var[1]
                    if 0<=r_temp<rsize and 0<=c_temp<csize:
                        if mask[r_temp][c_temp] == 0:
                            is_edge = True
                            break
    
                if is_edge == True:
                    edge[r][c]=1
            
    return edge

def save_image(filename, image):
    img = image.astype(np.uint8)
    mpimg.imsave(filename,img)

def load_image(filename):
    img = mpimg.imread(filename)
    if len(img[0][0])==4: # if png file
        img = np.delete(img, 3, 2)
    if type(img[0][0][0])==np.float32:  # if stored as float in [0,..,1] instead of integers in [0,..,255]
        img = img*255
        img = img.astype(np.uint8)
    mask = np.ones((len(img),len(img[0]))) # create a mask full of "1" of the same size of the laoded image
    img = img.astype(np.int32)
    return img, mask

def display_image(image, mask):
    # if using Spyder, please go to "Tools -> Preferences -> IPython console -> Graphics -> Graphics Backend" and select "inline"
    tmp_img = image.copy()
    edge = compute_edge(mask)
    for r in range(len(image)):
        for c in range(len(image[0])):
            if edge[r][c] == 1:
                tmp_img[r][c][0]=255
                tmp_img[r][c][1]=0
                tmp_img[r][c][2]=0
 
    plt.imshow(tmp_img)
    plt.axis('off')
    plt.show()
    print("Image size is",str(len(image)),"x",str(len(image[0])))

def menu():
    
    img = mask = np.array([])  
    
    
    A = "e - exit\nl - load a picture\ns - save the current picture\n1 - adjust brightness\n2 - adjust contrast\n3 - apply grayscale\n4 - apply blur\n5 - edge detection\n6 - embossed\n7 - rectangle select\n8 - magic wand select\nNote: If you want to apply effects to a specific part of the image, please select option 7 or 8 first"
        
    print("What do you want to do ?")
    print("e - exit\nL - load a picture")
    #choice = input("Your choice:")
    print("")
    
    while True:
        choice = input("Your choice:")
        if choice == "L":
            while True:
                try:
                    filename = input("Please enter valid name of file you want to load:")
                    image, mask = load_image(filename)
                    break
                except OSError:
                    print("Invalid filename entered.") 
            print("\nLoading...\n")
            display_image(image, mask)
            
            
            print("\nWhat do you want to do ?\n")
            print(A)
        elif choice == "e":
            break
        elif choice == "s":
            print("\nSaving...\nFile saved\n")
            save_image(filename, image)
            print("What do you want to do ?\n")
            print(A)
        elif choice == "1":
            while True:
                try:
                    value = int(input("To change brightness, please input an integer value from -255 to 255:"))
                    if value >= -255 and value <= 255:
                        break
                    else:
                        print("Invalid! Please input an integer value from -255 to 255.")
                except ValueError:
                    print("Invalid! Please input an integer value from -255 to 255.")
            print("Adjusting brightness...")
            changed_image = change_brightness(image, value)
            for r in range(len(image)):
                for c in range(len(image[0])):
                    if mask[r][c] == 0:
                        for z in range(3):
                            changed_image[r][c][z] = image[r][c][z]
            display_image(changed_image, mask)
            
            print("\nBrightness changed! What do you want to do ?\n")
            print(A)
    
        
        elif choice == "2":
            while True:
                try:
                    value = int(input("To change contrast, please input an integer value from -255 to 255:"))
                    if value >= -255 and value <= 255:
                        break
                    else:
                        print("Invalid! Please input an integer value from -255 to 255.")
                except ValueError:
                    print("Invalid! Please input an integer value from -255 to 255.")
            print("Adjusting contrast...")
            C = change_contrast(image, value)
            for r in range(len(image)):
                for c in range(len(image[0])):
                    if mask[r][c] == 0:
                        for z in range(3):
                            C[r][c][z] = image[r][c][z]
            
            display_image(C, mask)
            
            print("\nContrast changed! What do you want to do ?\n")
            print(A)
            
        elif choice == "3":
            print("Applying grayscale")
            G = grayscale(image)
            for r in range(len(image)):
                for c in range(len(image[0])):
                    if mask[r][c] == 0:
                        for z in range(3):
                            G[r][c][z] = image[r][c][z]
            display_image(G, mask)
            
            print("Grayscale applied!")
            print(A)
            
        elif choice == "4":
            print("Applying blur...")
            blur = blur_effect(image)
            for r in range(len(image)):
                for c in range(len(image[0])):
                    if mask[r][c] == 0:
                        for z in range(3):
                            blur[r][c][z] = image[r][c][z]
            display_image(blur, mask)
            
            print("Blur effect applied!")
            print(A)
        
        elif choice == "5":
            print("Edge detection...")
            edge_detect = edge_detection(image)
            for r in range(len(image)):
                for c in range(len(image[0])):
                    if mask[r][c] == 0:
                        for z in range(3):
                            edge_detect[r][c][z] = image[r][c][z]
            display_image(edge_detect, mask)
            print("Edge detection complete!")
            print(A)
            
        elif choice == "6":
            print("Embossing...")
            emboss = embossed(image)
            for r in range(len(image)):
                for c in range(len(image[0])):
                    if mask[r][c] == 0:
                        for z in range(3):
                            emboss[r][c][z] = image[r][c][z]
            display_image(emboss, mask)
            print("Embossed!")
            print(A)
    
        elif choice == "7":
            print("Rectangle selection...")
            img = image.copy()
            while True:
                try:
                    x1 = int(input("Please select left integer value of top left pixel, from 0 to " + str(len(mask)-1) + ": "))
                    x2 = int(input("Please select right integer value of top left pixel, from 0 to " + str(len(mask)-1) + ": "))
                    y1 = int(input("Please select left integer value of bottom right pixel from 0 to " + str(len(mask[0]) -1) + ": "))
                    y2 = int(input("Please select right integer value of top left pixel, from 0 to " + str(len(mask[0]) -1) + ": "))
                    if x1>=0 and x1 <= len(mask) and x2>= 0 and x2<= len(image[0]):
                        if y1>=0 and y1 <= len(mask) and y2 >= 0 and y2 <= len(image[0]):
                            break
                    else:
                        print("Invalid value! Please enter an appropriate integer value!")
                except ValueError:
                    print("Invalid value! Please enter an appropriate integer value!")
            x = (x1,x2)
            y = (y1, y2)
            mask = rectangle_select(image, x, y)
            
            display_image(image, mask)
            print("Selected!")
            print(A)
            
        elif choice == "8":
            print("Magic Wand Select")
            while True:
                try:
                    x1 = int(input("Please select left integer value of top left pixel, from 0 to " + str(len(mask)-1) + ": "))
                    x2 = int(input("Please select right integer value of top left pixel, from 0 to " + str(len(mask)-1) + ": "))
                    thres = int(input("Please enter a threshold value of integer value: "))
                    if x1>=0 and x1 <= len(mask)-1 and x2>= 0 and x2<= len(image[0])-1:
                        break
                    else:
                        print("Invalid value! Please enter an appropriate integer value!")
                except ValueError:
                    print("Invalid value! Please enter an appropriate integer value!")
            x = (x1, x2)
            
            mask = magic_wand_select(image, x, thres)
            
            display_image(image, mask)
            print(A)
        
       
if __name__ == "__main__":
    menu()           
