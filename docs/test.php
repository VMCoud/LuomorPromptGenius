<?php
function UnicodeEncode($str) {
    //split word
    preg_match_all('/./u', $str, $matches);
 
    $unicodeStr = "";
    foreach($matches[0] as $m) {
        //拼接
        $unicodeStr .= "&#" . base_convert(bin2hex(iconv('UTF-8', "UCS-4", $m)), 16, 10);
    }
    return $unicodeStr;
}
 
$str = "新浪微博";
echo UnicodeEncode($str);

$test = array(
    "{像这样）"
);
echo json_encode($test);