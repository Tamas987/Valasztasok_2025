import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO

sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

file_path = "Adatbazis.xlsx"
base_columns = [
    "Judet", "UAT", "Localitate", "Mediu",
    "Înscriși pe liste permanente", "Voturi Totale", "Barbati", "Femei"
]
age_columns_f = [f"Femei {i}" for i in range(18, 121)]
age_columns_m = [f"Barbati {i}" for i in range(18, 121)]
all_columns = base_columns + age_columns_f + age_columns_m

df = pd.read_excel(file_path, sheet_name=0, usecols=lambda col: col in all_columns)

# Kiszámolások

df['Reszvetel_arany'] = df['Voturi Totale'] / df['Înscriși pe liste permanente']

county_participation = df.groupby("Judet")[["Voturi Totale", "Înscriși pe liste permanente"]].sum()
county_participation["Reszvetel_arany"] = county_participation["Voturi Totale"] / county_participation["Înscriși pe liste permanente"]

env_participation = df.groupby("Mediu")[["Voturi Totale", "Înscriși pe liste permanente"]].sum()
env_participation["Reszvetel_arany"] = env_participation["Voturi Totale"] / env_participation["Înscriși pe liste permanente"]

gender_totals = df[["Barbati", "Femei"]].sum()

age_f = df[age_columns_f].sum()
age_m = df[age_columns_m].sum()
ages = list(range(18, 121))

top10_localities = df[["Localitate", "Reszvetel_arany"]].dropna().sort_values("Reszvetel_arany", ascending=False).head(10)

gender_by_county = df.groupby("Judet")[["Barbati", "Femei"]].sum().sort_values("Femei")

# Segédfüggvény a matplotlib ábrák base64-kódolásához
def fig_to_base64(fig):
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return img_base64

# 1. Megyénkénti részvételi arány
fig1, ax1 = plt.subplots()
county_participation["Reszvetel_arany"].sort_values().plot(kind="barh", color="teal", ax=ax1)
ax1.set_title("1. Megyénkénti részvételi arány")
ax1.set_xlabel("Részvételi arány")
fig1.tight_layout()
img1 = fig_to_base64(fig1)

# 2. Városi vs falusi részvétel
fig2, ax2 = plt.subplots()
env_participation["Reszvetel_arany"].plot(kind="bar", color=["skyblue", "orange"], ax=ax2)
ax2.set_title("2. Városi vs falusi részvétel")
ax2.set_ylabel("Részvételi arány")
ax2.set_xticklabels(env_participation.index, rotation=0)
fig2.tight_layout()
img2 = fig_to_base64(fig2)

# 3. Nemek szerinti részvétel
fig3, ax3 = plt.subplots()
gender_totals.plot(kind="bar", color=["cornflowerblue", "lightcoral"], ax=ax3)
ax3.set_title("3. Nemek szerinti részvétel")
ax3.set_ylabel("Szavazatszám")
ax3.set_xticklabels(["Férfiak", "Nők"], rotation=0)
fig3.tight_layout()
img3 = fig_to_base64(fig3)

# 4. Életkori eloszlás nemek szerint
fig4, ax4 = plt.subplots()
ax4.plot(ages, age_f.values, label="Nők", color="red")
ax4.plot(ages, age_m.values, label="Férfiak", color="blue")
ax4.set_title("4. Életkori eloszlás nemek szerint")
ax4.set_xlabel("Életkor")
ax4.set_ylabel("Szavazatszám")
ax4.legend()
fig4.tight_layout()
img4 = fig_to_base64(fig4)

# 5. Top 10 település részvételi arány szerint
fig5, ax5 = plt.subplots()
sns.barplot(data=top10_localities, x="Reszvetel_arany", y="Localitate", palette="viridis", ax=ax5)
ax5.set_title("5. Top 10 település részvételi arány szerint")
ax5.set_xlabel("Részvételi arány")
fig5.tight_layout()
img5 = fig_to_base64(fig5)

