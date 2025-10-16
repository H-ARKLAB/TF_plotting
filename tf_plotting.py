# -*- coding: utf-8 -*-

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
df = pd.read_csv(
    "/content/sites.txt",
    sep=r"\s+",
    engine="python",
    header=1)
df['NAME'] = df['name'].copy()
df=df.set_index('name')[['NAME','index', 'start', 'end', 'score']]
df.index = df.index+df['index'].astype(str)
df = df.drop('index', axis=1)

occ = pd.read_csv(
    "/content/occ.txt",
    sep=r"\s+",
    engine="python",
    header=0,
)
occ.rename(columns={'theonlyone':'occupancy'}, inplace=True)
occ = occ.set_index("site")

merged = occ.join(df, how="left")
merged.set_index('NAME', inplace=True)
merged.index = merged.index.str.strip()
merged

cols = ['start',	'end',	'score',	'occupancy']
regions = {
    "FP1": [-238, -219, None,1],
    "R1": [-196, -181, None,1],
    "R2": [-161, -146, None,1],
    "R3": [-146, -130, None,1],
    "SIRE": [-109,  -94, None,1]
}
to_add = pd.DataFrame.from_dict(regions, orient='index', columns=cols)
final = pd.concat([merged, to_add])
#final

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

df = final.copy()
# df: columns = ['name','start','end','score','occupancy'] (또는 인덱스가 name면 reset)
if 'name' not in df.columns:
    df = df.reset_index().rename(columns={'index':'name'})
df['name'] = df['name'].astype(str).str.strip()

# 1) regions 묶기
REGIONS = ['FP1','R1','R2','R3','SIRE']
df['row'] = np.where(df['name'].isin(REGIONS), 'regions', df['name'])

# 2) y축 순서 정의: regions를 맨 위(또는 원하는 위치)로
others = [n for n in df['row'].unique() if n != 'regions']
tfs = ['regions'] + sorted(others)   # 원하면 정렬 대신 원하는 순서 리스트로 지정
y_map = {tf:i for i, tf in enumerate(tfs)}

# 3) 그림 그리기
fig_h = max(4, 0.45*len(tfs) + 1.5)
fig, ax = plt.subplots(figsize=(12, fig_h))
colors = plt.cm.tab20(np.linspace(0, 1, len(tfs)))

for i, (key, g) in enumerate(df.groupby('row')):
    y = y_map[key]
    color = colors[i % len(colors)]
    for _, r in g.iterrows():
        x0, x1 = float(r['start']), float(r['end'])
        w = x1 - x0
        alpha = np.clip(0.25 + float(r.get('occupancy', 0)), 0.25, 0.95)
        ax.add_patch(
            patches.Rectangle((x0, y-0.35), w, 0.7,
                              facecolor=color, edgecolor='k', linewidth=0.8, alpha=alpha)
        )

# 배경 하이라이트 영역 (FP, R1, R2, R3, SIRE 등)
highlight_regions = [
    #{"name": "FP2", "xmin": -280, "xmax": -268, "color": "plum"},
    {"name": "FP1", "xmin": -238, "xmax": -219, "color": "plum"},
    {"name": "R1", "xmin": -196, "xmax": -181, "color": "yellow"},
    {"name": "R2", "xmin": -161, "xmax": -146, "color": "yellow"},
    {"name": "R3", "xmin": -146, "xmax": -130, "color": "gold"},
    {"name": "SIRE", "xmin": -109, "xmax": -94, "color": "peachpuff"}
]

for region in highlight_regions:
    ax.axvspan(region['xmin'], region['xmax'], color=region['color'], alpha=0.3)
    ax.text((region['xmin'] + region['xmax']) / 2, 8.3,
            region['name'], ha='center', va='center', fontweight='bold')


# 4) 축/라벨
ax.set_yticks([y_map[t] for t in tfs])
ax.set_yticklabels(tfs)
ax.set_ylim(-1, len(tfs))
ax.set_xlim(df['start'].astype(float).min()-10, df['end'].astype(float).max()+10)
ax.set_xlabel('Position')
ax.set_ylabel('Transcription Factors')
plt.tight_layout()
plt.show()
