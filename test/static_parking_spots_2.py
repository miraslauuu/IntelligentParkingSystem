import cv2

# Funkcja do wczytania współrzędnych prostokątów z pliku
def load_rectangles(file_path):
    rectangles = []
    with open(file_path, "r") as file:
        for line in file:
            if line.startswith("Prostokąt"):
                parts = line.split(":")[1].strip().split(", ")
                x = int(parts[0].split("=")[1])
                y = int(parts[1].split("=")[1])
                w = int(parts[2].split("=")[1])
                h = int(parts[3].split("=")[1])
                rectangles.append((x, y, w, h))
    return rectangles

# Wczytaj współrzędne z pliku
rectangles = load_rectangles("rectangles_2_modified.txt")

# Ustawienie początkowego numeru dla tej części parkingu
start_number = 8

cv2.namedWindow("Podgląd wideo", cv2.WINDOW_NORMAL)  # Wymuszenie działania okna na Mac/Linux

#video_path = "parking_2_clear.mp4" #kawałek parkingu bez pojazdów
#video_path = "parking_2_clear.mp4" # cały filmik
video_path = "parking_z_pojazdami_2.mp4" # kawałek z pojazdami

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Nie udało się otworzyć pliku wideo.")
    exit()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Koniec filmu lub błąd odczytu.")
        break

    # Narysuj prostokąty i podpisz ich rzeczywiste numery
    for i, rect in enumerate(rectangles):
        x, y, w, h = rect
        real_number = start_number + i  # Numeracja zaczyna się od `start_number`

        # Rysowanie prostokąta
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Dodawanie numeru prostokąta
        cv2.putText(
            frame,
            str(real_number),      # Numer rzeczywisty miejsca
            (x, y - 10),           # Pozycja tekstu (nad prostokątem)
            cv2.FONT_HERSHEY_SIMPLEX, 
            0.6,                   # Rozmiar czcionki
            (0, 255, 0),           # Kolor tekstu (zielony)
            2,                     # Grubość linii tekstu
            cv2.LINE_AA            # Antyaliasing
        )

    # Wyświetlenie ramki wideo z prostokątami
    cv2.imshow("Podgląd wideo", frame)

    # Wyjście po naciśnięciu klawisza 'q'
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Zwolnij zasoby
cap.release()
cv2.destroyAllWindows()
