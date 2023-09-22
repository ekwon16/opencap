'''
    ---------------------------------------------------------------------------
    OpenCap processing: utilsPlotting.py
    ---------------------------------------------------------------------------

    Copyright 2022 Stanford University and the Authors
    
    Author(s): Antoine Falisse, Scott Uhlrich
    
    Licensed under the Apache License, Version 2.0 (the "License"); you may not
    use this file except in compliance with the License. You may obtain a copy
    of the License at http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
'''

import numpy as np
import matplotlib.pyplot as plt

def plot_dataframe(dataframes, x=None, y=[], xlabel=None, ylabel=None, 
                   labels=None, title=None, xrange=None):
    
    # Handle case specific number of subplots.
    if not x and not y:
        nRow = int(np.ceil(np.sqrt(dataframes[0].shape[1]-1)))
        nCol = int(np.ceil(np.sqrt(dataframes[0].shape[1]-1)))
        if not xlabel:
            xlabel = list(dataframes[0].columns)[0]
        x = 'time'
        y = list(dataframes[0].columns)[1:]        
    elif not x and y:
        nRow = int(np.ceil(np.sqrt(len(y))))
        nCol = int(np.ceil(np.sqrt(len(y))))
        if not xlabel:
            xlabel = list(dataframes[0].columns)[0]
        x = 'time'
    else:
        nRow = int(np.ceil(np.sqrt(len(y))))
        nCol = int(np.ceil(np.sqrt(len(y))))
        if not xlabel:
            xlabel = x
        if not ylabel:
            ylabel = y[0]        
    if nRow >= len(y):
        nRow = 1
    nAxs = len(y)
        
    # Labels for legend.
    if not labels:
        labels = ['dataframe_' + str(i) for i in range(len(dataframes))]
    elif len(labels) != len(dataframes):
        print("WARNING: The number of labels ({}) does not match the number of input dataframes ({})".format(len(labels), len(dataframes)))
        labels = ['dataframe_' + str(i) for i in range(dataframes)]
 
    if nCol == 1: # Single plot.
        fig = plt.figure()
        color=iter(plt.cm.rainbow(np.linspace(0,1,len(dataframes)))) 
        for c, dataframe in enumerate(dataframes):
            c_color = next(color)     
            plt.plot(dataframe[x], dataframe[y], c=c_color, label=labels[c])
            if xrange is not None:
                plt.xlim(xrange)
    else: # Multiple subplots.
        fig, axs = plt.subplots(nRow, nCol, sharex=True)     
        for i, ax in enumerate(axs.flat):
            color=iter(plt.cm.rainbow(np.linspace(0,1,len(dataframes)))) 
            if i < nAxs:
                for c, dataframe in enumerate(dataframes):
                    c_color = next(color)                
                    ax.plot(dataframe[x], dataframe[y[i]], c=c_color, label=labels[c])
                    ax.set_title(y[i])
                    if xrange is not None:
                        plt.xlim(xrange)
            if i == 0:
                handles, labels = ax.get_legend_handles_labels()
        
    # Axis labels and legend.
    if nRow > 1 and nCol > 1:
        plt.setp(axs[-1, :], xlabel=xlabel)
        plt.setp(axs[:, 0], ylabel=ylabel)
        axs[0][0].legend(handles, labels)
    elif nRow == 1 and nCol > 1:
        plt.setp(axs[:,], xlabel=xlabel)
        plt.setp(axs[0,], ylabel=ylabel)
        axs[0,].legend(handles, labels)
    else:
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend(labels)
        
    if nRow == 1 and nCol == 1:
        # Add figure title.
        if title:
            plt.title(title)        
    else:
        # Add figure title.
        if title:
            fig.suptitle(title)
        # Align labels.        
        fig.align_ylabels()
        # Hidde empty subplots.
        nEmptySubplots = (nRow*nCol) - len(y)
        axs_flat = axs.flat
        for ax in (axs_flat[len(axs_flat)-nEmptySubplots:]):
            ax.set_visible(False)
                   
    # Tight layout (should make figure big enough first).
    # fig.tight_layout()
    
    # Show plot (needed if running through terminal).
    plt.show()
    

