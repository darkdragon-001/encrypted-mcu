# Encrypted Multipoint Control Unit (MCU)

Proof of concept for an encrypted audio Multipoint Control Unit (MCU) _(inspired by [MIT CryptDB](https://css.csail.mit.edu/cryptdb/))_.

Multiple senders stream (uncompressed WAV/AIFF) audio to any number of receivers. In order to save bandwidth for the receivers, an MCU is added to combine all the streams from the senders into a single audio stream for the receivers. Since the MCU is not trusted, data should be end-to-end encrypted. Therefore, a homomorphic encryption scheme ([Paillier](https://en.wikipedia.org/wiki/Paillier_cryptosystem)) is used such that the server can mix the received audio streams into a single one before forwarding them to the receivers. The receivers can then decrypt these streams.

## Run

    pip3 install -r requirements.txt
    # put audio files in assets/ and change paths in app.py
    python3 app.py

