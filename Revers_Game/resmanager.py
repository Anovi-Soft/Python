import pickle
from pygame.locals import *
from header import *


class ImgTransform:
    def __init__(self, window_width,
                 window_height,
                 data_dir='data',
                 image_dir='image'):
        self.width = window_width
        self.height = window_height
        self.width_tr = 1
        self.height_tr = 1
        self.dir_name = os.path.join(data_dir, image_dir)

    def set_tr(self, width, height):
        self.width_tr = width
        self.height_tr = height

    def mtransform(self, img_name):
        return pygame.transform.scale(self.get_image(img_name),
                                      (int(self.width*self.width_tr),
                                       int(self.height*self.height_tr)))

    def transform(self, img_name, width_tr, height_tr):
        return pygame.transform.scale(self.get_image(img_name),
                                      (int(self.width*width_tr),
                                       int(self.height*height_tr)))

    def get_image(self, name):
        fullname = os.path.join(self.dir_name, name)
        try:
            image = pygame.image.load(fullname)
        except pygame.error:
            print('Cannot load image: {0}'.format(name))
            raise SystemExit
        else:
            return image.convert_alpha()


class ResManager:
    """Class for the storage and manipulation resources"""
    def __init__(self,
                 data_dir='data',
                 image_dir='image',
                 music_dir='music'):
        self.data_dir = data_dir
        self.image_dir = image_dir
        self.music_dir = music_dir
        self.message = None
        self.records = {}
        self.options = {}
        self.img_dict = {}
        self.music_dict = {}
        self.load_options()
        self.load_records()

    def get_image(self, name):
        fullname = os.path.join(self.data_dir,
                                os.path.join(self.image_dir, name))

        try:
            image = pygame.image.load(fullname)
        except pygame.error:
            print('Cannot load image: {0}'.format(name))
            raise SystemExit
        else:
            image = image.convert_alpha()

            return image

    def __transform(self, img, part):
        return pygame.transform.scale(img,
                                      (int(self.options[Opt.width]/part),
                                       int(self.options[Opt.height]/part)))

    def load_options(self):
        fullname = os.path.join(self.data_dir, "options.cfg")
        if os.path.exists(fullname):
            with open(fullname, "rb") as opt:
                self.options = pickle.load(opt)
        else:
            self.options[Opt.full_screen] = False
            self.options[Opt.width] = 640
            self.options[Opt.height] = 360
            self.options[Opt.point_b] = "point_black.png"
            self.options[Opt.point_w] = "point_white.png"
            self.options[Opt.block_b] = "block_black.png"
            self.options[Opt.block_w] = "block_white.png"
            self.options[Opt.point] = "point.png"
            self.options[Opt.background] = "background.jpg"
            self.options[Opt.black_hall] = "black_hall.png"
            self.dump_options()

    def dump_options(self):
        with open(os.path.join(self.data_dir, "options.cfg"), "wb") as opt:
            pickle.dump(self.options, opt)

    def load_game(self):
        from tkinter import filedialog, Tk
        root = Tk()
        root.withdraw()
        file_name = filedialog.askopenfilename(initialdir=self.data_dir,
                                               title="Choose file name",
                                               filetypes=(("python save",
                                                           "*.save"),))
        root.destroy()
        if file_name == '':
            return None
        with open(file_name, "rb") as gm:
            return pickle.load(gm)

    def dump_game(self, game):
        from tkinter import filedialog, Tk, messagebox
        root = Tk()
        root.withdraw()
        file = filedialog.asksaveasfile(mode='wb',
                                        initialdir=self.data_dir,
                                        title="Choose file name",
                                        filetypes=(("python save",
                                                    "*.save"),))
        root.destroy()
        try:
            pickle.dump(game, file)
        except Exception:
            messagebox.showinfo("Error", "Cant save")

    def load_images(self, points_size=1):
            size = 1/5*4/points_size
            size2 = 1//20
            coef = self.options[Opt.width]/self.options[Opt.height]
            tr = ImgTransform(self.options[Opt.width],
                              self.options[Opt.height],
                              self.data_dir,
                              self.image_dir)
            if points_size == 1:
                self.img_dict[Img.background] =\
                    tr.transform(self.options[Opt.background], 1, 1)
                self.img_dict[Img.load_background] =\
                    tr.transform("backgroundload.jpg", 1.5, 1.5*coef)
                self.img_dict[Img.logo] =\
                    tr.transform("logo.png", 0.5, 0.5)
                self.img_dict[Img.loading_end] =\
                    tr.transform("loading.png", 0.5, 1/12)
                self.img_dict[Img.left_substrate] =\
                    tr.transform("substrate.png", 0.2, 1)
                self.img_dict[Img.right_substrate] =\
                    tr.transform("substrate.png", 0.8, 1)
                self.img_dict[Img.radio_select] =\
                    tr.transform("radio_s.png", 0.05, 0.05*coef)
                self.img_dict[Img.radio_no_select] =\
                    tr.transform("radio_n.png", 0.05, 0.05*coef)

                tr.set_tr(1/coef/4, 1/4)
                self.img_dict[Img.select_stock_point] =\
                    tr.mtransform("select_stock_points.png")
                self.img_dict[Img.deselect_stock_point] =\
                    tr.mtransform("deselect_stock_points.png")
                self.img_dict[Img.select_politics_point] =\
                    tr.mtransform("select_politics_points.png")
                self.img_dict[Img.deselect_politics_point] =\
                    tr.mtransform("deselect_politics_points.png")
            else:
                tr.set_tr(1/coef*size, size)
                self.img_dict[Img.point_b] =\
                    tr.mtransform(self.options[Opt.point_b])
                self.img_dict[Img.point_w] =\
                    tr.mtransform(self.options[Opt.point_w])
                self.img_dict[Img.block_b] =\
                    tr.mtransform(self.options[Opt.block_b])
                self.img_dict[Img.block_w] =\
                    tr.mtransform(self.options[Opt.block_w])
                self.img_dict[Img.black_hall] =\
                    tr.mtransform(self.options[Opt.black_hall])
                self.img_dict[Img.point] =\
                    tr.mtransform(self.options[Opt.point])

                tr.set_tr(1/coef*size2, size2)
                self.img_dict[Img.step_black] =\
                    tr.mtransform(self.options[Opt.point_b])
                self.img_dict[Img.step_white] =\
                    tr.mtransform(self.options[Opt.point_w])

    def load_music(self):
        self.message = "load"
        try:
            self.music_dict[MUS.step] = get_music("step.ogg")
        except Exception:
            print("Can`t find sound(step.ogg)")
        self.message = "end"

    def load_records(self):
        try:
            fullname = os.path.join(self.data_dir, "records.cfg")
            if os.path.exists(fullname):
                with open(fullname, "rb") as res:
                    self.records = pickle.load(res)
            else:
                for i in range(4, 21):
                    self.records[i] = [("Nobody", 0)]*10
                self.dump_records()
        except Exception:
            self.records = None

    def dump_records(self):
        try:
            with open(os.path.join(self.data_dir, "records.cfg"), "wb") as opt:
                pickle.dump(self.records, opt)
        except Exception:
            from tkinter import messagebox
            messagebox.showinfo("Error", "Cant save")
