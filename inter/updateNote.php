<?php

session_start();
if(!isset($_SESSION['user'])) {
    echo "false";
    exit();
}

require_once dirname ( __FILE__ ) . '/tools/SQLHelper.class.php';

if(!isset($_POST['id']) || !isset($_POST['content'])) {
    echo "false";
    exit();
} else {
    $id = $_POST['id'];
    $content = $_POST['content'];
}

$sqlHelper = new SQLHelper();
$sql = "update t_note set notetime=now(), content='" . $content . "' where id=" . $id;
$res = $sqlHelper->execute_dqm($sql);

if($res == 1) {
    echo "success";
} else {
    echo "fail";
}

?>