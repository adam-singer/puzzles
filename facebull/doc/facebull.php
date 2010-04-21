#!/usr/bin/env php
<?php

/* http://blogofayogi.blogspot.com/2009/09/finished-facebull-and-submitted-applied.html */

$input_file = $argv[1];

$handle = fopen($input_file, "r");
$contents_raw = fread($handle, filesize($input_file));
fclose($handle);

$contents = trim($contents_raw);

$machine_array = array();


$machine_array = nl2br($contents);//create line breaks
$machine_array_by_line = explode('
', $machine_array);//explode on line breaks
$machine_array_by_line_by_value = array();

foreach($machine_array_by_line as $value){

//replace non-word characters with single space

$pattern = '/(\w+)\W+(\w+)\W+(\w+)\W+(\w+)/';
$replacement = '${1} ${2} ${3} ${4}';
$properly_spaced_line = preg_replace($pattern, $replacement, $value);
$holder_array = array();

//explode on single space
$holder_array = explode(' ', $properly_spaced_line);
$machine_array_by_line_by_value[] = $holder_array;
//and create an array of machines, prices and chemicals
}

/* Section ---------- 2
* ******************************
* Calculate total number of chemicals and fill the machine prices array at the same time
*
*/

$machine_prices = array();


$cpairs = array();
$highest_c_found = 0;
foreach ($machine_array_by_line_by_value as $value){
$machine_name = trim($value[0]);
$machine_price = trim($value[3]);

$machine_prices[$machine_name] = $machine_price;

$c1 = $value[1];


$pattern = '/.(\w)/';
$replacement = '${1}';


$c1_int_string = preg_replace($pattern, $replacement, $c1);

if($c1_int_string > $highest_c_found)
$highest_c_found = $c1_int_string;

}

$num_chems = $highest_c_found;

/* Section ---------- 3
* ******************************
* Create an array with all paths from one chemical to another.
*
*/

//-----------------------------section 3.1
$basic_trans_array = array();//all one-step transformations from one chemical to another

for($i=1; $i <= $num_chems; $i++){
for($j=1; $j <= $num_chems; $j++){
if($i != $j){

foreach($machine_array_by_line_by_value as $value){//loop through the array, and find the cheapest for each
if($value[1] == "C$i" && $value[2] == "C$j"){

if(isset($basic_trans_array["C$i" . "C$j"][1]) && $value[3] < $basic_trans_array["C$i" . "C$j"][1]){

$basic_trans_array["C$i" . "C$j"][0] = $value[0];//the name of the machine
}

if(!isset($basic_trans_array["C$i" . "C$j"])){
$basic_trans_array["C$i" . "C$j"][0] = trim($value[0]);//the name of the machine
}
}
}
}
}
}



//-----------------------------section 3.2 - loading the $basic_trans_array into $compute_lowest_cost_array
$compute_lowest_cost_array = array();//this array will be used in the final calculation of lowest cost
foreach($basic_trans_array as $key => $value){
$compute_lowest_cost_array[$key][1] = $value; //load the level one conversions into the master compute_lowest_cost array
}


//-----------------------------section 3.3 - computes all possible paths from one chemical to another and loads into the $compute_lowest_cost_array
for($i = 2; $i <= $num_chems; $i++){//taking longer paths, starting from 1 jump in between
for($j = 1; $j <= $num_chems; $j++){//for the first chemical
for($k = 1; $k <= $num_chems; $k++){//for the second chemical

if($j != $k){//chemicals 1 and 2 are different

for($g = 1; $g <= $num_chems; $g++){

if($g != $k){//c1 leads to c!2 if we're looking for paths c1 to c2

if(isset($compute_lowest_cost_array["C$j" . "C$g"][1])){

$j_to_g_machine = $compute_lowest_cost_array["C$j" . "C$g"][1][0];

if(isset($compute_lowest_cost_array["C$g" . "C$k"][($i - 1)])){

foreach($compute_lowest_cost_array["C$g" . "C$k"][($i -1)] as $value){
$i_minus_one_machines_array = $j_to_g_machine . '_' . $value;
$compute_lowest_cost_array["C$j" . "C$k"][$i][] = $i_minus_one_machines_array;
}

}
}
}
}
}
}
}
}

/* Section ---------- 4
* ******************************
* Create a counter array and then compute every possible combination of machines, and the price.
*
*/

//-----------------------------section 4.1 - creating counter array and transfering machine values to another array
$counter_array = array();

foreach($compute_lowest_cost_array as $key => $value){

$counter_max = count($compute_lowest_cost_array[$key], COUNT_RECURSIVE) - count($compute_lowest_cost_array[$key]);

$counter_array[$key] = array('counter'=>1, 'counter_max'=>$counter_max);
}
$names_of_machines = array();

//creates a new array of combinations that is easier to parse through
foreach($compute_lowest_cost_array as $key => $value){
foreach($value as $value2){
foreach($value2 as $value3){
$names_of_machines[$key][] = $value3;//this makes it easier to add the prices of machines
}
}
}

//$compute_lowest_cost_array
$lowest_cost = compute_total_cost($names_of_machines, $counter_array, $num_chems);//set the initial value. All future tests will be to find something lower
$total_cost = array(0, 0);
$the_end = 0;

$counter = 0;
while($the_end == 0){

$total_cost = compute_total_cost($names_of_machines, $counter_array, $num_chems);

if($total_cost[1] < $lowest_cost[1]){//machines to produce cost, cost
$lowest_cost = $total_cost;
}

$the_end = advance_counter($counter_array, $num_chems);//if $the_end != 0, break

}

//-----------------------------section 4.2 - writing the output file

$output_string = $lowest_cost[1] . "\n";

$lowest_cost_machines = array();

foreach($lowest_cost[0] as $key => $value){
$lowest_cost_machines[] = trim($key, 'M');
}

sort($lowest_cost_machines, SORT_NUMERIC);

foreach($lowest_cost_machines as $key => $value){
$output_string .= $value . ' ';
}
echo $output_string;

//-----------------------------section 4.3 - writing the output file

/* Section ---------- 5
* ******************************
* Functions for computing total cost and advancing counter
*
*/

function compute_total_cost(&$names_of_machines, &$counter_array, $num_chems){
$machines_total = array();
$total_cost = 0;

global $machine_prices;

for($j = 1; $j <= $num_chems; $j++){//for the first chemical
for($k = 1; $k <= $num_chems; $k++){//for the second chemical
if($j != $k){//chemicals 1 and 2 are different
$counter = $counter_array["C$j" . "C$k"]['counter'] - 1;//so we can access the proper array element directly

$machines = $names_of_machines["C$j" . "C$k"][$counter];
$machines_as_arr = explode('_', $machines);

foreach($machines_as_arr as $value){
if(!isset($machines_total[$value])){
$machines_total[$value] = 1;//records each machine that is needed only once
$total_cost += $machine_prices[$value];
}
}
}
}
}

return array($machines_total, $total_cost);//machines and cost array
}

function advance_counter(&$counter_array, $num_chems){
for($j = 1; $j <= $num_chems; $j++){//taking longer paths, starting from 1 jump in between
for($k = 1; $k <= $num_chems; $k++){
if($j != $k){
if($counter_array["C$j" . "C$k"]['counter'] < $counter_array["C$j" . "C$k"]['counter_max']){
$counter_array["C$j" . "C$k"]['counter'] = $counter_array["C$j" . "C$k"]['counter'] + 1;
break 2;
} else {
if($j == $num_chems && ($k == $num_chems - 1)) {
return 1;//if we're are the very end
} else {
$counter_array["C$j" . "C$k"]['counter'] = 1;
}
}
}
}
}

return 0;

}
?>
