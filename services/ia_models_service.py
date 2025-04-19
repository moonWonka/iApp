import requests
import json
from config.settings import GEMINI_API_KEY, OPENAI_API_KEY
from models.entities import (
    ProcessStatusDTO,
    AnalisisResumenDTO,
    RiesgoEvaluacionDTO,
    PropuestaAccionDTO,
    TendenciasSentimientoDTO  # Importamos el nuevo DTO
)

class IAService:
    def __init__(self, prompt: str):
        self.prompt = prompt

    def call_openAI(self, prompt_type: str) -> object:
        """
        Realiza la llamada al modelo OpenAI y procesa la respuesta según el tipo de prompt.
        """
        print(f"Llamando al modelo: OpenAI")
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
        response_time = round(response.elapsed.total_seconds(), 2)
        print(f"Tiempo de respuesta: {response_time:.2f} segundos")

        if response.status_code == 200:
            response_json = response.json()
            try:
                # Extraer el contenido del JSON devuelto por el modelo
                output = response_json["output"][0]["content"][0]["text"]
                processed_data = json.loads(output.strip("```json").strip())

                # Procesar según el tipo de prompt
                return self._process_prompt_response(prompt_type, processed_data, response_time, response.status_code, "OPENAI")
            except (KeyError, ValueError, json.JSONDecodeError) as e:
                print(f"❌ Error al procesar la respuesta del modelo OpenAI: {e}")
                raise Exception("Error al procesar la respuesta del modelo OpenAI.")
        else:
            print(f"❌ Error en la petición: {response.status_code}")
            raise Exception(f"Error en la petición: {response.status_code}")

    def call_gemini(self, prompt_type: str) -> object:
        """
        Realiza la llamada al modelo Gemini y procesa la respuesta según el tipo de prompt.
        """
        print(f"Llamando al modelo: Gemini")
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

        # Realizar la solicitud
        response = requests.post(url, json=data, headers=headers, params=queryparam)
        response_time = round(response.elapsed.total_seconds(), 2)
        print(f"Tiempo de respuesta: {response_time:.2f} segundos")

        if response.status_code == 200:
            response_json = response.json()
            try:
                # Extraer el contenido del JSON devuelto por el modelo
                raw_text = response_json['candidates'][0]['content']['parts'][0]['text']
                processed_data = json.loads(raw_text.strip("```json").strip())

                # Procesar según el tipo de prompt
                return self._process_prompt_response(prompt_type, processed_data, response_time, response.status_code, "GEMINI")
            except (KeyError, ValueError, json.JSONDecodeError) as e:
                print(f"❌ Error al procesar la respuesta del modelo Gemini: {e}")
                raise Exception("Error al procesar la respuesta del modelo Gemini.")
        else:
            print(f"❌ Error en la petición: {response.status_code}")
            raise Exception(f"Error en la petición: {response.status_code}")

    def _process_prompt_response(self, prompt_type: str, data: dict, response_time: float, status_code: int, model_used: str) -> object:
        """
        Procesa la respuesta según el tipo de prompt y retorna el DTO correspondiente.
        """
        if prompt_type == "procesamiento_articulo":
            return ProcessStatusDTO(
                etiquetas_ia=data["etiquetas_ia"],
                sentimiento=data["sentimiento"],
                rating=float(data["rating"]),
                nivel_riesgo=data["nivel_riesgo"],
                indicador_violencia=data["indicador_violencia"],
                edad_recomendada=data["edad_recomendada"],
                is_processed=True,
                execution_time=f"{response_time} seg",
                status_code=status_code,
                model_used=model_used
            )
        elif prompt_type == "resumen_ejecutivo":
            return AnalisisResumenDTO(
                titulo=data.get("titulo", "Resumen Ejecutivo"),
                resumen=data.get("resumen", ""),
                elementos_clave=data.get("elementos_clave", []),
                posibles_implicaciones=data.get("posibles_implicaciones", []),
                preguntas_pendientes=data.get("preguntas_pendientes", [])
            )
        elif prompt_type == "evaluacion_riesgos":
            return RiesgoEvaluacionDTO(
                riesgo_general=data.get("riesgo_general", ""),
                factores_detonantes=data.get("factores_detonantes", []),
                recomendaciones=data.get("recomendaciones", [])
            )
        elif prompt_type == "comparativo_medios":
            return PropuestaAccionDTO(
                acciones_recomendadas=data.get("acciones_recomendadas", []),
                actores_clave=data.get("actores_clave", []),
                tiempo_estimado=data.get("tiempo_estimado", "")
            )
        elif prompt_type == "tendencias_sentimiento":
            return TendenciasSentimientoDTO(
                titulo=data.get("titulo", "Análisis de Tendencias Emocionales"),
                resumen=data.get("resumen", ""),
                elementos_clave=data.get("elementos_clave", []),
                posibles_implicaciones=data.get("posibles_implicaciones", []),
                preguntas_pendientes=data.get("preguntas_pendientes", [])
            )
        else:
            raise ValueError(f"Tipo de prompt '{prompt_type}' no soportado.")