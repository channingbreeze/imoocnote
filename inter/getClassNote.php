<?php

header("Access-Control-Allow-Origin:*");

require_once dirname ( __FILE__ ) . '/tools/SQLHelper.class.php';

if(isset($_GET['cid'])) {
    $cid = $_GET['cid'];
} else {
    echo "false";
    exit();
}

$sqlHelper = new SQLHelper();
$sql = "select * from t_note where cid=" . $cid . " order by notetime desc";
$arr = $sqlHelper->execute_dql_array($sql);

if(count($arr) > 0) {
    for($i=0; $i < count($arr); $i++) {
        $arr[$i]['notetime'] = strtotime($arr[$i]['notetime']) * 1000;
    }
}

echo json_encode($arr);

?>