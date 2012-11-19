<?php
$str='+id:"hallo test" -from:nochwas "test hallo" nochwas';

$part = explode(" ",$str);
$buff = array();
$inside = false;
for($i = 0; $i < count($part); $i++) {
	if($inside) $buff[count($buff)-1] .= ' '.$part[$i];
	else $buff[] = $part[$i];
	if(strstr($part[$i],'"')) $inside = !$inside;
	
} 

print_r($buff);
