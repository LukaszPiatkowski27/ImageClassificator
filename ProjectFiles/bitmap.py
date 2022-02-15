class Image:

    def __init__(self, file_path):
        file = open(file_path, 'rb')
        header = file.read(54)  # plik bmp ma naglowek wielkosci 54 bitow
        self.width = int(header[18])
        self.height = int(header[22])
        row_padded = (self.width * 3 + 3) & (~3)
        self.pixels = []
        for i in range(self.height):
            data = file.read(row_padded)
            for j in range(0, self.width * 3, 3):
                # zakladamy, ze obrazki sa czarno-biale, ale z glebia 24 - bitowa
                self.pixels.append(1 if data[j] == 255 else 0)
        file.close()

    @staticmethod
    def resize(img):
        result = []
        for y in range(0, img.height, 4):
            for x in range(0, img.width, 4):
                sum = img.pixels[x + img.width * y] + img.pixels[x + 1 + img.width * y] \
                    + img.pixels[x + 2 + img.width * y] + img.pixels[x + 3 + img.width * y] \
                    + img.pixels[x + img.width * (y + 1)] + img.pixels[x + 1 + img.width * (y + 1)] \
                    + img.pixels[x + 2 + img.width * (y + 1)] + img.pixels[x + 3 + img.width * (y + 1)]\
                    + img.pixels[x + img.width * (y + 2)] + img.pixels[x + 1 + img.width * (y + 2)] \
                    + img.pixels[x + 2 + img.width * (y + 2)] + img.pixels[x + 3 + img.width * (y + 2)]\
                    + img.pixels[x + img.width * (y + 3)] + img.pixels[x + 1 + img.width * (y + 3)] \
                    + img.pixels[x + 2 + img.width * (y + 3)] + img.pixels[x + 3 + img.width * (y + 3)]
                result.append(0 if (sum / 16 <= 0.75) else 1)
        img.width = 16
        img.height = 16
        img.pixels = result.copy()
