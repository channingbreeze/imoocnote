<?php

session_start();
if(!isset($_SESSION['user'])) {
    echo "false";
    exit();
}

require_once dirname ( __FILE__ ) . '/tools/SQLHelper.class.php';

if(!isset($_POST['id'])) {
    echo "false";
    exit();
} else {
    $id = $_POST['id'];
}

$sqlHelper = new SQLHelper();
$sql = "delete from t_note where id=" . $id;
$res = $sqlHelper->execute_dqm($sql);

if($res == 1) {
    $sql = "update t_class set hasnote=0 where id not in (select distinct cid from t_note)";
    $res = $sqlHelper->execute_dqm($sql);
    if($res != 0) {
        echo "success";
    } else {
        echo "fail";
    }
} else {
    echo "fail";
}

?>