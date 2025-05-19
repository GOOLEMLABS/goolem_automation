import os
import time
import base64
import io
import contextlib
from dotenv import load_dotenv
from litellm import completion
from goolem_bot.gbot_lnx import gKeyboard, gMouse, gScreen
import cv2
import re

# Cargar variables de entorno desde .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class GoolemAgent:
    def __init__(self):
        self.system_prompt = self.generate_system_prompt()
        self.gs = gScreen()
        self.gk = gKeyboard()
        self.gm = gMouse()
        self.history = [{"role": "system", "content": self.system_prompt}]
        self.screenshot_path = "/dev/shm/gscreenshot.png"

    def interact(self, user_input):
        self.history.append({"role": "user", "content": user_input})
        response = completion(
            model="gpt-4o",
            messages=self.history,
            api_key=OPENAI_API_KEY,
            temperature=0.3
        )
        content = response['choices'][0]['message']['content']
        self.history.append({"role": "assistant", "content": content})
        return content

    def execute_code(self, code_str):
        """
        Ejecuta código generado por el modelo, restringido a las clases del entorno gbot.
        Captura y devuelve la salida generada por el código.
        """
        safe_globals = {
            "__builtins__": None
        }
        safe_locals = {
            "gs": self.gs,
            "gk": self.gk,
            "gm": self.gm,
            "time": time,
            "ds": self.describe_screen,
            "dsc": self.describe_screen_contents,
            "fcfd": self.find_coordinates_from_description
        }

        output = io.StringIO()
        print(output)
        try:
            with contextlib.redirect_stdout(output):
                exec(code_str, safe_globals, safe_locals)
            result = output.getvalue().strip()

            if "resultado" in safe_locals:
                return f"📌 Resultado: {safe_locals['resultado']}"
            elif result:
                return f"📎 Salida:\n{result}"
            else:
                return "✅ Código ejecutado correctamente, sin salida visible."
        except Exception as e:
            return f"❌ Error al ejecutar el código: {e}"

    def describe_screen(self):
        self.gs.grab_screen("")
        return f"🖼️ Captura guardada en {self.screenshot_path}. "

    def describe_screen_contents(self):
        self.gs.grab_screen("")
        try:
            with open(self.screenshot_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        except FileNotFoundError:
            return "❌ No se pudo encontrar la imagen en /dev/shm/gscreenshot.png."

        vision_prompt = (
            "Describe brevemente en español lo que ves en la imagen proporcionada. Es un escritorio linux. "
            "Concéntrate en identificar íconos, ventanas abiertas o cualquier texto visible en pantalla."
        )

        response = completion(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": vision_prompt},
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/png;base64,{encoded_image}"}}
                ]}
            ],
            api_key=OPENAI_API_KEY,
            temperature=0.2
        )

        return response['choices'][0]['message']['content']

    def find_coordinates_from_description(self, description: str):
        self.gs.grab_screen("")
        try:
            with open(self.screenshot_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        except FileNotFoundError:
            return "❌ No se pudo encontrar la imagen en /dev/shm/gscreenshot.png."

        vision_prompt = (
            f"En la siguiente imagen, localiza {description}. "
            f"Devuélveme únicamente las coordenadas del centro del objeto {description} en formato: x=..., y=..."
            f"Encuentra en la pantalla el objeto o botón {description}."
        )

        response = completion(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": vision_prompt},
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/png;base64,{encoded_image}"}}
                ]}
            ],
            api_key=OPENAI_API_KEY,
            temperature=0.2
        )

        result = response['choices'][0]['message']['content']
        match = re.search(r"x\s*=\s*(\d+)\s*,\s*y\s*=\s*(\d+)", result)
        if match:
            x = int(match.group(1))
            y = int(match.group(2))
            return [x, y]
        else:
            return f"📎 Respuesta recibida pero sin coordenadas claras: {result}"

    def generate_system_prompt(self):
        function_specs = [
            {
                "clase": "gScreen (gs)",
                "descripcion": "Funciones relacionadas con la captura de pantalla y análisis visual.",
                "funciones": [
                    {
                        "firma": "gs.grab_screen(sector: str = '')",
                        "descripcion": "Captura la pantalla actual y la guarda en /dev/shm/gscreenshot.png.",
                        "ejemplo": 'gs.grab_screen("")'
                    }
                ]
            },
            {
                "clase": "gMouse (gm)",
                "descripcion": "Permite mover el cursor y hacer clic.",
                "funciones": [
                    {
                        "firma": "gm.move([x, y])",
                        "descripcion": "Mueve el cursor a las coordenadas indicadas.",
                        "ejemplo": "gm.move([100, 200])"
                    },
                    {
                        "firma": "gm.click()",
                        "descripcion": "Realiza un clic izquierdo en la posición actual.",
                        "ejemplo": "gm.click()"
                    },
                    {
                        "firma": "gm.press(button='left') / gm.release(button='left')",
                        "descripcion": "Simula mantener pulsado un botón del ratón (ej. arrastrar).",
                        "ejemplo": "gm.press(); gm.move([300,300]); gm.release()"
                    }
                ]
            },
            {
                "clase": "gKeyboard (gk)",
                "descripcion": "Simula pulsaciones de teclas.",
                "funciones": [
                    {
                        "firma": 'gk.type_string("texto")',
                        "descripcion": "Escribe una cadena de texto como si se tecleara.",
                        "ejemplo": 'gk.type_string("Hola Mundo")'
                    },
                    {
                        "firma": "gk.press(key), gk.release(key), gk.press_and_release(key)",
                        "descripcion": "Control directo sobre teclas individuales.",
                        "ejemplo": 'gk.press_and_release("ENTER")'
                    }
                ]
            },
            {
                "clase": "Funciones visuales GPT-4 Vision",
                "descripcion": "Operaciones asistidas por GPT para análisis de imagen.",
                "funciones": [
                    {
                        "firma": "describe_screen_contents()",
                        "descripcion": "Describe visualmente el contenido actual en pantalla.",
                        "ejemplo": "¿Qué está abierto ahora?"
                    },
                    {
                        "firma": 'find_coordinates_from_description("texto") -> [x, y]',
                        "descripcion": "Devuelve las coordenadas de un objeto visual descrito en lenguaje natural.",
                        "ejemplo": 'find_coordinates_from_description("botón de inicio de icewm")'
                    }
                ]
            }
        ]

        prompt = [
            "Eres un agente que controla un robot de escritorio en Linux para el proyecto goolem.io.",
            "Tu nombre es goolem bot.",
            "Solo puedes generar código que utilice las clases gScreen (gs), gMouse (gm), y gKeyboard (gk), además de funciones visuales asistidas por GPT-4.",
            "No puedes usar bibliotecas externas ni realizar imports.",
            "A continuación, las funciones disponibles:"
        ]

        for grupo in function_specs:
            prompt.append(f"\n### {grupo['clase']}\n{grupo['descripcion']}")
            for f in grupo["funciones"]:
                prompt.append(f"- **{f['firma']}**\n  - {f['descripcion']}\n  - 🧪 Ejemplo: `{f['ejemplo']}`")

        prompt.append(
            "\nAntes de ejecutar cualquier código, debes resumir la intención del usuario en español, de forma concisa."
            "\nNunca uses funciones fuera del entorno permitido. No utilices print(), import, open(), ni eval()."
            "\n⚠️ Si obtienes un resultado (por ejemplo coordenadas), asígnalo a una variable llamada `resultado` para que sea visible para el usuario."
        )

        return "\n".join(prompt)
