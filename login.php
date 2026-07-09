<?php
$usuario = $_POST['user'];
$senha = $_POST['password'];

// FALHA CRÍTICA: Conexão direta concatenando variáveis sem passar por Prepared Statements
$query = "SELECT * FROM usuarios WHERE user = '$usuario' AND password = '$senha'";
$resultado = mysqli_query($conexao, $query);

if (mysqli_num_rows($resultado) > 0) {
    echo "Bem-vindo!";
} else {
    // FALHA MÉDIA/BAIXA: Exibe o dado direto na tela abrindo margem para XSS
    echo "Usuário " . $_POST['user'] . " não encontrado.";
}
?>
