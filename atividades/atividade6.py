import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams["figure.dpi"] = 110

df = pd.read_csv("online_gaming_behavior_dataset.csv")
display(df.head())
display(df.dtypes)

# Histograma da duração média da sessão
coluna_numerica = "AvgSessionDurationMinutes"

plt.figure(figsize=(8,5))
sns.histplot(df[coluna_numerica], kde=True, bins=25)
plt.title(f"Distribuição de {coluna_numerica}")
plt.xlabel(coluna_numerica)
plt.ylabel("Frequência")
plt.grid(axis="y", alpha=0.4)
plt.show()

# Scatter: horas jogadas x compras no jogo
var_x = "PlayTimeHours"
var_y = "InGamePurchases"

plt.figure(figsize=(8,5))
sns.scatterplot(x=df[var_x], y=df[var_y], alpha=0.6)
plt.title(f"Relação entre {var_x} e {var_y}")
plt.xlabel(var_x)
plt.ylabel(var_y)
plt.grid(True, alpha=0.3)
plt.show()

# Boxplot: compras por gênero de jogo
var_cat = "GameGenre"
var_num = "InGamePurchases"

plt.figure(figsize=(9,5))
sns.boxplot(x=df[var_cat], y=df[var_num])
plt.title(f"Distribuição de {var_num} por {var_cat}")
plt.xlabel(var_cat)
plt.ylabel(var_num)
plt.grid(axis="y", alpha=0.4)
plt.show()

# Heatmap de correlação
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

# Pairplot das variáveis mais importantes
important_vars = ['PlayTimeHours', 'PlayerLevel', 'AchievementsUnlocked',
                  'SessionsPerWeek', 'AvgSessionDurationMinutes']

df_important = df[important_vars]

sns.set_palette("husl")

pair_plot = sns.pairplot(df_important,
                        diag_kind='hist',
                        plot_kws={'alpha': 0.6, 's': 20},
                        diag_kws={'bins': 30, 'alpha': 0.7})

pair_plot.fig.suptitle('Pair Plot - Variáveis Mais Importantes do Gaming Dataset',
                       fontsize=16, y=1.02)

plt.show()
