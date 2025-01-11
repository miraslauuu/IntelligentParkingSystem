import cv2

cv2.namedWindow("Podgląd wideo", cv2.WINDOW_NORMAL)  # Wymuszenie działania okna na Mac/Linux

video_path = "parking_test.mp4"  # Podmień na ścieżkę do filmu
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Nie udało się otworzyć pliku wideo.")
    exit()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Koniec filmu lub błąd odczytu.")
        break
    # Konwersja klatki do skali szarości
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Rozmycie w celu usunięcia szumów
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Binarizacja (prógowanie obrazu)
    _, threshold = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY)

    # Znajdowanie konturów
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Iteracja po konturach i rysowanie prostokątów
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
        if len(approx) == 4:  # Prostokąt
            x, y, w, h = cv2.boundingRect(cnt)
            if w > 50 and h > 20:  # Filtr wielkości prostokąta
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)


    cv2.imshow("Podgląd wideo", frame)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
