from matplotlib import pyplot as plt

def plot_Q_values(q_values):
    all_values_0 = [sub_dict[0]['value'] for sub_dict in q_values.values()]
    all_values_1 = [sub_dict[1]['value'] for sub_dict in q_values.values()]

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 5))
    width = 0.35  # the width of the bars
    x = range(len(q_values))

    rects1 = ax.bar(x, all_values_0, width, label='Value 0')
    rects2 = ax.bar([i + width for i in x], all_values_1, width, label='Value 1')

    ax.set_xlabel('Sub-dictionary Key')
    ax.set_ylabel('Values')
    ax.set_title('Paired Values for Each Sub-dictionary')
    ax.set_xticks([i + width/2 for i in x])
    ax.set_xticklabels(q_values.keys())

    legend_labels = ['Stick', 'Hit']
    ax.legend([rects1, rects2], legend_labels)
    plt.show()