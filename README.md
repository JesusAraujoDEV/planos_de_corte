# Solucionador de Programación Lineal Entera (PLE) con Planos de Corte

## Descripción General

Este proyecto implementa un solucionador interactivo para problemas de **Programación Lineal Entera (PLE)** utilizando el **método de Planos de Corte (Cutting Plane Method)**. El usuario puede definir su propio modelo de optimización (función objetivo, variables, restricciones) y el sistema encuentra la solución óptima entera aplicando iterativamente cortes sobre la relajación lineal.

El código está organizado en tres archivos principales, cada uno con una responsabilidad clara dentro del flujo de resolución:

---

## Estructura de Archivos y Funcionalidad

### 1. `main.py`

- **Propósito:** Es el punto de entrada del programa. Gestiona la interacción con el usuario y coordina el proceso de resolución.
- **Flujo:**
  1. Solicita al usuario los datos del modelo (tipo de problema, variables, restricciones) de forma interactiva.
  2. Construye un objeto `ILPModel` con la información ingresada.
  3. Crea una instancia de `CuttingPlaneSolver` usando el modelo definido.
  4. Ejecuta el método de planos de corte y muestra los resultados finales (solución óptima entera o mensaje de error).
- **No contiene lógica matemática de optimización**, solo orquesta el flujo y la entrada/salida.

### 2. `ilp_model.py`

- **Propósito:** Define la estructura del modelo de Programación Lineal Entera (PLE) y sus componentes.
- **Clases principales:**
  - `Variable`: Representa una variable de decisión (continua, entera o binaria), con sus cotas y tipo.
  - `Constraint`: Representa una restricción lineal (coeficientes, tipo de comparación y lado derecho).
  - `ILPModel`: Gestiona el conjunto de variables, restricciones y la función objetivo. Permite:
    - Agregar variables y restricciones.
    - Construir la relajación lineal del modelo (ignorando temporalmente la integralidad).
    - Resolver la relajación LP usando la librería `PuLP`.
- **No resuelve el problema entero**, solo modela y resuelve la versión relajada (continua) del problema.

### 3. `cutting_plane_solver.py`

- **Propósito:** Implementa el algoritmo de **planos de corte** para encontrar soluciones enteras.
- **Clases principales:**
  - `CuttingPlaneSolver`: Recibe un `ILPModel` y aplica el siguiente ciclo:
    1. Resuelve la relajación LP del modelo.
    2. Si la solución es entera, termina y devuelve el resultado.
    3. Si hay variables fraccionarias que deberían ser enteras, genera un "corte" (restricción adicional) para eliminar la solución fraccionaria actual.
    4. Añade el corte al modelo y repite el proceso.
    5. Si no se pueden generar más cortes o el problema se vuelve infactible, informa el resultado.
- **Nota:** La generación de cortes es conceptual/simplificada (no implementa cortes de Gomory exactos, sino cortes de redondeo para propósitos didácticos).

---

## Ejecución Paso a Paso

1. **(Opcional pero recomendado) Crear y activar un entorno virtual:**

   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Linux/Mac:
   source venv/bin/activate
   ```

2. **Instalar dependencias:**

   ```bash
   pip install -r requirements.txt
   ```
   > Esto instalará `PuLP` (y opcionalmente `numpy` si decides usarlo para extensiones).

3. **Ejecutar el programa principal:**

   ```bash
   python main.py
   ```

4. **Seguir las instrucciones interactivas:**
   - El programa te pedirá que definas el tipo de problema (maximizar/minimizar), las variables (nombre, tipo, cotas, coeficientes), y las restricciones (coeficientes, tipo, RHS).
   - El solucionador aplicará el método de planos de corte y mostrará el resultado paso a paso.

---

## Ejemplo de Uso

```
¿Cuál es el tipo de problema?
  0. Maximizar
  1. Minimizar
Seleccione una opción (0 o 1): 0
Ingrese el número de variables de decisión: 2
Ingrese el nombre de la variable 1 (ej., x1): x1
Ingrese el tipo de la variable x1:
  0. Continua
  1. Entera
  2. Binaria (0 o 1)
Seleccione una opción (0, 1 o 2): 1
Ingrese la cota inferior para x1 (deje en blanco para 0):
Ingrese la cota superior para x1 (deje en blanco para sin límite, o para binarias se ajusta automáticamente):
Ingrese el coeficiente de x1 en la función objetivo: 2
... (continúa para las demás variables y restricciones)
```

---

## Notas y Extensiones
- El método de planos de corte implementado es conceptual y didáctico. Para problemas grandes o cortes más sofisticados (como cortes de Gomory reales), se requeriría acceso al tableau simplex y una lógica más avanzada.
- Puedes modificar o extender las clases para agregar más tipos de restricciones, validaciones, o mejorar la generación de cortes.

---

## Créditos
- Basado en técnicas clásicas de optimización y el uso de la librería [PuLP](https://coin-or.github.io/pulp/).
