<?php

header("Access-Control-Allow-Origin:*");

require_once dirname ( __FILE__ ) . '/tools/SQLHelper.class.php';

if(isset($_GET['curPage'])) {
    $curPage = $_GET['curPage'];
} else {
    $curPage = 1;
}

$count = 6;

$sqlHelper = new SQLHelper();
$sql = "select * from t_class limit " . (($curPage-1) * $count) . "," . $count;
$arr = $sqlHelper->execute_dql_array($sql);

$sql = "select count(id) as count from t_class";
$total = $sqlHelper->execute_dql_array($sql);

$res = array();
$res['curPage'] = $curPage;
$res['totalCount'] = (int)($total[0]['count'] / $count);
if($total % $count != 0) {
    $res['totalCount']++;
}
$res['data'] = $arr;

echo json_encode($res);

?>