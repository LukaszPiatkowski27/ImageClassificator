from network import NeuralNetwork
from bitmap import Image
from sys import argv


EPOCH_COUNT = 15
TRAIN_IMAGES_PER_CLASS = 60
TEST_IMAGES_PER_CLASS = 30

CLASSES = ['car', 'man', 'sun']

TRAIN_DIR = 'graphics/'
TEST_DIR = 'sample/'


def load_graphics(directory, name, count, smpl):
    result = []
    for i in range(count):
        temp = Image(
            directory + name + ('-0' if i + 1 < 10 else '-') + str(i + 1) + ('.bmp' if not smpl else '_smpl.bmp'))
        if temp.width == 64 and temp.height == 64:
            Image.resize(temp)  # wynik będzie miał rozmiar 16 x 16
        result.append(temp)
    return result


print('Wczytywanie danych treningowych oraz testowych...')
try:
    train_data = []
    test_data = []
    for class_name in CLASSES:
        train_data.append(load_graphics(TRAIN_DIR, class_name, TRAIN_IMAGES_PER_CLASS, False))
        test_data.append(load_graphics(TEST_DIR, class_name, TEST_IMAGES_PER_CLASS, True))
except FileNotFoundError as err:
    print('Blad podczas wczytywania danych: {}'.format(err))
else:
    print('Dane zostaly wczytane pomyslnie')

try:
    print('Tworzenie sieci')  # kształt sieci oraz współczynnik uczenia zostały dostosowane metodą prób i błędów
    brain = NeuralNetwork(len(train_data[0][0].pixels), [128, 64, 32], 3, 0.03)
    print('Siec zostala utworzona')
except Exception as err:
    print('Blad podczas tworzenia sieci: {}'.format(err))

# print('Poczatek odczytu')     # opcja wczytania wcześniej zapisanej sieci w celu doszkalania lub testowania
# brain.load('test_network.nn')
# print('Koniec odczytu')


# sesja treningowa

print('Trening w toku...')
try:
    for i in range(EPOCH_COUNT):
        for j in range(TRAIN_IMAGES_PER_CLASS):
            for k in range(len(CLASSES)):
                brain.train(train_data[k][j].pixels, [1 if (x == k) else 0 for x in range(len(CLASSES))])
        errors = []
        good = 0
        for j in range(TEST_IMAGES_PER_CLASS):
            for k in range(len(CLASSES)):
                test = brain.feed_forward(test_data[k][j].pixels)
                correct_output = [1 if (x == k) else 0 for x in range(len(CLASSES))]
                errors.append(sum(abs(test[class_index] - correct_output[class_index])
                                  for class_index in range(len(CLASSES))))
                if max(test) == test[k]:
                    good += 1
        error = sum(errors) / len(errors)
        acc = good / (TEST_IMAGES_PER_CLASS * len(CLASSES))
        print("epoch: ", i+1, "/", EPOCH_COUNT)
        print("error:", error)
        print("accuracy:", acc, "\n")
except Exception as err:
    print("Podczas treningu wystapil blad: {}".format(err))
else:
    print('Trening zakonczony')


try:        # jesli jako argument podamy sciezke do obrazka, to wykonamy pojedynczy test
    if len(argv) > 1:
        test_img = Image(argv[1])
        if test_img.width == 64 and test_img.height == 64:
            Image.resize(test_img)
        test = brain.feed_forward(test_img.pixels)
        print(test, "predicted class:", CLASSES[test.index(max(test))])
except Exception as err:
    print("Podczas testu wystapil blad: {}".format(err))


# print('Poczatek zapisu')      # gotowa siec moze zostac zapisana do pliku w celu ponownego uzycia
# brain.save('test_network.nn')
# print('Koniec zapisu')