# 6. Megyénkénti férfi/nő részvétel összevetése
fig6, ax6 = plt.subplots()
gender_by_county.plot(kind="barh", stacked=False, color=["blue", "pink"], ax=ax6)
ax6.set_title("6. Megyénkénti férfi/nő részvétel összevetése")
ax6.set_xlabel("Szavazatszám")
fig6.tight_layout()
img6 = fig_to_base64(fig6)

# HTML tartalom összeállítása
# ... (az előző kód ugyanaz marad)

html_content = f"""
<!DOCTYPE html>
<html lang="hu">
<head>
<meta charset="UTF-8" />
<title>A romániai államelnöki választások elsőkörös részvételi arányának elemzése</title>
<style>
    body {{ font-family: Arial, sans-serif; max-width: 900px; margin: auto; padding: 20px; background: #f9f9f9; }}
    h1 {{ color: #2c3e50; }}
    h2 {{ color: #34495e; margin-top: 40px; }}
    .qa-section {{ background: #ecf0f1; padding: 15px; border-radius: 8px; margin-bottom: 30px; }}
    .question {{ font-weight: bold; color: #2980b9; margin-top: 20px; }}
    .answer {{ margin-left: 20px; }}
    img {{ max-width: 100%; height: auto; border: 1px solid #ccc; margin-top: 10px; }}
</style>
</head>
<body>

<h1>A romániai államelnöki választások elsőkörös részvételi arányának elemzése</h1>

<div class="qa-section">
    <div class="question">Q1: Miről szól a projekt?</div>
    <div class="answer">A projekt a 20205-ös államelnöki választás első körében leadott szavazatszámok eloszlását dolgozza fel. Célja szemléltetni földrajzi, nemszerinti és korszerinti bontásban a választási részvétel alakulását.</div>

    <div class="question">Q2: Milyen adatokat használsz?</div>
    <div class="answer">Az adatok az Állandó Választási Iroda weboldaláról kerültek letöltésre. Utólagos feldolgozásnak vetettük alá, a meglévő adatokból új, releváns változókat hoztunk létre.</div>

    <div class="question">Q3: Miért érdekesek az adatok?</div>
    <div class="answer">A jelenlegi politikai és szociális kontextusban talán egyike a legrelevánsabb témáknak. Az adatok egy olyan, a teljes társadalomra kiterjedő döntés numerikus aspektusait vetítik le, amely az elkövetkezendő időszak alakulását hordozza magában.</div>

    <div class="question">Q4: Ki a cél-felhasználó?</div>
    <div class="answer">A vizualizációink cél-felhasználói a választóképes állampolgárok, valamint azon hatóságok és csoportosulások, akik stratégiai döntések meghozatalában hasonló eloszlásokra támaszkodnak.</div>
</div>

<h2>1. Megyénkénti részvételi arány</h2>
<img src="data:image/png;base64,{img1}" alt="Megyénkénti részvételi arány" />

<h2>2. Városi vs falusi részvétel</h2>
<img src="data:image/png;base64,{img2}" alt="Városi vs falusi részvétel" />

<h2>3. Nemek szerinti részvétel</h2>
<img src="data:image/png;base64,{img3}" alt="Nemek szerinti részvétel" />

<h2>4. Életkori eloszlás nemek szerint</h2>
<img src="data:image/png;base64,{img4}" alt="Életkori eloszlás nemek szerint" />

<h2>5. Top 10 település részvételi arány szerint</h2>
<img src="data:image/png;base64,{img5}" alt="Top 10 település részvételi arány szerint" />

<h2>6. Megyénkénti férfi/nő részvétel összevetése</h2>
<img src="data:image/png;base64,{img6}" alt="Megyénkénti férfi/nő részvétel összevetése" />

</body>
</html>
"""

# HTML mentése fájlba
with open("jelentes.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("A jelentes.html fájl elkészült, nyisd meg a böngésződben!")
