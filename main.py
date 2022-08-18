import tkinter as tk
import numpy as np
from PIL import Image, ImageColor, ImageTk
from PIL import ImageDraw
from idlelib.tooltip import Hovertip

class MainWindow(tk.Frame):
    canvas_width = 800
    canvas_height = 600
    __x0 = -2.2
    __y0 = -1.2
    __x1 = 1
    __y1 = 1.2
    __button1_press_x = 0
    __button1_press_y = 0
    __button1_release_x = 0
    __button1_release_y = 0
    __x_step = 1
    __y_step = 1

    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.root = root
        self.initUI()

    def initUI(self):
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, cursor="cross")
        self.canvas.bind('<Button-1>', self.canvas_b1press)
        self.canvas.bind('<ButtonRelease-1>', self.canvas_b1release)
        self.canvas.bind('<B1-Motion>', self.canvas_b1motion)
        self.canvas.bind('<MouseWheel>', self.canvas_mousewheel)
        self.canvas.grid(column=0, row=0)
        self.rect = self.canvas.create_rectangle(0, 0, 0, 0)
        self.lbl_x0 = tk.Label(self.root, font=("Courier", 20), text="x0: " + str(self.__x0))
        self.lbl_x0.grid(column=0, row=1, sticky="NW")
        self.lbl_x1 = tk.Label(self.root, font=("Courier", 20), text="x1: " + str(self.__x1))
        self.lbl_x1.grid(column=0, row=2, sticky="NW")
        self.lbl_y0 = tk.Label(self.root, font=("Courier", 20), text="y0: " + str(self.__y0))
        self.lbl_y0.grid(column=0, row=3, sticky="NW")
        self.lbl_y1 = tk.Label(self.root, font=("Courier", 20), text="y1: " + str(self.__y1))
        self.lbl_y1.grid(column=0, row=4, sticky="NW")
        self.canvs_tip = Hovertip(self.canvas, 'Use Mouse Wheel to zoom in and zoom out \n Select region by Mouse to enlarge it')



    def draw_mandelbrot(self, x0, y0, x1, y1):
        self.canvas.delete("all")
        result = self.mandelbrot(x0, y0, x1, y1)
        self.image = Image.fromarray(result)
        self.fract_img = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.fract_img, anchor=tk.NW)
        self.canvas.update()
        self.image.close()


    def mandelbrot(self, x0, y0, x1, y1):
        self.__x_step = (x1 - x0) / self.canvas_width
        self.__y_step = (y1 - y0) / self.canvas_height
        x = np.arange(x0, x1, self.__x_step).reshape((1, self.canvas_width))
        y = np.arange(y0, y1, self.__y_step).reshape((self.canvas_height, 1))
        c = x + 1j * y
        z = np.zeros(c.shape, dtype=np.complex128)
        iterations = np.zeros(c.shape, dtype=int)
        not_done = np.full(c.shape, True, dtype=bool)
        for i in range(100):
            z[not_done] = z[not_done] ** 2 + c[not_done]
            diverged = np.greater(np.abs(z), 2, out=np.full(c.shape, False), where=not_done)
            iterations[diverged] = i
            not_done[np.abs(z) > 2] = False
        return iterations

    def canvas_b1press(self, event):
        self.__button1_press_x = event.x
        self.__button1_press_y = event.y

    def canvas_b1release(self, event):
        if event.x < self.__button1_press_x:
            self.__button1_release_x = self.__button1_press_x
            self.__button1_press_x = event.x
        else:
            self.__button1_release_x = event.x

        if event.y < self.__button1_press_y:
            self.__button1_release_y = self.__button1_press_y
            self.__button1_press_y = event.y
        else:
            self.__button1_release_y = event.y

        if self.__button1_press_x == self.__button1_release_x or self.__button1_press_y == self.__button1_release_y:
            self.canvas.delete(self.rect)
            return

        new_x0 = self.__button1_press_x * self.__x_step + self.__x0
        new_x1 = self.__button1_release_x * self.__x_step + self.__x0
        self.__x0 = new_x0
        self.__x1 = new_x1

        new_y0 = self.__y0 + self.__button1_press_y * self.__y_step
        new_y1 = self.__y0 + self.__button1_release_y * self.__y_step
        self.__y0 = new_y0
        self.__y1 = new_y1
        self.lbl_x0.config(fg='red', text="x0: " + str(self.__x0))
        self.lbl_x0.update()
        self.lbl_x1.config(fg='red', text="x1: " + str(self.__x1))
        self.lbl_x1.update()
        self.lbl_y0.config(fg='red', text="y0: " + str(self.__y0))
        self.lbl_y0.update()
        self.lbl_y1.config(fg='red', text="y1: " + str(self.__y1))
        self.lbl_y1.update()

        self.draw_mandelbrot(self.__x0, self.__y0, self.__x1, self.__y1)

        self.lbl_x0.config(fg='black')
        self.lbl_x0.update()
        self.lbl_x1.config(fg='black')
        self.lbl_x1.update()
        self.lbl_y0.config(fg='black')
        self.lbl_y0.update()
        self.lbl_y1.config(fg='black')
        self.lbl_y1.update()

    def canvas_b1motion(self, event):
        self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.__button1_press_x, self.__button1_press_y, event.x, event.y,
                                                 fill='green', stipple='gray25', outline='green')

    def canvas_mousewheel(self, event):
        zoom = event.delta / 120
        if zoom > 0:
            x_dist = self.__x1 - self.__x0
            new_x0 = self.__x0 + x_dist / 4
            new_x1 = self.__x1 - x_dist / 4
            self.__x0 = new_x0
            self.__x1 = new_x1
            y_dist = self.__y1 - self.__y0
            new_y0 = self.__y0 + y_dist / 4
            new_y1 = self.__y1 - y_dist / 4
            self.__y0 = new_y0
            self.__y1 = new_y1
        else:
            x_dist = self.__x1 - self.__x0
            new_x0 = self.__x0 - x_dist / 2
            new_x1 = self.__x1 + x_dist / 2
            self.__x0 = new_x0
            self.__x1 = new_x1
            y_dist = self.__y1 - self.__y0
            new_y0 = self.__y0 - y_dist / 2
            new_y1 = self.__y1 + y_dist / 2
            self.__y0 = new_y0
            self.__y1 = new_y1

        self.lbl_x0.config(fg='red', text="x0: " + str(self.__x0))
        self.lbl_x0.update()
        self.lbl_x1.config(fg='red', text="x1: " + str(self.__x1))
        self.lbl_x1.update()
        self.lbl_y0.config(fg='red', text="y0: " + str(self.__y0))
        self.lbl_y0.update()
        self.lbl_y1.config(fg='red', text="y1: " + str(self.__y1))
        self.lbl_y1.update()

        self.draw_mandelbrot(self.__x0, self.__y0, self.__x1, self.__y1)

        self.lbl_x0.config(fg='black')
        self.lbl_x0.update()
        self.lbl_x1.config(fg='black')
        self.lbl_x1.update()
        self.lbl_y0.config(fg='black')
        self.lbl_y0.update()
        self.lbl_y1.config(fg='black')
        self.lbl_y1.update()


def main():
    global window
    window = tk.Tk()
    window.title("Fractal")
    window.geometry("1000x780+300+30")
    win = MainWindow(window)
    win.draw_mandelbrot(-2.2, -1.2, 1, 1.2)
    window.mainloop()


if __name__ == '__main__':
    main()