def plot_dataframe_with_shading(mean_dataframe, sd_dataframe=None, y=None, 
                                leg=None, xlabel=None, title=None, legend_entries=None):
    if not isinstance(mean_dataframe, list):
        mean_dataframe = [mean_dataframe]
    
    if sd_dataframe is not None:
        if not isinstance(sd_dataframe, list):
            sd_dataframe = [sd_dataframe]
            
    if not isinstance(leg, list):
        leg = [leg] * len(mean_dataframe)
    
    if y is None:
        y = [col for col in mean_dataframe[0].columns if col != 'time']

    columns = [col for col in y if not any(sub in col for sub in ['_beta', 'mtp', 'time'])]

    if leg[0] == 'r':
        columns = [col for col in columns if not col.endswith('_l')]
    elif leg[0] == 'l':
        columns = [col for col in columns if not col.endswith('_r')]

    num_columns = len(columns)
    num_rows = (num_columns + 3) // 4  # Always 4 columns per row

    colormap = plt.cm.get_cmap('viridis', len(mean_dataframe))

    fig, axes = plt.subplots(num_rows, 4, figsize=(12, 8))
    axes = axes.flatten()

    for i, column in enumerate(columns):
        row = i // 4
        ax = axes[i]

        for j, (mean_df, sd_df) in enumerate(zip(mean_dataframe, sd_dataframe)):
            if len(mean_dataframe) > 1:
                color = np.multiply(colormap(j),.7) # avoid yellow at end of viridis
            else:
                color = 'black'
            
            if leg[j] is not None and (column.endswith('_r') or column.endswith('_l')):
                col=column[:-2] + '_' + leg[j]
                colLabel = column[:-2]
            else:
                col = column
                colLabel = column
            
            mean_values = mean_df[col]
            
            if legend_entries is None: 
                thisLegend = [] 
            else: 
                thisLegend = legend_entries[j]

            ax.plot(mean_values, color=color, label=thisLegend)

            # Check if sd_df is not None before plotting
            if sd_df is not None:
                sd_column = col
                if sd_column in sd_df.columns:
                    sd_values = sd_df[sd_column]
                    ax.fill_between(
                        range(len(mean_values)),
                        mean_values - sd_values,
                        mean_values + sd_values,
                        color=color,
                        alpha=0.3,
                        linewidth=0,  # Remove surrounding line
                    )
                    

        ax.set_xlabel(xlabel if row == num_rows - 1 else None, fontsize=12)
        ax.set_ylabel(colLabel, fontsize=12)

        # Increase font size for axis labels
        ax.tick_params(axis='both', which='major', labelsize=10)
        
    # Create the legend in the first subplot if legend_entries is provided
    if legend_entries:
        axes[0].legend()

    # Remove any unused subplots
    if num_columns < num_rows * 4:
        for i in range(num_columns, num_rows * 4):
            fig.delaxes(axes[i])

    # Title
    if title is not None:
        fig.suptitle(title)

    plt.tight_layout()
    plt.show()

# def custom_bar(lower_bound, upper_bound, vertical_values, reverse_colors=False):
#     middle_width = upper_bound - lower_bound
#     green_width = 2 * middle_width  # Green segment is twice the width of the middle segment
#     red_width = 2 * middle_width    # Red segment is twice the width of the middle segment

#     if reverse_colors:
#         colors = ['green', 'yellow', 'red']
#     else:
#         colors = ['red', 'yellow', 'green']
    
#     fig, ax = plt.subplots(figsize=(10, 2))
    
#     # Plot the green segment to the left
#     ax.barh(0, green_width, left=lower_bound - green_width, color=colors[0], height=1, label='Below Lower Bound')
    
#     # Plot the yellow (middle) segment
#     ax.barh(0, middle_width, left=lower_bound, color=colors[1], height=1, label='Between Bounds')
    
#     # Plot the red segment to the right
#     ax.barh(0, red_width, left=upper_bound, color=colors[2], height=1, label='Above Upper Bound')
    
#     # Plot vertical bars for the specified values
#     for value in vertical_values:
#         ax.axvline(value, color='black', linestyle='--', linewidth=1)
    
#     ax.set_xlim(lower_bound - green_width, upper_bound + red_width)  # Adjusted xlim
#     ax.set_yticks([])
#     ax.set_xticks([])

#     # Hide all spines
#     for spine in ax.spines.values():
#         spine.set_visible(False)   

#     plt.show()

# # Example usage:
# lower_bound = -40
# upper_bound = 40
# vertical_values = [-30, 0, 20]
# custom_bar(lower_bound, upper_bound, vertical_values, reverse_colors=True)

def create_custom_bar_subplots(data_dict_list):
    num_subplots = len(data_dict_list)
    fig, axs = plt.subplots(num_subplots, 1, figsize=(6, 2 * num_subplots), sharex=False)
    
    for i, data_dict in enumerate(data_dict_list):
        name = data_dict['name']
        lower_bound, upper_bound = data_dict['bounds']
        vertical_values = data_dict['values']
        reverse_colors = data_dict.get('reverse_colors', False)

        middle_width = upper_bound - lower_bound
        green_width = 2 * middle_width  # Green segment is twice the width of the middle segment
        red_width = 2 * middle_width    # Red segment is twice the width of the middle segment

        if reverse_colors:
            colors = ['#06D6A0', '#FFD166', '#FF6B6B']  # Warm color palette
        else:
            colors = ['#FF6B6B', '#FFD166', '#06D6A0']  # Warm color palette, reversed

        axs[i].barh(0, green_width, left=lower_bound - green_width, color=colors[0], height=1, label='Below Lower Bound')
        axs[i].barh(0, middle_width, left=lower_bound, color=colors[1], height=1, label='Between Bounds')
        axs[i].barh(0, red_width, left=upper_bound, color=colors[2], height=1, label='Above Upper Bound')

        for value in vertical_values:
            axs[i].axvline(value, color='black', linestyle='-', linewidth=3)

        axs[i].set_xlim(lower_bound - green_width, upper_bound + red_width)
        axs[i].set_yticks([])
        if reverse_colors:
            axs[i].set_xticks([lower_bound])
        else:
            axs[i].set_xticks([upper_bound])

        for spine in axs[i].spines.values():
            spine.set_visible(False)

        axs[i].set_title(name)

    plt.tight_layout()
    plt.show()

# Example usage:
# data_dict_list = [
#     {
#         'name': 'Custom Bar 1',
#         'bounds': (-2, 1),
#         'values': [-1, 0, 1],
#         'reverse_colors': False
#     },
#     {
#         'name': 'Custom Bar 2',
#         'bounds': (-400, 1367),
#         'values': [-300, 0, 300, 800, 1200],
#         'reverse_colors': True
#     },
#     {
#         'name': 'Custom Bar 3',
#         'bounds': (-10, 10),
#         'values': [-5, 0, 5]
#     }
# ]