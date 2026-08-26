# PROGETTO FINALE

import random
from datetime import datetime,timedelta
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# Directory di output per CSV e immagini
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# PARTE 1
negozi = ["Verona", "Roma", "Milano", "Napoli", "Torino", "Bologna"]
prodotti = ["Smartphone", "PC Gaming", "Air Pods", "TV OLed", "SoundBar", "Monitor 144Hz-2K",]
prezzi = {
    "Smartphone": 199.99,
    "PC Gaming": 1800.00,
    "Air Pods": 45.00,
    "TV OLed": 1500.00,
    "SoundBar": 200.00,
    "Monitor 144Hz-2K": 350.00,
}

vendite = {
    "data": [],
    "negozio": [],
    "prodotto": [],
    "quantita": [],
}

for _ in range(50):
    prodotto = random.choice(prodotti)

    vendite["data"].append((datetime(2026, 1, 1) + timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d"))
    vendite["negozio"].append(random.choice(negozi))
    vendite["prodotto"].append(prodotto)
    vendite["quantita"].append(random.randint(1, 20))

# PARTE 2
df = pd.DataFrame(vendite)
df["prezzo_unitario"] = df["prodotto"].map(prezzi)
df.to_csv(os.path.join(OUTPUT_DIR, "vendite.csv"), index=False)

print("File 'vendite.csv' salvato correttamente!")
print("\nStampa delle prime 5 righe")
print(df.head())
print(df.shape)
df.info()

# PARTE 3
df["incasso"] = df["quantita"] * df["prezzo_unitario"]

df.to_csv(os.path.join(OUTPUT_DIR, "vendite.csv"), index=False)
print("Aggiunta colonna INCASSO. File csv, salvato correttamente")

incasso_totale = df["incasso"].sum()
print(f"Incasso totale della catena: € {incasso_totale:,.2f}")

incasso_medio_negozio = df.groupby("negozio")["incasso"].sum().mean()
print(f"Incasso medio per negozio: € {incasso_medio_negozio:,.2f}")

prodotti_top3 = (
    df.groupby("prodotto")["quantita"].sum().sort_values(ascending=False).head(3)
)
print("\nI 3 prodotti più venduti (quantità):")
print(prodotti_top3)

raggruppamento = df.groupby(["negozio", "prodotto"])["incasso"].mean()
print("\nIncasso medio per Negozio e Prodotto (Anteprima):")
print(raggruppamento.head(5))

# PARTE 4

qta = df["quantita"].to_numpy()

media = np.mean(qta)
print (f"Quantità media venduta: {media:.2f} | Minimo: {np.min(qta)} | Massimo: {np.max(qta)} | Dev. Standard: {np.std(qta):.2f}")

vendite_sopra_media = (len(qta[qta > media]) / len(qta))*100
print (f"La percentuale di vendite sopra la media è: {vendite_sopra_media:.2f}%")

qta_prezzo = df[["quantita","prezzo_unitario"]].to_numpy()

incasso_calcolato = qta_prezzo[:,0] * qta_prezzo[:,1]

controllo_incassi = np.allclose(incasso_calcolato,df["incasso"].to_numpy())
print(f"Verifica incassi (Pandas Vs Numpy): {controllo_incassi}")

# PARTE 5

inc_neg = df.groupby("negozio")["incasso"].sum()
plt.figure(figsize=(8,4))
plt.bar(inc_neg.index, inc_neg.values, color="skyblue", edgecolor="black")
plt.xticks(rotation=45, ha="right")
plt.ylabel("Incasso (€)")
plt.title("Incasso Totale per Negozio")
plt.savefig(os.path.join(OUTPUT_DIR, "grafico_barre_prodotti.png"))
plt.tight_layout()
plt.show()


# Grafico a torta: percentuali nella torta + legenda con valore in € e percentuale
inc_prd = df.groupby("prodotto")["incasso"].sum()
labels = inc_prd.index.tolist()
values = inc_prd.values
total = values.sum()
fig, ax = plt.subplots(figsize=(8, 6))
# disegna la torta mostrando solo le percentuali dentro le fette
wedges, texts, autotexts = ax.pie(
    values,
    labels=None,            # niente etichette direttamente sulla torta
    autopct="%1.1f%%",      # percentuale dentro ogni fetta
    startangle=90,
    wedgeprops={"edgecolor": "white"}
)
ax.set_title("Percentuale Incassi per Prodotto")
ax.axis("equal")  # mantiene la torta circolare
# costruisce le stringhe di legenda con valore assoluto e percentuale
percent = values / total * 100
legend_labels = [f"{lab}: € {val:,.0f} ({pct:.1f}%)" for lab, val, pct in zip(labels, values, percent)]
# legenda sincronizzata con i colori della torta, posizionata a destra
ax.legend(wedges, legend_labels, title="Prodotto", loc="center left", bbox_to_anchor=(1, 0.5), fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "grafico_torta_prodotti.png"), bbox_inches="tight", dpi=300)
plt.show()


# 3. Grafico a linee: andamento giornaliero degli incassi totali della catena
plt.figure(figsize=(10, 4))
# Importante ordinare per data per visualizzare la linea correttamente
df.groupby("data")["incasso"].sum().plot(kind="line", marker="o", color="green")
plt.title("Andamento Giornaliero degli Incassi Totali")
plt.xlabel("DATA")
plt.ylabel("Incasso Totale (€)")
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "grafico_linee_andamento.png"))
plt.show()


