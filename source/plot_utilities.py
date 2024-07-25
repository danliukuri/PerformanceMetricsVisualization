import matplotlib.pyplot as plt


def circle_legend(ax, labels, label_colors, position=(0, 0), label_spacing=0.7, line_spacing=0.2, circle_kwargs=None,
                  text_kwargs=None):
    if circle_kwargs is None:
        circle_kwargs = {}
    if text_kwargs is None:
        text_kwargs = {}

    rect = plt.Circle(xy=position, **circle_kwargs)
    ax.add_patch(rect)

    x, y = position
    total_height = len(labels) * label_spacing
    start_y = y + total_height / 2 - label_spacing / 2

    for i, label in enumerate(labels):
        lines = label.split('\n')
        for j, line in enumerate(lines):
            y_pos = start_y - i * label_spacing + line_spacing / 2 - j * line_spacing
            ax.text(x, y_pos, line, color=label_colors[i], **text_kwargs)
