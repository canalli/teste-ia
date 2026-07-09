import subprocess

def ping_host(ip_address: str) -> str:
    """
    Executa um ping em um endereço IP fornecido para verificar se o host está ativo.
    
    Args:
        ip_address (str): O endereço IP a ser testado (ex: "8.8.8.8").
        
    Returns:
        str: O resultado do comando ping.
    """
    
    # A variável ip_address é concatenada diretamente na string do comando.
    command = f"ping -c 1 {ip_address}"
    
    try:
        # A vulnerabilidade está aqui: shell=True com entrada de usuário não sanitizada.
        output = subprocess.check_output(command, shell=True, text=True)
        return output
    
    except subprocess.CalledProcessError as e:
        return f"Falha ao executar o ping. Erro: {e}"

# Exemplo de uso normal:
# print(ping_host("127.0.0.1"))

# Exemplo de exploração da vulnerabilidade (Payload malicioso):
# print(ping_host("127.0.0.1; cat /etc/passwd"))
