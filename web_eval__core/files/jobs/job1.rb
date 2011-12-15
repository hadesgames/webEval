#!/usr/bin/env ruby

$fin = File.new("adunare.in", "r")
$fout = File.new("adunare.out", "w")

a = $fin.gets.chomp.to_i
b = $fin.gets.chomp.to_i

$fout.puts a + b

$fout.close
