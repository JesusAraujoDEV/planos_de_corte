import pulp

class Variable:
    def __init__(self, name: str, var_type: str, low_bound: float = 0, up_bound: float = None):
        """
        Clase para representar una variable de decisión.
        :param name: Nombre de la variable (ej., "x1").
        :param var_type: Tipo de variable ("Continuous", "Integer", "Binary").
        :param low_bound: Cota inferior de la variable.
        :param up_bound: Cota superior de la variable.
        """
        self.name = name
        self.var_type = var_type
        self.low_bound = low_bound
        self.up_bound = up_bound
        self.pulp_var = None # Se asignará cuando se construya el modelo PuLP

    def create_pulp_var(self):
        """Crea y retorna la variable PuLP correspondiente."""
        if self.var_type == "Continuous":
            return pulp.LpVariable(self.name, self.low_bound, self.up_bound, pulp.LpContinuous)
        elif self.var_type == "Integer":
            return pulp.LpVariable(self.name, self.low_bound, self.up_bound, pulp.LpInteger)
        elif self.var_type == "Binary":
            return pulp.LpVariable(self.name, 0, 1, pulp.LpBinary) # Binaria tiene cotas fijas
        else:
            raise ValueError(f"Tipo de variable desconocido: {self.var_type}")

    def get_value(self):
        """Retorna el valor actual de la variable PuLP."""
        return self.pulp_var.varValue if self.pulp_var else None

    def is_integer_required(self) -> bool:
        """Verifica si la variable debe ser entera."""
        return self.var_type in ["Integer", "Binary"]

    def is_fractional(self, tolerance: float = 1e-6) -> bool:
        """
        Verifica si el valor actual de la variable es fraccionario.
        :param tolerance: Tolerancia para considerar un número como entero.
        """
        if not self.is_integer_required() or self.pulp_var is None:
            return False # No es entera requerida o no tiene valor
        
        val = self.get_value()
        if val is None:
            return False # No hay solución aún
            
        return abs(val - round(val)) > tolerance


class Constraint:
    def __init__(self, coeffs: list[float], comparison_type: str, rhs: float):
        """
        Clase para representar una restricción.
        :param coeffs: Lista de coeficientes para las variables en la restricción.
        :param comparison_type: Tipo de comparación ("<=", ">=", "=").
        :param rhs: Lado derecho de la restricción.
        """
        self.coeffs = coeffs
        self.comparison_type = comparison_type
        self.rhs = rhs
        self.pulp_constraint = None # Se asignará cuando se construya el modelo PuLP


class ILPModel:
    def __init__(self):
        """
        Clase que representa el modelo de Programación Lineal Entera (PLE).
        """
        self.objective_type = None # "Maximize" o "Minimize"
        self.objective_coeffs = []
        self.variables: list[Variable] = []
        self.constraints: list[Constraint] = []
        self.pulp_prob: pulp.LpProblem = None

    def set_objective(self, coeffs: list[float], obj_type: str):
        """
        Define la función objetivo del modelo.
        :param coeffs: Coeficientes de la función objetivo.
        :param obj_type: Tipo de objetivo ("Maximize" o "Minimize").
        """
        self.objective_coeffs = coeffs
        self.objective_type = obj_type.capitalize() # Asegura Mayúscula inicial

    def add_variable(self, name: str, var_type: str, low_bound: float = 0, up_bound: float = None):
        """
        Añade una nueva variable al modelo.
        :param name: Nombre de la variable.
        :param var_type: Tipo de variable ("Continuous", "Integer", "Binary").
        :param low_bound: Cota inferior.
        :param up_bound: Cota superior.
        """
        self.variables.append(Variable(name, var_type, low_bound, up_bound))

    def add_constraint(self, coeffs: list[float], comparison_type: str, rhs: float):
        """
        Añade una nueva restricción al modelo.
        :param coeffs: Coeficientes de la restricción para las variables.
        :param comparison_type: Tipo de comparación ("<=", ">=", "=").
        :param rhs: Lado derecho de la restricción.
        """
        self.constraints.append(Constraint(coeffs, comparison_type, rhs))

    def build_lp_relaxation(self):
        """
        Construye o actualiza el modelo PuLP como una relajación LP (ignorando
        temporalmente las restricciones de integralidad).
        """
        if self.objective_type == "Maximize":
            self.pulp_prob = pulp.LpProblem("ILP_Relaxation", pulp.LpMaximize)
        elif self.objective_type == "Minimize":
            self.pulp_prob = pulp.LpProblem("ILP_Relaxation", pulp.LpMinimize)
        else:
            raise ValueError("Tipo de objetivo no definido. Use set_objective primero.")

        # Crear variables PuLP (todas como continuas para la relajación)
        for var in self.variables:
            # Para la relajación LP, todas las variables son continuas
            var.pulp_var = pulp.LpVariable(var.name, var.low_bound, var.up_bound, pulp.LpContinuous)

        # Definir función objetivo
        obj_expr = pulp.lpSum(self.objective_coeffs[i] * self.variables[i].pulp_var
                              for i in range(len(self.objective_coeffs)))
        self.pulp_prob += obj_expr, "Objective Function"

        # Añadir restricciones
        for i, constr in enumerate(self.constraints):
            constr_expr = pulp.lpSum(constr.coeffs[j] * self.variables[j].pulp_var
                                     for j in range(len(constr.coeffs)))
            if constr.comparison_type == "<=":
                self.pulp_prob += constr_expr <= constr.rhs, f"Constraint_{i+1}"
            elif constr.comparison_type == ">=":
                self.pulp_prob += constr_expr >= constr.rhs, f"Constraint_{i+1}"
            elif constr.comparison_type == "=":
                self.pulp_prob += constr_expr == constr.rhs, f"Constraint_{i+1}"
            else:
                raise ValueError(f"Tipo de comparación de restricción desconocido: {constr.comparison_type}")

    def solve_lp_relaxation(self):
        """
        Resuelve la relajación LP actual y actualiza los valores de las variables.
        Retorna el estado de la solución y el valor del objetivo.
        """
        if self.pulp_prob is None:
            self.build_lp_relaxation()

        status = self.pulp_prob.solve()
        
        # Actualizar valores de las variables
        for var in self.variables:
            if var.pulp_var and var.pulp_var.varValue is not None:
                var.pulp_var.varValue = var.pulp_var.varValue # Esto ya se actualiza internamente por PuLP

        return pulp.LpStatus[status], pulp.value(self.pulp_prob.objective)