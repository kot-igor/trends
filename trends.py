import requests, random
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import time


def trends():
    response = requests.get('https://yastroka.yandex.net/trends')
    trends = response.json()['queries']

    return trends


def live_plotter(ax, words, x_loc, y_loc, color, size_input, rotation):
    if ax == []:
        plt.ion()
        fig = plt.figure(figsize=(11, 6))
        ax = fig.add_subplot(111, frameon=False)
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
        annot1 = []
        plt.show()
        return ax, annot1

    annot1 = ax.annotate(words, xy=(x_loc, y_loc), fontsize=size_input, xycoords='figure pixels', color=color,
                         rotation=rotation)
    plt.pause(0.01)

    return ax, annot1


ax = []
font_pixel_density = 17  # 16px per character
yandex_vals = trends()
ax, annot1 = live_plotter(ax, ' ', 0.0, 0.0, 'k', font_pixel_density, 0.0)
fig = ax.get_figure()
fig_size = fig.get_dpi() * fig.get_size_inches()
cmap = matplotlib.cm.get_cmap('tab10')
while True:
    yandex_vals = trends()

    for ii in range(0, len(yandex_vals)):

        annot_text = yandex_vals[ii]
        # find the size of the word in pixels
        annot_x_size = len(yandex_vals[ii]) * font_pixel_density
        # randomize the location of the word
        zoom_ratio = 0.95
        x_loc = random.uniform(0.0 + zoom_ratio, 1.0 - zoom_ratio) * (fig_size[0] - annot_x_size)
        y_loc = random.uniform(0.0 + zoom_ratio, 1.0 - zoom_ratio) * (fig_size[1] - font_pixel_density)

        # randomize the color,rotation angle, and size of the word text
        color = matplotlib.cm.colors.to_hex(cmap(np.random.rand(1))[0])
        # rotation = random.uniform(-1, 1)*30
        rotation = 0.0
        size_var = random.uniform(0.4, 1) * font_pixel_density
        prev_children = ax.get_children()
        ax, annot1 = live_plotter(ax, annot_text, x_loc, y_loc, color, size_var, rotation)
        for ii in prev_children:
            try:
                jj = (annot1.get_window_extent()).extents
                if jj[2] - ii.get_window_extent().extents[0] >= 0 and ii.get_window_extent().extents[2] - jj[0] >= 0 and \
                        jj[3] - ii.get_window_extent().extents[1] >= 0 and ii.get_window_extent().extents[3] - jj[
                    1] >= 0:
                    ii.remove()

            except:
                pass
        time.sleep(0.4)