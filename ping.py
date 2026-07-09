import subprocess

def ping_host(ip_address: str) -> str:
    """
    Executa um ping em um endereço IP fornecido para verificar se o host está ativo.
     
 Args:
        ip_address (str): O endereço IP a ser testado (ex: "8.8.8.8").
        
    Returns:
         str: O resultado do comando ping.
     """
    
   # Sanitizando a entrada para prevenir SQL Injection
    sanitized_ip = subprocess.quote(ip_address)
   
    command = f"ping -c 1 {sanitized_ip}"
     
     try:
       output = subprocess.run(command, shell=False, text=True)
       sanitized_command = subprocess.run(command, shell=False, text=True)
       return sanitized_command.stdout if sanitized_command.returncode == 0 else "Falha ao executar o ping"
     
     except subprocess.CalledProcessError as e:
         return f"Falha ao executar o ping. Erro: {e}"
