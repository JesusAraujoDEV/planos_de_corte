from ilp_model import ILPModel
from cutting_plane_solver import CuttingPlaneSolver

def get_user_input():
    """Solicita al usuario los datos del modelo de programación lineal con opciones numéricas."""
    model = ILPModel()

    print("--- Definición del Modelo de Programación Lineal Entera ---")

    # Tipo de objetivo
    print("\n¿Cuál es el tipo de problema?")
    print("  0. Maximizar")
    print("  1. Minimizar")
    obj_choice = input("Seleccione una opción (0 o 1): ").strip()
    while obj_choice not in ["0", "1"]:
        obj_choice = input("Entrada inválida. Por favor, ingrese '0' o '1': ").strip()
    
    obj_type = "Maximize" if obj_choice == "0" else "Minimize"

    # Variables
    num_vars = int(input("\nIngrese el número de variables de decisión: "))
    obj_coeffs = []
    for i in range(num_vars):
        name = input(f"Ingrese el nombre de la variable {i+1} (ej., x1): ")
        
        print(f"Ingrese el tipo de la variable {name}:")
        print("  0. Continua")
        print("  1. Entera")
        print("  2. Binaria (0 o 1)")
        var_type_choice = input("Seleccione una opción (0, 1 o 2): ").strip()
        while var_type_choice not in ["0", "1", "2"]:
            var_type_choice = input(f"Tipo inválido. Ingrese '0', '1' o '2' para {name}: ").strip()
        
        if var_type_choice == "0":
            var_type = "Continuous"
        elif var_type_choice == "1":
            var_type = "Integer"
        else: # var_type_choice == "2"
            var_type = "Binary"
            
        low_bound_str = input(f"Ingrese la cota inferior para {name} (deje en blanco para 0): ")
        low_bound = float(low_bound_str) if low_bound_str else 0.0

        up_bound_str = input(f"Ingrese la cota superior para {name} (deje en blanco para sin límite, o para binarias se ajusta automáticamente): ")
        up_bound = float(up_bound_str) if up_bound_str else None

        model.add_variable(name, var_type, low_bound, up_bound)
        
        obj_coeff = float(input(f"Ingrese el coeficiente de {name} en la función objetivo: "))
        obj_coeffs.append(obj_coeff)
    
    model.set_objective(obj_coeffs, obj_type)

    # Restricciones
    num_constraints = int(input("\nIngrese el número de restricciones: "))
    for i in range(num_constraints):
        print(f"\n--- Restricción {i+1} ---")
        constraint_coeffs = []
        for var in model.variables:
            coeff = float(input(f"Ingrese el coeficiente de {var.name} en la restricción {i+1}: "))
            constraint_coeffs.append(coeff)
        
        print(f"Ingrese el tipo de comparación para la restricción {i+1}:")
        print("  0. Menor o Igual que (<=)")
        print("  1. Mayor o Igual que (>=)")
        print("  2. Igual a (=)")
        comp_type_choice = input("Seleccione una opción (0, 1 o 2): ").strip()
        while comp_type_choice not in ["0", "1", "2"]:
            comp_type_choice = input("Tipo de comparación inválido. Ingrese '0', '1' o '2': ").strip()
        
        if comp_type_choice == "0":
            comp_type = "<="
        elif comp_type_choice == "1":
            comp_type = ">="
        else: # comp_type_choice == "2"
            comp_type = "="
        
        rhs = float(input(f"Ingrese el lado derecho (RHS) de la restricción {i+1}: "))
        model.add_constraint(constraint_coeffs, comp_type, rhs)
    
    return model

if __name__ == "__main__":
    try:
        ilp_model = get_user_input()
        solver = CuttingPlaneSolver(ilp_model)
        final_solution, final_obj_value = solver.solve()

        if final_solution is not None:
            print("\n--- Resultados Finales ---")
            print("Solución Óptima Encontrada:")
            for var_name, value in final_solution.items():
                print(f"  {var_name} = {value:.4f}")
            print(f"Valor Óptimo de la Función Objetivo: {final_obj_value:.4f}")
        else:
            print("\nEl problema no pudo ser resuelto a una solución entera óptima.")

    except ValueError as e:
        print(f"Error en la entrada de datos: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")