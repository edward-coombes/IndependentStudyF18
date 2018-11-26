# -*- coding: utf-8 -*-
from __future__ import print_function
from keras.callbacks import LambdaCallback
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
import numpy as np
import random
import sys
import os
import io
import codecs
maxlen = 40

def sample(preds, temperature=1.0):
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)


def on_epoch_end(epoch, logs, log = codecs.open("log.txt","a","utf-8")):
    # Function invoked at end of each epoch.
    # Prints generated text.

    log.write(u"\n")
    log.write(u'----- Generating text after Epoch: %d' % epoch)
    print("text for epoch: %d" % epoch)
    start_index = random.randint(0, len(text) - maxlen - 1)

    for diversity in [0.2, 0.5, 1.0, 1.2]:
        log.write(u'----- diversity: ' + str(diversity))
        generated = u''
        sentence = text[start_index: start_index + maxlen]
        generated += sentence
        log.write(u'----- Generating with seed: "' + sentence + '"')
        print(u'----- Generating with seed: "' + sentence + '"')
        sys.stdout.write(generated)

        for i in range(400):
            x_pred = np.zeros((1, maxlen, len(chars)))
            for t, char in enumerate(sentence):
                x_pred[0, t, char_indices[char]] = 1.
            preds = model.predict(x_pred, verbose=0)[0]
            next_index = sample(preds, diversity)
            next_char = indices_char[next_index]
            generated += next_char
            sentence = sentence[1:] + next_char
            log.write(next_char)
            sys.stdout.write(next_char)
            sys.stdout.flush()
        log.write(u"\n")
        print()

def vectorizeIt(startRange,endRange,step):
 
    # cut the text in semi-redundant sequences of maxlen characters
    sentences = []
    next_chars = []

    for i in range(startRange, endRange - maxlen, step):
        sentences.append(text[i:i+maxlen])
        next_chars.append(text[i+maxlen])

    print('nb sequences:', len(sentences))

    #vectorize it
    print('Vectorization...')
    print(len(sentences))
    print(maxlen)
    print(len(chars))

    x = np.zeros((len(sentences), maxlen, len(chars) ), dtype=np.bool)
    y = np.zeros((len(sentences), len(chars)), dtype=np.bool)

    for i, sentence in enumerate(sentences):
        for t, char in enumerate(sentence):
            x[i, t, char_indices[char]] = 1
#    print(char_indices)
#    print(next_chars[i])
        y[i, char_indices[next_chars[i]]] = 1
    return x,y


def buildModel():
# build the model: a single LSTM
    print('Build model...')
    model = Sequential()
    model.add(LSTM(128, input_shape=(maxlen, len(chars))))
    model.add(Dense(len(chars)))
    model.add(Activation('softmax'))
    optimizer = RMSprop(lr=0.01)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer)
    print("Model built...")
    
    return model

def trainModel(model,step=3,batchSize=200000):

    for i in range(0,len(text)//batchSize):
        print("Training on data chunk " + str(i))
        start = i*batchSize
        end = (i+1)*batchSize if (i+1)*batchSize < len(text) else len(text)
        x,y = vectorizeIt(start,end,step)
        print_callback = LambdaCallback(on_epoch_end=on_epoch_end)
        model.fit(x, y,

          batch_size=128,

          epochs=60,

          callbacks=[print_callback])
    model.save(os.path.realpath(__file__).replace(".py",".hd5"))
    
if __name__ == "__main__":
    print("starting...")
    path = "effCorpus.txt"
    #get all text
    global text
    text = io.open(path, encoding='utf-8').read().lower()
    print('corpus length:', len(text))

    #get unique characters
    chars = sorted(list(set(text)))
    print('total chars:', len(chars))

    #make somm dictionaries
    char_indices = dict((c, i) for i, c in enumerate(chars))
    indices_char = dict((i, c) for i, c in enumerate(chars))

    model = buildModel()
    trainModel(model)
    log.close()
