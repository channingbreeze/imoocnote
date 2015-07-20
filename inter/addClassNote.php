<?php

session_start();
if(!isset($_SESSION['user'])) {
    echo "false";
    exit();
}

require_once dirname ( __FILE__ ) . '/tools/SQLHelper.class.php';

if(!isset($_POST['cid']) || !isset($_POST['content'])) {
    echo "false";
    exit();
} else {
    $cid = $_POST['cid'];
    $content = $_POST['content'];
}

$sqlHelper = new SQLHelper();
$sql = "insert into t_note (cid, notetime, content) values (" . $cid . ", now(), '" . $content . "')";
$res = $sqlHelper->execute_dqm($sql);

if($res == 1) {
    $sql = "update t_class set hasnote=1 where id=" . $cid;
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