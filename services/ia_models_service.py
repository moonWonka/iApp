import requests
import os
import json
from config.settings import GEMINI_API_KEY, OPENAI_API_KEY
from core.processor import ProcessStatusDTO
from models.entities import IAProcessedData

class IAService:

    def __init__(self, prompt: str):
        self.prompt = prompt

    def call_openAI(self) -> ProcessStatusDTO:
        """
        Realiza la llamada al modelo OpenAI y procesa la respuesta para devolver una instancia de ProcessStatusDTO.
        """
        url: str = "https://api.openai.com/v1/responses"
        headers: dict[str, str] = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        payload: dict[str, str] = {
            "model": "gpt-4o",
            "input": self.prompt
        }

        # Realizar la solicitud
        response = requests.post(url, headers=headers, json=payload)
        response_time = round(response.elapsed.total_seconds(), 2)  # Tiempo en segundos con 2 decimales
        print(f"Tiempo de respuesta: {response_time:.2f} segundos")

        if response.status_code == 200:
            response_json = response.json()
            try:
                # Extraer el contenido del JSON devuelto por el modelo
                output = response_json["output"][0]["content"][0]["text"]

                # Convertir el texto JSON a un diccionario
                processed_data: IAProcessedData = json.loads(output.strip("```json").strip())

                # Crear y retornar una instancia de ProcessStatusDTO
                return ProcessStatusDTO(
                    etiquetas_ia=processed_data["etiquetas_ia"],
                    sentimiento=processed_data["sentimiento"],
                    rating=float(processed_data["rating"]),
                    nivel_riesgo=processed_data["nivel_riesgo"],
                    indicador_violencia=processed_data["indicador_violencia"],
                    edad_recomendada=processed_data["edad_recomendada"],
                    is_processed=1,
                    execution_time=response_time,  # Tiempo en segundos con 2 decimales
                    status_code=response.status_code,
                    model_used="OPENAI"
                )
            except (KeyError, ValueError, json.JSONDecodeError) as e:
                print(f"❌ Error al procesar la respuesta del modelo OpenAI: {e}")
                raise Exception("Error al procesar la respuesta del modelo OpenAI.")
        else:
            print(f"❌ Error en la petición: {response.status_code}")
            try:
                error_response = response.json()
                print("Respuesta del servicio:", error_response)
            except ValueError:
                print("No se pudo decodificar la respuesta como JSON. Respuesta en texto:")
                print(response.text)
            raise Exception(f"Error en la petición: {response.status_code}")

    def call_gemini(self) -> ProcessStatusDTO:
        """
        Realiza la llamada al modelo Gemini y procesa la respuesta para devolver una instancia de IAProcessedData.
        """
        url: str = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

        headers: dict[str, str] = {
            "Content-Type": "application/json"
        }

        queryparam: dict[str, str | None] = {
            "key": GEMINI_API_KEY
        }

        data = {
            "contents": [ 
                {
                    "parts": [
                        {
                            "text": self.prompt
                        }
                    ]
                } 
            ]
        }

        response = requests.post(url, json=data, headers=headers, params=queryparam)
        response_time = round(response.elapsed.total_seconds(), 2)  # Tiempo en segundos con 2 decimales
        print(f"Tiempo de respuesta: {response_time:.2f} segundos")    

        if response.status_code == 200:
            response_json = response.json()
            # Extraer el contenido del JSON devuelto por el modelo
            raw_text = response_json['candidates'][0]['content']['parts'][0]['text']
            
            # Eliminar el bloque de código ```json y convertirlo a un diccionario
            processed_data: IAProcessedData = json.loads(raw_text.strip("```json").strip())

            # Crear una instancia de IAProcessedData
            return ProcessStatusDTO(
                etiquetas_ia=processed_data.etiquetas_ia,
                sentimiento=processed_data.sentimiento,
                rating=float(processed_data.rating),
                nivel_riesgo=processed_data.nivel_riesgo,
                indicador_violencia=processed_data.indicador_violencia,
                edad_recomendada=processed_data.edad_recomendada,
                is_processed=1,
                execution_time=response_time,  # Tiempo en segundos con 2 decimales
                status_code=response.status_code,
                model_used="GEMINI"
            )
        else:
            print(f"Error en la petición: {response.status_code}")
            raise Exception(f"Error en la petición: {response.status_code}")

    @staticmethod
    def to_json(data: IAProcessedData) -> str:
        """
        Convierte una instancia de IAProcessedData a un JSON válido.
        """
        return json.dumps({
            "etiquetas_ia": data.etiquetas_ia,
            "sentimiento": data.sentimiento,
            "rating": data.rating,
            "nivel_riesgo": data.nivel_riesgo,
            "indicador_violencia": data.indicador_violencia,
            "edad_recomendada": data.edad_recomendada
        })

# Ejemplo de uso:
#titulo = "Acusan a profesor de la UFRO de hacer 'llave de estrangulación' a un alumno"
#descripcion = "La situación ya habría ocurrido en 2022 sin que las autoridades sancionaran al docente. Alumnos de la Facultad de Ingeniería y Ciencias llamaron a un paro hoy."
#prompt = f"""
#Analiza el siguiente artículo de prensa y completa estrictamente los siguientes campos en formato JSON:

#Artículo:
#"{titulo}"
#"{descripcion}"

#Devuelve tu respuesta en formato JSON respetando el siguiente esquema y sin ningún comentario adicional(un json limpio):

#{{
#    "etiquetas_ia": [ "etiqueta1", "etiqueta2", "..." ],
#    "sentimiento": "positivo | negativo | neutro",
#   "rating": "número_decimal_entre_1.0_y_5.0",
#   "nivel_riesgo": "bajo | medio | alto",
#   "indicador_violencia": "sí | no | moderado",
#   "edad_recomendada": "+13 | +18 | todo público"
# }}
# """

#a = IAService(prompt=prompt)
#processed_data = a.call_openAI()
#print(processed_data)
# # Convertir a JSON usando el método estático
# print(IAService.to_json(processed_data))