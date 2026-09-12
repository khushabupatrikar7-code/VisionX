import cv2

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cv2.imwrite("test_image.jpg", frame)
print("Saved as test_image.jpg")
cap.release()