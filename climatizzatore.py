import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Definizione delle variabili linguistiche per i due input e l'output
temperatura_esterna = ctrl.Antecedent(
    np.arange(-10, 41, 1), 'temperatura_esterna')
persone = ctrl.Antecedent(np.arange(0, 11, 1), 'persone')
stanza = ctrl.Consequent(np.arange(-10, 31, 1), 'stanza')

# Definizione delle funzioni di appartenenza per le variabili linguistiche
temperatura_esterna['molto freddo'] = fuzz.trapmf(
    temperatura_esterna.universe, [-10, -10, 5, 10])
temperatura_esterna['freddo'] = fuzz.trimf(
    temperatura_esterna.universe, [5, 10, 20])
temperatura_esterna['moderato'] = fuzz.trimf(
    temperatura_esterna.universe, [15, 20, 25])
temperatura_esterna['caldo'] = fuzz.trimf(
    temperatura_esterna.universe, [20, 25, 35])
temperatura_esterna['molto caldo'] = fuzz.trapmf(
    temperatura_esterna.universe, [25, 35, 40, 40])

persone['poche'] = fuzz.trapmf(persone.universe, [0, 0, 2, 5])
persone['normali'] = fuzz.trimf(persone.universe, [3, 5, 8])
persone['molte'] = fuzz.trimf(persone.universe, [6, 10, 10])

stanza['fredda'] = fuzz.trapmf(stanza.universe, [-10, -10, 5, 18])
stanza['normale'] = fuzz.trimf(stanza.universe, [10, 15, 25])
stanza['calda'] = fuzz.trimf(stanza.universe, [20, 30, 30])

# Definizione delle regole fuzzy
# Regole per il caso in cui le persone sono poche
rule1 = ctrl.Rule(
    temperatura_esterna['molto freddo'] & persone['poche'], stanza['fredda'])
rule2 = ctrl.Rule(temperatura_esterna['freddo']
                  & persone['poche'], stanza['fredda'])
rule3 = ctrl.Rule(
    temperatura_esterna['moderato'] & persone['poche'], stanza['normale'])
rule4 = ctrl.Rule(temperatura_esterna['caldo']
                  & persone['poche'], stanza['calda'])
rule5 = ctrl.Rule(
    temperatura_esterna['molto caldo'] & persone['poche'], stanza['calda'])

# Regole per il caso in cui le persone sono normali
rule6 = ctrl.Rule(
    temperatura_esterna['molto freddo'] & persone['normali'], stanza['fredda'])
rule7 = ctrl.Rule(temperatura_esterna['freddo']
                  & persone['normali'], stanza['normale'])
rule8 = ctrl.Rule(
    temperatura_esterna['moderato'] & persone['normali'], stanza['normale'])
rule9 = ctrl.Rule(temperatura_esterna['caldo']
                  & persone['normali'], stanza['calda'])
rule10 = ctrl.Rule(
    temperatura_esterna['molto caldo'] & persone['normali'], stanza['calda'])

# Regole per il caso in cui le persone sono molte
rule11 = ctrl.Rule(
    temperatura_esterna['molto freddo'] & persone['molte'], stanza['fredda'])
rule12 = ctrl.Rule(
    temperatura_esterna['freddo'] & persone['molte'], stanza['normale'])
rule13 = ctrl.Rule(
    temperatura_esterna['moderato'] & persone['molte'], stanza['calda'])
rule14 = ctrl.Rule(
    temperatura_esterna['caldo'] & persone['molte'], stanza['calda'])
rule15 = ctrl.Rule(
    temperatura_esterna['molto caldo'] & persone['molte'], stanza['calda'])

stanza_ctrl = ctrl.ControlSystem(
    [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule1, rule2, rule3, rule4, rule5])

stanza_sim = ctrl.ControlSystemSimulation(stanza_ctrl)

inputTemp = 20
inputPersone = 8

stanza_sim.input['temperatura_esterna'] = inputTemp
stanza_sim.input['persone'] = inputPersone

stanza_sim.compute()

print("Temperatura esterna:", inputTemp)
print("Numero di persone nella stanza:", inputPersone)
print("Temperatura della stanza:", stanza_sim.output['stanza'])

temperatura_esterna.view()
plt.savefig("temperatura.png")

persone.view()
plt.savefig("persone.png")

stanza.view()
plt.savefig("stanza.png")
