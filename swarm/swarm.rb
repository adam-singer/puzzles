#!/usr/bin/ruby
# ZERGRUSH
# Kanwei Li, 2009
#
# e^(-63s+10)/(e^(-63s+10)+e^(-21z)) * m >= 1
# m * e^(-63s+10) >= e^(-63s+10) + e^(-21z)
# m * e^(-63s+10) - e^(-63s+10) >= e^(-21z)
# e^(-63s+10) (m-1) >= e^(-21z)
# ln(m-1) + (-63s+10) >= -21z

# e^(-63s+10)/(e^(-63s+10)+e^(-21z)) * m = g
# m * e^(-63s+10) = g(e^(-63s+10) + e^(-21z))
# m * e^(-63s+10) - g*e^(-63s+10) = g*e^(-21z)
# e^(-63s+10) (m-g) = g*e^(-21z)
# ln(m-g) + (-63s+10) = ln(g) - 21z
# ln(g) - ln(m-g) = -63s + 10 + 21z
# g/(m-g) = e^(-63s + 10 + 21z)
# let cc = e^(-63s + 10 + 21z)
# g = (m-g) * cc
# g + g*cc = m*cc
# g(1 + cc) = m*cc
# g = m*cc/(1 + cc)

def optimize(ary, total)
  return [] if ary.empty?
  table = []
  (ary.size+1).times { |i| table[i] = [] }
  (0..total).each { |zerg| table[0][zerg] = 0 }
  (1..ary.size).each do |base|
    table[base][0] = 0
    (1..total).each do |zerg|
      if ary[base-1].zerg <= zerg && (ary[base-1].minerals + table[base-1][zerg - ary[base-1].zerg] > table[base-1][zerg])
        table[base][zerg] = ary[base-1].minerals + table[base-1][zerg - ary[base-1][1]]
      else
        table[base][zerg] = table[base-1][zerg]
      end
    end
  end
  result = []
  i, k = ary.size, total
  while i > 0 && k > 0
    if table[i][k] != table[i-1][k]
      result << ary[i-1]
      k -= ary[i-1].zerg
    end
    i -= 1
  end
  result
end

def cartesian_prod(ary)
  ary.inject([[]]){|old,lst|
    new = []
    lst.each{|e| new += old.map{|c| c.dup << e }}
    new
  }
end

def gain(minerals, terran, zerg)
  n = -63 * terran + 10 + 21 * zerg
  return 0 if n < 0
  return minerals if n > 10
  cc = Math.exp(n)
  (minerals * cc / (1 + cc)).round
end

def zerg_needed_for_feasible(minerals, terran)
  ((Math.log(minerals-1) + (-63 * terran + 10)) / -21).ceil
end

def feasible?(minerals, terran, zerg)
  return false if minerals <= 1
  Math.log(minerals-1) + (-63 * terran + 10) >= (-21 * zerg).to_f
end

# Make sure input file exists and read from it
filename = ARGV[0]
unless filename && File.exist?(filename)
  puts "error: must specify a valid input file"
  exit
end
input = File.open(filename)

num_planets = input.gets.to_i
out = ""

Base = Struct.new(:index, :zerg, :minerals)

num_planets.times do
  bases, zerg = input.gets.split(/\s+/).collect { |i| i.to_i }
  feasible = []
  bases.times do |n|
    terran, minerals = input.gets.split(/\s+/).collect { |i| i.to_i }
    if feasible?(minerals, terran, zerg)
      zerg_needed = zerg_needed_for_feasible(minerals, terran)
      last_gain = nil
      base_ary = []
      loop do
        g = gain(minerals, terran, zerg_needed)
        break if last_gain && last_gain == g
        base_ary << Base.new(n, zerg_needed, g)
        last_gain = g
        zerg_needed += 1
      end
      feasible << base_ary
    end
  end
  candidates = cartesian_prod(feasible)
  
  best_zerg, best_minerals, best_ary = nil, nil, nil
  candidates.each do |cand|
    cand = cand.sort_by { |a| [a.zerg, a.minerals] }
    cand_ary = optimize(cand, zerg)
    cand_ary.sort! { |a, b| a.index <=> b.index }
    total_zerg = cand_ary.inject(0) { |sum, i| sum += i.zerg }
    total_minerals = cand_ary.inject(0) { |sum, i| sum += i.minerals }
    if best_minerals.nil? || (total_minerals >= best_minerals)
      best_zerg, best_minerals = total_zerg, total_minerals
      best_ary = cand_ary
    end
  end
  out << "#{best_zerg} #{best_minerals}\n"
  out << best_ary.inject([]) { |ary, base| ary << base.index << base.zerg }.join(' ') << "\n"
end

puts out
