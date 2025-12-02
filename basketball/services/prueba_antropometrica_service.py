"""
Servicio para PruebaAntropometrica
TODO: Implementar la lógica de negocio para PruebaAntropometrica
"""


class PruebaAntropometricaService:
    """Servicio para la lógica de negocio de PruebaAntropometrica"""
    
    def __init__(self):
        # TODO: Inicializar DAO
        pass
    
    def listar_pruebas(self, solo_activas: bool = True):
        """Listar todas las pruebas antropométricas"""
        # TODO: Implementar
        pass
    
    def obtener_prueba(self, prueba_id: int):
        """Obtener una prueba por ID"""
        # TODO: Implementar
        pass
    
    def crear_prueba(self, datos: dict):
        """Crear una nueva prueba antropométrica"""
        # TODO: Implementar validaciones y cálculo de IMC/índice córnico
        pass
    
    def actualizar_prueba(self, prueba_id: int, datos: dict):
        """Actualizar una prueba"""
        # TODO: Implementar validaciones y recálculo de índices
        pass
    
    def eliminar_prueba(self, prueba_id: int):
        """Eliminar una prueba (soft delete)"""
        # TODO: Implementar
        pass
    
    def obtener_pruebas_por_atleta(self, atleta_id: int):
        """Obtener pruebas de un atleta"""
        # TODO: Implementar
        pass
    
    def obtener_ultima_prueba_atleta(self, atleta_id: int):
        """Obtener la última prueba de un atleta"""
        # TODO: Implementar
        pass
    
    def calcular_imc(self, peso: float, estatura: float) -> float:
        """Calcular IMC"""
        # TODO: Implementar
        pass
    
    def calcular_indice_cornico(self, altura_sentado: float, estatura: float) -> float:
        """Calcular índice córnico"""
        # TODO: Implementar
        pass
    
    def obtener_estadisticas_atleta(self, atleta_id: int):
        """Obtener estadísticas antropométricas de un atleta"""
        # TODO: Implementar
        pass
