from goolem_agent.agent_gpt import GoolemAgent

def main():
    agent = GoolemAgent()
    print("🤖 GoolemBot iniciado. Escribe instrucciones para controlar el escritorio Linux.\n")

    while True:
        try:
            user_input = input("🧠 Instrucción: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["salir", "exit", "quit"]:
                print("👋 Saliendo de GoolemBot.")
                break

            print("\n📌 Respuesta de GoolemBot:\n")
            assistant_response = agent.interact(user_input)
            print(assistant_response)

            # Buscar si contiene un bloque de código en triple backtick
            import re
            match = re.search(r"```python(.*?)```", assistant_response, re.DOTALL)
            if match:
                code_block = match.group(1).strip()
                print("\n⚙️ Ejecutando código...\n")
                execution_result = agent.execute_code(code_block)
                print(f"{execution_result}\n")
            else:
                print("⚠️ No se encontró ningún bloque de código para ejecutar.\n")

        except KeyboardInterrupt:
            print("\n👋 Interrupción recibida. Cerrando GoolemBot.")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()
