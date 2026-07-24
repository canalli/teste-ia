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
