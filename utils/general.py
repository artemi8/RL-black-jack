from matplotlib import pyplot as plt

# def plot_Q_values(q_values):
#     all_values_0 = [sub_dict[0]['value'] for sub_dict in q_values.values()]
#     all_values_1 = [sub_dict[1]['value'] for sub_dict in q_values.values()]

#     # Plotting
#     fig, ax = plt.subplots(figsize=(10, 5))
#     width = 0.35  # the width of the bars
#     x = range(len(q_values))

#     rects1 = ax.bar(x, all_values_0, width, label='Value 0')
#     rects2 = ax.bar([i + width for i in x], all_values_1, width, label='Value 1')

#     ax.set_xlabel('Sub-dictionary Key')
#     ax.set_ylabel('Values')
#     ax.set_title('Paired Values for Each Sub-dictionary')
#     ax.set_xticks([i + width/2 for i in x])
#     ax.set_xticklabels(q_values.keys())

#     legend_labels = ['Stick', 'Hit']
#     ax.legend([rects1, rects2], legend_labels)
#     plt.show()
    
def plot_monte_carlo_q_values(agent, usable_ace, deck_feature_representative=0):
    x = range(2, 22)  # Assuming current_sum ranges from 1 to 21

    # q_stick = [agent.Q[sum_val - 1, int(usable_ace), deck_feature_representative, 0] for sum_val in x]
    # q_hit = [agent.Q[sum_val - 1, int(usable_ace), deck_feature_representative, 1] for sum_val in x]
    
    q_stick = [agent.Q[sum_val-2, int(usable_ace), 0, 0] for sum_val in x]
    q_hit = [agent.Q[sum_val-2, int(usable_ace), 1, 0] for sum_val in x]

    fig, ax = plt.subplots()

    bar_width = 0.35
    bar_stick = [i - bar_width / 2 for i in x]
    bar_hit = [i + bar_width / 2 for i in x]

    ax.bar(bar_stick, q_stick, bar_width, label='Stick')
    ax.bar(bar_hit, q_hit, bar_width, label='Hit')

    ax.set_xlabel('Current Sum')
    ax.set_ylabel('Q-Value')
    ax.set_title('Q-values with Usable Ace' if usable_ace else 'Q-values with Unusable Ace')
    ax.set_xticks(x)
    ax.set_xticklabels(x)
    ax.legend()

    plt.show()
