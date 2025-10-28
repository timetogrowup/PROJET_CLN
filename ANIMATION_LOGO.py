import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image
import numpy as np

# Charger l'image PNG
def load_image(image_path):
    img = Image.open(image_path)
    return img

# Fonction pour créer une animation de rotation du logo
def animate_logo(image_path, save_path='logo_animation.mp4'):
    # Charger l'image du logo
    img = load_image(image_path)

    # Préparer le canvas d'animation
    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    # Convertir l'image en tableau numpy pour affichage
    img_np = np.asarray(img)
    logo = ax.imshow(img_np, origin='upper')

    # Limiter les axes en fonction de la taille de l'image
    ax.set_xlim(0, img_np.shape[1])
    ax.set_ylim(img_np.shape[0], 0)  # Inverser l'axe Y pour afficher correctement l'image

    def update(frame):
        # Appliquer une rotation à l'image
        rotated_img = img.rotate(frame)
        logo.set_array(np.asarray(rotated_img))
        return [logo]

    # Créer l'animation (rotation de 360°)
    ani = animation.FuncAnimation(fig, update, frames=np.arange(0, 360, 1), blit=True, repeat=True)

    # Sauvegarder l'animation sous forme de fichier vidéo
    ani.save(save_path, writer='ffmpeg', fps=30)
    plt.show()

# Exécuter l'animation avec le fichier logo PNG
animate_logo('LOGO_CLN.png')