# PARTE 6 – Analisi Avanzata
# 1) Definire le categorie per prodotto
product_to_category = {
    "Smartphone": "Telefonia",
    "PC Gaming": "Informatica",
    "Air Pods": "Audio",
    "TV OLed": "TV",
    "SoundBar": "Audio",
    "Monitor 144Hz-2K": "Informatica",
}

# 2) Creare la colonna 'Categoria' nel DataFrame
df["categoria"] = df["prodotto"].map(product_to_category).fillna("Altro")

# 3) Calcolare per ogni categoria: incasso totale e quantità media venduta

# Calcola riepilogo per categoria (DataFrame separato)
riepilogo_categoria = df.groupby("categoria").agg(
    Incasso_totale = ("incasso", "sum"),
    Quantita_media  = ("quantita", "mean")
).reset_index()

# (Opzionale) arrotonda la quantità media per leggibilità
riepilogo_categoria["Quantita_media"] = riepilogo_categoria["Quantita_media"].round(2)

# Unisci i risultati al DataFrame originale: ora ogni riga avrà le colonne aggregate della sua categoria
df = df.merge(riepilogo_categoria, on="categoria", how="left")

# Controllo veloce che siano presenti le nuove colonne
print(df.head())
#(Opzionale) vedi tutti i nomi di colonna
print(df.columns.tolist())

# Salva il DataFrame aggiornato (contiene Categoria, Incasso_totale, Quantita_media)
df.to_csv(os.path.join(OUTPUT_DIR, "vendite_analizzate.csv"), index=False)

# (Opzionale) salva anche il riepilogo per categoria in un file separato
riepilogo_categoria.to_csv(os.path.join(OUTPUT_DIR, "vendite_per_categoria.csv"), index=False)


# 1. Grafico combinato (Incasso medio per categoria = barre, Quantità media = linea)
fig, ax1 = plt.subplots(figsize=(8, 5))

# raggruppa usando i nomi reali delle colonne
categoria_stats = df.groupby("categoria").agg(
    Incasso_Medio=("incasso", "mean"),
    Quantita_Media=("quantita", "mean")
).sort_values("Incasso_Medio", ascending=False)

# barre: incasso medio
categoria_stats["Incasso_Medio"].plot(
    kind="bar", ax=ax1, color="orange", alpha=0.7, label="Incasso medio (€)"
)
ax1.set_ylabel("Incasso medio (€)", color="orange")
ax1.tick_params(axis="y", labelcolor="orange")

# asse secondario: quantità media (linea)
ax2 = ax1.twinx()
x = np.arange(len(categoria_stats))
ax2.plot(x, categoria_stats["Quantita_Media"].values, color="blue", marker="s",
         linewidth=2, label="Quantità media")
ax2.set_ylabel("Quantità media venduta", color="blue")
ax2.tick_params(axis="y", labelcolor="blue")

# allinea i tick x con le etichette delle categorie
ax1.set_xticks(x)
ax1.set_xticklabels(categoria_stats.index, rotation=45, ha="right")

plt.title("Incasso medio per categoria e quantità media venduta")
fig.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, "grafico_combinato_categoria.png"), bbox_inches="tight", dpi=300)  # salva prima di show
plt.show()


# 2. Funzione top_n_prodotti: restituisce i top-n prodotti per incasso totale
def top_n_prodotti(n, df=df):
    #Restituisce una Series (o DataFrame se preferisci) con i n prodotti con maggior incasso totale.
    return (
        df.groupby("prodotto")["incasso"]
          .sum()
          .sort_values(ascending=False)
          .head(n)
    )

# Esempio d'uso
print("Top 3 prodotti per incasso totale:")
print(top_n_prodotti(3))
