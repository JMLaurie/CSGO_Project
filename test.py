import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt
from PIL import Image


df = pd.read_csv("**INSERT PATH TO CSV**")
df.rename(columns={'0': 'x_scaled', '1': 'y_scaled'}, inplace=True)
df.drop(columns=['Unnamed: 0'], inplace=True)


def kde_plot(frame):
    image = Image.open(r"**INSERT PATH TO IMAGE HERE**")

    width, height = image.size

    data = np.array(frame).T

    kde = gaussian_kde(data)

    x_grid = np.linspace(0, width, 100)
    y_grid = np.linspace(0, height, 100)
    X, Y = np.meshgrid(x_grid, y_grid)
    grid_coords = np.vstack([X.ravel(), Y.ravel()])

    Z = kde.evaluate(grid_coords).reshape(X.shape)

    Z_norm = Z / np.max(Z)


    fig, ax = plt.subplots()
    ax.imshow(image, extent=[0, width, height, 0],)

    plt.contourf(X, Y, Z_norm, levels=50, cmap='Reds',alpha=0.5)

    plt.scatter(data[0], data[1], c="blue", s=10)

    plt.show()

kde_plot(df)