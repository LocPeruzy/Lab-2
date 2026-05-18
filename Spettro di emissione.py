import numpy as np
# Forza l'uso del backend 'Agg' prima di importare pyplot per evitare errori su server headless
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def wavelength_to_rgb(wavelength):
    """
    Semplificazione dell'algoritmo di Dan Bruton per convertire 
    una lunghezza d'onda (nm) in coordinate RGB nel visibile (380-750 nm).
    """
    w = float(wavelength)
    if 380 <= w < 440:
        R, G, B = -(w - 440) / (440 - 380), 0.0, 1.0
    elif 440 <= w < 490:
        R, G, B = 0.0, (w - 440) / (490 - 440), 1.0
    elif 490 <= w < 510:
        R, G, B = 0.0, 1.0, -(w - 510) / (510 - 490)
    elif 510 <= w < 580:
        R, G, B = (w - 510) / (580 - 510), 1.0, 0.0
    elif 580 <= w < 645:
        R, G, B = 1.0, -(w - 645) / (645 - 580), 0.0
    elif 645 <= w <= 750:
        R, G, B = 1.0, 0.0, 0.0
    else:
        R, G, B = 0.0, 0.0, 0.0

    # Fattore di intensità per la sensibilità dell'occhio ai bordi dello spettro
    if 380 <= w < 420:
        factor = 0.3 + 0.7 * (w - 380) / (420 - 380)
    elif 420 <= w < 701:
        factor = 1.0
    elif 701 <= w <= 750:
        factor = 0.3 + 0.7 * (750 - w) / (750 - 701)
    else:
        factor = 0.0

    return (R * factor, G * factor, B * factor)

def genera_spettro(wavelengths, titolo, ax):
    """
    Disegna uno spettro di emissione su fondo nero su un asse matplotlib.
    """
    w_min, w_max = 380, 750
    spettro_img = np.zeros((100, w_max - w_min, 3))
    
    ax.imshow(spettro_img, extent=[w_min, w_max, 0, 10])
    ax.set_facecolor('black')
    
    for wl in wavelengths:
        if w_min <= wl <= w_max:
            color = wavelength_to_rgb(wl)
            ax.axvline(x=wl, color=color, linewidth=2.5, alpha=0.9, 
                       solid_capstyle='butt')
            
    ax.set_title(titolo, fontsize=12, fontweight='bold', pad=10)
    ax.set_xlabel(r"Lunghezza d'onda $\lambda$ [nm]", fontsize=10)
    ax.set_xlim(w_min, w_max)
    ax.set_yticks([])  
    ax.grid(False)

# --- Dati ---
dati_sperimentali = {
    'angoli': [51.1, 50.2, 49.4, 48.3, 48.1, 47.3],
    'wavelengths': [424, 468, 472, 483, 546, 649]
}
wavelengths_hg_teorico = [404.66, 435.83, 546.07, 576.96, 579.07]

# --- Generazione ed esportazione ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
fig.patch.set_facecolor('#f4f4f4')

# Task 1
genera_spettro(dati_sperimentali['wavelengths'], "Task 1: Spettro di Emissione del Gas Ionizzato (Dati Sperimentali)", ax1)

# Task 2
genera_spettro(wavelengths_hg_teorico, "Task 2: Spettro di Emissione Teorico del Mercurio (Hg)", ax2)

plt.tight_layout(pad=3.0)

# Sostituzione critica per il funzionamento su GitHub: salvataggio dell'output come immagine statica
nome_file = "spettro_emissione.png"
plt.savefig(nome_file, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
print(f"Grafico salvato con successo come {nome_file}")