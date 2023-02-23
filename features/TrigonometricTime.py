
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


def add_trigonometric_time(df):
    # Sin and cos time are calculated by finding minutes from midnight for each date time
    df['date_time'] = pd.to_datetime(df['date_time'])
    sin_time = []
    cos_time = []
    for i in df.index:
        minutes_after_midnight = (df.at[i, 'date_time'] - df.at[i, 'date_time'].replace(
            hour=0, minute=0, second=0, microsecond=0)).total_seconds() / (60)

        # Use numpy to create sine and cosine values
        minutes_in_day = 24 * 60
        sin_time.append(np.sin(
            2 * np.pi * minutes_after_midnight / minutes_in_day))
        cos_time.append(np.cos(
            2 * np.pi * minutes_after_midnight / minutes_in_day))
    df['sin_time'] = sin_time
    df['cos_time'] = cos_time
    return df


'''
#klokke-figur fra Nina

fig2, ax2 = plt.subplots(figsize=(8, 8))
df.sample(100).plot.scatter('sin_time', 'cos_time', ax=ax2).set_aspect('equal')
ax2.set_xlabel('sin_time', fontsize=20, labelpad=20)
ax2.set_ylabel('cos_time', fontsize=20, labelpad=20)
ax2.set_title('Sin and cos time plotted against each other',
              fontsize=22, pad=20)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.tight_layout()
plt.show()
'''
