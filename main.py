import math
import flet as ft
from decimal import Decimal

const_e_double = Decimal(0.00669437999014)
const_a = Decimal(6378137.0)


def dms_to_radians(
        degrees: float,
        minutes: float = 0,
        seconds: float = 0
) -> float:
    """
    Method convert degrees, minutes and seconds to radians

    Args:
        degrees: Degrees
        minutes: Minutes
        seconds: Seconds

    Return:
        Returns the angle value in radians
    """
    negative_flag = False
    if degrees < 0:
        degrees = abs(degrees)
        negative_flag = True
    decimal_degrees = degrees + minutes / 60 + seconds / 3600
    radians = math.radians(decimal_degrees)
    return -radians if negative_flag else radians


class Coord():
    def __init__(self):
        self.latitude = ft.TextField(
            value="0", text_align=ft.TextAlign.CENTER, width=200)
        self.longitude = ft.TextField(
            value="0", text_align=ft.TextAlign.CENTER, width=200)
        self.height = ft.TextField(
            value="0", text_align=ft.TextAlign.CENTER, width=200)

        self.x = 0
        self.y = 0
        self.z = 0

        self.coord = ft.Row(
            [
                # ft.IconButton(ft.icons.REMOVE, on_click=...),
                ft.Text("Широта"),
                self.latitude,
                ft.Text("Долгота"),
                self.longitude,
                ft.Text("Высота"),
                self.height,
            ],
            alignment=ft.MainAxisAlignment.CENTER,)

    def calc(self):
        B = self.latitude.value.split(' ')
        L = self.longitude.value.split(' ')
        H = self.height.value

        N = Decimal(const_a / Decimal(math.sqrt(Decimal(1) - const_e_double *
                                                Decimal(math.sin(dms_to_radians(*list(map(float, B))))) * Decimal(math.sin(dms_to_radians(*list(map(float, B))))))))

        x = Decimal((N + Decimal(H))*Decimal(math.cos(dms_to_radians(*list(map(float, B)))))
                    * Decimal(math.cos(dms_to_radians(*list(map(float, L))))))
        self.x = float(x)
        y = Decimal((N + Decimal(H)) * Decimal(math.cos(dms_to_radians(*list(map(float, B)))))
                    * Decimal(math.sin(dms_to_radians(*list(map(float, L))))))
        self.y = float(y)
        z = Decimal((N + Decimal(H) - N * const_e_double) *
                    Decimal(math.sin(dms_to_radians(*list(map(float, B))))))
        self.z = float(z)
        print(f"{B=} {L=} {H=} {N=} {x=} {y=} {z=}")
        print(f"X {self.x} Y {self.y} Z {self.z}")
        return self.x, self.y, self.z


class Answer():
    def __init__(self, x=0, y=0, z=0):
        self.answer = ft.Row(
            [
                # ft.text(f"X {x} Y {y} Z {z}"),
                ft.Text(f"X {x}"),
                ft.Text(f"Y {y}"),
                ft.Text(f"Z {z}"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,)


def main(page: ft.Page):
    page.title = "Geo calc"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    coord = Coord()
    coords = [coord]
    answers = []

    def print_page():
        page.add(
            ft.Row(
                [ft.IconButton(ft.icons.ADD, on_click=add_coord),
                 ft.IconButton(ft.icons.CALCULATE, on_click=calc),],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )
        for current_coord in coords:
            page.add(current_coord.coord)
        for current_answer in answers:
            page.add(current_answer.answer)

    def add_coord(e):
        page.clean()
        if len(coords) >= 5:
            ...
        else:
            new_coord = Coord()
            coords.append(new_coord)
            print_page()

    def calc(e):
        answers.clear()
        for i in range(len(coords)):
            answers.append(1)
        for i in range(len(coords)):
            x, y, z = coords[i].calc()
            answer = Answer(x, y, z)
            answers[i] = answer

        page.clean()

        print_page()

    print_page()


ft.app(target=main)
