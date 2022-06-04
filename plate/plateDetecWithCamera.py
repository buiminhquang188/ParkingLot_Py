import cv2
import pytesseract
body_data = dict(twoFirstDigits="string", fourLastDigits="string", licensePlates="string")
valid_num = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-']


def camera_get_plate(camera_ip):

    if len(str(camera_ip)) > 1:
        link_camera = "https://" + str(camera_ip) + '/video'
    else:
        link_camera = 0
    cap = cv2.VideoCapture(link_camera)

    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    contours, h = cv2.findContours(thresh, 1, 2)
    largest_rectangle = [0, 0]
    for cnt in contours:
        length = 0.01 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, length, True)
        if len(approx) == 4:
            area = cv2.contourArea(cnt)
            if area > largest_rectangle[0]:
                largest_rectangle = [cv2.contourArea(cnt), cnt, approx]
    x, y, w, h = cv2.boundingRect(largest_rectangle[1])
    image = frame[y:y + h, x:x + w]
    cv2.drawContours(frame, [largest_rectangle[1]], 0, (0, 255, 0), 8)
    cv2.putText(frame, "BIEN SO", (x, y),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5,
                (0, 255, 255), 4)
    cv2.imshow('Dinh Vi Bien So Xe', frame)
    cv2.drawContours(frame, [largest_rectangle[1]], 0, (255, 255, 255), 18)
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening
    data = pytesseract.image_to_string(invert, lang='eng', config='--psm 6')
    result = ""
    for each in data:
        if each in valid_num or each.isalpha():
            result = result + each
    # print("Bien so xe tai camera_ip {} la: {}  ".format(camera_ip, result))
    body_data['twoFirstDigits'] = result[:2]
    body_data['fourLastDigits'] = result[-4:]
    body_data['licensePlates'] = result
    print(body_data)

    key = cv2.waitKey(1)



