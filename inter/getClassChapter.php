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
$sql = "select * from t_title where cid=" . $cid . ' order by id';
$arr = $sqlHelper->execute_dql_array($sql);

$res = array();
$index = -1;
$subIndex = 0;

foreach($arr as $title) {
    if($title['pid'] == 0) {
        $index = $index + 1;
        $res[$index] = $title;
        $res[$index]['subTitle'] = array();
        $subIndex = 0;
    } else {
        $res[$index]['subTitle'][$subIndex] = $title;
        $subIndex = $subIndex + 1;
    }
}

echo json_encode($res);

?>