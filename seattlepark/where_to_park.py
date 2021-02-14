# where_to_park.py
# wraps up all the other functions
from slice_df import slice_df
from max_freespace import max_freespace


def where_to_park(nhood, daytype, hour):
    df = slice_df(nhood, daytype, hour)
    (block, spaces) = max_freespace(df)
    print('Try parking on %s, which has an average of %3.1f open spaces at this time.' % (block, spaces))


if __name__ == '__main__':
    where_to_park('roosevelt','weekday',12)