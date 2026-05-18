import numpy as np
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
    # Range dello spettro visibile standard
    w_min, w_max = 380, 750
    
    # Creazione della matrice di sfondo nero
    spettro_img = np.zeros((100, w_max - w_min, 3))
    
    # Visualizzazione dell'asse e del fondo scuro
    ax.imshow(spettro_img, extent=[w_min, w_max, 0, 10])
    ax.set_facecolor('black')
    
    # Disegno delle righe di emissione caricate
    # Si usa una funzione gaussiana sottile per simulare la larghezza finita della riga
    x = np.linspace(w_min, w_max, w_max - w_min)
    
    for wl in wavelengths:
        if w_min <= wl <= w_max:
            color = wavelength_to_rgb(wl)
            # Disegna una linea verticale spessa o un gradiente per simulare la riga spettrale
            ax.axvline(x=wl, color=color, linewidth=2.5, alpha=0.9, 
                       solid_capstyle='butt', label=f'{wl} nm' if wl in wavelengths[:3] else "")
            
    ax.set_title(titolo, fontsize=12, fontweight='bold', pad=10)
    ax.set_xlabel(r"Lunghezza d'onda $\lambda$ [nm]", fontsize=10)
    ax.set_xlim(w_min, w_max)
    ax.set_yticks([])  # Rimuove l'asse Y non significativo per uno spettro
    ax.grid(False)

# --- Dati Sperimentali e Teorici ---

# Task 1: Dati forniti del gas ionizzato sperimentale
# Gli angoli sono inclusi nel dizionario per completezza metodologica associata alla relazione
dati_sperimentali = {
    'angoli': [51.1, 50.2, 49.4, 48.3, 48.1, 47.3],
    'wavelengths': [424, 468, 472, 483, 546, 649]
}

# Task 2: Righe teoriche principali del Mercurio (Hg) nel visibile
# Valori standard da manuale: Violetto (404.7 nm), Blu (435.8 nm), Verde (546.1 nm), Giallo (577.0 nm, 579.1 nm)
wavelengths_hg_teorico = [404.66, 435.83, 546.07, 576.96, 579.07]

# --- Generazione dei Grafici ---

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
fig.patch.set_facecolor('#f4f4f4')

# Task 1
genera_spettro(dati_sperimentali['wavelengths'], "Task 1: Spettro di Emissione del Gas Ionizzato (Dati Sperimentali)", ax1)

# Task 2
genera_spettro(wavelengths_hg_teorico, "Task 2: Spettro di Emissione Teorico del Mercurio (Hg)", ax2)

plt.tight_layout(pad=3.0)
plt.show()