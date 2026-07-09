import subprocess

def ping_host(ip_address: str) -> str:
    # A variável ip_address é concatenada diretamente na string do comando.
    command = f"ping -c 1 {ip_address}"
    
    try:
        # Sanitizando a entrada para prevenir SQL Injection
        sanitized_command = subprocess.run(command, shell=False, text=True)
        return sanitized_command.stdout if sanitized_command.returncode == 0 else "Falha ao executar o ping"
    
    except subprocess.CalledProcessError as e:
        return f"Falha ao executar o ping. Erro: {e}"

# Exemplo de uso normal:
# print(ping_host("127.0.0.1"))

# Exemplo de exploração da vulnerabilidade (Payload malicioso):
# print(ping_host("127.0.0.1; cat /etc/passwd"))
