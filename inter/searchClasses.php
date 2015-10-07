<?php

session_start();
if(!isset($_SESSION['user'])) {
    echo "false";
    exit();
}

require_once dirname ( __FILE__ ) . '/tools/SQLHelper.class.php';

if(isset($_GET['curPage'])) {
    $curPage = $_GET['curPage'];
} else {
    $curPage = 1;
}

if(isset($_GET['keyword'])) {
    $keyword = $_GET['keyword'];
} else {
    $keyword = '';
}

$count = 6;

$sqlHelper = new SQLHelper();
if(!empty($keyword)) {
    $sql = "select * from t_class where title like '%" . $keyword . "%' order by lorder desc, id asc limit " . (($curPage-1) * $count) . "," . $count;
} else {
    $sql = "select * from t_class order by lorder desc, id asc limit " . (($curPage-1) * $count) . "," . $count;
}
$arr = $sqlHelper->execute_dql_array($sql);

if(!empty($keyword)) {
    $sql = "select count(id) as count from t_class where title like '%" . $keyword . "%'";
} else {
    $sql = "select count(id) as count from t_class";
}
$total = $sqlHelper->execute_dql_array($sql);

$res = array();
$res['curPage'] = $curPage;
$res['totalCount'] = (int)($total[0]['count'] / $count);

if($total[0]['count'] % $count != 0) {
    $res['totalCount']++;
}
$res['data'] = $arr;

echo json_encode($res);

?>