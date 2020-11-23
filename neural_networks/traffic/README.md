# Traffic Exercise Experimentation Process

Neural network trained on [German Traffic Sign Recognition Benchmark (GTSRB)](http://benchmark.ini.rub.de/?section=gtsrb&subsection=news) dataset.

## Layer Arrangement
I implemented a feed-forward convolutional neural network, whith a similar structure to the code used for the handwriting recognition presented during the [lecture](https://video.cs50.io/J1QD9hLDEDY?screen=qNDOwwNlCD0).

After adding a second layer of convolution (with a 3x3px kernel) and pooling, I found that the accuracy increased by about 15 percentage points. This presumable happens through more detailed modeling of the street sign images. I also found that increasing the filter size to 64 for that second layer improved accuracy. 

## Hidden Layer
I also added a second dense hidden layer to model more complex relationships between the labels and the data, with 1/2 of the first hidden layer units—this improved accuracy by ten percentage points from 0.78 to .88.

### Hidden Layer Dropout

While testing this parameter, I found that a dropout rate of 0.33 worked best. I started with 0.5 and selected 0.35, which increased another six percentage points (from .88 to .94). This process systematically deactivates units of the model to make it more robust.  I tried values between tried 0.2  and 0.7.

