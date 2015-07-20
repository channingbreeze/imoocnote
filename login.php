<?php
    session_start();
    if(isset($_POST['username']) && isset($_POST['password'])) {
        $username = $_POST['username'];
        $password = $_POST['password'];
        if($username == "username" && $password == "password") {
            $_SESSION['user'] = $username;
            header("Location: index.php");
        } else {
            header("Location: login.php");
        }
    }
?>
<!DOCTYPE html>
<head>
    <meta charset=utf-8 />
	<title>Handlebars</title>
</head>
<body>
    <form action="#" method="post">
        用户名：<input type="text" name="username" />
        密　码：<input type="password" name="password" />
        <input type="submit" value="submit" />
    </form>
</body>
