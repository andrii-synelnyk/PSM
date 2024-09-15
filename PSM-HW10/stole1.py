import turtle
import sys

# Zwiększenie limitu by nie było Stack Overflow
sys.setrecursionlimit(10000)


class FractalPlant:
    def __init__(self, slowo_poczatkowe, liczba_iteracji, kat, dlugosc):
        # Reguły do generowania rośliny
        self.reguly = {
            "X": "F+[[X]-X]-F[-FX]+X",
            "F": "FF"
        }
        self.slowo_poczatkowe = slowo_poczatkowe
        self.liczba_iteracji = liczba_iteracji
        self.kat = kat
        self.dlugosc = dlugosc

    def ustaw_zasady(self, slowo):
        # Na przechowywanie przekształconych znaków
        nowe_slowo = ""
        for char in slowo:
            # Dodajemy znaki do nowego słowa przechowującego ciąg znaków z zamienienia
            nowe_slowo += self.reguly.get(char, char)
        return nowe_slowo

    def wygeneruj_slowo(self):
        slowo = self.slowo_poczatkowe
        # Pętla wykona się tyle razy, ile wynosi self.liczba_iteracji
        for _ in range(self.liczba_iteracji):
            # Wywołujemy ustawianie zasad dla aktualnego słowa
            slowo = self.ustaw_zasady(slowo)
        return slowo

    def rysuj(self, slowo):
        # Prędkość rysowania
        turtle.speed(0)
        # Kolor tła
        turtle.bgcolor("white")
        # Kolor ścieżki
        turtle.color("green")
        # Szerokość ścieżki
        turtle.width(3)
        # Do ukrycia żółwia
        turtle.hideturtle()

        # Nie chcemy by rysował jak go przenosimy na start
        turtle.penup()
        # Pozycja wejściowa X = 0 i Y = 0
        turtle.goto(0, 0)
        # Początek rysowania
        turtle.pendown()
        # Kąt początkowy - 90 stopni zapewni, że roślina będzie rosnąc w górę
        turtle.setheading(90)

        stack = []
        for char in slowo:
            # Idź do przodu zostawiając ślad
            if char == "F":
                turtle.forward(self.dlugosc)
            # Obrót o 25 st
            elif char == "+":
                turtle.left(self.kat)
            # Obrót o 25 st
            elif char == "-":
                turtle.right(self.kat)
            # Odłóż wartości na stos
            elif char == "[":
                pozycja = turtle.position()
                kat_obrotu = turtle.heading()
                stack.append((pozycja, kat_obrotu))
            # Zdejmij ze stosu
            elif char == "]":
                pozycja, kat_obrotu = stack.pop()
                turtle.penup()
                turtle.setposition(pozycja)
                turtle.setheading(kat_obrotu)
                turtle.pendown()

    def run(self):
        slowo_koncowe = self.wygeneruj_slowo()
        self.rysuj(slowo_koncowe)
        turtle.done()


if __name__ == "__main__":
    wzrost_rosliny = FractalPlant("X", 5, 25, 3)
    wzrost_rosliny.run()