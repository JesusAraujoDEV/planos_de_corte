# Solucionador de Programación Lineal Entera (PLE) con Planos de Corte

## Descripción

Este proyecto implementa un solucionador interactivo para problemas de Programación Lineal Entera (PLE) utilizando el **método de Planos de Corte (Cutting Plane Method)**. El programa permite al usuario ingresar los datos de un modelo de programación lineal (función objetivo, restricciones, y tipo de variables) y luego aplica iterativamente el algoritmo de planos de corte para encontrar la solución óptima entera.

La implementación sigue un diseño Orientado a Objetos (POO) para modularizar las diferentes partes del problema (modelo, variables, restricciones, y el propio algoritmo de solución), facilitando su comprensión, mantenimiento y posible extensión.

## Características

* **Entrada Interactiva de Modelos**: El usuario puede definir su propio problema de PLE (maximización o minimización, variables continuas/enteras/binarias, restricciones lineales).
* **Método de Planos de Corte**: Aplica el algoritmo de planos de corte para encontrar soluciones enteras.
* **Flexibilidad**: Permite definir modelos con múltiples variables y restricciones.
* **Diseño POO**: Estructura el código en clases (`ILPModel`, `Variable`, `Constraint`, `CuttingPlaneSolver`) para una mejor organización y claridad.
* **Uso de `PuLP`**: Se apoya en la librería `PuLP` para resolver las relajaciones continuas del problema en cada iteración.

## Requisitos

Para ejecutar este programa, necesitarás tener instalado Python y las siguientes librerías:

* **`PuLP`**: Una librería para modelar y resolver problemas de optimización lineal.
* **`NumPy`**: (Opcional, pero recomendado para manejo de arrays y cálculos numéricos si se implementan cortes de Gomory más complejos).

Puedes instalarlas usando pip:

```bash
pip install pulp numpy
