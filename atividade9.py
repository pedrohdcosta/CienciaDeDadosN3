import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('online_gaming_behavior_dataset.csv')

numeric_columns = ['Age', 'PlayTimeHours', 'InGamePurchases', 'SessionsPerWeek',
                  'AvgSessionDurationMinutes', 'PlayerLevel', 'AchievementsUnlocked']

df_numeric = df[numeric_columns]

correlation_matrix = df_numeric.corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix,
           annot=True,
           cmap='RdBu_r',
           center=0,
           square=True,
           fmt='.2f',
           cbar_kws={'label': 'Coeficiente de Correlação'})

plt.title('Heatmap de Correlação - Dataset Gaming Online', fontsize=16, pad=20)
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()

important_vars = ['PlayTimeHours', 'PlayerLevel', 'AchievementsUnlocked',
                  'SessionsPerWeek', 'AvgSessionDurationMinutes']

df_important = df[important_vars]

plt.style.use('default')
sns.set_palette("husl")

fig = plt.figure(figsize=(15, 12))
pair_plot = sns.pairplot(df_important,
                        diag_kind='hist',
                        plot_kws={'alpha': 0.6, 's': 20},
                        diag_kws={'bins': 30, 'alpha': 0.7})

pair_plot.fig.suptitle('Pair Plot - Variáveis Mais Importantes do Gaming Dataset',
                       fontsize=16, y=1.02)

pair_plot.fig.tight_layout()

for i in range(len(important_vars)):
    for j in range(len(important_vars)):
        if i != j:
            ax = pair_plot.axes[i, j]
            corr = df_important.iloc[:, j].corr(df_important.iloc[:, i])
            ax.text(0.05, 0.95, f'r = {corr:.3f}',
                   transform=ax.transAxes, fontsize=10,
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))

plt.show()

