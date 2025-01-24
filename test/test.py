import cv2

cv2.namedWindow("Podgląd wideo", cv2.WINDOW_NORMAL)  # Wymuszenie działania okna na Mac/Linux

video_path = "parking_clear_1_UPDATE.mp4"  
#video_path = "parking_clear_2_UPDATE.mp4"  

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Nie udało się otworzyć pliku wideo.")
    exit()

rectangle_count = 0  # Licznik znalezionych prostokątów

# Otwórz plik tekstowy do zapisu
output_file = "rectangles_1.txt"
# output_file = "rectangles_2.txt"

with open(output_file, "w") as file:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Koniec filmu lub błąd odczytu.")
            break

        # Konwersja klatki do skali szarości
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Rozmycie w celu usunięcia szumów
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Adaptive Gaussian Threshold (Invert the image to focus on black lines)
        threshold = cv2.adaptiveThreshold(
            blurred, 255,                    # Maksymalna wartość piksela
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,  # Metoda adaptacyjna
            cv2.THRESH_BINARY_INV,           # Inverted binary thresholding to focus on black lines
            11,                              # Rozmiar bloku (musi być nieparzysty)
            2                                # Stała, którą odejmuje się od średniej
        )

        # Znajdowanie konturów
        contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Iteracja po konturach i rysowanie prostokątów
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
            if len(approx) == 4:  # Prostokąt
                x, y, w, h = cv2.boundingRect(cnt)
                if w > 30 and h > 10:  # Filtr wielkości prostokąta
                    rectangle_count += 1
                    # Zapisz współrzędne do pliku
                    file.write(f"Prostokąt {rectangle_count}: x={x}, y={y}, w={w}, h={h}\n")

                    # Przerwij, jeśli znaleziono 9 prostokątów
                    if rectangle_count == 9:
                  # if rectangle_count == 6:
                        cap.release()
                        cv2.destroyAllWindows()
                        print(f"Współrzędne zapisano do pliku {output_file}")
                        exit()

        cv2.imshow("Podgląd wideo", frame)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
