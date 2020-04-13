#!/bin/python3
#
# Proof of concept for an encrypted audio mixer
#

import itertools as it
import numpy as np

import wave
from phe import paillier

def load_and_encrypt(public_key, filename):
  with wave.open(filename) as f:
    # check file
    params = f.getparams()
    assert params.nchannels == 1
    #assert params.sampwidth == 2
    assert params.framerate == 44100
    #assert params.nframes == 1234567890
    assert params.comptype == 'NONE'
    #assert params.compname == 'not compressed'
    
    # load file
    dt = np.dtype('<i'+str(params.sampwidth))  # '<': little endian, 'i': signed
    frames = np.frombuffer(f.readframes(params.nframes), dtype=dt)
    
    # encrypt
    return np.vectorize(public_key.encrypt,otypes=[paillier.EncryptedNumber])(frames)

def mix_encrypted(public_key, data):  # [d11,d12,d12],[d21,d22]
  # pad and sum data
  zero = public_key.encrypt(0)
  frame_tuples = list(it.zip_longest(*data, fillvalue=zero))  # [ (d11,d21), (d12,d22), d13,0) ]
  return np.sum(frame_tuples, 1)  # [ d11+d21, d12+d22, d13+0]

def decrypt_and_save(private_key, encrypted, filename):
  # decrypt
  decrypted = np.vectorize(private_key.decrypt)(encrypted)
  
  # save
  # create parameters
  params = wave._wave_params(
    nchannels = 1,
    sampwidth = 2,
    framerate = 44100,
    nframes = len(decrypted),
    comptype = 'NONE', compname = 'not compressed'
  )
  # prepare data type
  dt = np.dtype('<i'+str(params.sampwidth))  # '<': little endian, 'i': signed
  decrypted = decrypted.astype(np.int16, copy=False)
  # write
  f = wave.open(filename, mode='wb')
  f.setparams(params)
  f.writeframes(decrypted.tobytes())
  f.close()


# generate keys
public_key, private_key = paillier.generate_paillier_keypair(n_length=64)  # NOTE 2048 should be used in production

# sender (untrusted): load and encrypt data
sender = []
sender += [load_and_encrypt(public_key, 'assets/car.wav')]
sender += [load_and_encrypt(public_key, 'assets/cheer.wav')]

# mixer (untrusted)
mixer = mix_encrypted(public_key, sender)

# receiver (trusted): decrypt and save data
receiver = decrypt_and_save(private_key, mixer, 'assets/mixx.wav')

