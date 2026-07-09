import subprocess

def ping_host(ip_address: str) -> str:
    """
    Executa um ping em um endereço IP fornecido para verificar se o host está ativo.
    
    Args:
        ip_address (str): O endereço IP a ser testado (ex: "8.8.8.8").
        
    Returns:
        str: O resultado do comando ping.
    """
    
    # Utilizando subprocess.run() com entrada de usuário sanitizada
    command = f"ping -c 1 {ip_address}"
    
    try:
        output = subprocess.run(command, shell=False, text=True)
        return output.stdout if output.returncode == 0 else "Falha ao executar o ping"
    
    except subprocess.CalledProcessError as e:
        return f"Falha ao executar o ping. Erro: {e}"

# Exemplo de uso normal:
# print(ping_host("127.0.0.1"))

# Exemplo de exploração da vulnerabilidade (Payload malicioso):
# print(ping_host("127.0.0.1; cat /etc/passwd"))
