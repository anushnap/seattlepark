# max_freespace.py
# this function takes a sliced dataframe and returns (as str) the block with highest space availability
import pandas as pd
import numpy as np


def max_freespace(df):
    # Make new column combining Unitdesc and Side
    df['Block_And_Side'] = df['Unitdesc'] + " (" + df['Side'] + " side)"
    # List of unique blocks/sides
    blockfaces = df['Block_And_Side'].unique()
    # Loop through blocks and calculate average # of free spaces
    free_spaces = np.ndarray((len(blockfaces), ))
    for i, block in enumerate(blockfaces):
        this_block = df[df['Block_And_Side'] == block]
        num_obs = this_block.shape[0]
        free_spaces[i] = this_block['Free_Spaces'].sum() / num_obs # Use num_obs instead of sum of total parking spots?
        
    max_spaces = np.max(free_spaces)
    k = np.argmax(free_spaces)
    best_block = blockfaces[k]
    

    return best_block, max_spaces
