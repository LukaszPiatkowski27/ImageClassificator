# ImageClassificator

Simple feed forward neural network based classificator for black-white bitmaps of size 64 x 64 px and 24 bit color depth.

The neural network itself has been written from scratch without using any external packages.

This repo contains example data for training and testing (3 classes) as well as example pre-trained network to test.

---------------

In order to omit training of already trained network you should just comment out the training section from main.py file <br>
and make sure, that network-loading code is not commented out.

If you want to perform a single test on an image, you should pass its path as an argument:<br>
`python3 main.py path_to_the_file`

---------------

At the bottom of the main.py file there is a section that allows to save current network to file,
so if you want to use it - make sure it's not commented out.

---------------

Project was created entirely by me ([@LukaszPiatkowski27](https://github.com/LukaszPiatkowski27))<br>
for the purposes of computer science studies at the Silesian University of Technology - 2021
